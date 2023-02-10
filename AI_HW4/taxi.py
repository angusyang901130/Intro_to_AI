import numpy as np
import os
import gym
import random
import sys
from tqdm import tqdm

total_reward = []
sys.setrecursionlimit(3000)

epNum = 0
EPISODE = 0
max_reward = -100
initial_state = 0

class Agent():
    def __init__(self, env, epsilon=0.05, learning_rate=0.8, gamma=0.9):
        """
        Parameters:
            env: target enviornment.
            epsilon: Determinds the explore/expliot rate of the agent.
            learning_rate: Learning rate of the agent.
            gamma: discount rate of the agent.
        """
        self.env = env

        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.gamma = gamma

        # Initialize qtable
        self.qtable = np.zeros((env.observation_space.n, env.action_space.n))

        self.qvalue_rec = []

    def choose_action(self, state):
        """
        Choose the best action with given state and epsilon.

        Parameters:
            state: A representation of the current state of the enviornment.
            epsilon: Determines the explore/expliot rate of the agent.

        Returns:
            action: The action to be evaluated.
        """
        # Begin your code
        prob = random.uniform(0, 1)
        if prob > self.epsilon:
            return np.argmax(self.qtable[state])
        else:
            return self.env.action_space.sample()
        # End your code

    def learn(self, state, action, reward, next_state, done):
        """
        Calculate the new q-value base on the reward and state transformation observered after taking the action.

        Parameters:
            state: The state of the enviornment before taking the action.
            action: The exacuted action.
            reward: Obtained from the enviornment after taking the action.
            next_state: The state of the enviornment after taking the action.
            done: A boolean indicates whether the episode is done.

        Returns:
            None (Don't need to return anything)
        """
        # Begin your code
        best_qvalue = np.amax(self.qtable[next_state])
        current_qvalue = self.qtable[state, action]
        if not done:
            self.qtable[state, action] += self.learning_rate * (reward + self.gamma * best_qvalue - current_qvalue)
        else:
            self.qtable[state, action] += self.learning_rate * (reward - current_qvalue)
        # End your code

        # You can add some conditions to decide when to save your table
        global epNum
        global EPISODE
        global max_reward
        global initial_state
        
        if done:
            epNum += 1  

            if epNum == EPISODE:
                rewards = []

                for _ in range(25):
                    state = initial_state
                    count = 0
                    while True:
                        action = np.argmax(self.qtable[state])
                        next_state, reward, done, _ = self.env.step(action)
                        count += reward
                        if done == True:
                            rewards.append(count)
                            break

                        state = next_state

                if np.mean(rewards) > max_reward:  
                    max_reward = np.mean(rewards)      
                    np.save("./Tables/taxi_table.npy", self.qtable) 

    def check_max_Q(self, state):
        """
        - Implement the function calculating the max Q value of given state.
        - Check the max Q value of initial state

        Parameter:
            state: the state to be check.
        Return:
            max_q: the max Q value of given state
        """
        # Begin your code
        max_q = np.amax(self.qtable[state])

        #taxi->B: 3 steps / pickup at B: 1 step / B->G: 5 steps / pickoff: 1 step 
        # -1 + (-1)*g + (-1)*g^2 + ... + (-1)*g^(3+1+5-1) + 20*g^(3+1+5+1-1)
        power = np.power(self.gamma, 9)
        opt_Q = (-1) * (1 - power) / (1 - self.gamma) + power * 20

        print(f"Optimal Q:{opt_Q}")
        return max_q
        # End your code


def extract_state(ori_state):
        state = []
        
        if ori_state % 4 == 0:
            state.append('R')
        else:
            state.append('G')
        
        ori_state = ori_state // 4

        if ori_state % 5 == 2:
            state.append('Y')
        else:
            state.append('B')
        
        print(f"Initial state:\ntaxi at (2, 2), passenger at {state[1]}, destination at {state[0]}")
        

def train(env):
    """
    Train the agent on the given environment.

    Paramenters:
        env: the given environment.

    Returns:
        None (Don't need to return anything)
    """
    training_agent = Agent(env)
    episode = 3000
    rewards = []
    global EPISODE
    global epNum
    EPISODE = episode
    epNum = 0

    for ep in tqdm(range(episode)):
        state = env.reset()
        done = False

        count = 0
        while True:
            action = training_agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)

            training_agent.learn(state, action, reward, next_state, done)
            count += reward

            if done:
                rewards.append(count)
                break

            state = next_state

    total_reward.append(rewards)


def test(env):
    """
    Test the agent on the given environment.

    Paramenters:
        env: the given environment.

    Returns:
        None (Don't need to return anything)
    """
    testing_agent = Agent(env)
    testing_agent.qtable = np.load("./Tables/taxi_table.npy")
    rewards = []

    for _ in range(100):
        state = testing_agent.env.reset()
        count = 0
        while True:
            action = np.argmax(testing_agent.qtable[state])
            next_state, reward, done, _ = testing_agent.env.step(action)
            count += reward
            if done == True:
                rewards.append(count)
                break

            state = next_state
    # Please change to the assigned initial state in the Google sheet
    state = 253

    global initial_state
    initial_state = state

    print(f"average reward: {np.mean(rewards)}")
    extract_state(state)
    print(f"max Q:{testing_agent.check_max_Q(state)}")


def seed(seed=20):
    '''
    It is very IMPORTENT to set random seed for reproducibility of your result!
    '''
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    random.seed(seed)


if __name__ == "__main__":
    '''
    The main funtion
    '''
    # Please change to the assigned seed number in the Google sheet
    SEED = 76

    env = gym.make("Taxi-v3")
    seed(SEED)
    env.seed(SEED)
    env.action_space.seed(SEED)
        
    if not os.path.exists("./Tables"):
        os.mkdir("./Tables")
    
    # training section:
    if os.path.exists("./Tables/taxi_table.npy"):
        os.remove("./Tables/taxi_table.npy")

    for _ in range(5):
        train(env)   
    # testing section:
    test(env)
        
    if not os.path.exists("./Rewards"):
        os.mkdir("./Rewards")

    np.save("./Rewards/taxi_rewards.npy", np.array(total_reward))

    env.close()