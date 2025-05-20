# Créer une simulation physique réaliste de la chute verticale d’un objet soumis à la gravité
# et à une force de frottement de l’air, avec résolution numérique (méthode d’Euler) et visualisation
# des résultats sous forme de graphiques.

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk

class ChuteLibre:
    def __init__(self, masse, frottement, hauteur_initiale, dt, t_max):
        self.m = masse
        self.k = frottement
        self.y0 = hauteur_initiale
        self.dt = dt
        self.t_max = t_max
        self.g = 9.81

    def simuler_avec_frottement(self):
        t, v, y = 0, 0, self.y0
        T, V, Y = [t], [v], [y]

        while y > 0 and t < self.t_max:
            a = self.g - (self.k / self.m) * v
            v += a * self.dt
            y -= v * self.dt
            t += self.dt
            y = max(0, y)

            T.append(t)
            V.append(v)
            Y.append(y)

        return T, V, Y

    def simuler_sans_frottement(self):
        t, v, y = 0, 0, self.y0
        T, V, Y = [t], [v], [y]

        while y > 0 and t < self.t_max:
            a = self.g
            v += a * self.dt
            y -= v * self.dt
            t += self.dt
            y = max(0, y)

            T.append(t)
            V.append(v)
            Y.append(y)

        return T, V, Y

    def vitesse_limite(self):
        if self.k == 0:
            return float('inf')
        return self.m * self.g / self.k

    def exporter_csv(self, t, v1, v2, y1, y2):
        df = pd.DataFrame({
            'Temps (s)': t,
            'Vitesse avec frottement': v1,
            'Vitesse sans frottement': v2,
            'Hauteur avec frottement': y1,
            'Hauteur sans frottement': y2
        })
        df.to_csv("resultats_simulation.csv", index=False)

    def tracer_graphiques(self, t, y1, y2, v1, v2):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        ax1.plot(t, y1, label="Avec frottement")
        ax1.plot(t, y2, label="Sans frottement", linestyle='--')
        ax1.set_title("Hauteur en fonction du temps")
        ax1.set_xlabel("Temps (s)")
        ax1.set_ylabel("Hauteur (m)")
        ax1.legend()
        ax1.grid(True)

        ax2.plot(t, v1, label="Avec frottement")
        ax2.plot(t, v2, label="Sans frottement", linestyle='--')
        ax2.set_title("Vitesse en fonction du temps")
        ax2.set_xlabel("Temps (s)")
        ax2.set_ylabel("Vitesse (m/s)")
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

    def animer(self, t, y):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, max(y) + 1)
        ax.set_title("Animation de la chute")
        ax.set_xlabel("Position horizontale fixe")
        ax.set_ylabel("Hauteur (m)")
        ax.axhline(0, color='black', linewidth=1)  # sol visible

        point, = ax.plot([0.5], [y[0]], 'ro', markersize=10)  # point initial visible

        def update(frame):
            point.set_data([0.5], [y[frame]])
            return point,

        ani = animation.FuncAnimation(fig, update, frames=len(t), interval=30, blit=True, repeat=False)
        plt.show()


class InterfaceSimulation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulateur de chute libre")

        self.resultat = tk.StringVar()

        self._creer_widgets()
        self.root.mainloop()

    def _creer_widgets(self):
        labels = ["Masse (kg)", "Frottement k (kg/s)", "Hauteur initiale (m)", "Pas de temps (s)", "Durée max (s)"]
        defaults = ["2", "0.3", "10", "0.01", "20"]
        self.entries = []

        for i, (label, default) in enumerate(zip(labels, defaults)):
            tk.Label(self.root, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(self.root)
            entry.grid(row=i, column=1)
            entry.insert(0, default)
            self.entries.append(entry)

        tk.Button(self.root, text="Lancer la simulation", command=self.simuler).grid(row=5, column=0, pady=10)
        tk.Button(self.root, text="Afficher animation", command=self.animer).grid(row=5, column=1, pady=10)

        tk.Label(self.root, textvariable=self.resultat, justify="left").grid(row=6, column=0, columnspan=2)

    def simuler(self):
        try:
            m, k, y0, dt, t_max = map(lambda e: float(e.get()), self.entries)
            simulateur = ChuteLibre(m, k, y0, dt, t_max)

            t1, v1, y1 = simulateur.simuler_avec_frottement()
            t2, v2, y2 = simulateur.simuler_sans_frottement()

            t_min = min(len(t1), len(t2))
            t = t1[:t_min]
            v1, v2 = v1[:t_min], v2[:t_min]
            y1, y2 = y1[:t_min], y2[:t_min]

            temps = round(t[-1], 2)
            v_fin = round(v1[-1], 2)
            v_lim = round(simulateur.vitesse_limite(), 2)

            phrase = (
                f"\U0001F4CA Résultats de la simulation :\n"
                f"- \u23F1 Temps total de chute : {temps} secondes\n"
                f"- \U0001F4A8 Vitesse finale atteinte : {v_fin} m/s\n"
                f"- \U0001F9EE Vitesse limite théorique : {v_lim} m/s\n"
                f"\n\U0001F4DD Comparaison avec chute sans frottement :\n"
                f"- Chute plus rapide sans frottement\n"
                f"- Vitesse augmente sans limite sans résistance de l’air"
            )
            self.resultat.set(phrase)

            simulateur.tracer_graphiques(t, y1, y2, v1, v2)
            simulateur.exporter_csv(t, v1, v2, y1, y2)

        except Exception as e:
            self.resultat.set(f"Erreur : {e}")

    def animer(self):
        try:
            m, k, y0, dt, t_max = map(lambda e: float(e.get()), self.entries)
            simulateur = ChuteLibre(m, k, y0, dt, t_max)
            t, v, y = simulateur.simuler_avec_frottement()
            simulateur.animer(t, y)
        except Exception as e:
            self.resultat.set(f"Erreur animation : {e}")

if __name__ == '__main__':
    InterfaceSimulation()
