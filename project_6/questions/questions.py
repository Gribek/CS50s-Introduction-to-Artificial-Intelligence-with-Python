import os
import math
import nltk
import string
import sys

FILE_MATCHES = 4
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files_dict = {}
    files = os.listdir(directory)
    for file in files:
        with open(os.path.join(directory, file)) as f:
            files_dict[file] = f.read()
    return files_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(text=document)
    stopwords = nltk.corpus.stopwords.words('english')
    x = [word.lower() for word in words if
         word not in string.punctuation and word not in stopwords]
    return x


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words_set = set(word for words in documents.values() for word in words)
    number_of_documents = len(documents)
    idf_dict = {}
    for word in words_set:
        occurrence = 0
        for document in documents:
            if word in documents[document]:
                occurrence += 1
        idf_dict[word] = math.log(number_of_documents / occurrence)
    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf = {file: 0 for file in files}
    for word in query:
        if word not in idfs:
            continue
        for file, words in files.items():
            tf_idf[file] += words.count(word) * idfs[word]
    return sorted(files, key=lambda f: tf_idf[f], reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf = {sentence: 0 for sentence in sentences}
    for word in query:
        if word not in idfs:
            continue
        for sentence, words in sentences.items():
            if word not in words:
                continue
            idf[sentence] += idfs[word]
    return sorted(sentences,
                  key=lambda s: (idf[s], calc_qtr(query, sentences[s])),
                  reverse=True)[:n]


def calc_qtr(query, sentence):
    """
    Given a query and a sentence calculate query term density.
    """
    return len([word for word in sentence if word in query]) / len(sentence)


if __name__ == "__main__":
    main()
