
from flask import Flask, render_template,request,jsonify
from pymongo import MongoClient

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
        print("INNNNN")
        return jsonify('message HIII')
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

