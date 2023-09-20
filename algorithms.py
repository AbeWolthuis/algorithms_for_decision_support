# Imports
from collections import deque
import numpy as np

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

def get_best_result(results):
    decisions = np.array(list(results.keys()), dtype=object)
    scores = np.array([sum(results[tuple(key)]) for key in decisions])
    
    min_score = scores.min()
    best_keys = decisions[scores == min_score]

    return [(tuple(key), min_score) for key in best_keys]


    
def attempt2(people, days, seats, seat_prices, hotel_prices):
    res = {}

    # Call the generator function enumerate_ways
    for division in enumerate_ways(people, seats):
        # Calculate the score for this division
        sent_home_running_total = 0
        score_per_day = [0 for i in range(days)]
        for i in range(days):
            # First, update the running total of people sent home (so we know how many people are left to send to the hotel the next day)
            # score = sent_home_price_that_day + hotel_price_that_day
            sent_home_running_total += division[i]
            score_per_day[i] = division[i] * seat_prices[i] + (people - sent_home_running_total) * hotel_prices[i]
            
        # Store the result
        res[division] = score_per_day

    return res

def test2():
    res = attempt2(10, 3, seats=[5,5,5], seat_prices=[10,10,10], hotel_prices=[15,15,15])

    # Print all keys with the lowest score (there might be ties). The score is the sum of the values of the key (a tuple).
    min_score = min([sum(res[key]) for key in res])

    best = get_best_result(res)

    print('best: ', best)
    print('\n')
    # for k,v in res.items():
    #     print(k, (v))


def test1():
    # Call the generator function enumerate_ways
    for way in enumerate_ways(n=5, bins=[3,3,3]):
        print(way)
        pass



# Check if main, then run
if __name__ == "__main__":
    test1()

