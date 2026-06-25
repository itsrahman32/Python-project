# ----------------------------- Write Functions -----------------------------

def write_products(products):
    """
    Writes the updated list of products to the file 'products.txt'.
    
    This function overwrites the existing content in 'products.txt' with the new list of products,
    formatted in CSV style. It includes a header row followed by the product details.

    Parameters:
    -----------
    products : list
        A list of dictionaries, each representing a product.
        Required keys: 'sn', 'name', 'brand', 'quantity', 'price', 'country'.

    Returns:
    --------
    None

    Raises:
    -------
    Exception:
        If an error occurs while writing to 'products.txt', it is caught and printed.
    """
    try:
        # Open the file in write mode
        with open("products.txt", "w") as file:
            # Write the header
            file.write("SN,Name,Brand,Quantity,Price,Country\n")
            
            # Write each product's data
            for p in products:
                # Manually concatenate the line
                line = (
                    p['sn'] + "," +
                    p['name'] + "," +
                    p['brand'] + "," +
                    str(p['quantity']) + "," +
                    str(p['price']) + "," +
                    p['country'] + "\n"
                )
                # Write to the file
                file.write(line)
    except Exception as e:
        # Print the error if something goes wrong
        print("Error writing to file: " + str(e))


def save_invoice(invoice_text, filename):
    """
    Saves the generated invoice to a text file with the specified filename.
    
    This function creates or overwrites a text file with the provided invoice content.

    Parameters:
    -----------
    invoice_text : str
        The complete invoice text to be written to the file.
    
    filename : str
        The name of the file where the invoice will be saved.

    Returns:
    --------
    None

    Raises:
    -------
    Exception:
        If an error occurs while saving the invoice, it is caught and printed.
    """
    try:
        # Open the file in write mode
        with open(filename, "w") as file:
            # Write the invoice text to the file
            file.write(invoice_text)
    except Exception as e:
        # Print the error if something goes wrong
        print("Error saving invoice: " + str(e))
