from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect
import json
import mysql.connector
from bd import config  # Assurez-vous d'avoir le bon import ici

app = Flask(__name__)

# Ajouter une route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Charger les données en français et en anglais
def charger_donnees_langue(chemin_fichier, langue_cible):
    donnees = charger_donnees_json(chemin_fichier)

    # Vérifier la structure des données
    for item in donnees:
        if not isinstance(item.get('soustitre', []), list) or not item.get('soustitre',[]):
            message = f"Erreur: Structure incorrecte dans les données pour l'élément {item}."
            return json.dumps({'error': message}), 400, {'Content-Type': 'application/json'}

    sous_titres = [item.get('soustitre', [''])[0] for item in donnees]
    titres = [item['title'] for item in donnees]
    
    return {'titles': titres, 'subtitles': sous_titres}

def charger_donnees_json(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)
    return donnees

# Fonction pour détecter la langue
def detecter_langue(texte):
    try:
        langue = detect(texte)
    except:
        langue = ''
        
    if langue not in ['fr', 'en']:
        langue_manuelle = input(f"Langue détectée : {langue}. Entrez la langue correcte (fr/en) : ").lower()
        if langue_manuelle in ['fr', 'en']:
            langue = langue_manuelle
        else:
            print("Langue non valide. Utilisation de la détection automatique.")
    
    return langue

# Fonction pour rechercher les sous-titres par mots-clés
def rechercher_sous_titres_par_mots_cles(tfidf_vectorizer, tfidf_matrix, titres, sous_titres, top_k=10, keywords=None):
    if not keywords:
        keywords = input("Entrez les mots-clés (séparés par des espaces) : ").split()
    
    if not isinstance(keywords, list):
        keywords = [keywords]
        
    vecteur_mots_cles = tfidf_vectorizer.transform(keywords)
    scores_similarite = cosine_similarity(vecteur_mots_cles, tfidf_matrix)
    
    indices_pertinents = scores_similarite.argsort()[0][::-1][:top_k]
    
    titres_pertinents = [titres[i] for i in indices_pertinents]
    
    return titres_pertinents

# Fonction pour récupérer les images depuis la base de données
def recuperer_images_depuis_bdd(titres_pertinents):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        images_resultats = []

        for titre in titres_pertinents:
            cursor.execute("SELECT image FROM tabserie WHERE nom = %s", (titre,))
            result = cursor.fetchone()

            if result:
                chemin_image = result[0]
                images_resultats.append({'title': titre, 'image': chemin_image})

        print("Résultats récupérés depuis la base de données avec succès")

        return images_resultats

    except Exception as e:
        print(f"Erreur lors de la récupération des résultats depuis la base de données : {str(e)}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Endpoint pour la recherche par mots-clés
@app.route('/search-subtitles', methods=['POST'])
def search_subtitles():
    data = request.form

    language_target = data.get('language', 'fr')
    keywords = data.get('keywords', [])

    if language_target not in ['fr', 'en']:
        response_data = {'error': 'Langue non valide.'}
        return json.dumps(response_data), 400, {'Content-Type': 'application/json'}
        
    if not keywords:
        response_data = {'error': 'Aucun mot-clé fourni.'}
        return json.dumps(response_data), 400, {'Content-Type': 'application/json'}

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

    # Utiliser la fonction recuperer_images_depuis_bdd pour afficher les images des séries correspondant aux titres
    images_results = recuperer_images_depuis_bdd(results)
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

if __name__ == '__main__':
    app.run(debug=True)
