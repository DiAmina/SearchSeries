from flask import Flask, request, jsonify,redirect, url_for, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect
import json
from flask import render_template
import mysql.connector
from bd import config, image_directory
import os
from request import *
from fonctions import *

app = Flask(__name__)
#app.config.from_pyfile('app.config')
#ajouter une route pour la page d'accueil
@app.route('/')
def index():
    #recover_all_series = recuperer_tous_series()
    return redirect(url_for('search_subtitles'))


# Endpoint pour la recherche par mots-clés
@app.route('/search-subtitles', methods=['GET'])
def search_subtitles():
    data = request.args

    language_target = data.get('language', 'fr')
    keywords = data.get('keywords', [])

    if language_target not in ['fr', 'en']:
        response_data = {'error': 'Langue non valide.'}
        return json.dumps(response_data), 400, {'Content-Type': 'application/json'}
        
    if not keywords:
        results = recuperer_tous_series()
        images_results = recuperer_images_depuis_bdd([serie['title'] for serie in results], image_directory)
        return render_template('index.html', results=images_results)

    if language_target == 'fr':
        tfidf_vectorizer = tfidf_vectorizer_francais
        tfidf_matrix = tfidf_matrix_francais
        titres = titres_francais
        sous_titres = sous_titres_francais
    elif language_target == 'en':
        tfidf_vectorizer = tfidf_vectorizer_anglais
        tfidf_matrix = tfidf_matrix_anglais
        titres = titres_anglais
        sous_titres = sous_titres_anglais

    results = rechercher_sous_titres_par_mots_cles(tfidf_vectorizer, tfidf_matrix, titres, sous_titres, keywords=keywords)

    #utiliser la fonction recuperer_images_depuis_bdd pour afficher les images des series correspondant aux titres
    images_results = recuperer_images_depuis_bdd(results, image_directory)
    return render_template('index.html', results=images_results)

# Endpoint pour charger les données de langue
@app.route('/load-language-data/<lang>', methods=['GET'])
def load_language_data(lang):
    if lang not in ['fr', 'en']:
        return jsonify({'error': 'Langue non valide.'}), 400

    if lang == 'fr':
        chemin_fichier = r'C:\Users\Etudiant\Documents\BUT-S5\SAE\seriesVF.json'
    elif lang == 'en':
        chemin_fichier = r'C:\Users\Etudiant\Documents\BUT-S5\SAE\seriesS.json'

    donnees = charger_donnees_langue(chemin_fichier, lang)

    return jsonify(donnees)

@app.route('/see-all', methods=['POST'])
def set_all_series():
    data = request.get_json()
    print(data)
    return jsonify(data)

@app.route('/see-more/<int:id>', methods=['GET'])
def see_more(id):
    print(f"ID  de la serie: {id}")
    result = recuperer_infos_serie(id)
    print(result)
    return render_template('detailsSerie.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
