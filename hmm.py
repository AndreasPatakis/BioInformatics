import numpy as np
import math

    #          TRANSITION PROBABILITIES
    #
    #             a    b
    #         a  0.9  0.1
    #         b  0.1  0.9
    #
    #
    #            EMISSION PROBABILITIES
    #
    #             A       G       T       C
    #         a  0.4     0.4     0.1     0.1
    #         b  0.2     0.2     0.3     0.3

class Hidden_Markov_Model:
    def __init__(self,states,observations,transition,emission):
        self.states = states
        self.observations = observations
        self.transition_prob = np.log(np.array(transition))
        self.a_priori_prob = self.a_priori_compute(np.array(transition))
        self.emission_prob = np.log(np.array(emission))

    def a_priori_compute(self,transition_prob):
        #The sum of all states adds up to 1 because its the same of all possible outcomes
        #In our case we have 2 states so state1 + state2  = 1
        states = np.ones(2)
        be_state1 = transition_prob[:,0]
        #Equation for state1 is represented as: state1 = prob_x0 * state1 + prob_x1 * state2
        #which is also equal to: prob_x0 * state1 - state1 + prob_x1 * state2 = 0
        be_state1[0] = be_state1[0] - 1
        #So in order to find the a priori probability for a random state to be state1 or state2
        #we solve the linear system of equations: prob_x0 * state1 - state1 + prob_x1 * state2 = 0, state1 + state2 = 1
        outcome = np.array([0,1])

        states_probabilities = np.linalg.solve([be_state1,states],outcome)
        return np.log(states_probabilities)

    def calc_sequence(self,sequence):
        observations = []
        num_of_states = len(self.states)
        seq_split = list(sequence)
        for observation in seq_split:
            observations.append(Observation(observation,num_of_states))
        for i,obs in enumerate(observations):
            observation_num = self.observations[obs.observation]
            #When calculating the probability of the first observation, we dont use the transition probabilities
            #(as there are no transitions) and we simply calculate the probability using the emission ans a_priori probabilities
            if i == 0:
                for key,value in self.states.items():
                    #We add up the probabilities(and not multiply them) because we use log ranking probabilities
                    probability = self.a_priori_prob[value] + self.emission_prob[value][observation_num]
                    observations[i].value[value] = probability
                    observations[i].state[value] = key
            else:
                for j,prev_state in enumerate(observations[i-1].state):
                    for key,value in self.states.items():
                    #For calculating the probability of state, we have to add up the transition, emission and the probability of previous state.
                    #Note that we add up the probabilities because we use logarithmic ranking
                        prev_state_value = self.states[prev_state]
                        prev_state_prob = observations[i-1].value[j]
                        transition_prob = self.transition_prob[prev_state_value][value]
                        emission_prob = self.emission_prob[value][observation_num]
                        #We add up the probabilities(and not multiply them) because we use log ranking probabilities
                        probability =  prev_state_prob + transition_prob + emission_prob
                        #In this step we make use of principle behind Viterbi algorithm
                        #In each step we only keep best the states derived by a certain observation
                        #The above means that in each new observation, we only have to calculate the probabilities
                        #of our states happening as we already have calculated the best path leading to  the previous state
                        if obs.value[value] == None or obs.value[value] < probability:
                            observations[i].value[value] = probability
                            observations[i].state[value] = key

        best_guess = []
        for guess in observations:
            max_prob_index = guess.value.index(max(guess.value))
            best_guess.append(guess.state[max_prob_index])
        return best_guess

class Observation():
    def __init__(self,observation,total_states):
        self.observation = observation
        self.state = [None]*total_states
        self.value = [None]*total_states



if __name__ == '__main__':

    states = {"α" : 0, "β": 1}
    observations = {"A":0,"G":1,"T":2,"C":3}

    transition = [[0.9, 0.1],[0.1, 0.9]]
    emission = [[0.4, 0.4, 0.1, 0.1],[0.2, 0.2, 0.3, 0.3]]

    sequence = "GGCT"
    hmm = Hidden_Markov_Model(states,observations,transition,emission)
    best_guess = hmm.calc_sequence(sequence)
    print(best_guess)
