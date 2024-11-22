# Ollama 
Mon projet Ollama permet d'apprendre un sujet à l'IA grâce à des PDF.

## Installation
Installez les bibliothèques avec la commande :

        pip install -r requirements.txt

## apprentissage

Pour lui faire apprendre un sujet via un PDF qui se trouve en lecture libre sur Google Drive, il faut, dans une première étape, copier le lien de partage du PDF puis, ensuite, exécuter la commande :

        python3 upload.py <lien de partage>

## Lancer Ollama

Pour finir, vous pouvez débuter votre discussion avec Ollama en exécutant la commande :

        python3 localrag.py --model <version du model>

## détails

Il faut savoir qu'il vous est possible de lui apprendre autant de choses que vous voulez et que votre machine est capable de faire fonctionner.
