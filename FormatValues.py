import re
from datetime import datetime

# Formatting functions
def format_currency(value):
    # Format value as currency
    return "${:,.2f}".format(value)

def format_title_case(value):
    # Convert string to title case
    return value.title()

def format_upper_case(value):
    # Convert string to upper case
    return value.upper()

# Validation functions
def validate_name(name):
    # Validate name (letters, apostrophes, hyphens)
    return bool(re.match(r"^[A-Za-z\'-]+$", name))

def validate_phone_number(phone_number):
    # Validate phone number (10 digits)
    return bool(re.match(r"^\d{10}$", phone_number))

def validate_postal_code(postal_code):
    # Validate postal code (Canadian format)
    return bool(re.match(r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$", postal_code))

def validate_city(city):
    # Validate city name (letters and spaces)
    return bool(re.match(r"^[A-Za-z ]+$", city))

def validate_num_cars(num_cars):
    # Validate number of cars (positive integers)
    return num_cars.isdigit()

def validate_yn_input(input_value):
    # Validate Y/N input
    return input_value.upper() in ['Y', 'N']

def validate_down_payment(amount):
    # Validate down payment amount (positive number with up to two decimal places)
    return bool(re.match(r"^\d+(\.\d{1,2})?$", amount))

def validate_claim_number(claim_number):
    # Validate claim number (5 digits)
    return bool(re.match(r"^\d{5}$", claim_number))

def validate_claim_date(claim_date):
    # Validate claim date (YYYY-MM-DD)
    try:
        date = datetime.strptime(claim_date, "%Y-%m-%d")
        return date <= datetime.now()
    except ValueError:
        return False

def validate_claim_amount(amount):
    # Validate claim amount (positive number with up to two decimal places)
    return bool(re.match(r"^\d+(\.\d{1,2})?$", amount))

def validate_payment_method(payment_method):
    # Validate payment method (Full, Monthly, Down Pay)
    return payment_method in ["Full", "Monthly", "Down Pay"]
