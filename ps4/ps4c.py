# Problem Set 4C
# Name: Ömer Coşkun
# Collaborators:
# Time Spent: x:xx

from ps4a import get_permutations

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


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        return self.valid_words
                
    def build_transpose_dict(self, vowels_permutation):
        d = {}
        punc = "!@#$%^&*()-_+={}[]|\:;'<>?,./\" "
        for i in range(5):
            d[VOWELS_LOWER[i]] = vowels_permutation[i]
            d[VOWELS_UPPER[i]] = vowels_permutation[i]
        for i in CONSONANTS_UPPER:
            d[i] = i
        for i in CONSONANTS_LOWER:
            d[i] = i
        for i in punc:
            d[i] = i
        return d
    
    def apply_transpose(self, transpose_dict):
        l = []
        for i in self.get_message_text():
            l.append(transpose_dict[i])
        return "".join(l)


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        wdlist = self.get_valid_words()
        perm = get_permutations("aeiou")
        count = []
        for i in perm:
            d = self.build_transpose_dict(i)
            words = self.apply_transpose(d)
            word = words.split()
            ct = 0
            for j in word:
                l = [letter for letter in j if letter.isalpha()]
                j = "".join(l)
                if j.lower() in wdlist:
                    ct += 1
            count.append((ct, words))
        ans = []
        for i in count:
            if int(i[0]) == int(max(count)[0]):
                ans.append(set(i))
        return ans

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    message = SubMessage('Hairy Chest')
    permutation = 'iauoe'
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hiury Chast!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose((enc_dict)))
    print('Decrypted message:', enc_message.decrypt_message())
