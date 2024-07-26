import csv
import time
from datetime import datetime, timedelta
from FormatValues import (
    format_currency, format_title_case, format_upper_case,
    validate_name, validate_phone_number, validate_postal_code,
    validate_city, validate_num_cars, validate_yn_input,
    validate_down_payment, validate_claim_number, validate_claim_date,
    validate_claim_amount, validate_payment_method
)

# Load default values from Const.dat
def load_defaults(file_path):
    # Load default values from a file
    defaults = {}
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    defaults[row[0]] = float(row[1]) if '.' in row[1] else int(row[1])
    except Exception as e:
        print(f"Error loading defaults: {e}")
    return defaults

# Load the default values
defaults = load_defaults('Const.dat')

def flashing_welcome_message():
    # Display a flashing company name with a welcome message
    company_name = "One Stop Insurance Company"
    welcome_message = "Welcome to One Stop Insurance Company"
    print("\n\n")
    for i in range(6):
        if i % 2 == 0:
            print(f"\r{company_name}".center(70), end="")
        else:
            print("\r" + " " * 70, end="")
        time.sleep(0.5)
    print(f"\r{welcome_message}".center(70))
    print("\n")

def blinking_processing_invoice():
    # Display a blinking "Processing Invoice" message
    for i in range(6):
        if i % 2 == 0:
            print("\rProcessing Invoice...", end="")
        else:
            print("\r                      ", end="")
        time.sleep(0.5)
    print("\rProcessing Invoice completed!".center(70))

def get_valid_input(prompt, validation_func, error_message):
    # Prompt user for input and validate it
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        else:
            print(error_message)

def get_customer_info():
    # Collect and validate customer information
    customer = {}
    customer['first_name'] = format_title_case(get_valid_input(
        "Enter the customer's first name: ", validate_name, "Invalid name. Examples: John, Mary-Anne, O'Brien"
    ))
    customer['last_name'] = format_title_case(get_valid_input(
        "Enter the customer's last name: ", validate_name, "Invalid name. Examples: Doe, Smith, O'Connor"
    ))
    customer['address'] = input("Enter the customer's address: ")
    customer['city'] = format_title_case(get_valid_input(
        "Enter the customer's city: ", validate_city, "Invalid city name. Example: Toronto"
    ))
    customer['province'] = get_valid_input(
        "Enter the customer's province (e.g., NL, ON): ", lambda x: x.upper() in ["NL", "ON", "BC", "AB", "MB", "NB", "NS", "NT", "NU", "PE", "QC", "SK", "YT"],
        "Invalid province. Example: NL"
    ).upper()
    customer['postal_code'] = get_valid_input(
        "Enter the customer's postal code: ", validate_postal_code, "Invalid postal code. Example: A1A 1A1"
    )
    customer['phone'] = get_valid_input(
        "Enter the customer's phone number: ", validate_phone_number, "Invalid phone number. Example: 1234567890"
    )
    customer['num_cars'] = int(get_valid_input(
        "Enter the number of cars being insured: ", validate_num_cars, "Invalid number of cars. Example: 2"
    ))
    customer['liability'] = format_upper_case(get_valid_input(
        "Extra liability up to $1,000,000 (Y/N): ", validate_yn_input, "Invalid input. Enter Y or N."
    ))
    customer['glass'] = format_upper_case(get_valid_input(
        "Optional glass coverage (Y/N): ", validate_yn_input, "Invalid input. Enter Y or N."
    ))
    customer['loaner'] = format_upper_case(get_valid_input(
        "Optional loaner car (Y/N): ", validate_yn_input, "Invalid input. Enter Y or N."
    ))
    customer['payment_method'] = format_title_case(get_valid_input(
        "Payment method (Full, Monthly, Down Pay): ", validate_payment_method, "Invalid input. Enter Full, Monthly, or Down Pay."
    ))
    if customer['payment_method'] == 'Down Pay':
        customer['down_payment'] = float(get_valid_input(
            "Enter the amount of the down payment: ", validate_down_payment, "Invalid amount. Example: 1000.00"
        ))
    
    customer['claims'] = []
    while True:
        add_claim = format_upper_case(get_valid_input(
            "Do you want to add a previous claim? (Y/N): ", validate_yn_input, "Invalid input. Enter Y or N."
        ))
        if add_claim == 'N':
            break
        claim_number = get_valid_input(
            "Enter claim number: ", validate_claim_number, "Invalid claim number. Example: 12345"
        )
        claim_date = get_valid_input(
            "Enter claim date (YYYY-MM-DD): ", validate_claim_date, "Invalid date format or date is in the future. Example: 2023-01-01"
        )
        claim_amount = float(get_valid_input(
            "Enter claim amount: ", validate_claim_amount, "Invalid amount. Example: 500.00"
        ))
        customer['claims'].append((claim_number, claim_date, claim_amount))
    
    return customer

def calculate_premium(num_cars, liability, glass, loaner):
    # Calculate the insurance premium based on the input parameters
    basic_premium = defaults['BasicPremium']
    discount = defaults['Discount']
    total_premium = basic_premium + (num_cars - 1) * basic_premium * (1 - discount)
    
    extra_costs = 0
    if liability == 'Y':
        extra_costs += num_cars * defaults['ExtraLiability']
    if glass == 'Y':
        extra_costs += num_cars * defaults['GlassCoverage']
    if loaner == 'Y':
        extra_costs += num_cars * defaults['LoanerCar']
    
    total_premium += extra_costs
    return total_premium, extra_costs

def calculate_final_cost(total_premium, hst_rate, payment_method, down_payment=0):
    # Calculate the final cost including HST and any applicable fees
    hst = total_premium * hst_rate
    total_cost = total_premium + hst
    monthly_payment = 0
    if payment_method == 'Monthly':
        total_cost += defaults['ProcessingFee']
        monthly_payment = total_cost / 8
    elif payment_method == 'Down Pay':
        total_cost += defaults['ProcessingFee']
        total_cost -= down_payment
        monthly_payment = total_cost / 8
    return total_cost, monthly_payment

def save_policy_data(customer, total_premium):
    # Save policy data to a text file
    policy_number = defaults['NextPolicyNumber']
    with open(f'Policy_{policy_number}.txt', 'w') as file:
        file.write(f"Policy Number: {policy_number}\n")
        file.write(f"Customer: {customer['first_name']} {customer['last_name']}\n")
        file.write(f"Total Premium: {format_currency(total_premium)}\n")
        file.write(f"Claims: {len(customer['claims'])}\n")
    defaults['NextPolicyNumber'] += 1

def display_receipt(customer, total_premium, extra_costs, hst, total_cost, monthly_payment):
    # Format the output as requested
    company_name = "One Stop Insurance Company"
    invoice_date = datetime.now().strftime("%A, %B %d, %Y")
    customer_id = f"{customer['first_name'][0].upper()}{customer['last_name'][0].upper()}{int(defaults['NextPolicyNumber'])}"
    policy_number = int(defaults['NextPolicyNumber'])

    # Format customer name with initial and last name
    customer_name = f"{customer['first_name'][0].upper()}. {customer['last_name'].title()}"

    # Calculate the first payment date as the first day of the next month
    today = datetime.today()
    first_payment_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1).strftime("%A, %B %d, %Y")

    # Printing the formatted invoice
    print("\n" + "-" * 70)
    print("Invoice".center(70))
    print("-" * 70)
    print(f"\n{company_name:<45}{invoice_date:>20}")
    print(f"\n{customer_name:<45}Customer ID: {customer_id:>8}")
    print(f"{'':<45}Policy Number: {policy_number:>6}")
    print(f"\t{customer['address']}")
    print(f"\t{customer['city']}, {customer['province']}, {customer['postal_code']}")
    print(f"\tPhone: {customer['phone']}")
    print("\n" + "-" * 70)
    print("Policy Details".center(70))
    print("-" * 70)
    print(f"{'Number of Cars Insured:':<35} {customer['num_cars']:>30}")
    print(f"{'Liability Coverage:':<35} {'Yes' if customer['liability'] == 'Y' else 'No':>30}")
    print(f"{'Glass Coverage:':<35} {'Yes' if customer['glass'] == 'Y' else 'No':>30}")
    print(f"{'Loaner Car:':<35} {'Yes' if customer['loaner'] == 'Y' else 'No':>30}")
    print(f"{'Payment Method:':<35} {customer['payment_method']:>30}")
    if customer['payment_method'] == "Down Pay":
        print(f"{'Down Payment:':<35} {format_currency(customer['down_payment']):>30}")

    print("\n" + "-" * 70)
    print("Charges".center(70))
    print("-" * 70)
    print(f"{'Basic Premium:':<35} {format_currency(defaults['BasicPremium']):>30}")
    print(f"{'Total Extra Costs:':<35} {format_currency(extra_costs):>30}")
    print(f"{'Total Premium:':<35} {format_currency(total_premium):>30}")
    print(f"{'HST (15%):':<35} {format_currency(hst):>30}")
    print(f"{'Total Cost:':<35} {format_currency(total_cost):>30}")

    if customer['payment_method'] != "Full":
        print(f"{'Monthly Payment:':<35} {format_currency(monthly_payment):>30}")

    print("\n" + "-" * 70)
    print("Previous Claims".center(70))
    print("-" * 70)
    print(f"{'Claim #':<20} {'Claim Date':<15} {'Amount':>15}")
    print("-" * 70)
    for claim in customer['claims']:
        print(f"{claim[0]:<20} {claim[1]:<15} {format_currency(claim[2]):>15}")
    print("-" * 70)

    print("\n" + "-" * 70)
    print("Payment Dates".center(70))
    print("-" * 70)
    print(f"{'Invoice Date:':<35} {invoice_date:>30}")
    print(f"{'First Payment Date:':<35} {first_payment_date:>30}")
    print("-" * 70)

def display_save_message():
    # Display a blinking save message
    for i in range(6):
        if i % 2 == 0:
            print("\rSaving policy data...", end="")
        else:
            print("\r                       ", end="")
        time.sleep(0.5)
    print("\rPolicy data saved successfully!     ")

def main():
    # Main function to run the insurance program
    flashing_welcome_message()
    while True:
        customer = get_customer_info()
        blinking_processing_invoice()
        total_premium, extra_costs = calculate_premium(customer['num_cars'], customer['liability'], customer['glass'], customer['loaner'])
        total_cost, monthly_payment = calculate_final_cost(total_premium, defaults['HST'], customer['payment_method'], customer.get('down_payment', 0))

        display_receipt(customer, total_premium, extra_costs, total_premium * defaults['HST'], total_cost, monthly_payment)
        save_policy_data(customer, total_premium)
        display_save_message()

        cont = input("Do you want to enter another customer? (Y/N): ").upper()
        if cont != 'Y':
            break

if __name__ == "__main__":
    main()
