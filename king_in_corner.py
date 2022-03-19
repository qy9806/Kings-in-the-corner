
# Import randint and shuffle from random module.
from random import randint, shuffle

######################################################################
# createDeck() produces a new, cannonically ordered, 52 card deck
# using a nested comprehension. Providing a value less than 13
# produces a smaller deck, like the semi-standard 40 card 4 suit 1-10
# deck used in many older card games (including tarot cards). Here,
# we'll use it with default values.
#
def createDeck(N=13, S=('spades', 'hearts', 'clubs', 'diamonds')):
    return([ (v, s) for s in S for v in range(1, N+1) ])

######################################################################
# Construct the representation of a given card using special unicode
# characters for hearts, diamonds, clubs, and spades. The input is a
# legal card, c, which is a (v, s) tuple. The output is a 2 or
# 3-character string 'vs' or 'vvs', where 's' here is the unicode
# character corresponding to the four standard suites (spades, hearts,
# diamonds or clubs -- provided), and v is a 1 or 2 digit string
# corresponding to the integers 2-10 and the special symbols 'A', 'K',
# 'Q', and 'J'.
#
# Example:
#    >>> displayCard((1, 'spades'))
#    'A♠'
#    >>> displayCard((12, 'hearts'))
#    'Q♡'
#
def displayCard(c):
    suits = {'spades':'\u2660', 'hearts':'\u2661', 'diamonds':'\u2662', 'clubs':'\u2663'}
    value = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K'}
    return(''.join( [ value[c[0]], suits[c[1]] ] ))

######################################################################
# Print out an indexed representation of the state of the table:
# foundation piles are numbered 0-3, corner piles 4-7.
#
# Example:
#   >>> showTable(F, C)
#     F0: 9♡...9♡
#     F1: 2♢...2♢
#     F2: 7♡...7♡
#     F3: 8♡...8♡
#     C4:
#     C5:
#     C6:
#     C7:
# Or, mid-game:
#     F0: 8♣...A♢
#     F1: J♣...J♣
#     F2: A♠...A♠
#     F3: 
#     C4: K♡...K♡
#     C5: 
#     C6: 
#     C7:
#
def showTable(F, C):
    for i in range(4):
        if not(F[i]):
            print('  F{}:'.format(i))
        else:
            print('  F{}: {}...{}'.format(i,displayCard(F[i][0]),displayCard(F[i][-1])))
    for i in range(4):
        if not(C[i]):
            print('  C{}:'.format(i+4))
        else:
            print('  C{}: {}...{}'.format(i+4,displayCard(C[i][0]),displayCard(C[i][-1])))

######################################################################
# Print out an indexed list of the cards in input list H, representing
# a hand. Entries are numbered starting at 8 (indexes 0-3 are reserved
# for foundation piles, and 4-7 are reserved for corners). The
# indexing is used to select cards for play.
#
# Example:
#   >>> showHand(H[0])
#   Hand: 8:A♢ 9:4♢ 10:3♡ 11:5♠ 12:6♠ 13:7♠ 14:8♠
#   >>> showHand(H[1])
#   Hand: 8:9♣ 9:5♢ 10:8♢ 11:9♢ 12:10♡ 13:A♠ 14:4♠
#
def showHand(H):
    print('Hand: {}'.format(' '.join([ "{}:{}".format(i+8, displayCard(H[i])) for i in range(len(H)) ] )))

######################################################################
# We'll use deal(N, D) to set up the game. Given a deck (presumably
# produced by createDeck()), shuffle it, then deal 7 cards to each of
# N players, and seed the foundation piles with 4 additional cards.
# Returns D, H, F, where D is what remains of the deck, H is a list of
# N 7-card "hands", and F is a list of lists corresponding to the four
# "seeded" foundation piles.
# 
# Example:
#   >>> D, H, F = deal(2, D)
#   >>> len(D)
#   34
#   >>> len(H)
#   2
#   >>> H[0][:3]
#   [(5, 'clubs'), (12, 'clubs'), (3, 'diamonds')]
#   >>> F[2]
#   [(11, 'hearts')]
#
# Todo: move any K to a corner pile. Would require returning C.
def deal(N, D):
    # Shuffle the deck, the return what's left of it after dealing 7
    # cards to each player and seeding the foundation piles.
    shuffle(D)
    return(D, [ sorted([ D.pop() for j in range(7) ], key=lambda card: (card[1], card[0])) for i in range(N) ], [ [ D.pop() ] for i in range(4) ])

######################################################################
# Returns True if card c can be appended to stack S. To be legal, c
# must be one less in value than S[-1], and should be of the "other"
# color (red vs black).
#
# Hint: Remember, S might be empty, in which case the answer should
# not be True.
#
# Hint: Use the encapsulated altcolor(c1, c2) helper function to check
# for alternating colors.
#
# Example:
#   >>> legal([(2, 'diamonds')], (1, 'spades'))
#   True
#   >>> legal([(2, 'diamonds')], (1, 'hearts'))
#   False
#
def legal(S, c):
    def altcolor(c1, c2):
        return (c1[1] in ('diamonds', 'hearts') and c2[1] in ('spades', 'clubs') or
                c1[1] in ('spades', 'clubs') and c2[1] in ('diamonds', 'hearts'))
    #print("Checking {} and {}".format(displayCard(c), displayCard(S[-1])))
    return (S and altcolor(c, S[-1]) and S[-1][0] == c[0]+1)

######################################################################
# Governs game play for N players (2 by default). This function sets
# up the game variables, D, H, F and C, then chooses the first player
# randomly from the N players. By convention, player 0 is the user,
# while all other player numbers are played by the auto player.
#
# Each turn, the current player draws a card from the deck D, if any
# remain, and then is free to make as many moves as he/she chooses. 
# 
# Hint: fill out the remainder of the function, replacing the pass
# statements and respecting the comments.
# 
def play(N=2):
    # Set up the game.
    D, H, F = deal(N, createDeck())
    C = [ [] for i in range(4) ]   # Corners, initially empty.

    # Randomly choose a player to start the game.
    player = randint(0,N-1)
    print('Player {} moves first.'.format(player))

    # Start the play loop; we'll need to exit explicitly when
    # termination conditions are realized.
    while True:
        # Draw a card if there are any left in the deck.
        H[player].append(D.pop())
        print('\n\nPlayer {} ({} cards) to move.'.format(player, len(H[player])))
        print('Deck has {} cards left.'.format(len(D)))
        # Now show the table.
        showTable(F, C)
        # Let the current player have a go.
        if player != 0:
            automove(F, C, H[player])
        else:
            usermove(F, C, H[player])

        # Check to see if player is out; if so, end the game.
        if H[player] == []:
            print('\n\nPlayer {} wins!'.format(player))
            showTable(F, C)
            break

        # Otherwise, go on to next player.
        player = (player+1) % N

######################################################################
# Prompts a user to play their hand.  See transcript for sample
# operation.
#
def usermove(F, C, hand):
    # Check if the index i indicates a valid F, C or hand index.  To
    # be valid, it cannot be an empty pile or an out-of-range hand
    def valid(i):
        return((0 <= i < 4 and F[i]) or (4 <= i < 8 and C[4+i]) or (8 <= i < 8+len(hand)))

    # Ensure the hand is sorted, integrating newly drawn card.
    hand.sort()

    # Give some instruction.
    print('Enter your move as "src dst": press "/" to refresh display; "." when done')

    # Manage any number of moves.
    while True:           # Until the user quits with a .
        # Display current hand.
        showHand(hand)

        # Read inputs and construct a tuple.
        move = []
        while not move or not valid(move[0]) or not valid(move[1]):
            move = input("Your move? ").split()
            if len(move) == 1:
                if move[0] == '.':
                    # Done. Return from this function to proceed.
                    print('Turn complete.')
                    return
                elif move[0] == '/':
                    showTable(F, C)
                    showHand(hand)
                    move = []
                    continue
            try:
                move = [int(move[0]), int(move[1])]
                # Execute the command, which looks like [from, to].
                # Remember, 0-3 are foundations, 4-7 are corners, 8+
                # are from your hand.
                if move[0] >= 8 and move[1] < 4 and (not F[move[1]] or legal(F[move[1]], hand[move[0]-8])):
                    # Playing a card from your hand to a foundation pile.
                    print('Moving {} to F{}.'.format(displayCard(hand[move[0]-8]), move[1]))
                    F[move[1]].append(hand.pop(move[0]-8))
                    showHand(hand)
                elif move[0] >= 0 and move[0] < 4 and move[1] >= 0 and move[1] < 4 and legal(F[move[1]], F[move[0]][0]):
                    # Moving a foundation pile to a foundation pile.
                    print('Moving F{} to F{}.'.format(move[0], move[1]))
                    F[move[1]].extend(F[move[0]])
                    F[move[0]] = []
                elif move[0] >= 8 and move[1] < 8 and ((not C[move[1]-4] and hand[move[0]-8][0]==13) or (C[move[1]-4] and legal(C[move[1]-4], hand[move[0]-8]))):
                    # Playing a card from your hand to a corner pile (K only to empty pile).
                    print('Moving {} to C{}.'.format(displayCard(hand[move[0]-8]), move[1]))
                    C[move[1]-4].append(hand.pop(move[0]-8))
                    showHand(hand)
                elif move[0] >= 0 and move[0] < 4 and move[1] >= 4 and move[1] < 8 and (not C[move[1]-4] and F[move[0]][0]==13) or (C[move[1]-4] and legal(C[move[1]-4], F[move[0]][0])):
                    # Moving a foundation pile to a corner pile.;
                    print('Moving F{} to C{}.'.format(move[0], move[1]))
                    C[move[1]-4].extend(F[move[0]])
                    F[move[0]] = []
                else:
                    print('Illegal move {}'.format(move))
            except:
                print('Ill-formed move {}'.format(move))
            # Make sure you still have cards, else reset move to go again.
            if not hand:
                return
            move = []

######################################################################
# Plays a hand automatically using a fixed but not particularly
# brilliant strategy. The strategy involves consolidating the table
# (to collapse foundation and corner piles), then scanning cards in
# your hand from highest to lowest, trying to place each card. The
# process is repeated until no card can be placed. See transcript for
# an example.
#
def automove(F, C, hand):
    # Keep playing cards while you're able to move something.
    moved = True
    while moved:
        moved = False	# Change to True if you move a card.

        # Start by consolidating the table.
        consolidate(F, C)

        # Sort the hand (destructively) so that you consider highest
        # value cards first.
        hand.sort()

        # Scan cards in hand from high to low value, which makes removing
        # elements easier.
        for i in range(len(hand)-1, -1, -1):
            #print('Trying {}:{}...'.format(i, displayCard(hand[i])))
            if hand[i][0] == 13:
                # Got a king; place in empty corner (guaranteed to be one).
                print('Moving {} to open corner.'.format(displayCard(hand[i])))
                C[C.index([])].append(hand.pop(i))
                moved = True
                continue
            # Try to place current card.
            for j in range(4):
                if C[j] and legal(C[j], hand[i]):
                    # Place current card on corner pile.
                    print('Moving {} to C{}.'.format(displayCard(hand[i]), j+4))
                    C[j].append(hand.pop(i))
                    moved = True
                    break
                elif F[j] and legal(F[j], hand[i]):
                    # Place current card on foundation pile.
                    print('Moving {} to F{}.'.format(displayCard(hand[i]), j))
                    F[j].append(hand.pop(i))
                    moved = True
                    break
                elif not F[j]:
                    # Start a new foundation pile.
                    print('Moving {} to open foundation.'.format(displayCard(hand[i])))
                    F[j].append(hand.pop(i))
                    moved = True
                    break

######################################################################
# consolidate(F, C) looks for opportunities to consolidate by moving a
# foundation pile to a corner pile or onto another foundation pile. It
# is used by the auto player to consolidate elements on the table to
# make it more playable.
#
# Example:
#   >>> showTable(F, C)
#     F0: 6♢...6♢
#     F1: 10♣...10♣
#     F2: J♡...J♡
#     F3: Q♠...Q♠
#     C4: K♢...K♢
#     C5:
#     C6:
#     C7:
#   >>> consolidate(F, C)
#   >>> showTable(F, C)
#     F0: 6♢...6♢
#     F1:
#     F2: 
#     F3: 
#     C4: K♢...10♣
#     C5:
#     C6:
#     C7:
#
def consolidate(F, C):
    # Move one foundation onto another.
    for j in range(0, 3):
        for k in range(j, 4):
            if not F[j] or not F[k]:
                continue
            if legal(F[j], F[k][0]):
                print('Moving F{} to F{}.'.format(k, j))
                F[j].extend(F[k])
                F[k] = []
            elif legal(F[k], F[j][0]):
                print('Moving F{} to F{}.'.format(j, k))
                F[k].extend(F[j])
                F[j] = []
    # Move a foundation onto a corner.
    for j in range(4):
        for k in range(4):
            if C[j] and F[k] and legal(C[j], F[k][0]):
                # Move F[k] onto C[j]
                print('Moving F{} to C{}.'.format(k, j+4))
                C[j].extend(F[k])
                F[k] = []
            elif not C[j] and F[k] and F[k][0][0] == 13:
                # Move F[k] onto empty C[j]
                print('Moving F{} to open corner.'.format(k))
                C[j] = F[k]
                F[k] = []

######################################################################
if __name__ == '__main__':
    play(3)
