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
    res = attempt2(PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES)
    
    best = get_best_result(PEOPLE, res)

    print('best: ', best)
    print('\n')
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

