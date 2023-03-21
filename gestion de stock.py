import tkinter as tk
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="azerty",
    database="boutique"
)

def ajouter_produit():
    nom = nom_var.get()
    description = description_var.get()
    prix = prix_var.get()
    quantite = quantite_var.get()
    categorie = categorie_var.get()
    

    if not nom or not description or not prix or not quantite or not categorie:
        tk.messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
        return
    

    try:
        prix = float(prix)
        if prix < 0:
            raise ValueError
    except ValueError:
        tk.messagebox.showerror("Erreur", "Le prix doit être un nombre positif")
        return
    
 
    try:
        quantite = int(quantite)
        if quantite < 0:
            raise ValueError
    except ValueError:
        tk.messagebox.showerror("Erreur", "La quantité doit être un entier positif")
        return
    
    cur = conn.cursor()
    sql = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, (nom, description, prix, quantite, categorie))
    conn.commit()
    afficher_produits()



def afficher_details_produit(event):
    index = produits_listbox.curselection()[0]
    produit = produits_listbox.get(index)
    nom_var.set(produit[1])
    description_var.set(produit[2])
    prix_var.set(str(produit[3]))
    quantite_var.set(str(produit[4]))
    categorie_var.set(produit[5])


def supprimer_produit():
    index = produits_listbox.curselection()[0]
    produit = produits_listbox.get(index)
    produit_id = produit[0]
    cur = conn.cursor()
    sql = "DELETE FROM produit WHERE id=%s"
    cur.execute(sql, (produit_id,))
    conn.commit()
    afficher_produits()



def modifier_produit():
    index = produits_listbox.curselection()[0]
    produit = produits_listbox.get(index)
    produit_id = produit[0]
    nom = nom_var.get()
    description = description_var.get()
    prix = float(prix_var.get())
    quantite = int(quantite_var.get())
    categorie = categorie_var.get()
    cur = conn.cursor()
    sql = "UPDATE produit SET nom=%s, description=%s, prix=%s, quantite=%s, id_categorie=%s WHERE id=%s"
    cur.execute(sql, (nom, description, prix, quantite, categorie, produit_id))
    conn.commit()
    afficher_produits()



def afficher_produits():
    produits_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    sql = "SELECT produit.id, produit.nom, produit.description, produit.prix, produit.quantite, categorie.nom FROM produit INNER JOIN categorie ON produit.id_categorie = categorie.id"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        produits_listbox.insert(tk.END, row)




root = tk.Tk()
root.title("Tableau de bord des stocks")
root.geometry("500x500")

produit_frame = tk.LabelFrame(root, text="Ajouter/modifier un produit")
produit_frame.pack(side=tk.LEFT, padx=10, pady=10)


nom_label = tk.Label(produit_frame, text="Nom:")
nom_label.grid(row=0, column=0, padx=5, pady=5)
nom_var = tk.StringVar()
nom_entry = tk.Entry(produit_frame, textvariable=nom_var)
nom_entry.grid(row=0, column=1, padx=5, pady=5)

description_label = tk.Label(produit_frame, text="Description:")
description_label.grid(row=1, column=0, padx=5, pady=5)
description_var = tk.StringVar()
description_entry = tk.Entry(produit_frame, textvariable=description_var)
description_entry.grid(row=1, column=1, padx=5, pady=5)

prix_label = tk.Label(produit_frame, text="Prix:")
prix_label.grid(row=2, column=0, padx=5, pady=5)
prix_var = tk.StringVar()
prix_entry = tk.Entry(produit_frame, textvariable=prix_var)
prix_entry.grid(row=2, column=1, padx=5, pady=5)

quantite_label = tk.Label(produit_frame, text="Quantité:")
quantite_label.grid(row=3, column=0, padx=5, pady=5)
quantite_var = tk.StringVar()
quantite_entry = tk.Entry(produit_frame, textvariable=quantite_var)
quantite_entry.grid(row=3, column=1, padx=5, pady=5)




ajouter_button = tk.Button(
    produit_frame, text="Ajouter", command=ajouter_produit)
ajouter_button.grid(row=5, column=0, padx=5, pady=5)

modifier_button = tk.Button(
    produit_frame, text="Modifier", command=modifier_produit)
modifier_button.grid(row=5, column=1, padx=5, pady=5)

supprimer_button = tk.Button(
    produit_frame, text="Supprimer", command=supprimer_produit)
supprimer_button.grid(row=5, column=2, padx=5, pady=5)


produits_frame = tk.LabelFrame(root, text="Produits en stock")
produits_frame.pack(side=tk.LEFT, padx=10, pady=10)



produits_listbox = tk.Listbox(produits_frame, width=50)
produits_listbox.pack()


root.mainloop()

conn.close()
