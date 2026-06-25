# ----------------------------- Read Functions -----------------------------

def read_products():
    """
    Reads the products from the 'products.txt' file and returns them as a list of dictionaries.

    Each line in the file is expected to contain the following comma-separated fields:
    S.N, Product Name, Brand Name, Quantity, Price, Country of Origin

    The function skips the header and converts each line into a dictionary, which is then added to a list.

    Parameters:
    -----------
    None

    Returns:
    --------
    list:
        A list of dictionaries representing the products.
        Each dictionary contains the keys: 'sn', 'name', 'brand', 'quantity', 'price', 'country'.

    Raises:
    -------
    FileNotFoundError:
        If 'products.txt' is not found, it prints an error and returns an empty list.
    """
    try:
        file = open("products.txt", "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        print("Error: 'products.txt' file not found.")
        return []

    products = []
    i = 1
    while i < len(lines):  # skip header line
        line = lines[i]
        new_line = ""
        j = 0

        # Manually strip the newline characters
        while j < len(line):
            if line[j] != "\n":
                new_line = new_line + line[j]
            j = j + 1

        # Split the line by commas manually
        parts = []
        part = ""
        k = 0
        while k < len(new_line):
            if new_line[k] == ",":
                parts.append(part)
                part = ""
            else:
                part = part + new_line[k]
            k = k + 1
        parts.append(part)

        # Only append if all required fields are available
        if len(parts) == 6:
            product = {
                "sn": parts[0],
                "name": parts[1],
                "brand": parts[2],
                "quantity": parts[3],
                "price": parts[4],
                "country": parts[5]
            }
            products.append(product)
        i = i + 1

    return products


# ----------------------------- Display Function -----------------------------

def display_products(products, show_markup=False):
    """
    Displays the list of products in a formatted table.
    If `show_markup` is True, the prices are shown with a 200% markup.

    Parameters:
    -----------
    products : list
        A list of dictionaries, each representing a product.
        Required keys: 'sn', 'name', 'brand', 'quantity', 'price', 'country'.

    show_markup : bool, optional
        If True, the product price is displayed with a 200% markup. (Default is False)

    Returns:
    --------
    None

    Raises:
    -------
    ValueError:
        If there is an error while reading product data (e.g., non-integer price or quantity).
    """
    # Header display
    print("_" * 80)
    print("| S.N | Product Name       | Brand Name         | Qty  | Price     | Country     |")
    print("-" * 80)

    i = 0
    while i < len(products):
        p = products[i]
        
        # Extracting values
        name = p["name"]
        brand = p["brand"]
        try:
            qty = str(p["quantity"])
            sn = str(p["sn"])
            country = p["country"]
            price_val = int(p["price"]) * 3 if show_markup else int(p["price"])
        except ValueError:
            print("Error reading product data. Skipping item.")
            i += 1
            continue

        # Formatting fields to fixed length
        price = "NRP " + str(price_val)

        # Manual alignment with spaces
        while len(name) < 18:
            name = name + " "
        while len(brand) < 18:
            brand = brand + " "
        while len(qty) < 5:
            qty = qty + " "
        while len(price) < 9:
            price = price + " "
        while len(country) < 12:
            country = country + " "
        if len(sn) == 1:
            sn = " " + sn

        # Displaying the product line
        print("|  " + sn + "  | " + name + " | " + brand + " | " + qty + " | " + price + " | " + country + " |")
        i = i + 1

    print("-" * 80)
