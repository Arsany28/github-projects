import pandas as pd
import json
from datetime import datetime, timedelta

# Define time slots
time_slots = ['9:00', '10:00', '11:00', '12:00', '1:00']

# Initialize service data with availability tracking
# Format: [date, day, [reservations per time slot]]
services_data = {
    "New Car ID": [
        ["18-04-2025", "Sunday",    [6, 10, 1, 10, 7]],
        ["19-04-2025", "Monday",    [10, 2, 10, 6, 4]],
        ["20-04-2025", "Tuesday",   [3, 1, 10, 10, 9]],
        ["21-04-2025", "Wednesday", [10, 8, 10, 7, 3]],
        ["22-04-2025", "Thursday",  [2, 10, 4, 10, 1]]
    ],
    "Renew Car ID": [
        ["18-04-2025", "Sunday",    [9, 8, 7, 10, 10]],
        ["19-04-2025", "Monday",    [2, 9, 10, 3, 10]],
        ["20-04-2025", "Tuesday",   [1, 1, 10, 9, 10]],
        ["21-04-2025", "Wednesday", [10, 3, 9, 10, 9]],
        ["22-04-2025", "Thursday",  [10, 5, 2, 10, 3]]
    ],
    "New Driving License": [
        ["18-04-2025", "Sunday",    [10, 2, 10, 4, 1]],
        ["19-04-2025", "Monday",    [3, 10, 4, 10, 5]],
        ["20-04-2025", "Tuesday",   [9, 10, 2, 6, 10]],
        ["21-04-2025", "Wednesday", [10, 3, 10, 5, 7]],
        ["22-04-2025", "Thursday",  [2, 10, 4, 6, 10]]
    ],
    "Renew Driving License": [
        ["18-04-2025", "Sunday",    [10, 4, 5, 10, 1]],
        ["19-04-2025", "Monday",    [5, 6, 10, 3, 10]],
        ["20-04-2025", "Tuesday",   [10, 8, 1, 3, 10]],
        ["21-04-2025", "Wednesday", [2, 9, 10, 10, 6]],
        ["22-04-2025", "Thursday",  [10, 7, 4, 10, 3]]
    ],
    "Lost ID": [
        ["18-04-2025", "Sunday",    [9, 10, 10, 9, 1]],
        ["19-04-2025", "Monday",    [3, 10, 4, 10, 4]],
        ["20-04-2025", "Tuesday",   [2, 9, 6, 10, 10]],
        ["21-04-2025", "Wednesday", [6, 10, 5, 10, 2]],
        ["22-04-2025", "Thursday",  [9, 10, 4, 10, 4]]
    ]
}

def signup_system():
    """Handle user registration"""
    print("Welcome to the Service Booking System!")
    print("Please sign up to continue.")
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    user_data = {
        'Username': [username],
        'Password': [password]
    }
    
    with open('registration_data.json', 'w') as f:
        json.dump(user_data, f, indent=1)
    
    print("Sign up successful! You can now log in.")

def login_system():
    """Handle user authentication"""
    print("Welcome to the Service Booking System!")
    
    try:
        with open('registration_data.json', 'r') as f:
            user_data = json.load(f)
            users_df = pd.DataFrame(user_data)
    except:
        print("No registration data found. Please sign up first.")
        return False

    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        if username in users_df['Username'].values:
            user_idx = users_df[users_df['Username'] == username].index[0]
            if users_df.iloc[user_idx]['Password'] == password:
                print("Login successful!")
                return True
        print("Invalid credentials! Please try again.")

def display_services():
    """Display available services"""
    services = {i+1: service for i, service in enumerate(services_data.keys())}
    print("\nAvailable Services:")
    for key, value in services.items():
        print(f"{key}. {value}")
    return services

def get_available_days():
    """Get list of available booking days"""
    return [day[0] for day in services_data["New Car ID"]]

def get_available_slots(service, selected_day):
    """Get available time slots for a service on a specific day"""
    day_data = next((day for day in services_data[service] if day[0] == selected_day), None)
    if not day_data:
        return []
    
    available_slots = []
    for i, slots in enumerate(day_data[2]):
        if slots < 10:
            available_slots.append((time_slots[i], 10 - slots))
    return available_slots

def booking_system():
    """Main booking system function"""
    if not login_system():
        return

    # Service selection
    services = display_services()
    while True:
        try:
            service_choice = int(input("\nSelect service number: "))
            if service_choice in services:
                selected_service = services[service_choice]
                break
            print("Invalid service number!")
        except ValueError:
            print("Please enter a valid number!")

    # Day selection
    available_days = get_available_days()
    print("\nAvailable Days:")
    for i, day in enumerate(available_days, 1):
        print(f"{i}. {day}")
    
    while True:
        try:
            day_choice = int(input("\nSelect day number: "))
            if 1 <= day_choice <= len(available_days):
                selected_day = available_days[day_choice-1]
                break
            print("Invalid day number!")
        except ValueError:
            print("Please enter a valid number!")

    # Time slot selection
    available_slots = get_available_slots(selected_service, selected_day)
    if not available_slots:
        print("No available slots for this day!")
        return

    print("\nAvailable Time Slots:")
    for i, (slot, available) in enumerate(available_slots, 1):
        print(f"{i}. {slot} ({available} slots available)")
    
    while True:
        try:
            slot_choice = int(input("\nSelect time slot number: "))
            if 1 <= slot_choice <= len(available_slots):
                selected_slot = available_slots[slot_choice-1][0]
                break
            print("Invalid slot number!")
        except ValueError:
            print("Please enter a valid number!")

    # User details
    user_id = input("\nEnter your ID: ")
    full_name = input("Enter your full name: ")

    # Save booking
    booking_data = {
        'Service': [selected_service],
        'Day': [selected_day],
        'Time': [selected_slot],
        'ID': [user_id],
        'Full Name': [full_name]
    }
    
    with open('booking_data.json', 'w') as f:
        json.dump(booking_data, f, indent=1)

    # Update availability
    for day_data in services_data[selected_service]:
        if day_data[0] == selected_day:
            slot_index = time_slots.index(selected_slot)
            day_data[2][slot_index] += 1
            break

    # Confirmation
    print("\nBooking Confirmation:")
    print(f"Service: {selected_service}")
    print(f"Day: {selected_day}")
    print(f"Time: {selected_slot}")
    print(f"ID: {user_id}")
    print(f"Full Name: {full_name}")
    print("\nBooking has been saved to booking_data.json")

if __name__ == "__main__":
    signup_system()
    booking_system()
