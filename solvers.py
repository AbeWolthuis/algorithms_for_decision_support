import numpy as np


def online(n_people, m_days, avail_seats, seat_prices, hotel_prices):
    # Because arrays start at 0
    last_day = m_days - 1

    fly = [0]*m_days
    hotel = [0]*m_days
    total_price = 0
    remaining = n_people
    day = 0

    while day < last_day:
        seats = avail_seats[day]
        seat_price = seat_prices[day]
        hotel_price = hotel_prices[day]

        if seat_price <= hotel_price:
            amount_send_home = min(seats, remaining)
            fly[day] = amount_send_home
            remaining -= amount_send_home
            total_price += amount_send_home * seat_price
            total_price += remaining * hotel_price

        else:
            hotel[day] = remaining
            total_price += remaining * hotel_price

        day += 1

    seat_price = seat_prices[last_day]
    total_price += remaining * seat_price
    fly[last_day] = remaining

    return (fly, hotel), total_price


def offline(n_people, m_days, avail_seats, seat_prices, hotel_prices):

    # When we fly the first day, we incur no hotel costs
    hotel_prices = hotel_prices.copy()
    hotel_prices.insert(0, 0)

    # How expensive have hotels been when we fly on day i
    # We don't count the last day, because we always fly on the last day anyway
    running_hotel_prices = np.array(hotel_prices[:-1]).cumsum(axis=0)

    # Flying on that day costs all previous days in hotel, plus seat_price
    total_price_per_day = running_hotel_prices + np.array(seat_prices)

    # Find ordering of cheapest to most expensive flight days
    cheapest_day_order = np.argsort(total_price_per_day)

    # We start on the first day
    i = 0

    # All people remain and have to be send back, and we've payed nothing yet
    remaining = n_people
    total_price = 0

    # We haven't decided what to do on each day, init zero for each day
    fly = [0]*m_days
    hotel = [0]*m_days

    # We need to send people home, untill everyone is home
    while remaining != 0 and i < len(cheapest_day_order):

        # First cheapest day from ordering
        day = cheapest_day_order[i]

        # Fly maximal amount of people on this cheap day
        seats_to_fly = avail_seats[day]
        send_n_home = min(remaining, seats_to_fly)
        fly[day] = send_n_home

        # The rest stays in hotel
        remaining -= send_n_home
        hotel[day] = remaining

        # The total price of taking hotels up to that day, and then flying
        total_price += total_price_per_day[day] * send_n_home

        # Go in next iteration to second cheapest day
        i += 1

    return (fly, hotel), total_price
