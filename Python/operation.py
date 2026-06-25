import read
import write
import datetime
import random

# ----------------------------- Buy Product -----------------------------

def buy_product():
    """
    Handles the buying (restocking) of products, including updating the inventory 
    and generating an invoice for the transaction.
    """
    products = read.read_products()
    if not products:
        return
    read.display_products(products)
    vendor_name = input("Enter vendor name: ")
    selected = []
    total = 0
    successful_transaction = False

    while True:
        sn = input("Enter S.N of product to restock (or 'new' to add new product, or 'done' to finish): ")

        if sn.lower() == "done":
            break
        elif sn.lower() == "new":
            name = input("Enter product name: ")
            brand = input("Enter brand: ")
            try:
                quantity = int(input("Enter quantity to add: "))
                price = int(input("Enter cost price (before markup): "))
            except ValueError:
                print("Invalid input. Please enter valid numbers for quantity and price.")
                continue
            country = input("Enter country of origin: ")
            new_sn = str(len(products) + 1)

            new_product = {
                "sn": new_sn,
                "name": name,
                "brand": brand,
                "quantity": quantity,
                "price": price,
                "country": country
            }
            products.append(new_product)
            selected.append([name, brand, quantity, price, quantity * price])
            total += quantity * price
            print("New product '" + name + "' added with S.N " + new_sn + ".")
            successful_transaction = True

        else:
            found = False
            for p in products:
                if p["sn"] == sn:
                    found = True
                    try:
                        qty = int(input("Enter quantity to add: "))
                        if qty <= 0:
                            print("Quantity must be a positive integer. Please try again")
                            break
                    except ValueError:
                        print("Invalid input.please enter a valid number")
                        break
                    try:
                        new_price = int(input("Enter updated cost price(before markup)"))
                    except ValueError:
                        print("Invalid input.please enter a valid number")
                        break
                    
                    p["quantity"] = int(p["quantity"]) + qty
                    p["price"] = new_price
                    amount = qty * new_price
                    selected.append([p["name"], p["brand"], qty, new_price, amount])
                    total += amount
                    print("Product '" + p["name"] + "' restocked. New quantity: " + str(p["quantity"]))
                    successful_transaction = True
                    break

           
    write.write_products(products)

    if successful_transaction:
        now = datetime.datetime.now()
        voucher = str(random.randint(1000, 9999))
        fname = "invoice_buy_" + voucher + "_" + now.strftime('%Y%m%d%H%M') + ".txt"
        invoice = "Voucher No: " + voucher + "\nVendor Name: " + vendor_name + "\nDate: " + now.strftime('%Y-%m-%d %H:%M') + "\n\n"
        invoice += "Product       Brand         Qty   Price   Amount\n"

        for item in selected:
            name = item[0]
            brand = item[1]
            qty = str(item[2])
            price = str(item[3])
            amount = str(item[4])

            line = name + " " * (14 - len(name))
            line += brand + " " * (14 - len(brand))
            line += qty + " " * (6 - len(qty))
            line += price + " " * (8 - len(price))
            line += amount + "\n"
            invoice += line

        invoice += "\nTotal Amount: " + str(total)
        print(invoice)
        write.save_invoice(invoice, fname)
        print("Voucher Number (Buy): " + voucher)

# ----------------------------- Sell Product -----------------------------
def sell_product():
    """
    Handles the selling of products, including updating the inventory 
    and generating an invoice for the transaction.

    This function allows the user to:
    - View the current list of products with their markup prices.
    - Sell products by entering their S.N (Serial Number).
    - Apply the "Buy 3, Get 1 Free" offer if applicable.
    - Generate an invoice for the transaction.

    Parameters:
    None

    Returns:
    None

    Raises:
    ValueError:
        If the user enters invalid data types for quantity or incorrect phone number format.
    """
    products = read.read_products()
    if not products:
        return
    read.display_products(products, show_markup=True)

    # Get valid customer name
    while True:
        customer_name = input("Enter customer name: ")
        if customer_name != "" and customer_name.isalpha():
            break
        else:
            print("Invalid customer name. Please enter a valid name (alphabets only).")

    # Get valid customer phone number
    while True:
        customer_phone = input("Enter customer phone number (10 digits): ")
        if customer_phone.isnumeric() and len(customer_phone) == 10:
            break
        else:
            print("Invalid phone number. Please enter a valid 10-digit phone number.")

    selected = []
    total = 0
    successful_transaction = False
    item_count = {}

    while True:
        sn = input("Enter S.N of product to sell (or 'done'): ")
        if len(sn) == 4 and (sn[0] == 'd' or sn[0] == 'D') and (sn[1] == 'o' or sn[1] == 'O') and (sn[2] == 'n' or sn[2] == 'N') and (sn[3] == 'e' or sn[3] == 'E'):
            break

        found = False
        for p in products:
            if p["sn"] == sn:
                found = True
                try:
                    qty = int(input("Enter quantity to sell: "))
                except:
                    print("Invalid quantity.")
                    break

                if qty <= 0:
                    print("Quantity must be in positive positive number and greater than 0.")
                    break

                available = int(p["quantity"])
                if sn not in item_count:
                    item_count[sn] = 0
                item_count[sn] += qty

                # Apply "Buy 3, Get 1 Free" logic
                free = item_count[sn] // 3
                total_items = qty + free

                if total_items > available:
                    print("Not enough stock. Only " + str(available) + " items available.")
                    break

                unit_price = int(p["price"]) * 3
                amount = qty * unit_price
                p["quantity"] = available - total_items
                selected.append([p["name"], p["brand"], qty, free, unit_price, amount])
                total += amount
                successful_transaction = True
                print("Product '" + p["name"] + "' sold successfully with " + str(free) + " free items.")
                break

        if not found:
            print("S.N not found.")

    # Write to the file if the transaction was successful
    if successful_transaction:
        write.write_products(products)
        print("\nTransaction Completed Successfully!\n")

        # Generate Invoice
        now = datetime.datetime.now()
        voucher = str(random.randint(1000, 9999))
        fname = "invoice_sell_" + voucher + "_" + now.strftime('%Y%m%d%H%M') + ".txt"

        # Header Information
        invoice = "Voucher No: " + voucher + "\n"
        invoice += "Customer Name: " + customer_name + "\n"
        invoice += "Phone Number: " + customer_phone + "\n"
        invoice += "Date: " + now.strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
        invoice += "Product       Brand         Qty   Free   Price   Amount\n"

        # Invoice Item Lines
        for item in selected:
            name = item[0]
            brand = item[1]
            qty = str(item[2])
            free = str(item[3])
            price = str(item[4])
            amount = str(item[5])

            # Manual alignment with spaces
            line = name + " " * (14 - len(name))
            line += brand + " " * (14 - len(brand))
            line += qty + " " * (6 - len(qty))
            line += free + " " * (6 - len(free))
            line += price + " " * (8 - len(price))
            line += amount + "\n"
            invoice += line

        # Total Amount
        invoice += "\nTotal Amount: " + str(total)
        print(invoice)

        # Save the invoice
        write.save_invoice(invoice, fname)
        print("Voucher Number (Sell): " + voucher)
