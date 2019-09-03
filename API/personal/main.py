'''
Python backend main program to return probability
to attend a destination from a given source  in a graph
in a given number of iterations.
'''
import pickle
import re


def preprocess(sentence):
    sentence = sentence.encode('utf -8').decode()
    # Remove all the special characters
    sentence = re.sub(r'\W', ' ', str(sentence))
    # remove all single characters
    sentence = re.sub(r'\s+[a-zA-Z]\s+', ' ', sentence)
    # Remove single characters from the start
    sentence = re.sub(r'\^[a-zA-Z]\s+', ' ', sentence) 
    # Substituting multiple spaces with single space
    sentence = re.sub(r'\s+', ' ', sentence, flags=re.I)
    # Removing prefixed 'b'
    sentence = re.sub(r'^b\s+', '', sentence)
    # Converting to Lowercase
    sentence = sentence.lower()
    # Converting Text to Numbers
    open_vectorizer = open("/code/API/personal/pickled_algos/TfidfVectorizer.pickle","rb")
    vectorizer = pickle.load(open_vectorizer)
    open_vectorizer.close()
    sentence = vectorizer.transform([sentence])
    sentence = sentence.toarray().tolist()
    return sentence
    
def predict(sentence):
    # Load Model
    open_file = open("/code/API/personal/pickled_algos/MultinomialNB.pickle", "rb")
    mnb = pickle.load(open_file)
    open_file.close()
    sentence = preprocess(sentence)
    return mnb.predict(sentence)[0], max(mnb.predict_proba(sentence).tolist()[0])


def main(sentence):
    return predict(sentence)

