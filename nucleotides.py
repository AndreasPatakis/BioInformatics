'''
6.14
* The player that is left without nucleotides wins
* Winning state comes from a losing state
* Losing state comes from a winning state
'''
m = int(input('Insert m: '))
n = int(input('Insert n: '))

init_state = sorted([m,n])

# The max length that a sequence can have when the game ends
MAX_WINNING_SEQUENCE_LENGTH = init_state[1] - (init_state[0] // 2 + 2 * (init_state[0] % 2))

winning = [[1,1]] + [[0,i] for i in range(MAX_WINNING_SEQUENCE_LENGTH + 1)]
losing = []
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
        new_states = [
            sorted([state[0] + 1, state[1] + 2]), 
            sorted([state[0] + 2, state[1] + 1])
        ]
 
        # Add only the unchecked states
        next_states.extend(filter(unchecked_state, new_states))

# Bottom up dynamic programming
# Start from the final winning states
# and build up to the initial state
while unchecked_state(init_state):
    get_next_states(winning, losing)
    get_next_states(losing, winning)
    moves += 1

# 1 if the 1st player wins and 2 if the 2nd player wins
winner = int(init_state in losing) + 1

# print(f'\nWINNING STATES: {winning}')
# print(f'\nLOSING STATES: {losing}')
print(f"\nPlayer {winner} wins in {moves + 1 - winner} moves!")
print(f"\nTotal moves: {2 * moves + 1 - winner}")
