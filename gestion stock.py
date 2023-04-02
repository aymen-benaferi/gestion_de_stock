import mysql.connector
import tkinter as tk
from tkinter import messagebox

# connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="azerty",
    database="boutique"
)

# création de la fenêtre principale
root = tk.Tk()
root.title("Gestion de stock")

# fonction pour afficher les produits


def afficher_produits():
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nom, description, prix, quantite, id_categorie FROM produit")
    produits = cursor.fetchall()
    output_text.delete("1.0", tk.END)
    for produit in produits:
        output_text.insert(
            tk.END, f"{produit[0]} - {produit[1]} ({produit[3]}€) - quantité : {produit[4]} - {produit[2]}\n")
    cursor.close()

# fonction pour ajouter un produit


def ajouter_produit():
    nom = nom_entry.get()
    description = description_entry.get()
    prix = prix_entry.get()
    quantite = quantite_entry.get()
    categorie = categorie_var.get()

    # vérifier que tous les champs sont remplis
    if nom != "" and description != "" and prix != "" and quantite != "" and categorie != "":
        cursor = conn.cursor()
        # Look up category ID based on name
        cursor.execute("SELECT id FROM categorie WHERE nom = %s", (categorie,))
        result = cursor.fetchone()
        if result:
            categorie_id = result[0]
        else:
            raise ValueError("Invalid category name: {}".format(categorie))

        # Insert new product with category ID
        cursor.execute("INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)",
                       (nom, description, prix, quantite, categorie_id))

        conn.commit()
        print("Produit ajouté avec succès !")
        cursor.close()
        messagebox.showinfo(
            "Produit ajouté", "Le produit a été ajouté avec succès !")
        # vider les champs après l'ajout
        nom_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        prix_entry.delete(0, tk.END)
        quantite_entry.delete(0, tk.END)
        categorie_menu.delete(0, tk.END)

    else:
        messagebox.showwarning(
            "Champs manquants", "Veuillez remplir tous les champs !")


# récupération de la liste des catégories depuis la base de données
cursor = conn.cursor()
cursor.execute("SELECT nom FROM categorie")
categories = cursor.fetchall()
cursor.close()


def supprimer_produit():
    id_produit = id_entry.get()

    # Vérifier que l'ID est valide
    if id_produit == "":
        messagebox.showwarning(
            "ID manquant", "Veuillez saisir l'ID du produit à supprimer.")
        return

    # Vérifier que l'ID existe dans la base de données
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produit WHERE id = %s", (id_produit,))
    produit = cursor.fetchone()
    cursor.close()

    if produit is None:
        messagebox.showwarning(
            "ID invalide", f"L'ID {id_produit} ne correspond à aucun produit.")
        return

    # Confirmer la suppression avec l'utilisateur
    confirmation = messagebox.askyesno(
        "Confirmer la suppression", f"Voulez-vous vraiment supprimer le produit {produit[1]} ({produit[3]}€) ?")

    if confirmation:
        # Supprimer le produit de la base de données
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produit WHERE id = %s", (id_produit,))
        conn.commit()
        cursor.close()

        # Effacer les champs et mettre à jour l'affichage des produits
        id_entry.delete(0, tk.END)
        quantite_modif_entry.delete(0, tk.END)
        afficher_produits()


def modifier_quantite():
    id_produit = id_entry.get()
    quantite = quantite_modif_entry.get()

    # Vérifier que les champs sont remplis
    if id_produit != "" and quantite != "":
        cursor = conn.cursor()
        # Vérifier que le produit existe dans la base de données
        cursor.execute("SELECT * FROM produit WHERE id=%s", (id_produit,))
        produit = cursor.fetchone()
        if produit:
            # Mettre à jour la quantité du produit
            cursor.execute(
                "UPDATE produit SET quantite=%s WHERE id=%s", (quantite, id_produit))
            conn.commit()
            print("Quantité mise à jour avec succès !")
            # Vider les champs après la modification
            id_entry.delete(0, tk.END)
            quantite_modif_entry.delete(0, tk.END)
            # Afficher le statut de l'opération en cours
            status_label.config(
                text="Quantité mise à jour avec succès !", fg="green")
        else:
            messagebox.showwarning("Produit introuvable",
                                   "Le produit avec cet ID n'existe pas.")
        cursor.close()
    else:
        messagebox.showwarning(
            "Champs manquants", "Veuillez remplir tous les champs !")


# widgets
nom_label = tk.Label(root, text="Nom du produit :")
nom_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

status_label = tk.Label(root, text="", fg="red")
status_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

nom_var = tk.StringVar()
nom_entry = tk.Entry(root, textvariable=nom_var)
nom_entry.grid(row=0, column=1, padx=5, pady=5)

description_label = tk.Label(root, text="Description du produit :")
description_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

description_var = tk.StringVar()
description_entry = tk.Entry(root, textvariable=description_var)
description_entry.grid(row=1, column=1, padx=5, pady=5)

prix_label = tk.Label(root, text="Prix du produit :")
prix_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

prix_var = tk.StringVar()
prix_entry = tk.Entry(root, textvariable=prix_var)
prix_entry.grid(row=2, column=1, padx=5, pady=5)

quantite_label = tk.Label(root, text="Quantité en stock :")
quantite_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

quantite_entry = tk.Entry(root)
quantite_entry.grid(row=3, column=1, padx=5, pady=5)

# création d'une variable Tkinter pour la catégorie sélectionnée
categorie_var = tk.StringVar(root)
categorie_var.set(categories[0][0])

# création du menu déroulant pour les catégories
categorie_label = tk.Label(root, text="Catégorie :")
categorie_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
categorie_menu = tk.OptionMenu(
    root, categorie_var, *[cat[0] for cat in categories])
categorie_menu.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

# création des boutons pour ajouter et afficher les produits

afficher_button = tk.Button(
    root, text="Afficher les produits", command=afficher_produits)
afficher_button.grid(row=5, column=0, padx=5, pady=5)

ajouter_button = tk.Button(
    root, text="Ajouter un produit", command=ajouter_produit)
ajouter_button.grid(row=5, column=1, padx=5, pady=5)

# création des champs pour modifier la quantité de stock d'un produit

id_label = tk.Label(root, text="ID du produit :")
id_label.grid(row=6, column=0, padx=5, pady=5)

id_var = tk.StringVar()
id_entry = tk.Entry(root, textvariable=id_var)
id_entry.grid(row=6, column=1, padx=5, pady=5)

quantite_modif_label = tk.Label(root, text="Nouvelle quantité :")
quantite_modif_label.grid(row=7, column=0, padx=5, pady=5)

quantite_modif_var = tk.StringVar()
quantite_modif_entry = tk.Entry(root, textvariable=quantite_modif_var)
quantite_modif_entry.grid(row=7, column=1, padx=5, pady=5)

modifier_button = tk.Button(
    root, text="Modifier la quantité", command=modifier_quantite)
modifier_button.grid(row=8, column=0, padx=5, pady=5)

supprimer_button = tk.Button(
    root, text="Supprimer un produit", command=supprimer_produit)
supprimer_button.grid(row=9, column=0, padx=5, pady=5)

# création du champ de texte pour afficher les produits

output_text = tk.Text(root, width=125, height=10)
output_text.grid(row=8, column=1, padx=5, pady=5)

# création d'une étiquette pour afficher le statut de l'opération en cours

status_label = tk.Label(root, text="")
status_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
