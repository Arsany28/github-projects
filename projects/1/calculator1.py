def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return "Error! Division by zero." if y == 0 else x / y

def calculator():
    while True:

        print("1. Add  2. Subtract  3. Multiply  4. Divide  5. Exit")
        
        choice = input("Enter choice (1/2/3/4/5): ")
        if choice == '5':
            print("Goodbye!")
            break

        if choice not in ('1', '2', '3', '4'):
            print("Invalid input! Try again.")
            continue

        try:
            num1 = int(input("Enter first number: "))
            num2 = int(input("Enter second number: "))
        except ValueError:
            print("Invalid input! Please enter numbers.")
            continue

        operations = {
            '1': add(num1, num2),
            '2': subtract(num1, num2),
            '3': multiply(num1, num2),
            '4': divide(num1, num2),
        }

        print(f"Result: {operations[choice]}")

# Run the calculator
calculator()
