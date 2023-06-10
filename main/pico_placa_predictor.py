# author: Jonathan Puglla
# date: June 9th, 2023

import re


def load_rules(file_path):
    """
    Loads the Pico y Placa rules from a file.
    :param file_path: the rules file path.
    :return: rules - a dictionary with the Pico y Placa rules.
    """
    rules = {}

    with open(file_path, 'r') as rules_file:
        for line in rules_file:
            plate_number, allowed_days = line.strip().split(':')
            rules[plate_number] = allowed_days.split(',')

    return rules


class PicoPlacaPredictor:
    def __init__(self, rules_file_path):
        self.rules = load_rules(rules_file_path)
        return

    def validate_plate_number(self, plate_number):
        """
        Validates the format (XXX-1234) of the license plate number.
        :param plate_number: the given license plate number.
        :return: boolean - true if the format is valid.
        """
        plate_number_pattern = r'^[A-Z]{3}-\d{4}$'
        return re.match(plate_number_pattern, plate_number) is not None

    def validate_date(self, date):
        """
        Validates the format (YYYY-MM-DD) of the given date.
        :param date: the given date.
        :return: boolean - true if the format is valid.
        """
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(date_pattern, date) is not None

    def validate_time(self, time_str):
        """
        Validates the format (HH:MM) of the given time.
        :param time_str: the given time.
        :return: boolean - true if the format is valid.
        """
        time_pattern = r'^\d{2}:\d{2}$'
        return re.match(time_pattern, time_str) is not None

    def is_restricted_time(self, time_obj):
        # TODO: add functionality
        return

    def is_plate_restricted(self, plate_number, date, time_str):
        if not self.validate_plate_number(plate_number):
            raise ValueError('Invalid plate number format (XXX-1234). ')

        return