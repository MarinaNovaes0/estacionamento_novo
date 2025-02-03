from flask import Flask

app = Flask(__name__, static_folder='../src/static', template_folder='../src/templates')
app.secret_key = "projeto123"
