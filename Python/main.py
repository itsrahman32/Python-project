import operation
import read
import write
import datetime
import random

# ----------------------------- Main Program -----------------------------

def main():
    """
    Main function to run the WeCare Wholesale System.

    This function runs the main menu interface for the WeCare Wholesale System, allowing users to:
    - View available products with their markups.
    - Buy (restock) products.
    - Sell products.
    - Exit the system.

    The system continues to loop through the menu options until the user selects 'Exit'.

    Parameters:
    -----------
    None

    Returns:
    --------
    None

    Raises:
    -------
    Exception
        If there is an unexpected error during program execution, it is caught and displayed to the user.
    """
    while True:
        try:
            print("\nWELCOME TO WECARE WHOLESALE SYSTEM")
            print("------------------------------------")
            print("\nAddress: Bagbazar, Kathmandu | Ph. 9821000760")
            print("---------------------------------------------")
            
            # Display the list of products with their markup
            read.display_products(read.read_products(), show_markup=True)
            
            print("\nMenu:")
            print("1. Buy Product (Restock)")
            print("2. Sell Product")
            print("3. Exit")

            # User selects an option
            choice = input("Enter Your choice (1/2/3): ")

            if choice == "1":
                # Buy (Restock) product
                operation.buy_product()
            elif choice == "2":
                # Sell product
                operation.sell_product()
            elif choice == "3":
                # Exit the application
                print("Thank you for using WeCare Wholesale System")
                break
            else:
                # If user enters an invalid option
                print("Invalid choice.")
        except Exception as err:
            print("An unexpected error occurred:", err)

# Entry point of the program
if __name__ == "__main__":
    main()
