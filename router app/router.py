"""
Arsany Router Watchdog (All-in-One)
- Colored, organized UI (like the earlier full version)
- Narrow buttons
- Splash screen with name + date/time
- Continuous ping (NO terminal windows)
- Auto Factory Reset when ping TIMEOUT/NULL
- Skip Wizard automatically (Next/Finish) before + after login
- Manual button: Skip Wizard Now (Next/Finish only, no reset)
- Manual button: Test Reset Now
- Handles iframes for reset page
"""

import subprocess
import time
import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================
# BRANDING
# =========================
APP_OWNER_NAME = "Arsany"


# =========================
# ROUTER / SELENIUM CONFIG
# =========================
ROUTER_IP = "192.168.1.1"
USERNAME = "admin"
PASSWORD = "D02B4C7E"
EDGE_DRIVER_PATH = r"C:\Windows\msedgedriver.exe"
WAIT_TIMEOUT = 30

# Ping monitoring
PING_INTERVAL_SECONDS = 1
POST_RESET_COOLDOWN_SECONDS = 120

# If True: trigger ONLY on "Request timed out" or empty output
# If False: trigger on any ping failure (no TTL)
TRIGGER_ONLY_ON_TIMED_OUT = True

# Wizard buttons (Skip Intro/Wizard)
INTRO_NEXT_ID = "Btn_Next"
INTRO_FINISH_ID = "Btn_apply_WizardSuss"
INTRO_MAX_NEXT_CLICKS = 10

# Login IDs
LOGIN_USER_ID = "Frm_Username"
LOGIN_PASS_ID = "Frm_Password"
LOGIN_BTN_ID = "LoginId"

# Menus
MENU_MGR_DIAG_ID = "mgrAndDiag"
MENU_DEV_MGR_ID = "devMgr"

# Factory reset elements
RESET_BAR_ID = "ResetManagBar"
RESET_BTN_ID = "Btn_reset"
CONFIRM_OK_ID = "confirmOK"


# =========================
# THREADING / UI QUEUE
# =========================
stop_event = threading.Event()
ui_queue = queue.Queue()  # ("log"|"ping"|"status", payload)
selenium_lock = threading.Lock()  # prevent concurrent Selenium sessions


def qlog(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    ui_queue.put(("log", f"[{ts}] {msg}"))


def qping(msg: str):
    ts = time.strftime("%H:%M:%S")
    ui_queue.put(("ping", f"[{ts}] {msg}"))


def qstatus(state: str, detail: str = ""):
    # state: IDLE/OK/TIMEOUT/FAILED/RESETTING/COOLDOWN/STOPPED
    ui_queue.put(("status", (state, detail)))


# =========================
# PING
# =========================
def run_ping_once(host: str) -> str:
    """Single ping without opening any console window."""
    try:
        out = subprocess.check_output(
            ["ping", "-n", "1", host],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return out or ""
    except subprocess.CalledProcessError as e:
        return getattr(e, "output", "") or ""
    except Exception:
        return ""


def parse_ping_state(ping_output: str) -> str:
    """Return: OK / TIMEOUT / FAILED / EMPTY"""
    out = (ping_output or "").strip()
    if out == "":
        return "EMPTY"
    if "TTL=" in out:
        return "OK"
    if "Request timed out" in out or "Request timed out." in out:
        return "TIMEOUT"
    return "FAILED"


def should_trigger_reset(ping_output: str) -> bool:
    out = (ping_output or "").strip()
    if out == "":
        return True
    if "Request timed out" in out or "Request timed out." in out:
        return True
    if TRIGGER_ONLY_ON_TIMED_OUT:
        return False
    return "TTL=" not in out


# =========================
# SELENIUM HELPERS
# =========================
def build_edge_driver() -> webdriver.Edge:
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--ignore-certificate-errors")
    edge_options.add_argument("--ignore-ssl-errors")
    edge_options.add_argument("--allow-insecure-localhost")

    service = Service(EDGE_DRIVER_PATH)
    return webdriver.Edge(service=service, options=edge_options)


def safe_js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)


def skip_intro_wizard(driver, where: str = "unknown"):
    """
    Press Next (Btn_Next) multiple times then Finish (Btn_apply_WizardSuss) if present.
    Btn_Next is duplicated in DOM (bad HTML), so we click the first visible/enabled.
    Never raises; logs only.
    """
    try:
        clicked_any = False

        for i in range(INTRO_MAX_NEXT_CLICKS):
            btns = driver.find_elements(By.ID, INTRO_NEXT_ID)
            btns = [b for b in btns if b.is_displayed() and b.is_enabled()]
            if not btns:
                break
            safe_js_click(driver, btns[0])
            clicked_any = True
            qlog(f"Wizard: Clicked Next ({i+1}) [{where}]")
            time.sleep(1)

        fins = driver.find_elements(By.ID, INTRO_FINISH_ID)
        fins = [b for b in fins if b.is_displayed() and b.is_enabled()]
        if fins:
            safe_js_click(driver, fins[0])
            clicked_any = True
            qlog(f"Wizard: Clicked Finish [{where}]")
            time.sleep(2)

        if not clicked_any:
            qlog(f"Wizard: Not found [{where}]")

    except Exception as e:
        qlog(f"Wizard: error [{where}]: {e!r}")


def try_login(driver, wait):
    """Login if login page exists; otherwise continue."""
    try:
        user_el = wait.until(EC.presence_of_element_located((By.ID, LOGIN_USER_ID)))
        pass_el = wait.until(EC.presence_of_element_located((By.ID, LOGIN_PASS_ID)))

        user_el.clear()
        pass_el.clear()
        user_el.send_keys(USERNAME)
        pass_el.send_keys(PASSWORD)

        wait.until(EC.element_to_be_clickable((By.ID, LOGIN_BTN_ID))).click()
        qlog("Login: submitted")
        time.sleep(2)
    except Exception:
        qlog("Login: fields not found (maybe already logged in)")


def do_factory_reset_flow(driver, wait, context_label: str):
    """
    Runs reset steps in the current browsing context (main or iframe).
    Assumes menus already opened.
    """
    qlog(f"Reset: trying in {context_label}")

    bar = wait.until(EC.presence_of_element_located((By.ID, RESET_BAR_ID)))
    safe_js_click(driver, bar)
    qlog("Reset: expanded 'Factory Reset Management'")

    wait.until(EC.element_to_be_clickable((By.ID, RESET_BTN_ID))).click()
    qlog("Reset: clicked 'Factory Reset' button")

    # confirmOK in DOM
    try:
        wait.until(EC.element_to_be_clickable((By.ID, CONFIRM_OK_ID))).click()
        qlog("Reset: clicked confirmOK")
    except Exception:
        qlog("Reset: confirmOK not found/clickable (ok)")

    # browser alert
    try:
        alert = wait.until(EC.alert_is_present())
        alert.accept()
        qlog("Reset: accepted alert")
    except Exception:
        qlog("Reset: no alert")


# =========================
# SELENIUM ACTIONS
# =========================
def manual_skip_wizard_only():
    """
    Opens router and skips wizard (Next/Finish) only.
    Does NOT reset. Used by "Skip Wizard Now" button.
    """
    if not selenium_lock.acquire(blocking=False):
        qlog("Manual Skip: Selenium is busy (another task running).")
        return

    driver = None
    try:
        qstatus("RESETTING", "Skipping wizard only...")
        qlog("Manual Skip Wizard: started")

        driver = build_edge_driver()
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        driver.get(f"https://{ROUTER_IP}")

        skip_intro_wizard(driver, "manual-before-login")
        try_login(driver, wait)
        skip_intro_wizard(driver, "manual-after-login")

        qlog("Manual Skip Wizard: done")
        qstatus("OK", "Monitoring...")
    except Exception as e:
        qlog(f"Manual Skip Wizard: failed: {e!r}")
        qstatus("FAILED", "Manual skip failed")
    finally:
        try:
            if driver:
                driver.quit()
        except Exception:
            pass
        selenium_lock.release()


def run_factory_reset():
    """
    Full factory reset flow:
    - open router
    - skip wizard before/after login
    - open menus
    - find reset section (iframe or main)
    - click reset + confirm
    """
    if not selenium_lock.acquire(blocking=False):
        qlog("Reset: Selenium is busy (another task running).")
        return

    driver = None
    try:
        qstatus("RESETTING", "Running Factory Reset...")
        qlog("Factory Reset: started")

        driver = build_edge_driver()
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        driver.get(f"https://{ROUTER_IP}")

        skip_intro_wizard(driver, "before-login")
        try_login(driver, wait)
        skip_intro_wizard(driver, "after-login")

        # Open menus
        wait.until(EC.element_to_be_clickable((By.ID, MENU_MGR_DIAG_ID))).click()
        wait.until(EC.element_to_be_clickable((By.ID, MENU_DEV_MGR_ID))).click()
        qlog("Menus: opened (Management/Diagnosis -> Device Management)")
        time.sleep(2)

        # Try iframes first
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        done = False
        for idx, fr in enumerate(iframes):
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame(fr)
                if driver.find_elements(By.ID, RESET_BAR_ID):
                    do_factory_reset_flow(driver, wait, f"iframe #{idx}")
                    done = True
                    break
            except Exception:
                continue

        if not done:
            driver.switch_to.default_content()
            do_factory_reset_flow(driver, wait, "main page")

        qlog("Factory Reset: command sent (router may reboot)")
        qstatus("COOLDOWN", f"Cooldown {POST_RESET_COOLDOWN_SECONDS}s")
    except Exception as e:
        qlog(f"Factory Reset: failed: {e!r}")
        qstatus("FAILED", "Factory reset failed")
    finally:
        try:
            if driver:
                driver.quit()
        except Exception:
            pass
        selenium_lock.release()


# =========================
# WATCHDOG LOOP
# =========================
def watchdog_loop():
    qlog("Watchdog: started")
    qstatus("OK", "Monitoring...")

    while not stop_event.is_set():
        out = run_ping_once(ROUTER_IP)
        state = parse_ping_state(out)

        if state == "OK":
            qping("PING OK (TTL)")
            qstatus("OK", f"{ROUTER_IP} reachable")
        elif state == "TIMEOUT":
            qping("PING TIMEOUT")
            qstatus("TIMEOUT", "Request timed out")
        elif state == "EMPTY":
            qping("PING EMPTY (NULL)")
            qstatus("FAILED", "Ping output empty")
        else:
            qping("PING FAIL (no TTL)")
            qstatus("FAILED", "Ping failed")

        if should_trigger_reset(out):
            qlog("Watchdog: trigger met -> running Factory Reset")
            run_factory_reset()

            # Cooldown
            for sec in range(POST_RESET_COOLDOWN_SECONDS, 0, -1):
                if stop_event.is_set():
                    break
                qstatus("COOLDOWN", f"Waiting {sec}s")
                qping(f"COOLDOWN... {sec}s")
                time.sleep(1)
        else:
            time.sleep(PING_INTERVAL_SECONDS)

    qlog("Watchdog: stopped")
    qstatus("STOPPED", "Stopped")


# =========================
# SPLASH SCREEN
# =========================
class Splash(tk.Toplevel):
    def __init__(self, master, duration_ms=2200):
        super().__init__(master)
        self.overrideredirect(True)
        self.configure(bg="#0F172A")

        w, h = 520, 260
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        card = tk.Frame(self, bg="#111827")
        card.place(relx=0.5, rely=0.5, anchor="center", width=480, height=220)

        tk.Label(card, text="Welcome", font=("Segoe UI", 22, "bold"),
                 bg="#111827", fg="#E5E7EB").pack(pady=(18, 6))

        tk.Label(card, text=APP_OWNER_NAME, font=("Segoe UI", 18, "bold"),
                 bg="#111827", fg="#60A5FA").pack(pady=(0, 10))

        now_date = time.strftime("%A, %d %B %Y")
        now_time = time.strftime("%H:%M:%S")
        tk.Label(card, text=f"{now_date}\n{now_time}", font=("Segoe UI", 11),
                 bg="#111827", fg="#9CA3AF").pack(pady=(0, 14))

        tk.Label(card, text="Starting program...", font=("Segoe UI", 10),
                 bg="#111827", fg="#9CA3AF").pack()

        self.after(duration_ms, self.destroy)


# =========================
# MAIN UI (COLORED + ORGANIZED) WITH NARROW BUTTONS
# =========================
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_OWNER_NAME} - Router Watchdog")
        self.geometry("980x680")
        self.minsize(920, 640)
        self.configure(bg="#0F172A")

        self.worker_thread = None

        # ---- ttk styling (same “full version” style)
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame", background="#0F172A")
        style.configure("Card.TFrame", background="#111827", relief="flat")
        style.configure("Title.TLabel", background="#0F172A", foreground="#E5E7EB",
                        font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", background="#0F172A", foreground="#9CA3AF",
                        font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background="#111827", foreground="#E5E7EB",
                        font=("Segoe UI", 12, "bold"))

        # Buttons: narrow + consistent
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Primary.TButton", background="#2563EB", foreground="#FFFFFF")
        style.map("Primary.TButton", background=[("active", "#1D4ED8")])

        style.configure("Danger.TButton", background="#DC2626", foreground="#FFFFFF")
        style.map("Danger.TButton", background=[("active", "#B91C1C")])

        style.configure("Ghost.TButton", background="#374151", foreground="#E5E7EB")
        style.map("Ghost.TButton", background=[("active", "#4B5563")])

        # Header
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill=tk.X, padx=18, pady=(16, 10))

        ttk.Label(header, text=f"{APP_OWNER_NAME} Router Watchdog", style="Title.TLabel").pack(side=tk.LEFT)
        ttk.Label(header, text=f"Monitoring: {ROUTER_IP} | Auto action: Factory Reset",
                  style="Sub.TLabel").pack(side=tk.LEFT, padx=(14, 0))

        # Main layout
        main = ttk.Frame(self, style="TFrame")
        main.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 16))

        left = ttk.Frame(main, style="TFrame")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = ttk.Frame(main, style="TFrame")
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(14, 0))

        # Status card
        status_card = ttk.Frame(left, style="Card.TFrame")
        status_card.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(status_card, text="Status", style="CardTitle.TLabel").pack(anchor="w", padx=14, pady=(12, 6))

        self.status_badge = tk.Label(
            status_card, text="IDLE",
            font=("Segoe UI", 12, "bold"),
            bg="#374151", fg="#E5E7EB",
            padx=12, pady=6
        )
        self.status_badge.pack(anchor="w", padx=14, pady=(0, 8))

        self.status_detail = tk.Label(
            status_card,
            text="Press Start to begin monitoring.",
            font=("Segoe UI", 10),
            bg="#111827", fg="#9CA3AF"
        )
        self.status_detail.pack(anchor="w", padx=14, pady=(0, 12))

        # Ping card
        ping_card = ttk.Frame(left, style="Card.TFrame")
        ping_card.pack(fill=tk.BOTH, expand=True)
        ttk.Label(ping_card, text="Ping Stream", style="CardTitle.TLabel").pack(anchor="w", padx=14, pady=(12, 6))

        self.ping_text = tk.Text(
            ping_card, height=10, wrap="word",
            bg="#0B1220", fg="#E5E7EB",
            insertbackground="#E5E7EB",
            relief="flat", font=("Consolas", 10)
        )
        self.ping_text.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        # Logs card
        logs_card = ttk.Frame(left, style="Card.TFrame")
        logs_card.pack(fill=tk.BOTH, expand=True, pady=(12, 0))
        ttk.Label(logs_card, text="Logs", style="CardTitle.TLabel").pack(anchor="w", padx=14, pady=(12, 6))

        self.log_text = tk.Text(
            logs_card, wrap="word",
            bg="#0B1220", fg="#E5E7EB",
            insertbackground="#E5E7EB",
            relief="flat", font=("Consolas", 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        # Controls card (narrow buttons)
        control_card = ttk.Frame(right, style="Card.TFrame")
        control_card.pack(fill=tk.X)
        ttk.Label(control_card, text="Controls", style="CardTitle.TLabel").pack(anchor="w", padx=14, pady=(12, 10))

        self.btn_start = ttk.Button(control_card, text="Start", style="Primary.TButton", command=self.start_watchdog)
        self.btn_start.pack(fill=tk.X, padx=14, pady=(0, 6))

        self.btn_stop = ttk.Button(control_card, text="Stop", style="Ghost.TButton",
                                   command=self.stop_watchdog, state=tk.DISABLED)
        self.btn_stop.pack(fill=tk.X, padx=14, pady=(0, 6))

        self.btn_test_reset = ttk.Button(control_card, text="Test Reset", style="Danger.TButton",
                                         command=self.test_reset_now)
        self.btn_test_reset.pack(fill=tk.X, padx=14, pady=(0, 6))

        self.btn_skip_wizard = ttk.Button(control_card, text="Skip Wizard", style="Ghost.TButton",
                                          command=self.skip_wizard_now)
        self.btn_skip_wizard.pack(fill=tk.X, padx=14, pady=(0, 14))

        # Notes card
        info_card = ttk.Frame(right, style="Card.TFrame")
        info_card.pack(fill=tk.X, pady=(12, 0))
        ttk.Label(info_card, text="Notes", style="CardTitle.TLabel").pack(anchor="w", padx=14, pady=(12, 6))

        info_txt = (
            "• No terminal windows will open.\n"
            "• Wizard is skipped automatically (Next/Finish).\n"
            "• Auto reset triggers on TIMEOUT/NULL.\n"
            "• Factory Reset erases router settings."
        )
        tk.Label(info_card, text=info_txt, justify="left",
                 bg="#111827", fg="#9CA3AF", font=("Segoe UI", 9)).pack(fill=tk.X, padx=14, pady=(0, 14))

        # UI update loop
        self.after(150, self.drain_ui_queue)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- UI helpers
    def set_badge(self, state: str, detail: str):
        colors = {
            "IDLE": ("#374151", "#E5E7EB"),
            "OK": ("#16A34A", "#0B1220"),
            "TIMEOUT": ("#F59E0B", "#0B1220"),
            "FAILED": ("#DC2626", "#0B1220"),
            "RESETTING": ("#2563EB", "#E5E7EB"),
            "COOLDOWN": ("#6D28D9", "#E5E7EB"),
            "STOPPED": ("#374151", "#E5E7EB"),
        }
        bg, fg = colors.get(state, ("#374151", "#E5E7EB"))
        self.status_badge.config(text=state, bg=bg, fg=fg)
        self.status_detail.config(text=detail if detail else "")

    @staticmethod
    def _trim_text(widget: tk.Text, max_lines: int):
        try:
            lines = int(widget.index("end-1c").split(".")[0])
            if lines > max_lines:
                widget.delete("1.0", "11.0")
        except Exception:
            pass

    # ---------- button actions
    def start_watchdog(self):
        if self.worker_thread and self.worker_thread.is_alive():
            return

        stop_event.clear()
        self.worker_thread = threading.Thread(target=watchdog_loop, daemon=True)
        self.worker_thread.start()

        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        qlog("GUI: Start pressed")
        qstatus("OK", "Monitoring...")

    def stop_watchdog(self):
        stop_event.set()
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        qlog("GUI: Stop pressed")
        qstatus("STOPPED", "Stopping...")

    def test_reset_now(self):
        if not messagebox.askyesno("Confirm", "Run Factory Reset flow now?"):
            return
        threading.Thread(target=run_factory_reset, daemon=True).start()

    def skip_wizard_now(self):
        if not messagebox.askyesno("Confirm", "Open router and skip wizard (Next/Finish) now?"):
            return
        threading.Thread(target=manual_skip_wizard_only, daemon=True).start()

    # ---------- queue drain
    def drain_ui_queue(self):
        try:
            while True:
                kind, payload = ui_queue.get_nowait()
                if kind == "log":
                    self.log_text.insert(tk.END, payload + "\n")
                    self.log_text.see(tk.END)
                    self._trim_text(self.log_text, 900)
                elif kind == "ping":
                    self.ping_text.insert(tk.END, payload + "\n")
                    self.ping_text.see(tk.END)
                    self._trim_text(self.ping_text, 120)
                elif kind == "status":
                    state, detail = payload
                    self.set_badge(state, detail)
        except queue.Empty:
            pass

        self.after(150, self.drain_ui_queue)

    def on_close(self):
        stop_event.set()
        self.destroy()


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app = App()
    app.withdraw()
    Splash(app, duration_ms=2200)
    app.after(2300, app.deiconify)
    app.mainloop()
