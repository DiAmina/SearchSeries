<img  style="float: center; " alt="logo barre de recherche" src="./STATIC/images/moteur-de-recherche.png">

# SearchSeries
L'aboutissement du projet est une application web interactive qui permet aux utilisateurs de rechercher des séries TV, d'accéder à des détails approfondis sur chaque série, et de recevoir des recommandations personnalisées.

## Objectif principal 
Notre projet avait pour objectif de créer une application de recherche de séries à partir d'une archive contenant des fichiers de sous-titres en français et en anglais et pouvoir avoir des recommendations. Voici une synthèse des étapes clés et des fonctionnalités de notre projet :

## Étapes du Projet :

### Prétraitement des Données :
- Nettoyages : Retirer tous les caracteres non utile pour la recherche de série, cela passe par ne pas faire de distinction de saison, épisode, enlever les stops-words
- Archivage : Rassembler plusieurs fichiers de sous-titres en français en un fichier json et un autre pour l'anglais en json aussi.
- Chargement des Données : Mettre en forme les données extraites de manière à ce qu'elles puissent être utilisées efficacement
  - Dans le but d'obtenir les données brutes à partir de l'archive, à les explorer, à extraire les informations pertinentes et à les prétraiter pour les préparer à être utilisées dans votre application.

### Analyse des Sous-Titres :

- Langue Automatique : Utiliser la détection automatique de la langue pour déterminer si les sous-titres sont en français ou en anglais.
- Vectorisation TF-IDF : Appliquer la vectorisation TF-IDF pour représenter les sous-titres sous forme de vecteurs numériques.

### Développement de l'Application :

- Flask : Utiliser le framework Flask pour créer une application web.
- Recherche par Mots-Clés : Mettre en place une fonctionnalité de recherche permettant aux utilisateurs de saisir des mots-clés.
- Affichage des Résultats : Afficher les résultats de la recherche sous forme d'images de séries, triées par pertinence.
- Base de Données : Stocker les détails des séries, y compris les images, dans une base de données MySQL.
- Affichage de Détails : Permettre aux utilisateurs de voir plus de détails sur une série spécifique, y compris le synopsis.

### Gestion des Erreurs :

- Validation de Langue : Gérer les cas où la langue n'est pas correctement détectée.

#### Etudiants non-alternants
- Lisa DUVALLET
- Amina MADI
