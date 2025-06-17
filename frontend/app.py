from flask import Flask, request, render_template
from datetime import datetime
import requests

BACKEND_URL = "http://127.0.0.1:8000"

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Application!"

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/contact/<name>')
def contact(name):
    return f"This is the contact {name}."

@app.route('/api/<a>/<b>')
def api(a, b):
    try:
        a = int(a)
        b = int(b)
        return f"The sum of {a} and {b} is {a + b}."
    except ValueError:
        return "Please provide valid integers."

@app.route('/post')
def post_example():
    name = request.values.get('name')
    age = request.values.get('age')
    if name and age:
        return f"Received name: {name} and age: {age}."
    else:
        return "Please provide both name and age."

@app.route('/html')
def html_example():
    day_of_week = datetime.now().strftime('%A')
    return render_template('index.html', day_of_week=day_of_week)

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)
    requests.post(BACKEND_URL + '/submit', data=form_data)
    return "Form submitted successfully!"

@app.route('/api')
def get_data():
    response = requests.get(BACKEND_URL + '/api')
    data = response.json().get('data', [])
    return {"data": data}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000",debug=True)