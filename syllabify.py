from syllable3 import *
import json

if __name__ == '__main__':
    if len(sys.argv) > 1:
        words = sys.argv[1:]
        for word in words:
            syllable = generate(word.rstrip())
            raw = get_raw(word.rstrip())
            if syllable:
                for syll in syllable:
                    for s in syll:
                        print(json.dumps(s, default=lambda o: o.__dict__))  # print syllables
                        print(s)
                    print('\n')
    else:
        print('Please input a word, or list of words (space-separated) as argument variables')
        print('e.g. python3 syllable3.py linguist linguistics')
