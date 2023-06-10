# author: Jonathan Puglla
# date: June 9th, 2023

import re
from datetime import datetime, time


def load_rules(file_path):
    """
    Loads the Pico y Placa rules from a file.

    :param file_path:
    :return: rules - a dictionary with the Pico y Placa rules
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
        :param plate_number:
        :return: boolean
        """
        pattern = r'^[A-Z]{3}-\d{4}$'
        return re.match(pattern, plate_number) is not None

    def is_plate_restricted(self, plate_number, date, time_str):
        # TODO: add functionality
        return

    def validate_date(self, date):
        # TODO: add functionality
        return

    def validate_time(self, time_str):
        # TODO: add functionality
        return

    def is_restricted_time(self, time_obj):
        # TODO: add functionality
        return
