# CAPI
Bienvenue sur la GitHub de notre projet de "Planning Poker". Ce page a pour but d'expliquer comment lancer le projet sans erreur.

# Librairie à installer
Dans notre projet, nous utilisons plusieurs librairies python externe à installer via la commande pip install. Nous utilisons les librairies `pip install pygame` et la librairie `pip install numpy`.

# Ouverture du projet
Une fois le projet téléchargé, il vous faudra exécuter via une commande python dans le terminal, le fichier main_capi.py `python ./main_capi.py`

# Architecture JSON
Vous pouvez déposer vos fichier json dans le dossier data_json tant qu'ils respectent l'architecture des autres json.
Ces fichiers s'organise de la manière suivante : {"Nom de la tache à effectuer", cout de la tâche}. Le coup de la tâche est initialisé à -1 pour notifier le fait que la tâche n'a pas été traité.

# Documentation
La documentation est généré sur une branche annexe gh-pages, une fois sur cette branche, pour lire la documentation, il faut éxécuter sur un navigateur le fichier index.html

# Tests unitaires
L'éxécution des tests est réalisé à chaque push sur le projet mais vous pouvez les retrouver à la racine du projet dans le fichier testUnitaires.py
