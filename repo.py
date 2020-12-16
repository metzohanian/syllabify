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

class DictCmu(Base):
  __tablename__ = "dict_cmu"

  id                    = Column(Integer, primary_key=True)
  dictionary_id         = Column(Integer)
  word                  = Column(String)
  arpabet               = Column(String)
  arpabet_plain         = Column(String)
  comment               = Column(String)
  syllables             = Column(String)
  encoding              = Column(String)

class DictIpa(Base):
  __tablename__ = "dict_ipa"

  id                    = Column(Integer, primary_key=True)
  dictionary_id         = Column(Integer)
  cmu_id                = Column(Integer)
  word                  = Column(String)
  ipa                   = Column(String)
  arpabet               = Column(String)
  arpabet_plain         = Column(String)
  syllables             = Column(String)
  encoding              = Column(String)


def make_syllable(syll):
  from syllable_types3 import Cluster

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