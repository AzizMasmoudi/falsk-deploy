# wsgi.py

import sys
import os

# Ajouter le dossier du projet au path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Option 1: Importation directe
from app.api.app_dynamic import app

# Alternative (Option 2): Création d'une nouvelle instance Flask
# from flask import Flask
# app = Flask(__name__)
# 
# @app.route('/predict', methods=['POST'])
# def predict_wrapper():
#     from app.api.app_dynamic import predict
#     return predict()

if __name__ == "__main__":
    app.run()
