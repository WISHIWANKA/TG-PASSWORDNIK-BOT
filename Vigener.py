ALPHABET1 = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h',
             8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm',
             13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r',
             18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w',
             23: 'x', 24: 'y', 25: 'z'}

ALPHABET = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5,
            'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11,
            'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17,
            's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23,
            'y': 24, 'z': 25}


class Vigener:

    def __init__(self):
        pass

    def get_new_positions(self, key):
        positions = []
        key = key.lower()
        for i in range(len(key)):
            if key[i] in ALPHABET:
                positions.append(ALPHABET.get(key[i]))
            else:
                positions.append(0)
        return positions

    def encode(self, key, line):
        line = line.lower()
        new_line = ''
        positions = self.get_new_positions(key)
        counter = 0
        for i in range(len(line)):
            if line[i] in ALPHABET:
                new_line += self.get_new_letter_encode(line[i], positions[counter])
                counter += 1
            else:
                new_line += line[i]

            if counter >= len(positions):
                counter = 0

        return new_line

    def get_new_letter_encode(self, letter, step):
        index = ALPHABET.get(letter)
        newindex = (index + step) % 26
        return ALPHABET1.get(newindex)

    def get_new_letter_decode(self, letter, step):
        index = ALPHABET.get(letter)
        newindex = (index + 26 - step) % 26
        return ALPHABET1.get(newindex)

    def decode(self, key, line):
        line = line.lower()
        positions = self.get_new_positions(key)
        decoded_line = ""
        counter = 0
        for i in range(len(line)):
            if line[i] in ALPHABET:
                decoded_line += self.get_new_letter_decode(line[i], positions[counter])
                counter += 1
            else:
                decoded_line += line[i]
            if counter >= len(positions):
                counter = 0
        return decoded_line

