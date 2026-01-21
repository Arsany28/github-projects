import os
import json
import re

# ---------- DATASETS ----------

time_slots = ['9:00', '10:00', '11:00', '12:00', '1:00']

services = [
    'New Car License Issuance',        # Service #1
    'Car License Renewal',
    'New Driving License Issuance',
    'Driving License Renewal',
    'Replacement for Lost ID'
]

# Dataset 1 for stats (used only in part 1.1)
new_car_id_1 = [
    ["13-04-2025", "Sunday",    [4, 6, 7, 8, 1]],
    ["14-04-2025", "Monday",    [2, 1, 8, 6, 4]],
    ["15-04-2025", "Tuesday",   [3, 1, 6, 6, 4]],
    ["16-04-2025", "Wednesday", [1, 6, 9, 8, 3]],
    ["17-04-2025", "Thursday",  [4, 7, 7, 10, 1]]
]

# Dataset 2 for booking system
new_car_id = [
    ["18-04-2025", "Sunday",    [6, 10, 1, 10, 7]],
    ["19-04-2025", "Monday",    [10, 2, 10, 6, 4]],
    ["20-04-2025", "Tuesday",   [3, 1, 10, 10, 9]],
    ["21-04-2025", "Wednesday", [10, 8, 10, 7, 3]],
    ["22-04-2025", "Thursday",  [2, 10, 4, 10, 1]]
]

renew_car_id = [
    ["18-04-2025", "Sunday",    [9, 8, 7, 10, 10]],
    ["19-04-2025", "Monday",    [2, 9, 10, 3, 10]],
    ["20-04-2025", "Tuesday",   [1, 1, 10, 9, 10]],
    ["21-04-2025", "Wednesday", [10, 3, 9, 10, 9]],
    ["22-04-2025", "Thursday",  [10, 5, 2, 10, 3]]
]

new_driving_license = [
    ["18-04-2025", "Sunday",    [10, 2, 10, 4, 1]],
    ["19-04-2025", "Monday",    [3, 10, 4, 10, 5]],
    ["20-04-2025", "Tuesday",   [9, 10, 2, 6, 10]],
    ["21-04-2025", "Wednesday", [10, 3, 10, 5, 7]],
    ["22-04-2025", "Thursday",  [2, 10, 4, 6, 10]]
]

renew_driving_license = [
    ["18-04-2025", "Sunday",    [10, 4, 5, 10, 1]],
    ["19-04-2025", "Monday",    [5, 6, 10, 3, 10]],
    ["20-04-2025", "Tuesday",   [10, 8, 1, 3, 10]],
    ["21-04-2025", "Wednesday", [2, 9, 10, 10, 6]],
    ["22-04-2025", "Thursday",  [10, 7, 4, 10, 3]]
]

lost_id = [
    ["18-04-2025", "Sunday",    [9, 10, 10, 9, 1]],
    ["19-04-2025", "Monday",    [3, 10, 4, 10, 4]],
    ["20-04-2025", "Tuesday",   [2, 9, 6, 10, 10]],
    ["21-04-2025", "Wednesday", [6, 10, 5, 10, 2]],
    ["22-04-2025", "Thursday",  [9, 10, 4, 10, 4]]
]

services_data = [
    new_car_id,
    renew_car_id,
    new_driving_license,
    renew_driving_license,
    lost_id
]

# ---------- UTILS ----------

USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def password_is_strong(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password)
    )

# ---------- PART 1.1 ----------

def calculate_mean(service_data):
    total = 0
    count = 0
    for day in service_data:
        total += sum(day[2])
        count += len(day[2])
    return total / count if count else 0

def most_crowded_day(service_data):
    max_res = -1
    max_day = None
    for day in service_data:
        total_res = sum(day[2])
        if total_res > max_res:
            max_res = total_res
            max_day = f"{day[0]} ({day[1]})"
    return max_day, max_res

def least_crowded_day(service_data):
    min_res = float('inf')
    min_day = None
    for day in service_data:
        total_res = sum(day[2])
        if total_res < min_res:
            min_res = total_res
            min_day = f"{day[0]} ({day[1]})"
    return min_day, min_res

# ---------- PART 1.2 ----------

def signup():
    users = load_users()
    print("\n--- Signup ---")
    while True:
        username = input("Enter username: ").strip()
        if username in users:
            print("Username already exists. Try another.")
        elif username == "":
            print("Username cannot be empty.")
        else:
            break

    while True:
        print("The password should be 8 characters with a mix of upper and lower cases.")
        password = input("Enter password: ")
        if not password_is_strong(password):
            print("Weak password. Please follow the requirements.")
            continue
        confirm = input("Confirm password: ")
        if password != confirm:
            print("Passwords do not match. Try again.")
            continue
        break

    users[username] = password
    save_users(users)
    print("Signup successful! You can now login.")

def login():
    users = load_users()
    print("\n--- Login ---")
    attempts = 3
    while attempts > 0:
        username = input("Username: ").strip()
        password = input("Password: ")
        if username in users and users[username] == password:
            print("Login successful!")
            return True
        else:
            attempts -= 1
            print(f"Login failed, {attempts} attempts left. Try again or sign up.")
    return False

# ---------- PART 1.3 Booking ----------

def display_services():
    print("\nAvailable Services:")
    for idx, service in enumerate(services, 1):
        print(f"{idx}. {service}")

def display_days(service_index):
    print("\nAvailable days:")
    for idx, day in enumerate(services_data[service_index], 1):
        print(f"{idx}. {day[0]} ({day[1]})")

def display_available_time_slots(service_index, day_index):
    day = services_data[service_index][day_index]
    print(f"\nAvailable time slots for {day[1]} ({day[0]}):")
    available_slots = []
    for i, reserved in enumerate(day[2]):
        remaining = 10 - reserved
        if remaining > 0:
            print(f"{i+1}. {time_slots[i]} ({remaining} slots available)")
            available_slots.append(i+1)
    if not available_slots:
        print("Sorry, no available time slots for this day.")
    return available_slots

def book_slot():
    display_services()
    while True:
        try:
            service_choice = int(input("Select a service by number: "))
            if 1 <= service_choice <= len(services):
                service_index = service_choice - 1
                break
            else:
                print("Invalid service number. Try again.")
        except ValueError:
            print("Please enter a number.")

    service_name = services[service_index]

    # Select day
    while True:
        display_days(service_index)
        try:
            day_choice = int(input("Select a day by number: "))
            if 1 <= day_choice <= len(services_data[service_index]):
                day_index = day_choice - 1
                break
            else:
                print("Invalid day number. Try again.")
        except ValueError:
            print("Please enter a number.")

    # Select time slot - updated logic for full slots
    while True:
        available_slots = display_available_time_slots(service_index, day_index)
        if not available_slots:
            print("No slots available for this day. Please select another day.")
            # Let user select day again
            while True:
                display_days(service_index)
                try:
                    day_choice = int(input("Select a different day by number: "))
                    if 1 <= day_choice <= len(services_data[service_index]):
                        day_index = day_choice - 1
                        break
                    else:
                        print("Invalid day number. Try again.")
                except ValueError:
                    print("Please enter a number.")
            continue  # Recheck available slots after day change

        slot_choice = input("Select a time slot by number: ")
        if not slot_choice.isdigit():
            print("Please enter a valid number.")
            continue
        slot_choice = int(slot_choice)

        if slot_choice not in available_slots:
            # The slot is either fully booked or invalid
            print("Selected slot is fully booked or invalid. Please choose from the available slots.")
            continue
        else:
            break

    # Input user info
    user_id = input("Enter your ID: ").strip()
    full_name = input("Enter your full name: ").strip()

    # Confirm booking by increasing reservation count
    day_data = services_data[service_index][day_index]
    day_data[2][slot_choice-1] += 1

    print("\nBooking Confirmed!")
    print(f"Service: {service_name}")
    print(f"Date: {day_data[0]} ({day_data[1]})")
    print(f"Time: {time_slots[slot_choice-1]}")
    print(f"ID: {user_id}")
    print(f"Name: {full_name}")

# ---------- MAIN ----------

def main():
    # Show stats for Service #1 from dataset 1
    print("--- Service #1 Booking Stats ---")
    mean_val = calculate_mean(new_car_id_1)
    print(f"Mean reservations: {mean_val:.2f}")

    mc_day, mc_res = most_crowded_day(new_car_id_1)
    lc_day, lc_res = least_crowded_day(new_car_id_1)
    print(f"Most crowded day: {mc_day} with {mc_res} reservations")
    print(f"Least crowded day: {lc_day} with {lc_res} reservations")

    print("\nWelcome to Car Licensing Booking Management System")
    while True:
        print("\n1. Signup\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            signup()
        elif choice == '2':
            if login():
                book_slot()
            else:
                print("Login failed. Try again or sign up.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
