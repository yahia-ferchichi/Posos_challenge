# Setting up the environment
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pickle
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import AllKNN
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import tarfile
import os
import pandas as pd
from stop_words import get_stop_words
import re

docker = "/code/"
#docker = "" #to directly run the script, uncomment this variable

class Model():
    """
    The model containig the preprocessing and the training procedures
    """
    
    def __init__(self, classifier=MultinomialNB()):
        """
        Constractor of the function containing main used functionalities
        if the model
        """
        self.stop = get_stop_words('french')
        self.vectorizer = TfidfVectorizer()
        self.model = classifier
        self.X = []
        self.y = []
        self.filenames = [docker + 'data/input_train.csv', docker + 'data/output_train.csv']
        
    def extract(self):
        """
        Decrypting and extracting data using Pandas
        """
        print("Extracting data...")
        #Decript files
        os.system('gpg --output ' + docker + 'data.tgz --decrypt ' + docker + 'data.tgz.gpg')
        tf = tarfile.open(docker + "data.tgz")
        tf.extractall(docker)
        tf.close()
        # Importing The dataset
        data = pd.read_csv(self.filenames[0])
        output   = pd.read_csv(self.filenames[1])
        final = data.join(output,how = 'left',on = 'ID',rsuffix = 'res').drop(
                'IDres',axis = 1)
        final['question']=final['question'].astype(str)
        return final

    def vectorize(self, final):
        """
        Vectorising Data stored into final dataframe
        """
        print("Vectorzing data...")
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(final['question']).toarray().tolist()
        self.y = final['intention'].tolist()
        # Save TfidfVectorizer
        save_vectorizer = open(docker + "API/personal/pickled_algos/TfidfVectorizer.pickle","wb")
        pickle.dump(self.vectorizer, save_vectorizer)
        save_vectorizer.close()
        
        
    def resample(self):
        """
        Resampling data usinf AllKNN and SMOTE
        """
        print("Sampling data...")
        # Under Sampling
        allknn = AllKNN(sampling_strategy={28:565})
        self.X, self.y = allknn.fit_resample(self.X, self.y)
        #Over Sampling
        smote = SMOTE(ratio="all")
        self.X, self.y = smote.fit_resample(self.X, self.y)
        #save_data = open("data.pickle","wb")
        #pickle.dump((self.X, self.y), save_data)
        #save_data.close()

    def preprocess(self):
        """
        Text Preprocessing
        """
        print("Preprocessing data...")
        def clean_and_stop_words(sen):
            sen = re.sub(r'\W', ' ', str(sen))
            sen = sen.lower()
            sen = re.sub(r'\s+', ' ', sen, flags=re.I)     
            return sen
        final = self.extract()
        final['question'] = final['question'].map(lambda x : clean_and_stop_words(x))
        # print(final['question'].head())
        self.vectorize(final)
        self.resample()
        print("Preprocessing done")

    def train_test(self):
        """
        Train and test the model
        """
        # Training and Test Sets
        train_X, val_X, train_y, val_y = train_test_split(self.X, self.y, random_state=1)
        # Training Text Classification Model
        # Specify Model
        mnb = self.model
        # Fit Model
        print("Training classifier")
        mnb.fit(train_X, train_y)
        print("Training done")
        # Save Model
        save_classifier = open(docker + "API/personal/pickled_algos/MultinomialNB.pickle","wb")
        pickle.dump(mnb, save_classifier)
        save_classifier.close()
        # Load Model
        #open_file = open("MultinomialNB.pickle", "rb")
        #mnb = pickle.load(open_file)
        #open_file.close()
        # Make validation predictions
        print("Testing classifier")
        val_predictions = mnb.predict(val_X)
        # Evaluate Model
        print(str(confusion_matrix(val_y,val_predictions)))
        print(str(classification_report(val_y,val_predictions)))
        print(str(accuracy_score(val_y, val_predictions)))
        print("Testing done")
        
if __name__ == "__main__":
    md = Model()
    md.preprocess()
    md.train_test()