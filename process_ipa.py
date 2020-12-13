from syllable3 import *
from repo import *

rowcount = 1
start = 0
while rowcount > 0:
  entries = DB.session.execute("SELECT ipa.id, ipa.word from dict_ipa ipa order by id limit :start, 500", { "start": start })
  start = start + 500

  print("Working " + str(start))

  for entry in entries:
    try:
      #print(entry.word.rstrip())
      syllable = generate(entry.word.strip())
      if syllable:
        syllables = []
        encoding = []
        for syll in syllable:
          for s in syll:
            syllables.append(make_syllable(s))
            encoding.append(s)
        ipa = DB.session.query(DictIpa).get(entry.id)
        #print(json.dumps(syllables, default=lambda o: o.__dict__), "\r")
        #print(json.dumps(encoding, default=lambda o: o.__dict__), "\r")
        ipa.syllables = json.dumps(syllables, default=lambda o: o.__dict__)
        ipa.encoding = json.dumps(encoding, default=lambda o: o.__dict__)
        DB.session.add(ipa)
        DB.session.flush()
        DB.session.commit()
    except:
      import traceback
      traceback.print_exc()
      DB.session.rollback()
      print("Processing Error: " + entry.word)

  rowcount = entries.rowcount
