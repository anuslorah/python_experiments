import sys
import logging
import os
import string
import re
import time


def main():
  # start timing
  t0 = time.time()

  # metrics setup
  metrics = {
  "total execution time": 0,
  "read mode: average readline time": 0,
  "read mode: average find word time": 0,
  "write mode: average write sentence time": 0,
  "sentenceCount": 0,
  "write mode: average find word time": 0 
  }

  # add logging
  logger = myLog('pythonReader', trace)
  
  # word program searches for
  word = "imperdiet"
  word = word.casefold()
  logger.debug(" searching for word {}".format(word))

  # intro
  print("This program will read a file to count occurrences of the word {}".format(word))
  print("in file and the number of lines that include given word.")
  print("You have the option to either upload your file or to create a file.")
  i = getInput("To create file type c, to upload type u: ")
  logger.debug(" user chose: " + i)

  # create a new file
  if i == 'c':
    metrics = writeMyFile(word, logger, metrics)
  # read a file
  else:
    metrics = readMyFile(word, logger, metrics)

  # end timing
  t1 = time.time()
  logger.trace(" time elapsed since starting the program: {}".format((t1-t0)))

  # offer user metrics
  ii = input("\nDo you want to see the metrics? Type y for yes, n for no: ").casefold()
  if ii == 'y':
    metrics["total execution time"] = t1-t0
    print('\nTotal execution time for program: ','%.7f'%metrics.get("total execution time"))
    if i == 'u':
      print('Average time to read a line: ','%.7f'%metrics.get("read mode: average readline time"))
      print('Average time to find word: ','%.7f'%metrics.get("read mode: average find word time"))
    else:
      print('Average time to write a sentence: ','%.7f'%metrics.get("write mode: average write sentence time"))
      print('Average time to find word: ','%.7f'%metrics.get("write mode: average find word time"))

# functions
# logging setup with added level (trace)
def myLog(programName, trace):
  # logging setup
  logging.basicConfig()
  logger = logging.getLogger(programName)
  # write logs to log file
  handler = logging.FileHandler('./' + programName + '.log')
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  # add TRACE to logging
  logging.addLevelName(5, 'TRACE')
  logging.Logger.trace = trace
  logger.setLevel(5)
  
  return logger

#add trace to logging
def trace(TRACE, message, *args, **kws):
  TRACE.log(5, message, *args, **kws)

# input prompt
def getInput(prompt):
  value = input(prompt)
  while not (value == 'u' or value == 'c'):
    print("This is not a valid choice")
    value = input("Please enter either c for create or u for upload: ")
  return value

# read file, count occurrences of word in file, count lines containing word
def readMyFile(word, logger, metrics):
  filepath = input("Please enter your file path: ")
  while not os.path.isfile(filepath):
    logger.error(" filepath " + filepath + " does not exist")
    print("File path {} does not exist. ".format(filepath))
    filepath = input("Please enter your file path: ")

  try:
    with open(filepath, encoding='utf8') as fp:
      if fp.mode == 'r':
        lineCount = 0
        wordCount = 0
        # timers
        t_line_start = 0
        t_line_end = 0
        t_line_total = 0
        t_word_start = 0
        t_word_end = 0
        t_word_total = 0
        for line in fp:
          t_line_start = time.time()
          line = re.split(r'\W+', line.casefold())
          if word in line:
            lineCount += 1
            t_word_start = time.time()
            for i in line:
              if i == word:
                wordCount += 1
                # print(line)
                t_word_end = time.time()
                t_word_total+=(t_word_end-t_word_start)
          t_line_end = time.time()
          t_line_total+=(t_line_end-t_line_start)

        logger.trace(" lines read: " + str(lineCount))
        logger.trace(" read mode: average read line time " + str(t_line_total/lineCount))
        logger.trace(" found "+ str(wordCount) + " instances of " + word)
        logger.trace(" read mode: average find " + word +" time " + str(t_word_total/wordCount))
        metrics["read mode: average find word time"] = t_word_total/wordCount
        metrics["read mode: average readline time"] = t_line_total/lineCount

        print("\nThere are {} lines that contain {}".format(lineCount, word))
        print("and {} occurrences of {} in the file {}\n".format(wordCount, word, filepath))

  except IOError:
    print("You don't have permissions to read this file. Exiting program.")
    logger.critical(" User tried to read " + filepath + " with no R permission")
    sys.exit(0)
  return metrics

# ask user sentences
def askForSentence(addFile, metrics, logger):    
  start = time.time()
  over = input("Enter the sentences for your file. When you are done, press 'enter' to proceed to next step:\n")
  sentenceCount = 0
  while len(over) > 0:
    addFile.write(over + ' ')
    sentenceCount += 1
    over = input("Next sentence:\n")
  elapsed = (time.time() - start)
  logger.trace(" user entered {} sentences".format(sentenceCount))
  if(sentenceCount > 0):
    logger.trace(" average time to write a sentence " + str(elapsed/sentenceCount))
    metrics["write mode: average write sentence time"] = elapsed/sentenceCount
  
  metrics["sentenceCount"] = sentenceCount
  return metrics

# create file, write to it, count occurrences of word in file, return metrics
def writeMyFile(word, logger, metrics):
  # open file, permission write, + denotes new file
  addFile = open("myFile.txt", "w+")
  # truncate file if it already exists
  #addfile.truncate(0)
  logger.debug(" created file myFile.txt")
  wordCount = 0
  metrics = askForSentence(addFile, metrics, logger)
  addFile.close()
  with open("myFile.txt", "r") as file:
    content = file.read()
    # separate punctuation from words, casefold for case-insensitive comparison
    words = re.split(r'\W+', content.casefold())
    #print(words)
    t0 = 0
    t1 = 0
    t = 0
    for w in words:
      t0 = time.time()
      if(w == word):
        wordCount = wordCount + 1
        t1 = time.time()
        t+=(t1-t0)

    if(wordCount > 0):
      logger.trace(" write mode: average find " + word + " time " + str(t/wordCount))
      metrics["write mode: average find word time"] = t/wordCount
    else:
      logger.trace(" write mode: no occurrences of " + word + " found")
      metrics[" write mode: average find word time"] = "no words found"

    print("\nThere are {} sentences in the file,".format(metrics.get("sentenceCount")))
    print("and {} occurrences of {} in the file".format(wordCount, word))

  return metrics

if __name__ == '__main__':
  main()