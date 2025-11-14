## Takes a store number and converts the number to an IP
# Example: store 1234 equals IP ##.#21.34.##
def convert_to_ip(number):
    # Ensure the number is within the 4-digit range
    if number < 0 or number > 9999:
        raise ValueError("Number must be between 0 and 9999")
    # Format the number as a 4-digit string with leading zeros
    four_digit_str = f"{number:04d}"
    # Extract the parts of the formatted string
    x = four_digit_str[0]
    y = four_digit_str[1]
    zz = four_digit_str[2:]
    # If the first z equals zero, don't include it
    if zz[0] == '0':
        zz = zz[1:]
    # Create the IP address in the format ##.#yx.zz.1
    ip_address_1 = f"##.#{y}{x}.{zz}.1"
    ip_address_2 = f"##.#{y}{x}.{zz}.255"

    ip_address = ip_address_1, ip_address_2 
    
    return ip_address
    
# Ask the user for a list of store numbers
store_numbers = input("Enter the store numbers, separated by commas: ").split(',')
# Trim any leading/trailing whitespace and convert to integers
store_numbers = [int(store_number.strip()) for store_number in store_numbers]
# Process each store number and print the corresponding IP address
for store_number in store_numbers:
    ip_address = convert_to_ip(store_number)
    print(f"{ip_address}")
