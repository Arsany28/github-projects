import os
import nbformat as nbf  # For saving notebook

# Updated Dataset for Service #1
new_car_id = [
    ["13-04-2025", "Sunday",    [6, 10, 1, 10, 7]],
    ["14-04-2025", "Monday",    [10, 2, 10, 6, 4]],
    ["15-04-2025", "Tuesday",   [3, 1, 10, 10, 9]],
    ["16-04-2025", "Wednesday", [10, 8, 10, 7, 3]],
    ["17-04-2025", "Thursday",  [2, 10, 4, 10, 1]]
]

time_slots = ['9:00', '10:00', '11:00', '12:00', '1:00']
USERS_FILE = 'bms_users.txt'

# -------------------- Utility functions --------------------
def calculate_mean(service):
    total_reservations = sum(sum(day[2]) for day in service)
    total_slots = len(service) * len(time_slots)
    return total_reservations / total_slots

def most_crowded_day(service):
    crowded = max(service, key=lambda day: sum(day[2]))
    return crowded[0], crowded[1], sum(crowded[2])

def least_crowded_day(service):
    least = min(service, key=lambda day: sum(day[2]))
    return least[0], least[1], sum(least[2])

# -------------------- Registration & Login --------------------
def register():
    print("\nThe password should be 8 characters with a mix of upper and lower cases.")
    while True:
        username = input("Enter new username: ").strip()
        password = input("Enter new password: ").strip()
        if len(password) >= 8 and any(c.islower() for c in password) and any(c.isupper() for c in password):
            with open(USERS_FILE, 'a') as f:
                f.write(f"{username},{password}\n")
            print("Registration successful! Please log in.")
            return True
        else:
            print("Password not strong enough. Please try again.")

def login():
    if not os.path.exists(USERS_FILE):
        print("No users found. Please sign up first.")
        return None
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    with open(USERS_FILE, 'r') as f:
        users = [line.strip().split(',') for line in f]
    for user, passw in users:
        if user == username and passw == password:
            print("Login successful.")
            return username
    print("Login failed. Please try again or sign up.")
    return None

# -------------------- Notebook Save Function --------------------
def save_to_notebook(username, service, date, day, time, user_id, full_name, notebook_path="bms.ipynb"):
    if os.path.exists(notebook_path):
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbf.read(f, as_version=4)
    else:
        nb = nbf.v4.new_notebook()
        nb['cells'] = []

    cell_content = f"""
### Reservation Confirmation

- **User:** {username}  
- **Service:** {service}  
- **Date:** {date} ({day})  
- **Time:** {time}  
- **ID:** {user_id}  
- **Full Name:** {full_name}  
"""
    nb['cells'].append(nbf.v4.new_markdown_cell(cell_content))
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Reservation saved to '{notebook_path}'.")

# -------------------- Booking Data --------------------
services = [
    "New Car ID", 
    "Renew Car ID", 
    "New Driving License", 
    "Renew Driving License", 
    "Lost ID Replacement"
]

datasets = {
    1: new_car_id,
    2: [
        ["18-04-2025", "Sunday",    [9, 8, 7, 10, 10]],
        ["19-04-2025", "Monday",    [2, 9, 10, 3, 10]],
        ["20-04-2025", "Tuesday",   [1, 1, 10, 9, 10]],
        ["21-04-2025", "Wednesday", [10, 3, 9, 10, 9]],
        ["22-04-2025", "Thursday",  [10, 5, 2, 10, 3]] 
    ],
    3: [
       ["18-04-2025", "Sunday",    [10, 2, 10, 4, 1]],
       ["19-04-2025", "Monday",    [3, 10, 4, 10, 5]],
       ["20-04-2025", "Tuesday",   [9, 10, 2, 6, 10]],
       ["21-04-2025", "Wednesday", [10, 3, 10, 5, 7]],
       ["22-04-2025", "Thursday",  [2, 10, 4, 6, 10]]
    ],
    4: [
        ["18-04-2025", "Sunday",    [10, 4, 5, 10, 1]],
        ["19-04-2025", "Monday",    [5, 6, 10, 3, 10]],
        ["20-04-2025", "Tuesday",   [10, 8, 1, 3, 10]],
        ["21-04-2025", "Wednesday", [2, 9, 10, 10, 6]],
        ["22-04-2025", "Thursday",  [10, 7, 4, 10, 3]]
    ],
    5: [
        ["18-04-2025", "Sunday",    [9, 10, 10, 9, 1]],
        ["19-04-2025", "Monday",    [3, 10, 4, 10, 4]],
        ["20-04-2025", "Tuesday",   [2, 9, 6, 10, 10]],
        ["21-04-2025", "Wednesday", [6, 10, 5, 10, 2]],
        ["22-04-2025", "Thursday",  [9, 10, 4, 10, 4]]
    ]
}

# -------------------- Booking Flow --------------------
def booking_flow(username):
    print("\nAvailable services:")
    for i, service in enumerate(services, 1):
        print(f"{i}. {service}")
    while True:
        choice = input("Select the service by number (1-5): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 5:
            service_no = int(choice)
            break
        else:
            print("Invalid choice. Please select 1-5.")

    dataset = datasets[service_no]
    print("\nAvailable days:")
    for i, day in enumerate(dataset, 1):
        print(f"{i}. {day[1]} ({day[0]})")
    while True:
        day_choice = input("Select the day by number: ").strip()
        if day_choice.isdigit() and 1 <= int(day_choice) <= len(dataset):
            day_idx = int(day_choice) - 1
            break
        else:
            print("Invalid choice.")

    day_data = dataset[day_idx]
    print(f"\nAvailable time slots for {day_data[1]} ({day_data[0]}):")
    for i, (slot, reserved) in enumerate(zip(time_slots, day_data[2]), 1):
        available = 10 - reserved
        status = f"({available} slots available)" if available > 0 else "(Fully booked)"
        print(f"{i}. {slot} {status}")

    while True:
        slot_choice = input("Select the slot by number: ").strip()
        if slot_choice.isdigit() and 1 <= int(slot_choice) <= len(time_slots):
            slot_idx = int(slot_choice) - 1
            if day_data[2][slot_idx] < 10:
                break
            else:
                print("Selected slot is fully booked. Please select another slot.")
        else:
            print("Invalid slot selection.")

    user_id = input("Enter your ID: ").strip()
    full_name = input("Enter your full name: ").strip()
    day_data[2][slot_idx] += 1

    # Save reservation to notebook
    save_to_notebook(
        username=username,
        service=services[service_no - 1],
        date=day_data[0],
        day=day_data[1],
        time=time_slots[slot_idx],
        user_id=user_id,
        full_name=full_name
    )

    print("\nReservation confirmed!")
    print("-" * 40)

# -------------------- Main --------------------
def main():
    mean_reservations = calculate_mean(new_car_id)
    most_crowded = most_crowded_day(new_car_id)
    least_crowded = least_crowded_day(new_car_id)

    print(f"\nMean reservations for Service #1: {mean_reservations:.2f}")
    print(f"Most crowded day: {most_crowded[0]} ({most_crowded[1]}) with {most_crowded[2]} total reservations")
    print(f"Least crowded day: {least_crowded[0]} ({least_crowded[1]}) with {least_crowded[2]} total reservations")

    while True:
        print("\nWelcome to the Booking Management System (BMS)")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            username = login()
            if username:
                booking_flow(username)
        elif choice == '2':
            if register():
                username = login()
                if username:
                    booking_flow(username)
        elif choice == '3':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
