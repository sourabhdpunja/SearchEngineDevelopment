from bs4 import BeautifulSoup
import os
import re
import string
import random

class Tokenize(object):

  DIRECTORY_FOR_DOCUMENTS = "../cacm/"

  def __init__(self):
    self.files = os.listdir(Tokenize.DIRECTORY_FOR_DOCUMENTS)
    self.created_files = []


  def process(self):
    self.create_directory()
    for filename in self.files:
      extension = os.path.splitext(filename)[1]
      if extension == ".html":
        link_to = filename.split(".")[0]
        f = open(Tokenize.DIRECTORY_FOR_DOCUMENTS + filename)
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')



        text = soup.get_text()

        text = re.sub(r"^\d+\t\d+\t\d+$", " ", text, flags=re.M)

        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = "\n".join(chunk for chunk in chunks if chunk)

        text = self.parse_text(text.encode('utf-8'))


        new_filename = self.parse_filename(link_to)

        if new_filename in self.created_files:
          new_filename = new_filename + str(random.randint(0, 100))

        self.created_files.append(new_filename)

        f = open("tokenized/" + new_filename + ".txt", "w+")
        f.write(text)

  def create_directory(self):
    directory = "tokenized"
    try:
      os.stat(directory)
    except:
      os.mkdir(directory)

  def parse_text(self, text):
    words = []
    for word in text.split():
      if not self.hasNumbers(word):
        for c in string.punctuation.replace("-", ""):
          word = word.replace(c, " ")
      words.append(word.lower())

    return " ".join(words)

  def hasNumbers(self, inputString):
    return bool(re.search(r'\d', inputString))


  def parse_filename(self, file_key):
    return file_key

t = Tokenize()
t.process()
