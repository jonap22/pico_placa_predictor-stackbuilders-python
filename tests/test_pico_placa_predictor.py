# author: Jonathan Puglla
# date: June 9th, 2023

import pytest
from datetime import time
from main.pico_placa_predictor import load_rules, validate_plate_number, validate_date, validate_time, \
    is_restricted_time, PicoPlacaPredictor


# Test cases for the loaded rules
def test_load_rules():
    file_path = '../data/pico_placa_rules.txt'
    expected_rules = {
        1: [1, 2],
        2: [3, 4],
        3: [5, 6],
        4: [7, 8],
        5: [9, 0]
    }
    rules = load_rules(file_path)
    assert rules == expected_rules


# Test cases for validating a license plate number
@pytest.mark.parametrize(
    "plate_number, expected_result",
    [
        ("ABC-1234", True),  # Valid plate number format
        ("abc-1234", False),  # Invalid plate number format (lowercase letters)
        ("ABC-12345", False),  # Invalid plate number format (extra digit)
        ("AB-1234", False),  # Invalid plate number format (missing letter)
        ("ABC-12A4", False),  # Invalid plate number format (letter should be followed by digits)
    ]
)
def test_validate_plate_number(plate_number, expected_result):
    result = validate_plate_number(plate_number)
    assert result == expected_result


# Test cases for validating a date
@pytest.mark.parametrize(
    "date, expected_result",
    [
        ("2023-06-09", True),  # Valid date format
        ("2023-6-9", False),  # Invalid date format (missing leading zeros)
        ("2023/06/09", False),  # Invalid date format (wrong delimiter)
        ("06-09-2023", False),  # Invalid date format (wrong order)
        ("2023-13-09", False),  # Invalid date format (invalid month)
        ("2023-06-32", False),  # Invalid date format (invalid day)
    ]
)
def test_validate_date(date, expected_result):
    result = validate_date(date)
    assert result == expected_result


# Test cases for validating the time
@pytest.mark.parametrize(
    "time_str, expected_result",
    [
        ("07:30", True),  # Valid time format
        ("7:30", False),  # Invalid time format (missing leading zeros)
        ("07-30", False),  # Invalid time format (wrong delimiter)
        ("07:60", False),  # Invalid time format (invalid minutes)
        ("24:00", False),  # Invalid time format (invalid hours)
    ]
)
def test_validate_time(time_str, expected_result):
    result = validate_time(time_str)
    assert result == expected_result


# Test cases for is_restricted_time function
@pytest.mark.parametrize(
    "time_obj, expected_result",
    [
        (time(6, 59), False),  # Not within restricted hours
        (time(7, 0), True),  # Within restricted hours
        (time(9, 30), True),  # Within restricted hours
        (time(12, 0), False),  # Not within restricted hours
        (time(16, 0), True),  # Within restricted hours
        (time(19, 30), True),  # Within restricted hours
        (time(20, 0), False),  # Not within restricted hours
    ]
)
def test_is_restricted_time(time_obj, expected_result):
    result = is_restricted_time(time_obj)
    assert result == expected_result


# Test cases for the predictor class
@pytest.fixture
def predictor():
    return PicoPlacaPredictor('../data/pico_placa_rules.txt')


@pytest.mark.parametrize(
    "plate_number, date_str, time_str, expected_result",
    [
        ("ABC-1231", "2023-06-05", "07:00", True),  # Cannot be on the road
        ("AFC-1234", "2023-06-06", "06:59", False),  # Can be on the road
        ("ADC-1235", "2023-06-07", "16:00", True),  # Cannot be on the road
        ("BBC-1238", "2023-06-08", "10:30", False),  # Can be on the road
        ("ABC-1230", "2023-06-09", "07:30", True),  # Cannot be on the road
        ("GMN-5678", "2023-06-09", "08:00", False),  # Can be on the road
        ("DEF-4321", "2023-06-10", "18:00", False),  # Can be on the road
        ("GHI-9876", "2023-06-11", "12:00", False),  # Can be on the road
        ("JKL-2468", "2023-06-12", "22:00", False),  # Can be on the road
        ("BDC-1232", "2023-06-05", "19:30", True),  # Cannot be on the road
    ]
)
def test_is_plate_restricted(predictor, plate_number, date_str, time_str, expected_result):
    result = predictor.is_plate_restricted(plate_number, date_str, time_str)
    assert result == expected_result
