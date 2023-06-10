# author: Jonathan Puglla
# date: June 9th, 2023

import re
from datetime import datetime, time


def load_rules(file_path):
    """
    Loads the Pico&Placa rules from a file.
    :param file_path: the rules file path.
    :return: rules - a dictionary with the Pico&Placa rules.
    """
    rules = {}

    with open(file_path, 'r') as rules_file:
        for line in rules_file:
            day_number, restricted_digits = line.strip().split(':')
            rules[int(day_number)] = [int(digit) for digit in restricted_digits.split(',')]

    return rules


def validate_plate_number(plate_number):
    """
    Validates the format (XXX-1234) of the license plate number.
    :param plate_number: the given license plate number.
    :return: boolean - true if the format is valid.
    """
    plate_number_pattern = r'^[A-Z]{3}-\d{4}$'
    return re.match(plate_number_pattern, plate_number) is not None


def validate_date(date):
    """
    Validates the format (YYYY-MM-DD) of the given date.
    :param date: the given date.
    :return: boolean - true if the format is valid.
    """
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(date_pattern, date) is not None


def validate_time(time_str):
    """
    Validates the format (HH:MM) of the given time.
    :param time_str: the given time.
    :return: boolean - true if the format is valid.
    """
    time_pattern = r'^\d{2}:\d{2}$'
    return re.match(time_pattern, time_str) is not None


def is_restricted_time(time_obj):
    """
    Checks the past rules of the Pico&Placa. (Hours: 7:00 am - 9:30 am / 4:00 pm - 7:30 pm).
    :param time_obj:
    :return: boolean - true if the time is within the restricted hours.
    """
    morning_start = time(7, 0)
    morning_end = time(9, 30)
    evening_start = time(16, 0)
    evening_end = time(19, 30)

    if morning_start <= time_obj <= morning_end or evening_start <= time_obj <= evening_end:
        return True

    return False


class PicoPlacaPredictor:
    def __init__(self, rules_file_path):
        self.rules = load_rules(rules_file_path)
        return

    def is_plate_restricted(self, plate_number, date_str, time_str):
        """
        Checks if a car can be on the road.
        :param plate_number:
        :param date_str:
        :param time_str:
        :return: boolean - True if the car cannot be on the road.
        """
        plate_number = plate_number.upper()

        if not validate_plate_number(plate_number):
            raise ValueError('Invalid plate number format (XXX-1234). ')

        if not validate_date(date_str):
            raise ValueError('Invalid date format (YYYY-MM-DD). ')

        if not validate_time(time_str):
            raise ValueError('Invalid time format (HH:MM). ')

        weekday = datetime.strptime(date_str, '%Y-%m-%d').isoweekday()
        my_time = datetime.strptime(time_str, '%H:%M').time()
        last_digit = int(plate_number[-1])

        if weekday in self.rules and last_digit in self.rules[weekday]:
            if is_restricted_time(my_time):
                return True

        return False
