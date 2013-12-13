#!/usr/bin/env python2.7
import os
import shutil
import argparse
import nltk
from nltk.probability import LidstoneProbDist
import uuid
import random

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
  except:
    raise

  tokens = nltk.word_tokenize(result)
  estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)  
  f = open(str(uuid.uuid1()), "w")
  
  for i in range(args.tries):  
    content_model = nltk.NgramModel(args.ply, tokens, estimator=estimator)
    starting_words = content_model.generate(args.words)[-2:] 
    content = content_model.generate(args.words, starting_words)
    f.write(" ".join(word for word in content) + "\n")
  f.close()  
