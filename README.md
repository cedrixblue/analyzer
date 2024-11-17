# analyzer
Analyzer est un outil qui permet de scanner des fichier avec ClamAV et Maldetect

**Prérequis**
- Disposer d’une VM fonctionnelle sous Ubuntu 24.04.
  
- Avoir un accès utilisateur avec des droits administrateurs (permettant d’utiliser sudo).


- Les fichiers suivants doivent être disponibles :

- analyzer.py : Script Python principal de l'application.
 
- run_analyzer.sh : Script Bash pour automatiser l'exécution de l'application.


# **Étape 1 :**
Installation des dépendances système

Mettez à jour le système :

*bash*

`sudo apt update && sudo apt upgrade -y`


Installez Python 3.12 et venv : Ubuntu 24.04 inclut Python 3.12.

Pour s'assurer que l'environnement virtuel fonctionne, installez les paquets suivants :

*bash*

`sudo apt install -y python3 python3-venv python3-pip`


Installez les outils antivirus nécessaires :

ClamAV :

*bash*

`sudo apt install -y clamav clamav-daemon`

`sudo systemctl stop clamav-freshclam.service`

`sudo freshclam  # Met à jour les définitions`


Maldetect :

*bash*

`sudo apt install -y maldetect`


# **Étape 2 :**

Préparation des fichiers de l'application

Copiez les fichiers sur la VM : Transférez les fichiers analyzer.py et run_analyzer.sh dans le répertoire utilisateur de la VM, par exemple /home/<utilisateur>.

Exemple avec SCP :

*bash*

`scp analyzer.py run_analyzer.sh <utilisateur>@<ip_de_la_vm>:/home/<utilisateur>/`


Rendez le script Bash exécutable :

*bash*

`chmod +x /home/<utilisateur>/run_analyzer.sh`


# **Étape 3 :**
Exécution initiale et configuration

Lancez le script Bash run_analyzer.sh : Ce script configure automatiquement l'environnement virtuel et exécute l'application :

*bash*

`./run_analyzer.sh`


# **Première exécution :**

## Le script Bash :

Crée un environnement virtuel Python dans /home/<utilisateur>/venv.

Installe les dépendances nécessaires (customtkinter).

Lance l’application analyzer.py.

Une fenêtre graphique apparaîtra avec l’interface de l’application.


## Tester l'application :

Effectuez un test de scan pour vérifier que ClamAV et Maldetect fonctionnent correctement.

Assurez-vous que les résultats s'affichent et que les rapports sont générés dans le répertoire de travail.


# **Notes supplémentaires**

## Dépannage :

Si le script Python ne se lance pas, vérifiez que customtkinter est bien installé dans l'environnement virtuel :

*bash*

`source /home/<utilisateur>/venv/bin/activate`

`pip install customtkinter`


Rapports :

Les rapports sont générés sous le format rapport_AA-MM-JJ_hh:mm_nomdufichier.txt dans le répertoire courant de l'application.


# **Résumé rapide**

Installez une VM Ubuntu 24.04.

Mettez à jour le système et installez Python, ClamAV, et Maldetect.

Transférez analyzer.py et run_analyzer.sh.

Exécutez run_analyzer.sh pour configurer et lancer l'application.

L'application est maintenant prête à être utilisée sur plusieurs machines !
