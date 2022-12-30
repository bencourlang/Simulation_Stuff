import simpy
import random
import statistics
import time
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation

wait_times = []

class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(0.05)

    def sell_food(self, moviegoer):
        yield self.env.timeout(1, 5)

    def go_to_movies(self, env, moviegoer, theater):
        arrival_time = env.now

        with theater.cashier.request() as request:
            yield request
            yield env.process(theater.purchase_ticket(moviegoer))

        with theater.usher.request() as request:
            yield request
            yield env.process(theater.check_ticket(moviegoer))

        if random.choice([True, False]):
            with theater.server.request() as request:
                yield request
                yield env.process(theater.sell_food(moviegoer))

        wait_times.append(env.now - arrival_time)

def run_theater(env, num_cashiers, num_servers, num_ushers):
    theater = Theater(env, num_cashiers, num_servers, num_ushers)

    for moviegoer in range(3):
        env.process(theater.go_to_movies(env, moviegoer, theater))

    while True:
        yield env.timeout(0.2)

        moviegoer += 1
        env.process(theater.go_to_movies(env, moviegoer, theater))

def get_wait_time(wait_times):
    return statistics.mean(wait_times)

def calculate_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)

    minutes, frac_minuets = divmod(average_wait, 1)
    seconds = frac_minuets * 60
    return round(minutes), round(seconds)

def get_user_input(): # not used
    num_cashiers = input("Input # of cashiers working: ")
    num_servers = input("Input # of servers working: ")
    num_ushers = input("Input # of ushers working: ")
    params = [num_cashiers, num_servers, num_ushers]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. The simulation will use default values:",
            "\n1 cashier, 1 server, 1 usher.",
        )
        params = [1, 1, 1]
    return params

def run_simulation(num_cashiers, num_servers, num_ushers, times_to_run):
    tot_min = []
    tot_sec = []

    times = []
    run = []

    for i in range(times_to_run):
        env = simpy.Environment()
        env.process(run_theater(env, num_cashiers, num_servers, num_ushers))
        env.run(until=90)

        mins, secs = calculate_wait_time(wait_times)

        tot_min.append(mins)
        tot_sec.append(secs)

        times.append(get_wait_time(wait_times))
        run.append(i)

        plt.cla()
        plt.plot(run, times)
        plt.pause(0.05)

    avg_min = round(statistics.mean(tot_min))
    avg_sec = round(statistics.mean(tot_sec))

    print(
      "Running simulation...",
      f"\nThe average wait time is {avg_min} minutes and {avg_sec} seconds.",
    )

    plt.show()

def main():
    random.seed(time.time())
    #num_cashiers, num_servers, num_ushers = get_user_input()
    num_cashiers = 10000
    num_servers = 2
    num_ushers = 1

    amount_to_run = 100

    run_simulation(num_cashiers, num_servers, num_ushers, amount_to_run)


if __name__ == '__main__':
    main()