from flask import Flask, render_template, send_from_directory, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    subprocess.Popen(['python3', 'combine19.py'])
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

