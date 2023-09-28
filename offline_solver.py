import numpy as np

def read_data():
    # with open('/Users/ellalouwenaar/Downloads/Data_Strike_Offline.txt') as f:
    with open('/Users/ellalouwenaar/Downloads/alternative_data.txt') as f:
        lines_list = f.readlines()
        n = int(lines_list[0])
        m = int(lines_list[1])
        num_seats = [int(val) for val in lines_list[2].split(',')]
        price_seats = [int(val) for val in lines_list[3].split(',')]
        price_hotel = [int(val) for val in lines_list[4].split(',')]
        return n, m, num_seats, price_seats, price_hotel

# alleen nog checken voor feasibility
def offline(n, m, s, p, h):
    # Create an empty array to store [cumulative_price, seats_available, day] for each day
    data_array = []
    
    # Populate data_array
    for i in range(0, m):
        leaving_day_array = [np.add(sum(h[:i]), p[i]), s[i], i + 1]
        data_array.append(leaving_day_array)
        
    # Sort data_array based on the price (cumulative_price)
    data_array.sort()
    
    # Initialize variables to keep track of people left, flying, and staying in hotel
    people_left = n
    flying = [0 for element in range(m)]
    hotel = [0 for element in range(m)]
    
    # Initialize total_price to 0
    total_price = 0
    
    # Debugging print statement
    # print(data_array)
    
    # Loop until all people have been moved
    while people_left > 0:
        
        # Check for feasibility, if not feasible, return an error message
        if len(data_array) == 0:
            return f"No feasible solution since it is not possible to move {n} people within {m} days. Maximum number of seats is {sum(s)}"
        
        # Pop the day with the lowest cost to move people
        price_cheapest, availability_cheapest_option, day = data_array.pop(0)
        
        # Debugging print statement
        # print(price_cheapest, availability_cheapest_option, day)
        
        # If more people are left than the available seats on the cheapest day
        if people_left > availability_cheapest_option:
            flying[day - 1] += availability_cheapest_option  # Update flying array
            hotel[:(day-1)] = [x + availability_cheapest_option for x in hotel[:(day-1)]]  # Update hotel array
            total_price += price_cheapest * availability_cheapest_option  # Update total price
            people_left -= availability_cheapest_option  # Update people_left
            continue
        # If fewer or equal people are left than the available seats on the cheapest day
        elif people_left <= availability_cheapest_option:
            flying[day - 1] += people_left  # Update flying array
            hotel[:(day-1)] = [x + people_left for x in hotel[:(day-1)]]  # Update hotel array
            total_price += price_cheapest * people_left  # Update total price
            people_left = 0  # Update people_left
            
    # Return the updated flying and hotel arrays, along with the total_price
    return [flying, hotel], total_price


if __name__ == '__main__':
    res = offline(n=10, m=3, s=[5,5,5], p=[10,10,10], h=[15,15,15])
    print(res)