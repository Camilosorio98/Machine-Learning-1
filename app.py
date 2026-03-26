from flask import Flask, render_template
import LinearRegression
app = Flask(_name_)

@app.route('/')
def home():
return render_template('index.html')

@app.route('/linearRegression')
def  calculateGrade();
    return = LinearRegression.calculateGrade(10)
return str (result) 