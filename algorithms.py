# Imports
from collections import deque
import numpy as np
import itertools

def enumerate_ways(n, bins):
    q = deque()
    q.append((0, [0]*len(bins), 0))  # Initialize the queue with a tuple (current_sum, current_combination, current_bin_index)

    while q:
        current_sum, current_combination, current_bin_index = q.popleft()
        # print(current_bin_index)
        
        if current_bin_index == len(bins) - 1:
            if current_sum + bins[current_bin_index] >= n:
                current_combination[current_bin_index] = n - current_sum
                yield tuple(current_combination)
            continue

        for i in range(min(bins[current_bin_index], n - current_sum) + 1):
            new_combination = current_combination.copy()
            new_combination[current_bin_index] = i
            q.append((current_sum + i, new_combination, current_bin_index + 1))

def get_best_result(people, results):
    decisions = np.array(list(results.keys()), dtype=object)
    scores = np.array([sum(results[tuple(key)]) for key in decisions])
    
    min_score = scores.min()
    best_keys = decisions[scores == min_score]

    # Calculate how many people stay each night
    stayers = get_stayers(people, best_keys[0])

    return [((tuple(key), tuple(stayers), min_score)) for key in best_keys]

def get_stayers(people, decision):
    """
    Calculates the number of people staying each night based on a decision array.

    Args:
    - people (int): total number of people
    - decision (tuple): decision array, where the value represents the amount of people leaving

    Returns:
    - stayers (list): list of integers representing the number of people staying each night
    """
    stayers = [people - x for x in itertools.accumulate(decision)]
    return stayers

    

import itertools

def smart_attempt(people, days, seats, seat_prices, hotel_prices):
    # First, create array of total price to leave on a certain day.
    # Contains tuples: (total_price, seats_available, day) Then, sort this array based on total_price.
    prices_array = [(sum(hotel_prices[:i]) + seat_prices[i], seats[i], i + 1) for i in range(days)]
    prices_array = sorted(prices_array, key=lambda x: x[0])

    # Store the "decisions" on each day
    staying_array = [0 for i in range(days)]
    leaving_array = [0 for i in range(days)]
    cost_array = [0 for i in range(days)]

    if sum(seats) < people:
        print(f"No feasible solution since it is not possible to move {people} people within {days} days. Maximum number of seats is {sum(seats)}")
        return (staying_array, leaving_array)
    else:
        # Loop until all people have been sent home. This takes at most M iterations, where M is the number of days. Since, we can move everyone in the total amount of days.
        remaining_people = people
        while remaining_people > 0:
            # Pop the day with the lowest cost to move people
            cheapest_price, cheapest_seats, cheapest_day = prices_array.pop(0)

            # We want to send as many people as possible home, since this option is now the cheapest.
            # But, if there are more people left than the available seats on the cheapest day, we can only send the amount of people that are left, so take the minimum.
            leavers_today = min(remaining_people, cheapest_seats)

            # Update the arrays
            leaving_array[cheapest_day - 1] = leavers_today
            staying_array[cheapest_day - 1] = remaining_people - leavers_today
            cost_array[cheapest_day - 1] = cheapest_price*leavers_today

            # Send home the leavers
            remaining_people -= leavers_today

        return (staying_array, leaving_array, sum(cost_array))





    
def attempt2(people, days, seats, seat_prices, hotel_prices):
    res = {}

    # Call the generator function enumerate_ways
    for division in enumerate_ways(people, seats):
        # Calculate the score for this division
        sent_home_running_total = 0
        score_per_day = [0 for i in range(days)]
        for day, (price, people_sent_home) in enumerate(zip(seat_prices, division)):
            # First, update the running total of people sent home (so we know how many people are left to send to the hotel the next day)
            # score = sent_home_price_that_day + hotel_price_that_day
            sent_home_running_total += people_sent_home
            score_per_day[day] = price * people_sent_home + (people - sent_home_running_total) * hotel_prices[day]

            # sent_home_running_total += division[i]
            # score_per_day[i] = division[i] * seat_prices[i] + (people - sent_home_running_total) * hotel_prices[i]
            
        # Store the result
        res[division] = score_per_day

    return res

def test2():
    PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES = (100, 3, [50,30,40], [10,10,10], [15,15,15])
    # PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES = (10, 3, [5,5,5], [10,10,10], [15,15,15])
    res = smart_attempt(PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES)
    
    # best = get_best_result(PEOPLE, res)

    print(res)

    # for k,v in res.items():
    #     print(k, sum(v))


def test1():
    # Call the generator function enumerate_ways
    for way in enumerate_ways(n=5, bins=[5,5,5]):
        print(way)
        pass



# Check if main, then run
if __name__ == "__main__":
    test2()

