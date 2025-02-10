# fazer todas as configuracoes aqui, inclusive a instancia do flet
from flask import Flask, render_template, request, jsonify, send_from_directory
from .services import *
import os
from datetime import datetime
import unicodedata



app = Flask(__name__)