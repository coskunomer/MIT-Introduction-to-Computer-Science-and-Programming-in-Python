# Problem Set 4A
# Name: Ömer Coşkun
# Collaborators:
# Time Spent: x:xx
from itertools import permutations
def get_permutations(sequence):
    perm = permutations(sequence)
    l = []
    for i in perm:
        l.append("".join(i))
    return l

if __name__ == '__main__':
    word = input()
    print(get_permutations(word))

