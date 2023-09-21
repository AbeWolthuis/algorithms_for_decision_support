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
    data_array = []
    for i in range(0, m):
        leaving_day_array = [np.add(sum(h[:i]), p[i]), s[i], i + 1]
        data_array.append(leaving_day_array)
    data_array.sort()
    people_left = n
    flying = [0 for element in range(m)]
    hotel = [0 for element in range(m)]
    total_price = 0
    print(data_array)
    while people_left > 0:
        if len(data_array) == 0:
            return f"No feasible solution since it is not possible to move {n} people within {m} days. Maximum number of seats is {sum(s)}"
        price_cheapest, availability_cheapest_option, day = data_array.pop(0)
        print(price_cheapest, availability_cheapest_option, day )
        if people_left > availability_cheapest_option:
            flying[day - 1] += availability_cheapest_option
            hotel[:(day-1)] = [x + availability_cheapest_option for x in hotel[:(day-1)]]
            total_price += price_cheapest * availability_cheapest_option
            people_left -= availability_cheapest_option
            continue
        if people_left <= availability_cheapest_option:
            flying[day - 1] += people_left
            hotel[:(day-1)] = [x + people_left for x in hotel[:(day-1)]]
            total_price += price_cheapest * people_left
            people_left = 0
    return [flying, hotel], total_price

n, m, s, p, h = read_data()
print(offline(n, m, s, p, h))
