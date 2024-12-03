# -*- coding: utf-8 -*-
"""Question_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j917i5XwlfvgkyZSHnQ0cO54FGWx1cez
"""

import numpy as np

# Define the states and actions
states = ['Hostel', 'Academic Building', 'Canteen']
actions = ['Attend Class', 'Eat Food']

# Define rewards
rewards = {
    'Hostel': -1,
    'Academic Building': 3,
    'Canteen': 1
}

# Define transition probabilities
transition_probs = {
    ('Hostel', 'Attend Class', 'Academic Building'): 0.50,
    ('Hostel', 'Attend Class', 'Hostel'): 0.50,
    ('Hostel', 'Eat Food', 'Canteen'): 1.00,
    ('Academic Building', 'Attend Class', 'Academic Building'): 0.70,
    ('Academic Building', 'Attend Class', 'Canteen'): 0.30,
    ('Academic Building', 'Eat Food', 'Canteen'): 0.80,
    ('Academic Building', 'Eat Food', 'Academic Building'): 0.20,
    ('Canteen', 'Attend Class', 'Academic Building'): 0.60,
    ('Canteen', 'Attend Class', 'Hostel'): 0.30,
    ('Canteen', 'Attend Class', 'Canteen'): 0.10,
    ('Canteen', 'Eat Food', 'Canteen'): 1.00
}

# Initialize parameters
gamma = 0.9  # Discount factor
epsilon = 1e-5  # Convergence threshold

# Value Iteration
def value_iteration():
    V = {state: 0 for state in states}  # Initialize value function
    while True:
        delta = 0
        new_V = V.copy()
        for s in states:
            v = V[s]
            new_V[s] = max(sum(transition_probs.get((s, a, s_prime), 0) *
                               (rewards[s_prime] + gamma * V[s_prime])
                               for s_prime in states)
                           for a in actions)
            delta = max(delta, abs(v - new_V[s]))
        V = new_V
        if delta < epsilon:
            break
    return V

def get_policy(V):
    policy = {}
    for s in states:
        policy[s] = max(actions, key=lambda a: sum(transition_probs.get((s, a, s_prime), 0) *
                                                      (rewards[s_prime] + gamma * V[s_prime])
                                                      for s_prime in states))
    return policy

V_value_iteration = value_iteration()
policy_value_iteration = get_policy(V_value_iteration)

# Policy Iteration
def policy_evaluation(policy):
    V = {state: 0 for state in states}  # Initialize value function
    while True:
        delta = 0
        new_V = V.copy()
        for s in states:
            v = V[s]
            a = policy[s]
            new_V[s] = sum(transition_probs.get((s, a, s_prime), 0) *
                           (rewards[s_prime] + gamma * V[s_prime])
                           for s_prime in states)
            delta = max(delta, abs(v - new_V[s]))
        V = new_V
        if delta < epsilon:
            break
    return V

def policy_improvement(V):
    policy = {}
    for s in states:
        policy[s] = max(actions, key=lambda a: sum(transition_probs.get((s, a, s_prime), 0) *
                                                    (rewards[s_prime] + gamma * V[s_prime])
                                                    for s_prime in states))
    return policy

def policy_iteration():
    policy = {s: np.random.choice(actions) for s in states}  # Initialize random policy
    while True:
        V = policy_evaluation(policy)
        new_policy = policy_improvement(V)
        if new_policy == policy:
            break
        policy = new_policy
    return V, policy

V_policy_iteration, policy_policy_iteration = policy_iteration()

# Compare the two policies
def compare_policies(policy1, policy2):
    return all(policy1[s] == policy2[s] for s in states)

# Output results
print("Optimal Values and Policy With Value Iteration")
print("Optimal Values :")
for s in states:
    print(f"{s}: {V_value_iteration[s]}")

print("\nOptimal Policy (Value Iteration):")
for s in states:
    print(f"{s}: {policy_value_iteration[s]}")

print("\nOptimal Values and Policy With Policy Iteration")
print("Optimal Values :")
for s in states:
    print(f"{s}: {V_policy_iteration[s]}")

print("\nOptimal Policy (Policy Iteration):")
for s in states:
    print(f"{s}: {policy_policy_iteration[s]}")

# Compare policies
if compare_policies(policy_value_iteration, policy_policy_iteration):
    print("\nThe policies from Value Iteration and Policy Iteration are the same.")
else:
    print("\nThe policies from Value Iteration and Policy Iteration are different.")