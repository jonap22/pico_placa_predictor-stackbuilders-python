# author: Jonathan Puglla
# date: June 9th, 2023

import re
from datetime import datetime, time


def load_rules(file_path):
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
