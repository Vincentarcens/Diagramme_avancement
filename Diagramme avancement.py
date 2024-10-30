import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Demande des noms des réactifs et des produits
nom_A = input("Nom du réactif A : ")
nom_B = input("Nom du réactif B : ")
nom_C = input("Nom du produit C : ")
nom_D = input("Nom du réactif D : ")

# Demande des coefficients stoechiométriques des réactifs et des produits
coeff_A = float(input(f"Coefficient stœchiométrique de {nom_A} : "))
coeff_B = float(input(f"Coefficient stœchiométrique de {nom_B} : "))
coeff_C = float(input(f"Coefficient stœchiométrique de {nom_C} : "))
coeff_D = float(input(f"Coefficient stœchiométrique de {nom_D} : "))

# Quantité initiale des réactifs
quantite_initiale_A = float(input(f"Quantité initiale de {nom_A} : "))
quantite_initiale_B = float(input(f"Quantité initiale de {nom_B} : "))

# Calcul de l'avancement où l'un des réactifs est consommé (réactif limitant)
avancement_A_epuise = quantite_initiale_A / coeff_A
avancement_B_epuise = quantite_initiale_B / coeff_B

# L'avancement maximal de la réaction est déterminé par le réactif limitant
avancement_max = min(avancement_A_epuise, avancement_B_epuise)

# Définir le pas d'avancement pour obtenir une bonne résolution
n_points = 100  # Par exemple, 100 points de données
avancement = np.linspace(0, avancement_max, n_points)

# Quantités en fonction de l'avancement
quantite_A = quantite_initiale_A - coeff_A * avancement  # réactif A
quantite_B = quantite_initiale_B - coeff_B * avancement  # réactif B
quantite_C = coeff_C * avancement                       # produit C
quantite_D = coeff_D * avancement                       # produit D

# Calcul du maximum pour l'axe des ordonnées
y_max = max(quantite_initiale_A, quantite_initiale_B, quantite_C[-1], quantite_D[-1]) * 1.1  # un peu d'espace au-dessus

# Préparation des données pour l'animation
# Configuration de la figure et des axes
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3, top=0.85)  # Ajuster pour le slider, le bouton et l'équation
ax.set_ylim(0, y_max)  # Fixer le maximum de l'axe des ordonnées

# Ajouter l'équation de réaction au-dessus du diagramme
equation_text = f"{int(coeff_A)}{nom_A} + {int(coeff_B)}{nom_B} → {int(coeff_C)}{nom_C} + {int(coeff_D)}{nom_D}"
plt.text(0.5, 1.05, equation_text, ha='center', va='center', transform=ax.transAxes, fontsize=14, fontweight='bold')

# Initialisation des barres avec les noms personnalisés
bar_labels = [nom_A, nom_B, nom_C, nom_D]
bar_colors = ['blue', 'orange', 'green', 'red']
bar_container = ax.bar(bar_labels, [quantite_A[0], quantite_B[0], quantite_C[0], quantite_D[0]], color=bar_colors)

# Ajout d'un axe pour le curseur
ax_slider = plt.axes([0.1, 0.15, 0.65, 0.05], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Avancement', 0, avancement_max, valinit=0, valstep=avancement_max / (n_points - 1))

# Fonction pour mettre à jour l'affichage des quantités
annotations = [ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.02, '', ha='center', va='bottom') for b in bar_container]

def update(val):
    avancement_val = slider.val
    frame = int((avancement_val / avancement_max) * (n_points - 1))

    # Mettre à jour les hauteurs et les annotations des barres
    for i, b in enumerate(bar_container):
        if i == 0:
            height = quantite_A[frame]
        elif i == 1:
            height = quantite_B[frame]
        elif i == 2:
            height = quantite_C[frame]
        else:
            height = quantite_D[frame]

        b.set_height(height)

        # Mettre à jour l'annotation pour chaque barre
        annotations[i].set_text(f'{height:.4f}')
        annotations[i].set_y(height + 0.02 if height > 0.02 else height + 0.005)  # Ajuster pour les petites valeurs

    # Désactiver le bouton "Avancer" si l'avancement est maximal
    if avancement_val >= avancement_max:
        button.color = 'lightgrey'  # Indicateur visuel
        button.label.set_text('Terminé')
        button.on_clicked(None)  # Désactiver le clic du bouton
    else:
        button.color = 'lightblue'
        button.label.set_text('Avancer')

    fig.canvas.draw_idle()

# Lier le curseur à la fonction de mise à jour
slider.on_changed(update)

# Ajouter un bouton pour augmenter l'avancement
ax_button = plt.axes([0.8, 0.15, 0.1, 0.05])
button = Button(ax_button, 'Avancer', color='lightblue')

# Utiliser deux fois le pas du slider pour accélérer l'incrément
increment_avancement = 5 * slider.valstep

# Fonction pour augmenter l'avancement
def increase_avancement(event):
    new_val = slider.val + increment_avancement
    if new_val > avancement_max:
        new_val = avancement_max
    slider.set_val(new_val)

button.on_clicked(increase_avancement)

# Ajouter un bouton pour remettre à zéro
ax_reset = plt.axes([0.8, 0.08, 0.1, 0.05])
reset_button = Button(ax_reset, 'Remise à zéro')

# Fonction pour remettre à zéro
def reset_avancement(event):
    slider.set_val(0)
    # Réactiver le bouton "Avancer"
    button.color = 'lightblue'
    button.label.set_text('Avancer')
    button.on_clicked(increase_avancement)

reset_button.on_clicked(reset_avancement)

# Affichage initial
update(0)

# Affichage de la figure avec curseur
plt.show()
