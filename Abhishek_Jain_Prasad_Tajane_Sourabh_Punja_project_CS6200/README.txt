### Dependencies
 - This code is written in python 3.5.2 (Please Install same version)
 - Install beautifulsoup
 - Install pickle
 - Install JAVA 8

TASK 1:

Prerequisites:

a. Tokenizer/Parsing: Run `python tokenizers.py`
b. Indexing: Run `python indexer.py`
c. Indexing stoplist: Run `python indexer_stoplist.py`

1. Lucene 

Run Java code in lib/NewHW4.java

To customise it with different query and runs, change following in the code:

1. corpusPath - Path for the corpus.
2. queryFilePath - Path for the queries directory.
3. queryFileName - Query file name.
4. outFilePath -  Directory where results will be added.
5. outFileName - Filename for the output.

2. BM25

In lib folder:
Run code: python ranking.py

Results in: results/BM25/


### For Stemmed version change below code to:

INVERTED_LIST_FILE = os.path.join("IndexStemmed" + ".pickle")
DOCUMENT_LENGTH = os.path.join("DocLengthStemed" + ".pickle")
DOC_RANK = 'doc_rank_dict_stemmed.txt'
RESULTS_DIRECTORY = "../results/BM25_stemmed/results_"
QUERY_FILE = os.path.join("QueryParsedStemmed" + ".pickle")

Results: results/BM25_stemmed/

### For Stoplist version change:

INVERTED_LIST_FILE = os.path.join("IndexStopped" + ".pickle")
DOCUMENT_LENGTH = os.path.join("DocLengthStopped" + ".pickle")
DOC_RANK = 'doc_rank_dict_stoplist.txt'
RESULTS_DIRECTORY = "../results/BM25_stoplist/results_"
QUERY_FILE = os.path.join("QueryParsedStopped" + ".pickle")

Results: results/BM25_stoplist/

### For Feedback version change:

INVERTED_LIST_FILE = os.path.join("Index" + ".pickle")
DOCUMENT_LENGTH = os.path.join("DocLength" + ".pickle")
DOC_RANK = 'doc_rank_dict.txt'
RESULTS_DIRECTORY = "../results/BM25_feedback/results_"
QUERY_FILE = os.path.join("new_query_dict_2" + ".txt")

Results: results/BM25_feedback/


3. tf-idf

In lib folder:
Run code: python vector_space.py

Results in: results/tf-idf/


PSEUDO RELEVANCE FEEDBACK

1. Pseudo relevance feedback (BM25):
a. Run python ranking.py as initial run (Original run as stated above)
b. Run python psr.py for query expansion
c. Run python ranking.py with Feedback version as stated above.
d. Result in: results/BM25_feedback/

2. Pseudo relevance feedback (Lucene):
a. Run Lucene as mentioned above.
b. run `python psr2.py` for query expansion.
c. Run Lucene as mentioned above again.
d. Results in results/Lucene_feedback


TASK 4:
Evaluation
a. Base Run: 
  1. tf-idf: Run `python evaluation.py tf-idf`
  2. BM25: Run `python evaluation.py BM25`
  3. Lucene: Run `python evaluation.py Lucene`
b. Pseudo Relevance:
  1. BM25: Run `python evaluation.py BM25_feedback`
  2. Lucene: Run `python evaluation.py Lucene_feedback`
c. Stoplist:
  1. BM25: Run `python evaluation.py BM25_stoplist`
  2. Lucene: Run `python evaluation.py Lucene_stoplist`

Bonus:
1. T-test: Run `python t_test.py`
Runs for all the baseline models against improved versions like stopped and feedback.
Output - t-test-scores.txt

2. Snippet and Query highlighting - 
a. Run `python snippet_creation.py`
b. Run `python snippet_results.py`

Snippets for all the queries is inside folder - results/SnippitResults/
Example: results_1.txt  - Snippet for first 10 Ranked docs for query ID 1.
