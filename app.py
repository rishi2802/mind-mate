
from flask import Flask, render_template,request,jsonify
from pymongo import MongoClient
import json
import string
import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
#nltk.download("punkt")
#nltk.download("wordnet")
data_file= open('RESPONSES.json').read()
data= json.loads(data_file)
words= []
classes =[]
data_X=[]
data_Y=[]
for intent in data["intents"]:
  for pattern in intent["patterns"]:
    tokens=nltk.word_tokenize(pattern)
    words.extend(tokens)
    data_X.append(pattern)
    data_Y.append(intent["tag"])
  if intent["tag"] not in classes:
    classes.append(intent["tag"])
lemmatizer=WordNetLemmatizer()
words=[lemmatizer.lemmatize(word.lower())for word in words if word not in string.punctuation]
words=sorted(set(words))
classes=sorted(set(classes))
training=[]
out_empty=[0]*len(classes)
for idx,doc in enumerate(data_X):
  bow=[]
  text=lemmatizer.lemmatize(doc.lower())
  for word in words:
    bow.append(1) if word in text else bow.append(0)
  output_row=list(out_empty)
  output_row[classes.index(data_Y[idx])]=1
  training.append([bow,output_row])
random.shuffle(training)
training=np.array(training, dtype=object)
train_X=np.array(list(training[:,0]))
train_Y=np.array(list(training[:,1]))
model=Sequential()
model.add(Dense(128,input_shape=(len(train_X[0]),),activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_Y[0]),activation="softmax"))
from tensorflow.keras.optimizers import Adam

adam = Adam(learning_rate=0.0001, decay=1e-6)
model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=["accuracy"])

model.fit(x=train_X,y=train_Y,epochs=1000,batch_size=32,verbose=1)
def clean_text(text):
  tokens=nltk.word_tokenize(text)
  tokens=[lemmatizer.lemmatize(word)for word in tokens]
  return tokens
def bag_of_words(text,vocab):
  tokens=clean_text(text)
  bow=[0]*len(vocab)
  for w in tokens:
    for idx,word in enumerate(vocab):
      if word==w:
        bow[idx]=1
  return np.array(bow)
def pred_class(text,vocab,labels):
  bow=bag_of_words(text,vocab)
  result=model.predict(np.array([bow]))[0]
  thresh=0.5
  y_pred=[[indx,res] for indx, res in enumerate(result) if res>thresh]
  y_pred.sort(key=lambda x:x[1], reverse=True)
  return_list=[]
  for r in y_pred:
    return_list.append(labels[r[0]])
  return return_list
def get_response(intents_list,intents_json):
  if len(intents_list)== 0:
    result= "Sorry! I don't understand"
  else:
    tag=intents_list[0]
    list_of_intents=intents_json["intents"]
    for i in list_of_intents:
      if i["tag"]==tag:
        result=random.choice(i["responses"])
        break
  return result


print("press 0 to quit")
while True:
  message=input("")
  if message=="0":
    break
  intents=pred_class(message,words,classes)
  result= get_response(intents,data)
  print(result)
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['Mindmate']  # Change 'your_database_name' to your desired database name
collection = db['Log']  # Change 'your_collection_name' to your desired collection name


@app.route('/')
def hello():
    return render_template("patientchat.html")

@app.route('/signup.html')
def signren():
    return render_template("signup.html")
@app.route('/login.html')
def logren():
    return render_template("login.html")
@app.route('/userip', methods=['GET', 'POST'])
def userip():
    if request.method == 'POST':
        data = request.get_json()
        intents = pred_class(data, words, classes)
        result = get_response(intents, data)
        return jsonify(result)
    else:
        # Handle GET requests here, if needed
        # For example, return some informative message
        return jsonify({'message': 'GET method not supported for this endpoint'})

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
@app.route('/logsub', methods=['POST'])
def logsub():
    email = request.form['email']
    password = request.form['password']

    # Check if email and password combination exists in the collection
    user = collection.find_one({"email": email, "password": password})
    if user:
        return render_template('index.html', email=email)  # Redirect to success page or any other page
    else:
        return render_template('login.html', text="Invalid email or password")

if __name__ == '__main__':
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

