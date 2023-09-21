# Imports
from parse import read_and_parse
from algorithms import attempt2, get_best_result
from offline_solver import offline


if __name__ == "__main__":
    # Settings
    instance_filename = 'alternative_data.txt'

    # Parse input
    PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES = read_and_parse(instance_filename)

    parameters = (PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES)
    print('parameters: ', parameters)

    # Run the algorithm
    result = attempt2(PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES)
    # print(result)

    # Visualise
    # print('Best result: ', get_best_result(result))
    print('Best result: ', get_best_result(result))

