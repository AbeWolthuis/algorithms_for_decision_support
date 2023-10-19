import os

def read_and_parse_instance(filename='test1.txt'):
    # Change working directory to the directory where the script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    foldername = 'instances'
    filepath = os.path.join(foldername, filename)

    """ Example file-layout:
        100           # People
        3             # Days
        100, 500, 250 # Amount of seats
        50, 100, 150  # Seat prices
        10, 1, 100    # Hotel prices
    """

    # Read and parse the file
    with open(filepath, 'r') as f:
        PEOPLE = int(f.readline().strip()) # Note, we can't have "fractional" people, days, or amount of seats.
        DAYS = int(f.readline().strip())
        SEATS = [int(seat.strip()) for seat in f.readline().split(",")]
        
        SEAT_PRICES = [float(price.strip()) for price in f.readline().split(",")] # Split each price, convert to list
        HOTEL_PRICES = [float(price.strip()) for price in f.readline().split(",")] # ... same as above

    return PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES

    
