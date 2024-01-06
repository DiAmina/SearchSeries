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


def charger_donnees_json(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)
    return donnees

def charger_donnees_langue(chemin_fichier, langue_cible):
    donnees = charger_donnees_json(chemin_fichier)

    # Vérifier la structure des données
    for item in donnees:
        if not isinstance(item.get('soustitre', []), list) or not item.get('soustitre',[]):
            message = f"Erreur: Structure incorrecte dans les données pour l'élément {item}."
            return json.dumps({'error': message}), 400, {'Content-Type': 'application/json'}

    sous_titres = [item.get('soustitre', [''])[0] for item in donnees]
    titres = [item['title'] for item in donnees]
    ids = [item['id'] for item in donnees]
    
    return json.dumps({'titles': titres, 'subtitles': sous_titres, 'id':ids}), 200, {'Content-Type': 'application/json'}

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


def rechercher_sous_titres_par_mots_cles(tfidf_vectorizer, tfidf_matrix, titres, sous_titres, keywords=None):
    if not keywords:
        keywords = input("Entrez les mots-clés (séparés par des espaces) : ").split()
    
    if not isinstance(keywords, list):
        keywords = [keywords]
        
    vecteur_mots_cles = tfidf_vectorizer.transform(keywords)
    scores_similarite = cosine_similarity(vecteur_mots_cles, tfidf_matrix)
    
    indices_pertinents = scores_similarite.argsort()[0][::-1]
    
    titres_pertinents = [titres[i] for i in indices_pertinents]
    
    return titres_pertinents


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


# Chemins des fichiers JSON
chemin_fichier_francais = r'C:\Users\Etudiant\Documents\BUT-S5\SAE\seriesVF.json'
chemin_fichier_anglais = r'C:\Users\Etudiant\Documents\BUT-S5\SAE\seriesS.json'

# Charger les données en français et en anglais
donnees_francais = charger_donnees_langue(chemin_fichier_francais, 'fr')
donnees_anglais = charger_donnees_langue(chemin_fichier_anglais, 'en')

# Accéder aux sous-titres en français et en anglais
sous_titres_francais = donnees_francais['subtitles']
sous_titres_anglais = donnees_anglais['subtitles']

# Accéder aux titres en français et en anglais
titres_francais = donnees_francais['titles']
titres_anglais = donnees_anglais['titles']

# Vectorisation TF-IDF pour le français
tfidf_vectorizer_francais = TfidfVectorizer()
tfidf_matrix_francais = tfidf_vectorizer_francais.fit_transform(sous_titres_francais)

# Vectorisation TF-IDF pour l'anglais
tfidf_vectorizer_anglais = TfidfVectorizer()
tfidf_matrix_anglais = tfidf_vectorizer_anglais.fit_transform(sous_titres_anglais)
