# Imports
from parse import read_and_parse
from algorithms import attempt2, get_best_result


if __name__ == "__main__":
    # Settings
    instance_filename = 'test2.txt'

    # Parse input
    PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES = read_and_parse(instance_filename)

    parameters = (PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES)
    print('parameters: ', parameters)

    # Run the algorithm
    result = attempt2(PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES)
    # print(result)

    # Visualise
    print(get_best_result(result))

