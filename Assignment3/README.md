## Assignment 3
### Q1
#### How to run code:
Run test.py. 

environment.py, rollout.py, q_table.npy must be in the same folder.

#### Number of steps taken:
Number of steps taken for agents to reach final position was 13 steps.

#### Method Used:
Q learning was applied to all the agents. Optimum values were calculated and stored in q_table.npy

### Details of method: 
``` bash
n_iterations = 1000
n_steps = 100
min_epsilon = 0.001
epsilon = 1.0
decay_rate = 0.9995
alpha = 0.15
gamma = 0.95
```

#### Results:

![ezgif com-animated-gif-maker](https://github.com/user-attachments/assets/b0a06f72-ac04-444b-9493-4bac16af5682)



##### Steps Vs Iterations in training.
![steps_](https://github.com/user-attachments/assets/b28cd39e-7582-4264-b3f8-a34f40e0c062)


We see the steps to completions reduce as training proceeds

##### Initial positions of agents.
<img width="390" alt="Screenshot 2024-11-20 204533" src="https://github.com/user-attachments/assets/184ec542-917d-4bb7-8047-5f06513adf40">


##### Final positions of agents.
<img width="443" alt="Screenshot 2024-11-20 200930" src="https://github.com/user-attachments/assets/20ea2ad7-ba78-4c38-b7b9-5f3bee79aeaa">



### Q2
#### How to run code:
Run test_random.py. 

environment.py, rollout.py, q_table_random.npy must be in the same folder.

#### Number of steps taken:
Number of steps taken for agents to reach final position varies depending on the initial positions of agents

#### Method Used:
Q learning was applied to all the agents. Epsilon greedy was applied on testing phase incase agent gets stuck indefinitely in states. Optimum values were calculated and stored in q_table.npy.

#### Results:
##### Final Positions of agents
<img width="428" alt="Screenshot 2024-11-20 201134" src="https://github.com/user-attachments/assets/0f5e212e-1598-4cb1-b227-6711edb2fbb9">


