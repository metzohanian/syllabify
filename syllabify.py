from syllable3 import *
import json

def get_backupword(word):
  import requests
  url = "https://wordsapiv1.p.rapidapi.com/words/" + word
  headers = {
      'x-rapidapi-key': "3308d1af8amshbd0031d17e3e271p141fd4jsn4b4f160bf1d3",
      'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
      }
  response = requests.request("GET", url, headers=headers)
  return response.json()

def _backup_syllabify(word):
  pass

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
      print(get_backupword(word))
      (syllables, encoding) = syllabify(word)
      print(json.dumps(encoding, default=lambda o: o.__dict__))

  else:
    print('Please input a word, or list of words (space-separated) as argument variables')
    print('e.g. python3 syllable3.py linguist linguistics')
