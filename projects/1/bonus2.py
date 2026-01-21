
input_string = input("Enter string ")

if len(input_string) >= 3:
    
    middle_index = len(input_string) // 2
    
    middle_three = input_string[middle_index - 1:middle_index + 2]
    print("The Three middle letters :", middle_three)
else:
    print("String should contain three letters at least ")
