#!/usr/bin/env python2.7
import os
import sys
import shutil
import string
import argparse
import nltk
from nltk.probability import LidstoneProbDist
import uuid
import random
import re
import charade

def open_dir(path='.'):
  path = os.path.abspath(path)
  dir_list = os.listdir(path)
  files = []
  for item in dir_list:
    fullpath = os.path.join(path, item)
    if os.path.isfile(fullpath):
      files.append(fullpath)
  return files

def read_files(files):
  result = ""
  for item in files:
    fb = open(item, "r")
    for line in fb:
      result = result + " " + line
  return result          

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Generate Markov chains from directory with text files")
  parser.add_argument("-d", "--dir", help="directory with files", required=True)
  parser.add_argument("-p", "--ply", help="PLY, default: 3", type=int, default="3")
  parser.add_argument("-w", "--words", help="Words, default: 100", type=int, default="100")
  parser.add_argument("-t", "--tries", help="Tries, default: 10", type=int, default="10")
  args = parser.parse_args()
  print args
  
  try:
    files = open_dir(args.dir)
    result = read_files(files)
    #print p.decode('your-system-encoding')
    enc = charade.detect(result)
    syscodepage =  sys.stdout.encoding
    chars = re.escape(string.punctuation)
    new_result = re.sub(r'[' + chars + ']', ' ', result.decode(enc['encoding']))
  except:
    raise

  tokens = nltk.word_tokenize(new_result.lower())
  estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
    
  f = open(str(uuid.uuid1()) + ".txt", "w")
  
  for i in range(args.tries):  
    content_model = nltk.NgramModel(args.ply, tokens, estimator=estimator)
    #l = len(content_model.generate(args.words*10))
    #random.seed()
    #rnd = random.randint(args.start, l - args.start)
    starting_words = content_model.generate(args.words*10)[-2:]
    try:
      print "Starting words:\t%s" % (" ".join(word.encode(syscodepage, "ignore") for word in starting_words))
    except:
      pass
    content = content_model.generate(args.words, starting_words)
    try:
      f.write(" ".join(word.encode("utf8") for word in content) + "\n")
    except Exception as e:
      f.close()
      print "Cannot write to file! Exception: %s" % e
  f.close()