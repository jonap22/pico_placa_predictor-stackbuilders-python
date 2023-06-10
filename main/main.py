# author: Jonathan Puglla
# date: June 9th, 2023

from pico_placa_predictor import PicoPlacaPredictor, validate_time, validate_date, validate_plate_number

MAX_RETRIES = 3  # max user input retries set to 3


def print_welcome_message():
    print("*"*60)
    print("Welcome to the Pico & Placa Predictor for StackBuilders!")
    print("*"*60)
    print("\nPlease enter the following information:")


def get_input(prompt):
    return input(prompt + ": ")


def print_result(is_restricted, plate_number, my_date, my_time):
    if is_restricted:
        print(f"The car with the license plate number "
              f"{plate_number} can NOT be on the road at {my_time} on {my_date}.")
    else:
        print(f"The car with the license plate number "
              f"{plate_number} can be on the road at {my_time} on {my_date}.")


def main():
    print_welcome_message()

    # Load the Pico & Placa rules and sets the retries to 0
    rules_file_path = '../data/pico_placa_rules.txt'
    my_predictor = PicoPlacaPredictor(rules_file_path)
    retries = 0

    while retries < MAX_RETRIES:
        try:
            # Get user input and checks if the user input is valid
            plate_number = get_input("License Plate Number (XXX-1234)")
            my_date = get_input("Date (YYYY-MM-DD)")
            my_time = get_input("Time (HH:MM)")

            if not validate_plate_number(plate_number):
                raise ValueError("Invalid license plate number (XXX-1234).")

            if not validate_date(my_date):
                raise ValueError("Invalid date (YYYY-MM-DD).")

            if not validate_time(my_time):
                raise ValueError("Invalid time (HH:MM).")

            # Check if the car can be on the road and prints the result
            is_restricted = my_predictor.is_plate_restricted(plate_number, my_date, my_time)
            print_result(is_restricted, plate_number, my_date, my_time)

            break

        except ValueError as error:
            print("Invalid input:", str(error))
            print("Please try again.\n")
            retries += 1

    if retries == MAX_RETRIES:
        print("Maximum number of retries reached.")


if __name__ == "__main__":
    main()
