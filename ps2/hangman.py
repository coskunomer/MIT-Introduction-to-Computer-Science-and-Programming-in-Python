# Problem Set 2, hangman.py
# Name: Ömer Coşkun
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
vowels = ["i", "o", "a", "e"]
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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    a = True
    for i in secret_word:
        if i not in letters_guessed:
            a = False
            break
    return a

def get_guessed_word(secret_word, letters_guessed):
    l = []
    for i in secret_word:
        if i not in letters_guessed:
            l.append("_ ")
        else: 
            l.append(i)
    return "".join(l)


def get_available_letters(letters_guessed):
    l = [i for i in string.ascii_lowercase if i not in letters_guessed]
    return "".join(l)

    

def hangman(secret_word):
    print("Secret word contains", len(secret_word), "letters.")
    l = []
    check = -1
    warnings = 3
    i = 6
    while i > 0:
        if warnings == -1:
            i -= 1
            warnings = 3
            continue
        print("You have", i, "guesses left.")
        print("Available letters: ", get_available_letters(l))
        g = input("Please guess a letter: ")
        if g not in list(get_available_letters(l)):
            warnings -= 1
            if g.isalpha() == True: 
                print("You have already guessed", g, ".", " You have", warnings, "warnings left:", get_guessed_word(secret_word, l))
            else:
                print("Invalid input. You have", warnings, "warnings left:", get_guessed_word(secret_word, l))
            continue
        else:
            l.append(g)
            if g in list(secret_word):
                print("Good guess: ", get_guessed_word(secret_word, l))
            elif g in vowels:
                print("Oops! That letter is not in my word", get_guessed_word(secret_word, l))
                i -= 2
            else:
                print("Oops! That letter is not in my word", get_guessed_word(secret_word, l))
                i -= 1
        if is_word_guessed(secret_word, l): 
            print("You guessed the word right. Congratulations!")
            word = get_guessed_word(secret_word, l)
            print("Your total score is", i * len(set(list(secret_word))))
            check = 0
            break
    if check == -1:
        print("Game is Over!")
        print("Secret word was", secret_word, ".")


def match_with_gaps(my_word, other_word):
    a = True
    my_word = my_word.replace(" ", "")
    for i in range(len(my_word)):
        if my_word[i] != other_word[i] and my_word[i] != "_":
            a = False
            break
        if my_word[i] == "_" and other_word[i] in list(my_word):
            a = False
            break
    return a

def show_possible_matches(my_word):
    my_word = my_word.replace(" ", "")
    wdlist = load_words()
    check = 0
    for i in wdlist:
        if len(i) == len(my_word):
            if match_with_gaps(my_word, i) == True:
                print(i, end=" ")
                check = -1
    if check == 0: print("No matches found")
    print()

def hangman_with_hints(secret_word):
    print("Secret word contains", len(secret_word), "letters.")
    l = []
    checkk = 0
    check = -1
    warnings = 3
    i = 6
    while i > 0:
        if warnings == -1:
            i -= 1
            warnings = 3
            continue
        print("You have", i, "guesses left.")
        print("Available letters: ", get_available_letters(l))
        g = input("Please guess a letter: ")
        if g == "*" and checkk == 0:
            show_possible_matches(get_guessed_word(secret_word, l))
            checkk = -1
            continue
        elif g not in list(get_available_letters(l)):
            warnings -= 1
            if g.isalpha() == True: 
                print("You have already guessed", g, ".", " You have", warnings, "warnings left:", get_guessed_word(secret_word, l))
            else:
                print("Invalid input. You have", warnings, "warnings left:", get_guessed_word(secret_word, l))
            continue
        else:
            l.append(g)
            if g in list(secret_word):
                print("Good guess: ", get_guessed_word(secret_word, l))
            elif g in vowels:
                print("Oops! That letter is not in my word", get_guessed_word(secret_word, l))
                i -= 2
            else:
                print("Oops! That letter is not in my word", get_guessed_word(secret_word, l))
                i -= 1
        if is_word_guessed(secret_word, l): 
            print("You guessed the word right. Congratulations!")
            word = get_guessed_word(secret_word, l)
            print("Your total score is", i * len(set(list(secret_word))))
            check = 0
            break
    if check == -1:
        print("Game is Over!")
        print("Secret word was", secret_word, ".")

    
if __name__ == "__main__":
     
    secret_word = "apple"
    hangman_with_hints(secret_word)  
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
