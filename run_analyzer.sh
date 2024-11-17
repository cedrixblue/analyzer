#!/bin/bash

# Variables
VENV_PATH="./python-env"
SCRIPT_PATH="./analyzer.py"

# Vérification de l'existence du venv
if [ ! -d "$VENV_PATH" ]; then
  echo "L'environnement virtuel n'existe pas. Création de l'environnement virtuel..."
  python3 -m venv "$VENV_PATH"
  echo "Environnement virtuel créé à $VENV_PATH."
fi

# Activation de l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source "$VENV_PATH/bin/activate"

# Installation des dépendances nécessaires
echo "Installation des dépendances requises..."
pip install --upgrade pip
#ip install customtkinter

# Vérification de l'existence du script
if [ ! -f "$SCRIPT_PATH" ]; then
  echo "Le script $SCRIPT_PATH est introuvable. Veuillez vérifier le chemin."
  deactivate
  exit 1
fi

# Exécution du script
echo "Exécution de $SCRIPT_PATH..."
python "$SCRIPT_PATH"

# Désactivation de l'environnement virtuel après exécution
echo "Désactivation de l'environnement virtuel..."
deactivate

