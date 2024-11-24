#!/usr/bin/env python3

import os
import subprocess
import threading
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, END
import time

# Constantes
HISTORIQUE_PATH = "historique_scans.txt"
COULEUR_CELADON = "#ACE1AF"  # Couleur céladon pour le thème clair
LARGEUR_BOUTON = 200  # Largeur fixe pour tous les boutons

# Configuration de customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class AntivirusApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Application Antivirus")
        self.geometry("600x700")  # Taille initiale
        self.configure(bg=COULEUR_CELADON)

        # Création des widgets de la page principale
        self.page_principale()

    def page_principale(self):
        """Affiche la page principale avec tous les widgets."""
        self.clear_frame()

        # Label principal
        self.label = ctk.CTkLabel(self, text="Application Antivirus", font=("Arial", 20))
        self.label.pack(pady=10)

        # Grande boîte de texte pour les résultats
        self.result_box = ctk.CTkTextbox(self, height=200, width=500)
        self.result_box.pack(pady=10)

        # Labels pour le timer et le statut
        self.timer_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.pack(pady=5)

        # Boutons fixes
        btn_update = ctk.CTkButton(self, text="Mettre à jour les définitions", command=self.mise_a_jour_definitions, width=LARGEUR_BOUTON)
        btn_update.pack(pady=5)

        btn_scan = ctk.CTkButton(self, text="Scanner un fichier", command=self.start_scan_fichier, width=LARGEUR_BOUTON)
        btn_scan.pack(pady=5)

        btn_history = ctk.CTkButton(self, text="Afficher l'historique des scans", command=self.page_historique, width=LARGEUR_BOUTON)
        btn_history.pack(pady=5)

        btn_quit = ctk.CTkButton(self, text="Quitter", command=self.quit, width=LARGEUR_BOUTON)
        btn_quit.pack(pady=5)

    def page_historique(self):
        """Affiche la page historique des scans."""
        self.clear_frame()

        # Label principal
        self.label = ctk.CTkLabel(self, text="Historique des Scans", font=("Arial", 20))
        self.label.pack(pady=10)

        if os.path.exists(HISTORIQUE_PATH):
            with open(HISTORIQUE_PATH, "r") as historique:
                historique_lignes = historique.readlines()

            for ligne in historique_lignes:
                date, nom_fichier, rapport = ligne.strip().split(' ', 2)
                bouton_texte = f"{date}_{nom_fichier}"

                btn_historique = ctk.CTkButton(
                    self, 
                    text=bouton_texte, 
                    command=lambda r=rapport: self.afficher_rapport(r), 
                    width=LARGEUR_BOUTON
                )
                btn_historique.pack(pady=5)
        else:
            label_aucun = ctk.CTkLabel(self, text="Aucun historique disponible.", font=("Arial", 14))
            label_aucun.pack(pady=10)

        # Bouton retour
        btn_back = ctk.CTkButton(self, text="Retour", command=self.page_principale, width=LARGEUR_BOUTON)
        btn_back.pack(pady=10)

    def afficher_rapport(self, rapport_nom):
        """Affiche le contenu complet d'un rapport dans la boîte de résultats."""
        self.clear_frame()

        # Label principal
        self.label = ctk.CTkLabel(self, text="Contenu du Rapport", font=("Arial", 20))
        self.label.pack(pady=10)

        self.result_box = ctk.CTkTextbox(self, width=500, height=500)
        self.result_box.pack(pady=10)

        if os.path.exists(rapport_nom):
            with open(rapport_nom, "r") as rapport:
                self.result_box.insert(END, rapport.read())
        else:
            self.result_box.insert(END, f"Le rapport {rapport_nom} est introuvable.")

        # Bouton retour
        btn_back = ctk.CTkButton(self, text="Retour à l'historique", command=self.page_historique, width=LARGEUR_BOUTON)
        btn_back.pack(pady=10)

    def clear_frame(self):
        """Efface tous les widgets pour afficher une nouvelle page."""
        for widget in self.winfo_children():
            widget.destroy()

    def mise_a_jour_definitions(self):
        """Met à jour les définitions antivirus de ClamAV et Maldetect."""
        self.result_box.delete("1.0", END)
        self.result_box.insert(END, "Mise à jour des définitions ClamAV en cours...\n")
        subprocess.run(["sudo", "freshclam"])
        self.result_box.insert(END, "Mise à jour des définitions Maldetect en cours...\n")
        subprocess.run(["sudo", "maldet", "--update"])
        self.result_box.insert(END, "Mise à jour terminée.\n")

    def start_scan_fichier(self):
        """Lance le scan d'un fichier avec un compteur de temps."""
        fichier = filedialog.askopenfilename(title="Sélectionnez un fichier à scanner")
        if fichier:
            self.scan_en_cours = True
            self.timer_thread = threading.Thread(target=self.update_timer)
            self.timer_thread.start()

            scan_thread = threading.Thread(target=self.scan_fichier, args=(fichier,))
            scan_thread.start()

    def update_timer(self):
        """Met à jour le timer."""
        start_time = time.time()
        while self.scan_en_cours:
            elapsed_time = int(time.time() - start_time)
            self.timer_label.configure(text=f"Temps écoulé : {elapsed_time} secondes")
            time.sleep(1)

    def scan_fichier(self, fichier):
        """Scanne un fichier avec ClamAV et Maldetect."""
        self.result_box.delete("1.0", END)
        self.result_box.insert(END, f"Scan du fichier : {fichier}\n")

        # Scan avec ClamAV
        self.status_label.configure(text="Scan avec ClamAV en cours...")
        clamav_scan = subprocess.run(["clamscan", fichier], capture_output=True, text=True)
        clamav_resultat = clamav_scan.stdout
        self.result_box.insert(END, "Scan avec ClamAV terminé.\n")

        # Scan avec Maldetect
        self.status_label.configure(text="Scan avec Maldetect en cours...")
        maldetect_scan = subprocess.run(["sudo", "maldet", "-a", fichier], capture_output=True, text=True)
        maldetect_resultat = maldetect_scan.stdout
        self.result_box.insert(END, "Scan avec Maldetect terminé.\n")

        self.scan_en_cours = False
        self.timer_label.configure(text="")
        self.status_label.configure(text="")
        self.result_box.insert(END, clamav_resultat)
        self.result_box.insert(END, maldetect_resultat)
        self.sauvegarder_rapport(fichier, clamav_resultat, maldetect_resultat)

    def sauvegarder_rapport(self, fichier, clamav_resultat, maldetect_resultat):
        """Sauvegarde le rapport complet."""
        date = datetime.now().strftime('%y-%m-%d_%H:%M')
        nom_fichier = os.path.basename(fichier)
        rapport_nom = f"rapport_{date}_{nom_fichier}.txt"
        with open(rapport_nom, "w") as f:
            f.write("=== Résultat ClamAV ===\n")
            f.write(clamav_resultat)
            f.write("\n=== Résultat Maldetect ===\n")
            f.write(maldetect_resultat)
        with open(HISTORIQUE_PATH, "a") as historique:
            historique.write(f"{date} {nom_fichier} {rapport_nom}\n")
        self.result_box.insert(END, f"\nRapport complet sauvegardé sous {rapport_nom}")

# Lancer l'application
if __name__ == "__main__":
    app = AntivirusApp()
    app.mainloop()
