# RL

### Contexte
* Agent : serpent  
* Système : grille dans laquelle évolue le serpent

### Markov Decision Process
* State : position horizontale et verticale de la pomme par rapport au serpent, obstacles autour de la tête du serpent (frontières ou queue du serpent)  
* Action : déplacer le serpent à gauche, à droite, en haut ou en bas
* Reward :  
-1 si le serpent a perdu (le serpent est en dehors de la grille de jeu ou s'est mordu la queue)   
+1 si le serpent mange la pomme  

### Stratégie $\epsilon$-greedy pour l'entrainement  
Combiner exploration (avec probabilité $\epsilon$) et exploitation (avec probabilité 1- $\epsilon$)  
Entrainement :  
Sur 40 jeux avec $\epsilon$ = 0.8  
Puis sur 40 jeux avec $\epsilon$ = 0.7  
Puis sur 40 jeux avec $\epsilon$ = 0.1  
Puis sur les jeux suivants avec $\epsilon$ = 0.01

### Start
Pour lancer l'entrainement et la visualisation : exécuter game.py
