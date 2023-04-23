# RL

## Markov Decision Process
* State : positions du snake et de la nourriture sur l'écran
* Action : déplacer le snake à gauche, à droite, en haut ou en bas
* Reward :  
-1 si game over (le snake est en dehors de l'écran ou se mord la queue)  
-1 si le snake s'éloigne de la nourriture  
1 si le snake se rapproche de la nourriture  
1 si le snake mange  

### Stratégie $\epsilon$-greedy pour l'entrainement  
Combiner exploitation (avec probabilité 1-$\epsilon$) et exploration (avec probabilité $\epsilon$)  
Entrainement sur 100 jeux avec $\epsilon$ = 0.1  
Puis exploitation de l'entrainement sur les jeux suivants ($\epsilon$ = 0)  