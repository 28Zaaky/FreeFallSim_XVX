# Simulateur de Chute Libre avec Frottements

Un simulateur interactif permettant d'étudier la chute verticale d’un objet sous l'effet de la gravité 🌍, avec ou sans force de frottement de l’air 💨. Le tout est visualisé via des graphiques, animations, et une interface conviviale en Python 🐍.

---

## Objectifs du projet

Ce projet vise à :

- Comprendre les différences entre la chute libre idéale (sans frottement) et la chute réelle (avec frottement).
- Appliquer la méthode d’Euler pour résoudre numériquement les équations du mouvement.
- Visualiser les effets du frottement sur la vitesse et la position d’un objet en chute.
- Illustrer la notion de vitesse limite dans un fluide.
- Exporter les données au format `.csv` pour analyse ou usage éducatif.

---

## Fonctionnalités

- **Interface utilisateur (Tkinter)** : entrez les paramètres (masse, frottement, hauteur…)
- **Simulation avec et sans frottement**
- **Visualisation des résultats** : graphiques hauteur/temps et vitesse/temps
- **Animation de la chute**
- **Export CSV** des résultats
- **Calcul automatique de la vitesse limite**

---

## Contexte scientifique

Lorsqu’un objet tombe :

### Sans frottement :
- L’objet est uniquement soumis à la gravité (`a = g = 9.81 m/s²`).
- La vitesse augmente indéfiniment (`v = g·t`).
- Le mouvement est idéal, sans résistance de l’air.

### Avec frottement :
- On considère une force de frottement proportionnelle à la vitesse : `F_f = -k·v`
- L'accélération devient `a = g - (k/m)·v`
- La vitesse finit par atteindre une **vitesse limite** : `v_lim = (m·g)/k`
- Le mouvement est ralenti, réaliste (par exemple, chute d’un parachutiste).

La résolution numérique est effectuée avec la **méthode d’Euler**, une approche simple d’intégration numérique qui permet de simuler des systèmes dynamiques sans résoudre d’équations différentielles analytiquement.

---

## Technologies utilisées

- `Python 3.x`
- `Tkinter` – interface graphique
- `Matplotlib` – graphiques et animations
- `Pandas` – export des résultats
- `NumPy` – calculs numériques
