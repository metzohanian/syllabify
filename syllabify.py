from syllable3 import *
from repo import make_syllable
import json

def syllabify(word):
  syllable = generate(word.rstrip())
  if syllable:
    syllables = []
    encoding = []
    for syll in syllable:
      for s in syll:
        syllables.append(make_syllable(s))
        encoding.append(s)
  return (syllables, encoding)


if __name__ == '__main__':

  if len(sys.argv) > 1:
    words = sys.argv[1:]
    for word in words:
      (syllables, encoding) = syllabify(word)
      print(json.dumps(encoding, default=lambda o: o.__dict__))

  else:
    print('Please input a word, or list of words (space-separated) as argument variables')
    print('e.g. python3 syllable3.py linguist linguistics')
