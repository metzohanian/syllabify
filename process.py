from syllable3 import *
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, DateTime, text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DECIMAL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os, json

load_dotenv(dotenv_path="/var/syllabify/.env")

Base = declarative_base()

def DB():
  engine = None
  Session = None
  session = None

DB.engine = create_engine("mysql+pymysql://" + os.getenv('DB_USERNAME') + ":" + os.getenv('DB_PASSWORD') + "@" + os.getenv('DB_HOSTNAME') + ":" + os.getenv('DB_PORT') + "/" + os.getenv('DB_DATABASE') + "?autocommit=true",
    isolation_level="READ UNCOMMITTED")
DB.Session = sessionmaker()
DB.Session.configure(bind=DB.engine)
DB.session = DB.Session()

class DictCmuSyllables(Base):
  __tablename__ = "dict_cmusyllables"

  dict_cmusyllables_id  = Column(Integer, primary_key=True)
  dict_entries_id       = Column(Integer)
  syllable_order        = Column(Integer)
  syllable              = Column(String)
  encoding              = Column(String)

def make_syllable(syll):

  def squeeze(phoneme_list):

    return ' '.join(p.phoneme for p in phoneme_list)
      
  phonemes = []
  if type(syll.onset) is Cluster:
    phonemes.append(squeeze(syll.onset.phoneme_list))
  if type(syll.rime.nucleus) is Cluster:
    phonemes.append(squeeze(syll.rime.nucleus.phoneme_list))
  if type(syll.rime.coda) is Cluster:
    phonemes.append(squeeze(syll.rime.coda.phoneme_list))

  return ' '.join(phonemes)

rowcount = 1
start = 90001
while rowcount > 0 and start < 120000:
  entries = DB.session.execute(
    "SELECT w.word, e.* \
      from tempotalk.dict_words w \
        left join tempotalk.dict_entries e on e.dict_words_id = w.dict_words_id limit :start, 500", { "start": start }
    )
  start = start + 500

  print("Working " + str(start))

  for entry in entries:
    try:
      syllable = generate(entry.word.rstrip())
      if syllable:
        for syll in syllable:
          scount = 0
          for s in syll:
            cmusyll = DictCmuSyllables()
            cmusyll.dict_entries_id = entry.dict_entries_id
            cmusyll.syllable_order = scount
            scount = scount + 1
            cmusyll.encoding = json.dumps(s, default=lambda o: o.__dict__)
            cmusyll.syllable = make_syllable(s)
            DB.session.add(cmusyll)
        DB.session.flush()
        DB.session.commit()
    except:
      print("Processing Error: " + entry.word)

  rowcount = entries.rowcount
