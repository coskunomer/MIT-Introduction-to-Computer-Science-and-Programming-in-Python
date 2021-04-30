# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Ömer Coşkun
# Collaborators : <your collaborators>
# Time spent    : <total time>
import math
import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
wdlist = ["a", "e", "i", "o", "u"]
SCRABBLE_LETTER_VALUES = {
    "*": 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    first_component = 0
    for i in word.lower():
        first_component += SCRABBLE_LETTER_VALUES[i]
    second_component = max(int(((7 * len(word)) - 3 * (n - len(word)))), 1)
    #print(first_component, second_component, len(word))
    score = int(first_component*second_component)
    return score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
        hand["*"] = 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    word = word.lower()
    new_hand = hand.copy()
    for i in word:
        new_hand[i] = new_hand.get(i, 0) - 1
        if new_hand[i] <= 0:
            new_hand.pop(i)
    return new_hand


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    c = True
    c_hand = hand.copy()
    wd = True
    word = word.lower()
    cword = word
    if "*" in word.lower():
        for i in wdlist:
            nword = word.replace("*", i)
            if nword in word_list:
                wd = True
                word = nword
                break
            else: wd = False
    for i in cword:
        c_hand[i] = c_hand.get(i, 0) - 1
        if c_hand[i] <= -1:
            c = False
            break
    return (word.isalpha() and word.lower() in word_list and c and wd)

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    return len(list(hand.values()))

def play_hand(hand, word_list):
    score = 0
    display_hand(hand)
    while len(hand) != 0:
        word = input("Please enter a word: ")
        if word == "!!" or len(word) == 0: break
        elif is_valid_word(word, hand, word_list) == False:
            hand = update_hand(hand, word)
            print("====Invalid input====\n")
            display_hand(hand)
        else:
            score += get_word_score(word, len(list(hand.values())))
            print("Your score: ", get_word_score(word, len(list(hand.values()))))
            hand = update_hand(hand, word)
            display_hand(hand)
            print("Sub total: ", score)
            if sum(list(hand.values())) == 0:
                break
    print("==Hand is over==\n")
    print("Total score of the hand: ", score)
    return score

def substitute_hand(hand, letter):
    if hand[letter] <= 0:
        print("==Letter is not available==\n")
    else:
        hand[random.choice("".join(list(set(list(VOWELS) + list(CONSONANTS)) - set(list(hand.keys())))))] = hand[letter]
        del hand[letter]
    return hand
       
    
def play_game(word_list):
    s, game_score, game_score2 = 0, 0, 0
    for i in range(int(input("Enter the number of hands: "))):
        hand = deal_hand(HAND_SIZE)
        display_hand(hand)
        chand = hand
        subs = input("Would you like to substitute letter?\n")
        if subs.lower() == "yes":
            chand = substitute_hand(chand, input("Enter a letter"))
        game_score = play_hand(chand, word_list)
        print("Your score is:", game_score)
        q = input("Would you like to replay the hand?\n")
        if q.lower() == "yes":
            game_score2 = play_hand(hand, word_list)
            print("Your score is:", game_score2)
        print("Your total score:", max(game_score, game_score2))
        s += max(game_score, game_score2)
    print("===Congratulations===")
    print("Game Score:", s)


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

