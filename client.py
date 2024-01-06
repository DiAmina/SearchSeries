import requests
import json

# URL de l'endpoint de recherche de sous-titres
url = "http://127.0.0.1:5000/search-subtitles"

# Langue spécifiée par l'utilisateur
langue_cible = input("Entrez la langue cible (fr/en) : ").lower()

# Mots-clés spécifiés par l'utilisateur (séparés par un espace)
mots_cles = input("Entrez les mots-clés (séparés par des espaces) : ")

# Données JSON à inclure dans la requête POST
data = {
    "language": langue_cible,
    "keywords": mots_cles.split()  # Divisez la chaîne en une liste de mots-clés
}

# Envoi de la requête POST avec l'en-tête Content-Type
headers = json.dumps({'Content-Type': 'application/json'})
response = requests.post(url, json=data, headers=headers)

# Affichage de la réponse
print(response.status_code)
print(response.json())
