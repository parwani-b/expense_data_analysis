import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
from colorama import init
from termcolor import colored

# I don't know about this but either colorama or termcolor uses it 
init()


# Function to establish MySQL connection
def create_connection(host, user, password, database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="expense_data_dev_test"
        )
        if connection.is_connected():
            print(colored('\n••••••••••••••', 'green'))
            print("\nConnected to MySQL database")
        else:
            print("Failed to connect to MySQL database")
    except Error as e:
        print(f"Error: {e}")
    return connection

# Function to execute MySQL query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Function to display main menu
def display_main_menu():
    print("*** Welcome to expense tracker ***\n\n")
    print("Please select your choice from the menu options:\n\n")
    print("1. Track expenses for current year\n\n")
    print("2. Track expenses for last year\n\n")
    print("3. Track expenses for the year for your choice\n\n")

# Function to display secondary menu
def display_secondary_menu(year):
    print(f"\n You have selected to track expenses for {year}. What would you like to track from these below options?")
    print("----> 1. How much total monthly expense I had in a specific month?")
    print("----> 2. How much dining out expenses I had in a specific month?")
    print("----> 3. How much grocery expenses I had in a specific month?")
    print("----> 4. How much gas/fuel expenses I had in a specific month?")
    print("----> 5. How much household supplies expenses I had in a specific month?")
    print("----> 6. How much car expenses I had in a specific month?")
    print("----> 7. How much hotel expenses I had in a specific month?")
    print("----> 8. How much heat/gas expenses I had in a specific month?")
    print("----> 9. How much electricity expenses I had in a specific month?")


# Function to get total monthly expense for a specific month
def get_total_expense_by_month(connection, year, month):
    query = f"SELECT SUM(cost) FROM personal_2024_export WHERE YEAR(date) = {year} AND MONTH(date) = {month}"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] is not None else 0

# Function to get total monthly expense in a specific category for a specific month
def get_total_expense_by_category(connection, year, month, category):
    query = f"SELECT SUM(cost) FROM personal_2024_export WHERE YEAR(date) = {year} AND MONTH(date) = {month} AND category = '{category}'"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] is not None else 0


# Function to get user input for month
def get_user_input_for_month():
    while True:
        try:
            month = int(input("\nFor which month would you like to track the expense (select month from 1-12)? "))
            if 1 <= month <= 12:
                return month
            else:
                print("Invalid input. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Function to display result based on user's choice
def display_result(choice, year, month, connection):
    if choice == 1:
        total_expense = get_total_expense_by_month(connection, year, month)
        print(f"\nTotal monthly expense in {year}-{month}: ${total_expense:.2f}")
    elif choice == 2:
        dining_out_expense = get_total_expense_by_category(connection, year, month, 'Dining out')
        print(f"\nTotal dining out expenses in {year}-{month}: ${dining_out_expense:.2f}")
    elif choice == 3:
        grocery_expense = get_total_expense_by_category(connection, year, month, 'Groceries')
        print(f"\nTotal grocery expenses in {year}-{month}: ${grocery_expense:.2f}")
    elif choice == 4:
        gas_expense = get_total_expense_by_category(connection, year, month, 'Gas/fuel')
        print(f"\nTotal gas/fuel expenses in {year}-{month}: ${gas_expense:.2f}")
    elif choice == 5:
        household_supply_expense = get_total_expense_by_category(connection, year, month, 'Household supplies')
        print(f"\nTotal household expenses in {year}-{month}: ${household_supply_expense:.2f}")
    elif choice == 6:
        car_expense = get_total_expense_by_category(connection, year, month, 'Car')
        print(f"\nTotal car expenses in {year}-{month}: ${car_expense:.2f}")
    elif choice == 7:
        hotel_expense = get_total_expense_by_category(connection, year, month, 'Hotel')
        print(f"\nTotal hotel expenses in {year}-{month}: ${hotel_expense:.2f}")
    elif choice == 8:
        heat_expense = get_total_expense_by_category(connection, year, month, 'Heat/Gas')
        print(f"\nTotal heat/gas expenses in {year}-{month}: ${heat_expense:.2f}")
    elif choice == 9:
        electric_expense = get_total_expense_by_category(connection, year, month, 'Electricity')
        print(f"\nTotal electricity expenses in {year}-{month}: ${electric_expense:.2f}")



# Main function
def main():
    try:
        host = "127.0.0.1",
        user = "root",
        password = "root",
        database = "expense_data_dev_test"

        connection = create_connection(host, user, password, database)

        if connection:
            display_main_menu()
            main_menu_choice = int(input())

            if main_menu_choice in [1, 2]:
                current_year = datetime.now().year
                last_year = current_year - 1
                year = current_year if main_menu_choice == 1 else last_year
                
                display_secondary_menu(year)
                secondary_menu_choice = int(input())

                if secondary_menu_choice in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    month = get_user_input_for_month()
                    display_result(secondary_menu_choice, year, month, connection)
                else:
                    print("Invalid choice for secondary menu.")
            
            elif main_menu_choice == 3:
                year_input = input("Please enter a 4-digit year: ")
                year = datetime.strptime(year_input, "%Y").year
                # if main_menu_choice == 1:
                    # year = current_year
                # elif main_menu_choice == 2:
                    # year =  last_year
                # elif main_menu_choice == 3:
                    # year = input("Please enter a 4-digit year: ")
                    # if year.isdigit() and len(year) == 4:
                        # return int(year)
                    # else:
                        # return int(input("Invalid value!! Please try again..\n"))
                
                display_secondary_menu(year)
                secondary_menu_choice = int(input())

                if secondary_menu_choice in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    month = get_user_input_for_month()
                    display_result(secondary_menu_choice, year, month, connection)
                else:
                    print("Invalid choice for secondary menu.")

            else:
                print("Invalid choice for main menu.")
        
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()