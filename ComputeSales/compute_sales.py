"""
computeSales.py

This code computes the total sales cost from a sales record file,
using product prices from a catalogue.
It takes two JSON files as input:
one with product prices and another with sales records.
The output is printed to the console and saved in a file
named 'SalesResults.txt'.

Usage:
    python computeSales.py priceCatalogue.json salesRecord.json
"""

# Instructions
# Req1. The program shall be invoked from a command line.
# The program shall receive two files as parameters.
# The first file will contain information in a JSON format about
# a catalogue of prices of products.
# The second file will contain a record for all sales in a company.
# Req 2. The program shall compute the total cost for all sales
# included in the second JSON archive.
# The results shall be print on a screen and on a file named SalesResults.txt.
# The total cost should include all items in the sale considering the cost
# for every item in the first file.
# The output must be human readable, so make it easy to read for the user.
# Req 3. The program shall include the mechanism to handle
# invalid data in the file.
# Errors should be displayed in the console and the execution must continue.
# Req 4. The name of the program shall be computeSales.py
# Req 5. The minimum format to invoke the program shall be as follows:
# python computeSales.py priceCatalogue.json salesRecord.json
# Req 6. The program shall manage files having from hundreds of
# items to thousands of items.
# Req 7. The program should include at the end of the execution
# the time elapsed for the execution and calculus of the data.
# This number shall be included in the results file and on the screen.
# Req 8. Be compliant with PEP8.

import json
import sys
import time


def load_json_file(filename):
    """
    Load and parse a JSON file.

    Args:
        filename (str): Path to the JSON file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename}: {e}")
        return {}


def convert_catalogue_to_dict(price_catalogue):
    """
    Convert the product catalogue list into a dictionary for lookup.

    Args:
        price_catalogue (list): List of product dictionaries
        with 'product' and 'price' keys.

    Returns:
        dict: Dictionary mapping product names to prices.
    """
    catalogue_dict = {}
    for item in price_catalogue:
        product = item.get("title")
        price = item.get("price")
        if isinstance(product, str) and isinstance(price, (int, float)):
            catalogue_dict[product] = price
        else:
            print(f"Warning: Invalid product entry {item}. Skipping.")
    return catalogue_dict


def compute_total_sales(price_catalogue, sales_record):
    """
    Compute the total sales cost based on the provided price
    catalogue and sales record.

    Args:
        price_catalogue (list): List of products and their prices.
        sales_record (list): List of sales transactions,
        each with product names and quantities.

    Returns:
        float: Total cost of all sales transactions.
    """
    total_cost = 0.0
    for sale in sales_record:
        product = sale.get("Product")
        quantity = sale.get("Quantity")

        price_catalogue_dict = convert_catalogue_to_dict(price_catalogue)

        if product not in price_catalogue_dict:
            print(f"Warning: '{product}' not found in catalogue. Skipping.")
            continue

        if not isinstance(quantity, (int, float)) or quantity < 0:
            print(f"Warning: Invalid quantity for '{product}'. Skipping.")
            continue

        total_cost += price_catalogue_dict[product] * quantity

    return total_cost


def save_results(filename, total_cost, elapsed_time):
    """
    Save the computed total sales cost and execution time to a file.

    Args:
        filename (str): Path to the output file.
        total_cost (float): Computed total sales cost.
        elapsed_time (float): Execution time in seconds.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Total Sales Cost: ${total_cost:,.2f}\n")
        file.write(f"Execution Time: {elapsed_time:.2f} seconds\n")


def main():
    """
    Main function to execute the sales computation script.
    """
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    start_time = time.time()

    price_catalogue = load_json_file(price_catalogue_file)
    sales_record = load_json_file(sales_record_file)

    if (not isinstance(price_catalogue, list) or
            not isinstance(sales_record, list)):
        print("Error: Invalid file format.")
        sys.exit(1)

    total_cost = compute_total_sales(price_catalogue, sales_record)
    elapsed_time = time.time() - start_time

    print(f"Total Sales Cost: ${total_cost:,.2f}")
    print(f"Execution Time: {elapsed_time:.2f} seconds")

    save_results("SalesResults.txt", total_cost, elapsed_time)


if __name__ == "__main__":
    main()
