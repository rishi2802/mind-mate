
from flask import Flask, render_template,request,jsonify
from pymongo import MongoClient
import nltk 
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')



nltk.download('punkt') 
#nltk.download('averaged_perceptron_tagger') 

# Set paths 

path_to_csv = 'mentalhealth.csv'
import pandas as pd
import nltk 
import numpy as np
import re

from nltk.stem import wordnet                                  # to perform lemmitization
from sklearn.feature_extraction.text import CountVectorizer    # to perform bow
from sklearn.feature_extraction.text import TfidfVectorizer    # to perform tfidf
from nltk import pos_tag                                       # for parts of speech
from sklearn.metrics import pairwise_distances                 # to perfrom cosine similarity
from nltk import word_tokenize                                 # to create tokens
from nltk.corpus import stopwords   
df = pd.read_csv(path_to_csv, nrows = 20)
df.head()
df.isnull().sum()
s = 'tell me about your personality'
words = word_tokenize(s)                    # tokenize words

#nltk.download('wordnet') 
#nltk.download('omw-1.4')
                   # uncomment if running the cell for the first time
lemma = wordnet.WordNetLemmatizer()         
lemma.lemmatize('absorbed', pos = 'v') 
pos_tag(nltk.word_tokenize(s),tagset = None)
nltk.download('stopwords')            # uncomment if running the cell for the first time

stop = stopwords.words('english')
def text_normalization(text):
    text = str(text).lower()                        # text to lower case
    spl_char_text = re.sub(r'[^ a-z]','',text)      # removing special characters
    tokens = nltk.word_tokenize(spl_char_text)      # word tokenizing
    lema = wordnet.WordNetLemmatizer()              # intializing lemmatization
    tags_list = pos_tag(tokens,tagset=None)         # parts of speech
    lema_words = []                                 # empty list 
    for token,pos_token in tags_list:               # lemmatize according to POS
        if pos_token.startswith('V'):               # Verb
            pos_val = 'v'
        elif pos_token.startswith('J'):             # Adjective
            pos_val = 'a'
        elif pos_token.startswith('R'):             # Adverb
            pos_val = 'r'
        else:
            pos_val = 'n'                           # Noun
        lema_token = lema.lemmatize(token,pos_val)

        if lema_token in stop: 
          lema_words.append(lema_token)             # appending the lemmatized token into a list
    
    return " ".join(lema_words) 
text_normalization('telling you some stuffs about me')  # example
df['lemmatized_text'] = df['Questions'].apply(text_normalization)   # clean text
df.head(5)
cv = CountVectorizer()                                  # intializing the count vectorizer
X = cv.fit_transform(df['lemmatized_text']).toarray()
# returns all the unique word from data 

#features = cv.get_feature_names()
features = cv.get_feature_names()
df_bow = pd.DataFrame(X, columns = features)
df_bow.head()
Question = 'What treatment options are available'                           # example
Question_lemma = text_normalization(Question)                               # clean text
Question_bow = cv.transform([Question_lemma]).toarray()                     # applying bow
# cosine similarity for the above question we considered.

cosine_value = 1- pairwise_distances(df_bow, Question_bow, metric = 'cosine' )
(cosine_value)
df['similarity_bow'] = cosine_value                                         # create cosine value as a new column
simiscores = pd.DataFrame(df, columns=['Answers','similarity_bow'])         # taking similarity value of responses for the question we took
simscoresDescending = simiscores.sort_values(by = 'similarity_bow', ascending=False)          # sorting the values
simscoresDescending.head()
threshold = 0.1                                                                       # considering the value of smiliarity to be greater than 0.1
df_threshold = simscoresDescending[simscoresDescending['similarity_bow'] > threshold] 
df_threshold
index_value = cosine_value.argmax()         # index number of highest value
index_value
df['Answers'].loc[index_value]              # The text at the above index becomes the response for the question
Question1 = 'What treatment options are available'


tfidf = TfidfVectorizer()                                             # intializing tf-id 
x_tfidf = tfidf.fit_transform(df['lemmatized_text']).toarray()        # transforming the data into array
Question_lemma1 = text_normalization(Question1)
Question_tfidf = tfidf.transform([Question_lemma1]).toarray()         # applying tf-idf
# returns all the unique word from data with a score of that word
#df_tfidf = pd.DataFrame(x_tfidf, columns=tfidf.get_feature_names())
df_tfidf = pd.DataFrame(x_tfidf, columns=tfidf.get_feature_names())


df_tfidf.head()
cos = 1-pairwise_distances(df_tfidf,Question_tfidf,metric='cosine')                     # applying cosine similarity
cos
df['similarity_tfidf'] = cos                                                    # creating a new column 
df_simi_tfidf = pd.DataFrame(df, columns=['Answers','similarity_tfidf'])        # taking similarity value of responses for the question we took
df_simi_tfidf
df_simi_tfidf_sort = df_simi_tfidf.sort_values(by='similarity_tfidf', ascending=False)            # sorting the values
df_simi_tfidf_sort.head(10)
threshold = 0.1                                                                       # considering the value of smiliarity to be greater than 0.1
df_threshold = df_simi_tfidf_sort[df_simi_tfidf_sort['similarity_tfidf'] > threshold] 
df_threshold
index_value1 = cos.argmax()                                                   # returns the index number of highest value
index_value1
df['Answers'].loc[index_value1]                                               # returns the text at that index
def chat_bow(text):
    lemma = text_normalization(text) # calling the function to perform text normalization
    bow = cv.transform([lemma]).toarray() # applying bow
    cosine_value = 1- pairwise_distances(df_bow,bow, metric = 'cosine' )
    index_value = cosine_value.argmax() # getting index value 
    return df['Answers'].loc[index_value]

def chat_tfidf(text):
    lemma = text_normalization(text) # calling the function to perform text normalization
    tf = tfidf.transform([lemma]).toarray() # applying tf-idf
    cos = 1-pairwise_distances(df_tfidf,tf,metric='cosine') # applying cosine similarity
    index_value = cos.argmax() # getting index value 
    return df['Answers'].loc[index_value]


app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['Mind']  # Change 'your_database_name' to your desired database name
collection = db['patient']  # Change 'your_collection_name' to your desired collection name
collection.insert_one({"email": "abc@gmail.com", "password": 1234, "age": 20, "gender": "male"})

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/signup.html')
def signren():
    return render_template("signup.html")
@app.route('/loginpg' ,methods=['POST'])
def login():
    return render_template("login.html")
@app.route('/login.html')
def logren():
    return render_template("login.html")
@app.route('/userip', methods=['GET', 'POST'])
def userip():
    if request.method == 'POST':
        data = request.get_json()
        print("INNNNN")
        return jsonify(chat_tfidf(data))
    else:
        # Handle GET requests here, if needed
        # For example, return some informative message
        return jsonify({'message': 'GET method not supported for this endpoint'})
@app.route('/careip', methods=['POST'])
def careip():
    data = request.get_json()
    return jsonify(chat_tfidf(data))

@app.route('/signsub', methods=['POST'])
def signsub():
    email = request.form['email']
    password = request.form['password']
    age = int(request.form['Age'])
    gender = request.form['Gender']

    # Check if email already exists in the collection
    if collection.find_one({"email": email}):
        return render_template('signup.html',text="Account exists for this Email")
    else:
        # Insert new record into the collection
        collection.insert_one({"email": email, "password": password, "age": age, "gender": gender})
        return render_template('index.html')
@app.route('/logout', methods=['POST'])
def logout():
    return render_template('index.html')
@app.route('/templates/logsub', methods=['POST'])
def logsub():
    email = request.form['email']
    password = request.form['password']
    if(email=='caretaker@gmail.com'):
        return render_template('caretaker.html')
    # Check if email and password combination exists in the collection
    user = collection.find_one({"email": email, "password": password})
    if user:
        return render_template('patientchat.html')  # Redirect to success page or any other page
    else:
        return render_template('patientchat.html', text="Invalid email or password")

if __name__ == '__main__':
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

