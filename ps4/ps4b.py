# Problem Set 4B
# Name: Ömer Coşkun
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    #>>> is_word(word_list, 'bat') returns
    True
    #>>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        assert shift == int(shift)
        lower_letters = string.ascii_lowercase * 2
        upper_letters = string.ascii_uppercase * 2
        punc = "!@#$%^&*()-_+={}[]|\:;'<>?,./\" "
        d = {}
        for i, let in enumerate(lower_letters[:26]):
            d[let] = lower_letters[i +shift]
        for i, let in enumerate(upper_letters[:26]):
            d[let] = upper_letters[i +shift]
        for let in punc:
            d[let] = let
        return d

    def apply_shift(self, shift):
        d = self.build_shift_dict(shift)
        l = []
        for i in self.message_text:
            l.append(d[i])
        r = "".join(l)
        return r

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        return self.get_shift()

    def get_encryption_dict(self):
        return self.get_encryption_dict

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.get_encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)
        self.shift = shift

class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)

    def decrypt_message(self):
        wlist = self.get_valid_words()
        count = []
        for i in range(26):
            a = self.apply_shift(i)
            words = a.split()
            ct = 0
            for word in words:
                if word.lower() in wlist:
                    ct += 1
            count.append((ct, i, a))
        ans = max(count)
        return ans[1:3]

if __name__ == '__main__':

    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    plaintext = PlaintextMessage('hairy balls', 1)
    print('Expected Output: ibjsz cbmmt')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    story = get_story_string()
    ciphertext = CiphertextMessage(story)
    print('Unencypted story:', ciphertext.decrypt_message())
