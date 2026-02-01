# 🖐️ Hand Tracking & Hand Mouse Control with OpenCV

Ce repository contient deux projets basés sur la **vision par ordinateur** permettant :
1. La détection et le suivi des mains en temps réel
2. Le contrôle de la souris à l’aide des gestes de la main

Les deux scripts utilisent **OpenCV** pour la capture vidéo et **MediaPipe Hands** pour la détection des points clés de la main.

##  Objectifs du projet

- Comprendre le fonctionnement de **MediaPipe Hands**
- Manipuler les **landmarks** (points clés) de la main
- Appliquer la vision par ordinateur à une interaction homme–machine
- Contrôler des périphériques (souris) via des gestes naturels

##  Scripts inclus
### Hand Tracking – Détection et suivi des mains

 #### Fichier : `hand_tracking.py`

Ce script permet de détecter jusqu’à **deux mains** et d’afficher :
- Les **21 points clés (landmarks)** de chaque main
- Les **connexions** entre les doigts

#### Fonctionnalités :
- Capture vidéo via la webcam
- Détection et suivi des mains en temps réel
- Affichage graphique des landmarks et des connexions
- Arrêt du programme avec la touche **q**

 Lancer le script :
```bash
python hand_tracking.py
```

### Hand Mouse Control – Contrôle de la souris par gestes

#### Fichier :  `hand_mouse_control.py `

Ce script permet de contrôler la souris de l’ordinateur à l’aide de la main :
- Le bout de l’index permet de déplacer le curseur
- Le pincement entre l’index et le pouce simule un clic de souris

#### Fonctionnalités :
- Détection de la main en temps réel via la webcam
- Suivi du bout de l’index pour déplacer le curseur de la souris
- Simulation d’un clic de souris par geste de **pincement** (index + pouce)
- Affichage visuel des points de la main et du geste de clic

 Lancer le script :
```bash
hand_mouse_control.py
```

##  Technologies utilisées

- **Python**
- **OpenCV** : capture et traitement vidéo
- **MediaPipe Hands** : détection et suivi des points de la main
- **PyAutoGUI** : contrôle du curseur et clic de la souris
- **Math** : calcul de distance entre les doigts

## Installation
```bash
pip install opencv-python mediapipe pyautogui
```

