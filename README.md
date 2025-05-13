# Projet de Recherche Opérationnelle

Ce projet implémente deux problèmes classiques d'optimisation :
1. Le problème du plus court chemin
2. Le problème du voyageur de commerce (TSP)

## Structure du Projet

- `Backend/` : Serveur Flask avec l'implémentation des algorithmes d'optimisation
  - `app.py` : Serveur pour le plus court chemin (port 5000)
  - `PLNE.py` : Serveur pour le TSP (port 5001)
  - `requirements.txt` : Dépendances Python

- `Frontend/shortest-path-app/` : Application Angular
  - Interface utilisateur moderne et interactive
  - Visualisation des graphes avec vis.js
  - Gestion des matrices d'adjacence/distance

## Technologies Utilisées

- Backend :
  - Python 3
  - Flask
  - Gurobi (solveur d'optimisation)
  - NumPy

- Frontend :
  - Angular
  - Bootstrap
  - vis.js pour la visualisation des graphes

## Installation

1. Backend :
```bash
cd Backend
pip install -r requirements.txt
```

2. Frontend :
```bash
cd Frontend/shortest-path-app
npm install
```

## Lancement

1. Backend :
```bash
# Dans un premier terminal
cd Backend
python app.py  # Lance le serveur du plus court chemin sur le port 5000

# Dans un second terminal
cd Backend
python PLNE.py  # Lance le serveur TSP sur le port 5001
```

2. Frontend :
```bash
cd Frontend/shortest-path-app
ng serve  # Lance l'application Angular sur http://localhost:4200
```

## Fonctionnalités

### Plus Court Chemin
- Ajout/suppression de nœuds
- Configuration de la matrice d'adjacence
- Calcul du plus court chemin entre deux nœuds
- Visualisation du résultat

### TSP
- Gestion des villes
- Configuration de la matrice des distances
- Résolution du TSP avec la formulation MTZ
- Visualisation du circuit optimal
