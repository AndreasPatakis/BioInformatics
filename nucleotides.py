'''
6.14

n,m

* The player that is left without nucleotides loses

* Losing state comes from a winning state

* Winning state comes from a losing state
'''
import numpy as np

m = int(input('Insert m: '))
n = int(input('Insert n: '))

init_state = sorted([m,n])

# The max length that a sequence can have when the game ends
MAX_LOSING_SEQUENCE_LENGTH = init_state[1] - (init_state[0] // 2 + 2 * (init_state[0] % 2))

losing = [[1,1]] + [[0,i] for i in range(MAX_LOSING_SEQUENCE_LENGTH + 1)]
winning = []
moves = 0

def unchecked_state(state):
    '''Checks if a state has not been examined'''
    return state not in losing and state not in winning

def get_next_states(current_states, next_states):
    '''
    Fills the next states of the game based on the current states.

    A state is always sorted in order to avoid
    recalculating isomorphic states.
    For example [1,2] and [2,1] would be calculated twice.
    '''
    for state in current_states:
        # Find new states
        new_states = [sorted(list(np.array(state) + [1,2])), sorted(list(np.array(state) + [2,1]))]
        
        # Add only the unchecked states
        next_states.extend(filter(unchecked_state, new_states))

# Bottom up dynamic programming
# Start from the final losing states
# and build up to the initial state
while unchecked_state(init_state):
    get_next_states(losing, winning)
    get_next_states(winning, losing)
    moves += 1

# 1 if the 1st player wins and 2 if the 2nd player wins
winner = int(init_state in losing) + 1

# print(f'\nWINNING STATES: {winning}')
# print(f'\nLOSING STATES: {losing}')
print(f"\nPlayer {winner} wins in {moves} moves!")
print(f"Total moves: {2*(moves-1) + winner}")
