import numpy as np
from scipy.stats import norm

def calculate_d_prime_and_c(hits, false_alarms, go_trials, no_go_trials):
    # Calculate hit rate and false alarm rate
    hit_rate = hits / go_trials
    false_alarm_rate = false_alarms / no_go_trials

    # Calculate z-scores
    z_hit = norm.ppf(hit_rate)
    z_false_alarm = norm.ppf(false_alarm_rate)

    # Calculate d' and c
    d_prime = z_hit - z_false_alarm
    c_prime = -(z_hit + z_false_alarm) / 2

    return d_prime, c_prime

# Example usage:

total = 150
n_backs = 25
n_hits = 70
n_false_alarms = 20
n_go_trials = total-n_backs
n_no_go_trials = n_backs

d_prime, c_prime = calculate_d_prime_and_c(n_hits, n_false_alarms, n_go_trials, n_no_go_trials)
print("d' (Sensitivity):", d_prime)
print("c (Response Bias):", c_prime)
