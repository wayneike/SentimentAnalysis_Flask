import re
import nltk
from joblib import load
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer

# Defining stopwords from pre-loaded dictionary
stop_words = stopwords.words('english')

# Removing "not" from the stopwords list as it conveys negative sentiment value
stop_words.remove('not')

# Lemmatization distills words to their foundational forms
lemmatizer = WordNetLemmatizer()

# ... from https://colab.research.google.com/drive/1yR2WBjPuzgzTgir9H6QAi20c6ALZlLEZ?usp=sharing
model = load("pkl/model.joblib")
vectorizer = load("pkl/vectorizer.joblib")

def data_preprocessing(review):

  # Remove HTML tags and numbers
  review = re.sub(re.compile('<.*?>'), '', review)
  review =  re.sub('[^A-Za-z0-9]+', ' ', review)

  # Lowercase
  review = review.lower()

  # Tokenization
  tokens = nltk.word_tokenize(review)

  # Stopword removal
  review = [word for word in tokens if word not in stop_words]

  # Lemmatization
  review = [lemmatizer.lemmatize(word) for word in review]

  review = ' '.join(review)

  return review

def predict(review):   
    # Preprocess the input features   
    preprocessedReview = data_preprocessing(review)
    input_tfidf = vectorizer.transform([preprocessedReview])

    # Make predictions using the loaded model
    prediction = model.predict(input_tfidf)

    return prediction[0]
