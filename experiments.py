"""Module containing code to run experiments on algorithms."""
from dataclasses import dataclass
import time
import os

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from solvers import online, offline

def read_and_parse_instance(filename='test1.txt'):
    """
    Reads in instance input, and parses to correct object.

    Example file-layout:
        100           # People
        3             # Days
        100, 500, 250 # Amount of seats
        50, 100, 150  # Seat prices
        10, 1, 100    # Hotel prices
    """
    # Change working directory to the directory where the script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    foldername = 'instances'
    filepath = os.path.join(foldername, filename)


    # Read and parse the file
    with open(filepath, 'r') as f:
        # Note, we can't have "fractional" people, days, or amount of seats.
        PEOPLE = int(f.readline().strip())
        DAYS = int(f.readline().strip())
        SEATS = [int(seat.strip()) for seat in f.readline().split(",")]

        # Split each price, convert to list
        SEAT_PRICES = [float(price.strip())
                       for price in f.readline().split(",")]
        HOTEL_PRICES = [float(price.strip())
                        for price in f.readline().split(",")]  # ... same as above

    return PEOPLE, DAYS, SEATS, SEAT_PRICES, HOTEL_PRICES


@dataclass
class InstanceSpace:
    """Instance space for generation of instances."""
    n: int = 100
    m: int = 10
    s_min: int = 1 
    s_max: int = 50
    p_min: int = 10 
    p_max: int = 100
    h_min: int = 10
    h_max: int = 100

    def gen(self):
        """Generate a random instance based on instance space parameters."""
        people = self.n
        days = self.m
        seats = np.random.randint(
            self.s_min, self.s_max + 1, size=self.m)

        seat_prices = np.random.randint(
            self.p_min, self.p_max + 1, size=self.m)
        hotel_prices = np.random.randint(
            self.h_min, self.h_max + 1, size=self.m)

        seats = seats.tolist()
        seats[-1] = people  # Ensure all can fly back on last day
        seat_prices = seat_prices.tolist()
        hotel_prices = hotel_prices.tolist()

        return people, days, seats, seat_prices, hotel_prices

    def gen_adversary(self):
        """Generate an adversary for this instance space."""
        people = self.n
        days = self.m
        seats = [self.n]*self.m
        seat_prices = [self.p_min] + [self.p_max]*(self.m - 1)
        hotel_prices = [price - 0.000000001 for price in seat_prices]

        seats[-1] = people  # Ensure all can fly back on last day

        return people, days, seats, seat_prices, hotel_prices

    @property
    def c_upper_bound(self):
        """The theoretical upper bound of the c-ratio"""
        return (self.p_max * (self.m - 1) + self.p_min) / self.p_min


def run_experiment(instance, verbose=False):
    """Run instance on both online and ofline algorithm, collect stats."""
    offline_start = time.time()
    optim = offline(*instance)
    offline_stop = time.time()
    offline_elapsed = offline_stop - offline_start

    online_start = time.time()
    algo = online(*instance)
    online_stop = time.time()
    online_elapsed = online_stop - online_start

    c_ratio = algo[2]/optim[2]

    if verbose:
        print(f"Ran offline in {offline_elapsed}s")
        print(f"Ran online in {online_elapsed}s")
        print(f"Optimal result from offline: {optim}")
        print(f"Result from online algorithm: {algo}")
        print(f"C-ratio: {c_ratio}")

    return optim, algo, c_ratio, (offline_elapsed, online_elapsed)


def run_experiments(instances, verbose=False):
    """Ran experiments on a collection of instances."""
    results = []

    for instance in instances:
        result = run_experiment(instance, verbose=verbose)
        results.append(result)

    return results


def run_experiment_from_files(filenames, verbose=False):
    """Read and parse files, and run experiments on them."""
    instances = [read_and_parse_instance(filename) for filename in filenames]
    run_experiments(instances, verbose=verbose)


def run_rand_experiments(instance_space, n_experiments):
    """
    Generate some random instances within an instance space, and run experiments on
    them.
    """

    cratios = []

    for _ in range(n_experiments):
        instance = instance_space.gen()
        _, _, cratio, _ = run_experiment(instance, verbose=False)
        assert cratio >= 1.0, cratio
        cratios.append(cratio)
    cratios = np.array(cratios)

    print(f"Average: {cratios.mean()}")
    print(f"Standard deviation: {cratios.std()}")
    print(f"Minimum: {cratios.min()}")
    print(f"Maximum: {cratios.max()}")

    plt.figure(figsize=(10, 6)) 
    sns.histplot(cratios, bins=50, color='skyblue', edgecolor='black')

    plt.xlabel("C-ratio")
    plt.ylabel("Frequency")
    plt.grid(True) 
    plt.show()


def run_hard_coded_experiments(verbose=True):
    """Load hard coded files and run experiments on them"""
    experiment_files = ["test1.txt", "test2.txt", "test3.txt"]
    return run_experiment_from_files(experiment_files, verbose=verbose)


def run_runtime_experiments(instance_space, start, stop, step=10):
    """
    Given an instance space, increase amount of days and generate instances.

    Plots the runtime for both online and offline afterwards.
    """
    optim_times = []
    algo_times = []

    for m in range(start, stop, step):
        instance_space.m = m
        instance = instance_space.gen()
        _, _, _, (optim_elapsed, algo_elapsed) = run_experiment(instance)
        optim_times.append(optim_elapsed)
        algo_times.append(algo_elapsed)

    plt.figure(figsize=(10, 6))
    plt.xlabel("Amount of days m")
    plt.ylabel("Time to find solution in seconds")
    sns.lineplot(x=range(start, stop, step),
                 y=optim_times, label="Offline runtime")
    sns.lineplot(x=range(start, stop, step),
                 y=algo_times, label="Online runtime")
    plt.show()


if __name__ == '__main__':
    # Amount of times to simulate
    ITERATIONS = 100_000

    # Run experiments on files
    run_hard_coded_experiments()

    # Define default instance space and run experiments
    original_instance_space = InstanceSpace()
    run_rand_experiments(original_instance_space, ITERATIONS)

    # Define altered instance space and run experiments
    instance_space_altered = InstanceSpace(p_min=50, p_max=150, h_min=1, h_max=49)
    run_rand_experiments(instance_space_altered, ITERATIONS)
