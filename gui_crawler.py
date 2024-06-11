import tkinter as tk
from tkinter import messagebox
import subprocess

class CrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Crawler")

        self.url_label = tk.Label(root, text="URL de base :")
        self.url_label.pack()

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.selectors_label = tk.Label(root, text="Classes ou ID des zones à indexer (séparés par des virgules, ex: .content, #main) :")
        self.selectors_label.pack()

        self.selectors_entry = tk.Entry(root, width=50)
        self.selectors_entry.pack()

        self.limit_label = tk.Label(root, text="Nombre de pages à crawler (0 pour tout le site) :")
        self.limit_label.pack()

        self.limit_entry = tk.Entry(root, width=50)
        self.limit_entry.pack()

        self.crawl_button = tk.Button(root, text="Lancer le crawl", command=self.start_crawl)
        self.crawl_button.pack()

        self.graph_button = tk.Button(root, text="Créer les graphiques", command=self.create_graphs)
        self.graph_button.pack()

        self.clear_button = tk.Button(root, text="Vider la base de données", command=self.clear_db)
        self.clear_button.pack()

        self.view_button = tk.Button(root, text="Consulter la base de données", command=self.view_data)
        self.view_button.pack()

    def start_crawl(self):
        url = self.url_entry.get()
        selectors = self.selectors_entry.get()
        limit = self.limit_entry.get()

        if not url or not selectors or not limit.isdigit():
            messagebox.showerror("Erreur", "Veuillez entrer une URL, des sélecteurs et un nombre de pages valide.")
            return

        try:
            command = f'python3 crawler.py {url} "{selectors}" {limit}'
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("Succès", "Le crawl et l'analyse sont terminés.")
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode() if e.output else str(e)
            messagebox.showerror("Erreur", error_msg)

    def create_graphs(self):
        try:
            subprocess.run("python3 barr.py", shell=True, check=True)
            subprocess.run("python3 forced_graph.py", shell=True, check=True)
            messagebox.showinfo("Succès", "Les graphiques ont été créés.")
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode() if e.output else str(e)
            messagebox.showerror("Erreur", error_msg)

    def clear_db(self):
        try:
            command = 'python3 -c "from crawler import Crawler; Crawler.clear_db()"'
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("Succès", "La base de données a été vidée.")
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode() if e.output else str(e)
            messagebox.showerror("Erreur", error_msg)

    def view_data(self):
        try:
            s
