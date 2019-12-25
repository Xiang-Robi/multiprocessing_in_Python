"""
Rational for estimating Pi value:
- In a 2D coordinate system, a series of random dots are generated.
- All the dots fall into a square (side_length=2) region centered at position (0, 0).
- A circle (radius=1) with centroid at position (0, 0) is enclosed in that square.
- Suppose the probability for a dot falling into the enclosed circle is P.
- P = circle_area / square_area = pi * (radius**2) / side_length ** 2
- Thus, pi = P * (side_length ** 2) / (radius**2)
- Values for radius and side_length are already known and P will be obtained by experiments, so pi can be calculated.
"""

import math
import timeit
import random
import multiprocessing


def worker(*args):

    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    
    radius = 1.0
    dist_dot_centroid = math.sqrt(x**2 + y**2)
    
    # True / 1 will be returned if the dot falls in the circle. 
    # Otherwise, False / 0 will be returned.
    # Square root can be omitted for performance.
    return dist_dot_centroid <= radius


if __name__ == '__main__':

    start = timeit.default_timer()
    num_processes = multiprocessing.cpu_count() - 1 or 1  # one process will be used for single core machine
    total_num_trials = int(1e7)  # 1e7 is float
    
    pool = multiprocessing.Pool(processes=num_processes)
    args_generator = (None for _ in range(total_num_trials))  # generator saves RAM
    trial_results = pool.map(worker, args_generator)

    radius = 1
    side_length = 2
    square_area = side_length ** 2
    # bool is a subtype of int and behaves like 1 and 0, so can be summed directly
    probability_a_dot_inside_the_circle = sum(trial_results) / total_num_trials
    pi = (probability_a_dot_inside_the_circle * square_area) / (radius**2)

    end = timeit.default_timer()

    print('num_processes: {}'.format(num_processes))
    print('execution time: {:.2f} seconds'.format(end - start))
    print('estimated pi value: {}'.format(pi))
