import re
import pandas as pd
import json

def validate_password(password):
    # Check if password is at least 8 characters
    if len(password) < 8:
        return False
    # Check if password contains both uppercase and lowercase letters
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
        return False
    return True

def registration_system():
    print("Welcome to the Registration System!")
    print("The password should be 8 characters with a mix of upper and lower cases")
    
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        if validate_password(password):
            print("Registration successful!")
            # Create a DataFrame with the registration data
            data = {
                'Username': [username],
                'Password': [password]
            }
            df = pd.DataFrame(data)
            
            # Create notebook structure
            notebook = {
                "cells": [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": [
                            "import pandas as pd\n",
                            f"df = pd.DataFrame({data})\n",
                            "df"
                        ]
                    }
                ],
                "metadata": {
                    "kernelspec": {
                        "display_name": "Python 3",
                        "language": "python",
                        "name": "python3"
                    }
                },
                "nbformat": 4,
                "nbformat_minor": 4
            }
            
            # Save as ipynb file
            with open('registration_data.ipynb', 'w') as f:
                json.dump(notebook, f, indent=1)
            
            print("Registration data has been saved to registration_data.ipynb")
            break
        else:
            print("Invalid password! Please try again.")

if __name__ == "__main__":
    registration_system()
