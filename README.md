# 🖐️ Hand Mouse Control with OpenCV & MediaPipe

Ce projet permet de contrôler la souris de l’ordinateur à l’aide des mouvements de la main en temps réel, en utilisant la webcam.  
Il repose sur la détection de la main avec **MediaPipe**, le traitement vidéo avec **OpenCV**, et le contrôle de la souris avec **PyAutoGUI**.

---

## 🚀 Fonctionnalités

- Détection de la main en temps réel via la webcam
- Suivi du bout de l’index pour déplacer le curseur de la souris
- Simulation d’un clic de souris par geste de **pincement** (index + pouce)
- Affichage visuel des points de la main et du geste de clic

---

## 🛠️ Technologies utilisées

- **Python**
- **OpenCV** : capture et traitement vidéo
- **MediaPipe Hands** : détection et suivi des points de la main
- **PyAutoGUI** : contrôle du curseur et clic de la souris
- **Math** : calcul de distance entre les doigts

--
## 📦 Installation
```bash
pip install opencv-python mediapipe pyautogui
```
lancer le projet 
```bash
python mouse.py
```

