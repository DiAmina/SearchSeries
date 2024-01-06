from bd import config, image_directory
import mysql.connector

def identification(username, password):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authentification WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            return True
        else:
            return False

    except Exception as e:
        print(f"Erreur lors de la récupération des résultats depuis la base de données : {str(e)}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


#afficher les images des series via la base de données
def recuperer_images_depuis_bdd(titres_pertinents,image_bdd):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        images_resultats = []

        for titre in titres_pertinents:
            cursor.execute("SELECT image,id FROM tabserie WHERE title = %s", (titre,))
            result = cursor.fetchone()

            if result:
                nom_image = result[0]
            
                chemin_images = "/".join([image_bdd, nom_image])
                images_resultats.append({'title': titre, 'image': chemin_images})

        print("Résultats récupérés depuis la base de données avec succès")

        return images_resultats

    except Exception as e:
        print(f"Erreur lors de la récupération des résultats depuis la base de données : {str(e)}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
#function qui recupere l'id s'une sie apres un click sur une image et revoie les informations de la serie
def recuperer_infos_serie(id):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, synopsis, image FROM tabserie WHERE id = %s", (id,))
        result = cursor.fetchone()

        if result:
            return {'id': result[0],
                    'title': result[1],
                    'synopsis': result[2],
                    'image': "/".join([image_directory, result[3]]),
                    }
        else:
            return {}

    except Exception as e:
        print(f"Erreur lors de la récupération des résultats depuis la base de données : {str(e)}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    
def recuperer_tous_series():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, image FROM tabserie")
        result = cursor.fetchall()

        if result:
            series = [{'id': item[0], 'title': item[1], 'image': "/".join([image_directory, item[2]])} for item in result]
            return series
        else:
            return []

    except Exception as e:
        print(f"Erreur lors de la récupération des résultats depuis la base de données : {str(e)}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
