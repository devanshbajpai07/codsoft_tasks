#!/usr/bin/env python3
"""
Simple Calculator Program
A basic calculator that performs arithmetic operations on two numbers.
Author: Human-like Code
Date: 2025
"""

def get_number(prompt):
    """
    Get a valid number from user input.
    Keeps asking until a valid number is entered.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("Please enter a number, don't leave it empty!")
                continue
            number = float(user_input)
            return number
        except ValueError:
            print("That's not a valid number. Please try again.")

def get_operation():
    """
    Get a valid operation choice from the user.
    Returns the operation symbol.
    """
    print("\nChoose an operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            return '+'
        elif choice == '2':
            return '-'
        elif choice == '3':
            return '*'
        elif choice == '4':
            return '/'
        else:
            print("Invalid choice! Please enter 1, 2, 3, or 4.")

def perform_calculation(num1, num2, operation):
    """
    Perform the actual calculation based on the operation.
    Returns the result or an error message.
    """
    if operation == '+':
        result = num1 + num2
        operation_name = "Addition"
    elif operation == '-':
        result = num1 - num2
        operation_name = "Subtraction"
    elif operation == '*':
        result = num1 * num2
        operation_name = "Multiplication"
    elif operation == '/':
        if num2 == 0:
            return None, "Error: Cannot divide by zero!"
        result = num1 / num2
        operation_name = "Division"
    else:
        return None, "Error: Invalid operation!"
    
    return result, operation_name

def format_result(result):
    """
    Format the result to look nice.
    Removes unnecessary decimal places for whole numbers.
    """
    if result == int(result):
        return str(int(result))
    else:
        return f"{result:.6f}".rstrip('0').rstrip('.')

def display_result(num1, num2, operation, result, operation_name):
    """
    Display the calculation result in a nice format.
    """
    print("\n" + "="*50)
    print(f"CALCULATION RESULT")
    print("="*50)
    print(f"Operation: {operation_name}")
    print(f"Expression: {format_result(num1)} {operation} {format_result(num2)}")
    print(f"Result: {format_result(result)}")
    print("="*50)

def ask_continue():
    """
    Ask user if they want to perform another calculation.
    """
    while True:
        choice = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def main():
    """
    Main function that runs the calculator program.
    """
    print("="*50)
    print("        WELCOME TO SIMPLE CALCULATOR")
    print("="*50)
    print("This calculator can perform basic arithmetic operations")
    print("on two numbers: addition, subtraction, multiplication, and division.")
    
    while True:
        try:
            # Get the first number
            print("\n" + "-"*30)
            num1 = get_number("Enter the first number: ")
            
            # Get the operation
            operation = get_operation()
            
            # Get the second number
            num2 = get_number("Enter the second number: ")
            
            # Perform the calculation
            result, operation_name = perform_calculation(num1, num2, operation)
            
            # Check if there was an error
            if result is None:
                print(f"\n{operation_name}")
                continue
            
            # Display the result
            display_result(num1, num2, operation, result, operation_name)
            
            # Ask if user wants to continue
            if not ask_continue():
                break
                
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Let's try again...")

    print("\nThank you for using the Simple Calculator!")
    print("Goodbye! 👋")

# This is the standard way to run a Python program
if __name__ == "__main__":
    main()