from app import app
from flask import Flask, render_template, jsonify, request


@app.route('/')
@app.route('/index')
def index():
    return render_template('homepage.html')
