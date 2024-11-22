import os
import PyPDF2
import re
import requests
import sys

import requests

def download_pdf(drive_url):

    output_file = "./file.pdf"
    # Étape 1 : Extraire FILE_ID de l'URL
    if "drive.google.com" in drive_url:
        try:
            file_id = drive_url.split("/d/")[1].split("/")[0]
        except IndexError:
            print("URL incorrecte. Assurez-vous qu'elle provient de Google Drive.")
            return
    else:
        print("Ce script fonctionne uniquement avec des liens Google Drive.")
        return
    
    # Étape 2 : Créer l'URL de téléchargement direct
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        # Étape 3 : Envoyer la requête GET pour télécharger le fichier
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        # Étape 4 : Écrire le contenu dans un fichier local
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Fichier téléchargé avec succès : {output_file}")
    
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors du téléchargement : {e}")

def delete_pdf():

    # Chemin du fichier à supprimer
    file_path = "./file.pdf"

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Le fichier '{file_path}' a été supprimé avec succès.")
        else:
            print(f"Le fichier '{file_path}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la suppression : {e}")


def append_unique_text(text_to_add):
    file_path = "vault.txt"
    
    # Ouvre le fichier en mode lecture pour vérifier s'il existe déjà
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as existing_file:
            existing_text = existing_file.read()

        # Vérifie si le texte est déjà présent
        if text_to_add.strip() in existing_text:
            print("Le texte est déjà présent dans le fichier.")
            return False

    # Si le texte n'est pas trouvé, on l'ajoute
    with open(file_path, "a", encoding="utf-8") as vault_file:
        vault_file.write(text_to_add.strip() + "\n")
        print("Texte ajouté avec succès.")
        return True

# Fonction pour convertir le PDF en texte
def convert_pdf_to_text(url):
    download_pdf(url)
    file_path = "file.pdf"
    # Vérifie si le fichier existe
    if not os.path.isfile(file_path):
        print(f"Le fichier '{file_path}' n'existe pas. Veuillez fournir un chemin valide.")
        return

    try:
        # Lecture du fichier PDF
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ''
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                if page.extract_text():
                    text += page.extract_text() + " "
            
            # Normalisation des espaces
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Découpage du texte en morceaux de 1000 caractères max
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            
            # Ajout des morceaux de texte dans le fichier 'vault.txt' après vérification
            for chunk in chunks:
                append_unique_text(chunk)
            print(f"Le contenu à apprendre été ajouté à 'vault.txt'.")
            delete_pdf()

    except Exception as e:
        print(f"Une erreur est survenue : {e}")

# Vérifie si le script est exécuté avec un fichier en argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation : python3 upload.py path/du/fichier.pdf")
        sys.exit(1)

    # Récupère le chemin du fichier PDF depuis les arguments
    file_path = sys.argv[1]
    convert_pdf_to_text(file_path)
