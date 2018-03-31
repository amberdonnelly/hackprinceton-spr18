import nltk
from nltk.stem.lancaster import LancasterStemmer
from Indexer_v2 import *

stemmer = LancasterStemmer()

training_data = []

# read training data
content = []
indexer = Indexer()

content = indexer.indexText("Articles/LeftBias/CNN1.txt")
for next in content:
    training_data.append({"class":"left", "sentence":next})

content = indexer.indexText("Articles/RightBias/RedState1.txt")
for next in content:
    training_data.append({"class":"right", "sentence":next})

# with open("Articles/CenterBias.txt") as f:
#     content = f.read().split(",")
# for next in content:
#     training_data.append({"class":"center", "sentence":next})

# with open("Articles/RightCenterBias.txt") as f:
#     content = f.read().split(",")
# for next in content:
#     training_data.append({"class":"rightcenter", "sentence":next})

# with open("Articles/RightBias.txt") as f:
#     content = f.read().split(",")
# for next in content:
#     training_data.append({"class":"right", "sentence":next})

print ("%s sentences of training data" % len(training_data))
print("\n")

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
print ("Class words: %s" % class_words)
print("\n")

# calculate a score for a given class taking into account word commonality
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

# # return the class with highest score for sentence
# def classify(sentence):
#     high_class = None
#     high_score = 0
#     # loop through our classes
#     for c in class_words.keys():
#         # calculate score of sentence for each class
#         score = calculate_class_score(sentence, c, show_details=False)
#         # keep track of highest score
#         if score > high_score:
#             high_class = c
#             high_score = score

#     return high_class, high_score

scores = []

def get_all_scores(sentence):
    # loop through classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score(sentence, c, show_details=False)
        scores.append(score)
    return scores

print(get_all_scores("this is the end of the world"))  