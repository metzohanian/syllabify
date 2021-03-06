from syllable3 import *
from repo import *

rowcount = 1
start = 0
while rowcount > 0:
  entries = DB.session.execute("SELECT cmu.id, cmu.word from dict_cmu cmu where syllables is null order by id limit :start, 500", { "start": start })
  start = start + 500

  print("Working " + str(start))

  for entry in entries:
    try:
      #print(entry.word.rstrip())
      syllable = generate(entry.word.rstrip())
      if syllable:
        syllables = []
        encoding = []
        for syll in syllable:
          for s in syll:
            syllables.append(make_syllable(s))
            encoding.append(s)
        cmu = DB.session.query(DictCmu).get(entry.id)
        #print(json.dumps(syllables, default=lambda o: o.__dict__), "\r")
        #print(json.dumps(encoding, default=lambda o: o.__dict__), "\r")
        cmu.syllables = json.dumps(syllables, default=lambda o: o.__dict__)
        cmu.encoding = json.dumps(encoding, default=lambda o: o.__dict__)
        DB.session.add(cmu)
        DB.session.flush()
        DB.session.commit()
    except:
      import traceback
      traceback.print_exc()
      print("Processing Error: " + entry.word)

  rowcount = entries.rowcount
