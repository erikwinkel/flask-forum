from flask import render_template, redirect, request
from models import *
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        return redirect('/')

@app.route('/signin', methods=["GET","POST"])
def sign_in():
    if request.method == "GET":
        return render_template('signin.html')
    elif request.method == "POST":
        return redirect('/')
    