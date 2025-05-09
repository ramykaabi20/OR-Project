# OR-Project

Un projet de cours en Recherche Opérationnelle.

## Présentation

Ce projet a été développé en utilisant **Python**, **Qt5** pour l'interface graphique (IHM) et **Gurobi** comme solveur d'optimisation.

L'application permet à l'utilisateur de résoudre deux types de problèmes d'optimisation :

- **Problème de Programmation Linéaire (PL)** : Problème de Transport.
- **Problème de Programmation Linéaire en Nombres Entiers (PLNE)** : Planification d’Ouverture de Centres de Distribution.

## Installation

Avant de lancer l'application, assurez-vous d'installer les dépendances :

```bash
pip install pygurobi
pip install PyQt5
```

## Lancement de l'application

```bash
python main.py
```

## Structure du projet

- `main.py` : Fenêtre principale de l'application avec présentation et navigation.
- `PL_model.py` : IHM et résolution du problème PL.
- `PLNE_model.py` : IHM et résolution du problème PLNE.
- `Test_pl.py` : Script de test pour le modèle PL (hors interface).
- `Test_plne.py` : Script de test pour le modèle PLNE (hors interface).
- `img.png` : Image affichée dans l'IHM principale.

### IHM Principale (`main.py`)

- Présente le projet et ses objectifs.
- Affiche une image d'accueil.
- Deux boutons permettent de lancer l’un des deux solveurs.

### Problèmes résolus

---

🔷 **1. Problème de Transport (PL)**  
🧠 **Problème** :  
Une entreprise possède deux entrepôts (A et B) qui livrent trois magasins (1, 2, 3). Chaque entrepôt a une capacité limitée, et chaque magasin a une demande à satisfaire. Le coût de transport d'une unité entre chaque entrepôt et magasin est connu. L'objectif est de minimiser le coût total de transport.

### Description détaillée :
L'entreprise doit organiser la distribution de ses produits à partir de ses deux entrepôts vers les trois magasins, tout en minimisant les coûts de transport.  
- Chaque entrepôt a une capacité maximale qu'il ne doit pas dépasser.  
- Chaque magasin a une demande spécifique qui doit être satisfaite.
- Le coût de transport d’une unité de produit varie selon l'entrepôt et le magasin. L'objectif est de déterminer la quantité à transporter entre chaque entrepôt et magasin de manière à minimiser le coût global.


🔷 **2. Planification d'Ouverture de Centres de Distribution (PLNE)**  
🧠 **Problème** :  
Une entreprise doit décider où ouvrir parmi 3 centres logistiques potentiels (avec un coût fixe d'ouverture), et combien livrer aux 2 magasins à partir de ces centres (avec un coût unitaire variable de transport). L'objectif est de minimiser les coûts d'ouverture et de transport tout en respectant la demande des magasins.

### Description détaillée :
L'entreprise doit choisir quels centres ouvrir parmi trois options disponibles, en prenant en compte les coûts fixes d'ouverture de chaque centre. Ensuite, elle doit décider de la quantité de produits à transporter des centres ouverts vers les magasins, en fonction des demandes et des coûts de transport.  
- Chaque centre a une capacité maximale qu'il ne doit pas dépasser.  
- Le coût de transport entre chaque centre et magasin dépend de la distance et d'autres facteurs logistiques.  
- L'objectif est de minimiser à la fois les coûts d'ouverture des centres et les coûts de transport des produits vers les magasins.


## Auteurs

Projet réalisé par :
- Rami Kaabi
- Maryem Dammak
- Ithar Hadj Amor

## Image

Une image illustrant le projet est intégrée dans l'interface graphique (`img.png`).

---

## Remarques

- Ce projet est à but pédagogique.
- Pour l'utiliser, il faut disposer d’une licence Gurobi (gratuite pour les étudiants).
