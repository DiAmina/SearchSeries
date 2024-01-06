import os
import mysql.connector

# Paramètres de connexion à la base de données
host = 'localhost'
user = 'amdjad'
password = '9dfe351b'
database = 'serie_net'

# Connexion à la base de données
conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = conn.cursor()

# Sélection de toutes les données de la table 'série'
select_query = "SELECT ID, name, etoiles, synopsis, poster FROM serie"
cursor.execute(select_query)
series_data = cursor.fetchall()

# Parcours des données et mise à jour de la colonne 'poster'
for serie in series_data:
    serie_id, name, etoiles, synopsis, poster = serie
    poster_filename = f"{serie_id}.jpg"

    # Vérification si le fichier image existe
    if os.path.exists(poster_filename):
        update_query = f"UPDATE serie SET poster = '{poster_filename}' WHERE ID = {serie_id}"
        cursor.execute(update_query)
        conn.commit()

# Fermeture de la connexion à la base de données
cursor.close()
conn.close()
