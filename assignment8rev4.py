# IS620 - Assignment 8
# Program: assignment8rev4.py
# Student: Neil Acampa
# Date:    10/18/16
# Function:



# 1. Choose a corpus of interest.
# 2. How many total unique words are in the corpus? (Please feel free to define unique words in any interesting, defensible way).

# 1    -  Perform runs on two corpuses
#      -  Read in Alice in Wonderland by Lewis Carroll on Pass1 
#      -  Read Far from the Maddening Crowd by Thomas Hardy on Pass2
#      -  Parse, remove special chars, set to lower case
#      -  Update masterdict with unique words and count
#      -  Update uniquewords: a 2 dimensional list of unique words and count
#      -  vocab: Sort of words by descending word count
#      -  vocab200: Top 200 words and word count
#      -  Custom functions:  remove_characters, remove_symbols, find_word


# 2    -  Use NLTK commands
#      -  Read in gutenberg corpus book: Far from the Maddening Crowd by Thomas Hardy or Alice in Wonderland
#      -  Strip punctuation
#      -  Set words to lower case
#      -  Tokenize ad sort

# 3    -  Perform statistics
#      -  wordcnt:   Count of Total words
#      -  uniquecnt: Count of unique words
#      -  wcnt:      Count of unique words that make up half of all words
#      -  zipfs:     Array of zipf distribution for the Top 20 words
#      -  teststat:  Test Chi Square stat (Observed - Expected)^2/Expected
#                    teststat = (word cnt - zipf count)^2 / zipf count
#         totChiStat: Test statictic 
#         ChiSquare : 9 dof and alpha .005: 38.582
#      -  Test Zipfs distribution against our corpus

#      -  Use FreqDist or Hist to show word frequency of top 200 words



from __future__ import absolute_import 
from __future__ import division
import re
import os 
import math
import decimal
import numpy as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import networkx as nx
import random
from urllib import urlopen
import nltk
nltk.download('gutenberg')
from nltk import word_tokenize
nltk.download('maxent_treebank_pos_tagger')
nltk.download('punkt')
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')




linelst=[]
lines  = ""
allwords       = []   # Contains all words
masterdict     = []   # Contains unique words
masterdictcnt  = []   # Contains count of unique words corresponding to masterdict
uniquewords    = []   # Contains unique words in the first dimension and the count in the second dim
                      # Will try to use if it works for unique word count

vocab          = []   # Unique words sorted by descending count
vocab200       = []   # Top 200 vocabulary words

vocabF         = []   # Vocabulary words for Freq Dist


# Zipfs table Headings

zheadings      = []
zheadings.append("Term")
zheadings.append("Word")
zheadings.append("Obs")
zheadings.append("Exp")
zheadings.append("ChiSqStat")


zipfs          = []  # Zipfs frequencies
chitest        = []  # Chi square test 

nltkflag       = 0   # Set to zero to use a local text file and functions
                     # Set to 1 to use nltk commands
halftot1       = []  # Store number of unique words reprenting 1/2 total words for pass 1
halftot2       = []  # Store number of unique words reprenting 1/2 total words for pass 1

rejectchars = [',','.','?','<','>','!','"','-','%','&','#','(',')','*',';'];
rcnt = len(rejectchars);


def remove_characters(word):
  """Replace special characters in the word"""
  
  for i in range(rcnt):
    rchar = rejectchars[i]
    if rchar in word:
      word = word.replace(rchar,"")

  return word


def remove_symbols(word):
  """Replace symbols in the word"""
  w = len(word)
  word = (ord(c) for c in word) 
  word = map(lambda x:x if x<123 or x>255 else " ", word)
  newword=""
  for c in range(w):
    if word[c] <> " ":
      newword += chr(word[c]);
  
  return newword


def find_word(word, masterdict):
  """Find and return index of word in dictionary"""

  masterlen = len(masterdict)
  find=0
  temp="x"
  try:
   temp = masterdict.index(word);
   return temp
  except ValueError:
   return temp


def display_hist(uniquevocab, corpus):
  """Display histogram of Top 200 most frequent words"""

  title = ("Histogram of Top 200 most frequent words in Corpus %s") % (corpus)
  plt.title(title) 
  plt.xlabel("Words")
  plt.ylabel("Count")
  yvalues = uniquevocab[1:]
  xvalues = uniquevocab[0:]
  plt.hist(yvalues, bins = 10, normed = True, color = 'b')
  plt.grid(True)
  fname = "Word Frequency.png"
  plt.savefig(fname) # save as png
  plt.show()
  return



def parse_data(linelst):
 """Parse each line and update arrays"""

 return




if __name__ == "__main__":
 linecnt  = 0
 print
 filepath=""
 temp    =""
 tokens  = ""
 valid   = 0
 p       = 1
 cwd = os.getcwd()
 while (p <=2):
  if (p == 1):
   corpus     = "Alice in Wonderland"
   fullcorpus = "Alice in Wonderland by Lewis Carroll"
   currfilepath = str(cwd) + "\carroll-alice.txt"
  else: 
   corpus     = "Far from the Maddening Crowd"
   fullcorpus = "Far from the Maddening Crowd by Thomas Hardy"
   currfilepath = str(cwd) + "\crowd13.txt"

  print currfilepath
  print ("Enter the Full File Path including the File")
  print ("or Press return to use current File Path %s") % (currfilepath)
  filepath = raw_input("Please enter the File Path now ")
  valid = 0
  if filepath == "":
     filepath = currfilepath

 
  try:
       #f = open("c:\carroll-alice.txt","r")
       f = open(filepath,"r")
       try:
         valid=1
         x =0
         j=0
         for lines in f:
           lines = lines.rstrip()
           temp = lines.split(" ");
           l = len(temp)
           for x in range(l):
             word = remove_characters(temp[x])
             word = remove_symbols(word)
             word = word.lower()
             word = word.replace(" ","")
             if (word != ''):
               allwords.append(word)
                     
       finally:
         if (nltkflag == 0):
            f.close()
         
  except IOError:
       print ("File not Found - Program aborting")

  if not(valid):
     exit()
 
 
  wordcnt     = len(allwords)
  halfwordcnt = int(wordcnt / 2)
    
  print 
  for x in range(wordcnt):
    word = allwords[x]
    findx = find_word(word, masterdict)
    if (findx == "x"):
       masterdict.append(word)
       masterdictcnt.append(1)
    else:
       masterdictcnt[findx]+=1
     
      
   

  uniquecnt = len(masterdict)
  print ("Statistics for Corpus:  %s") % (fullcorpus)
  print
  print("There are %d total words in the Corpus") % (wordcnt)
  print("There are %d total Unique words in the Corpus") % (uniquecnt)
  print

 
 
 
  for i in range(uniquecnt):
    uniquewords.append([masterdict[i], masterdictcnt[i]])
 
 
  print ("10 Unique Words in Corpus %s") % (corpus)
  for i in range(10):
    print (uniquewords[i])


  print
  print 
  vocab = sorted(uniquewords, key = lambda w: w[1:], reverse = True)
  print ("Top 10 Unique Words in Corpus %s") % (corpus)
  for i in range(10):
    print (vocab[i])


 
# Now Find the number of unique words that represent halve of the entire corpus
  i = -1
  wcnt = 0
  runtotal =0
  while (runtotal <= halfwordcnt):
    i=i+1
    runtotal+=vocab[i][1]
    wcnt=wcnt+1


  print
  print
  print("%d unique words represent 1/2 of the Total number of Words: %d in %s") % (wcnt, halfwordcnt, corpus)
  if (p == 1):
    halftot1.append(wcnt) 
    halftot1.append(halfwordcnt)
    halftot1.append(corpus)
  else:
    halftot2.append(wcnt) 
    halftot2.append(halfwordcnt)
    halftot2.append(corpus)

  print
  print("Frequency Distribution of Top 50 words")
  fd = nltk.FreqDist(allwords)
  fd.plot(50,cumulative=False)

  print
  print("Frequency Distribution of Top 200 words")
  fd = nltk.FreqDist(allwords)
  fd.plot(200,cumulative=False)

  vocab200 = vocab[1:200]
  #display_hist(vocab200, corpus)


# Zipf's Law
  print
  print
  print("Zipf's Law: T1 is the most common term in a collection,")
  print("            T2 is the next most common term in the collection")
  print("            The collection frequency of word cf(i) is proportional to 1/i * cf1")
  print
  print("            The most common term occurs cf1 times")
  print("            The second most common term occurs 1/2 cf1 times")
  print("            The third  most common term occurs 1/3 cf1 times")
  print

 # Update zipfs frequencies 
  for i in range(20):
   if (i == 0):
     zipfs.append(vocab[i][1])
   else:
     temp = int(zipfs[0] / (i+1))
     zipfs.append(temp)

 
  print ("Top 20 most Frequent words")
  print("Observed vrs Expected Word Frequencies")
  print ("Expected Frequencies are based on Zipfs Law")
  print
  print ("Chi Square test statistic calculated: (O-E)^2/E for each term")
  print
  print ("%s\t%s\t%s\t%s\t%s") % (zheadings[0], zheadings[1], zheadings[2], zheadings[3], zheadings[4])
  indx=0
  totChiStat=0
  for i in range(20):
   indx+=1
   teststat = 0
   teststat = (vocab[i][1] - zipfs[i])
   teststat = math.pow(teststat,2)
   teststat = teststat / zipfs[i]
   print("%d\t%s\t%d\t%d\t%.2f") % (indx, vocab[i][0], vocab[i][1], zipfs[i], teststat)
   totChiStat+=teststat


  print 
  print("h0: The observed relative frequency of words in %s follows Zipf's Law") % (corpus)
  print
  print("h1: The observed relative frequency of words in %s does not follow Zipf's Law") % (corpus)
  print
  print("The Test Statistic for 20 words is %.2f") % (totChiStat)
  print("At 19 dof the Chi Square for alpha .005 is 38.582")
  print("The probabiity of seeing a value of %.2f is less than .005") % (totChiStat)
  print
  print("Reject h0 and conclude:")
  print("The observed relative frequency of words in this corpus does not follow Zipf's Law")
  print
  print
  print("If Zipf's law represents the expected frequency of the Distribution of words")
  print("Then by both visual inspection of the top 20 terms and by the ChiSquare test")
  print("this particular corpus: %s") % (corpus)
  print("does not follow Zipf's Law of word Distribution")
  print
  print
  p=p+1
 
 print
 print("Unique words representing 1/2 of the Total number of Words")
 print
 pct1 = halftot1[0]/ halftot1[1]
 pct2 = halftot2[0]/ halftot2[1]
 print ("%s\t%s\t%s\t%s\t%s") % ("Run","Unique","HalfTot","Percent", "Corpus")
 indx = 1
 print("%d\t%d\t%d\t%.5f\t%s") % (indx, halftot1[0], halftot1[1], pct1, halftot1[2])
 indx = 2
 print("%d\t%d\t%d\t%.5f\t%s") % (indx, halftot2[0], halftot2[1], pct2, halftot2[2])
 print
 print
 print("The percentage of Unique Words that account for 1/2 of the total words")
 print("differs dramatically")
 print
 print("This may be related to each Author's style, the topic, the time period")
 print("More test would have to be performed in order to draw conclusions")
 print
 print("Do all books written by a single Author show the same pattern?")
 print
 print("Does a single Author's (unique word percentage of 1/2 total words) differ from book to book")
 print
 print("Are the unique words themselves similar from book to book, are there paterns?")
 

 

 

 
 
 
 