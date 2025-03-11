# Slicer Auto ROI Utility

Ce petit utilitaire pour 3D Slicer permet de créer et d'ajuster automatiquement une ROI (Region Of Interest) à partir d'un point d'intérêt défini dans un volume.

## Fonctionnalités

- **Création automatique d'une ROI**
  - Conversion d'un point d'intérêt en coordonnées IJK vers RAS à l'aide de la matrice de transformation du volume de référence
  - Création d'un nœud ROI avec un nom et une taille définis

- **Ajustement de la position de la ROI**
  - Possibilité de décaler le centre de la ROI pour aligner une de ses faces (top, bottom, front, back, right ou left) sur le point d'intérêt

- **Configuration centralisée**
  - Tous les paramètres (nom du volume, point initial IJK, nom de la ROI, taille, face de centrage) sont définis dans le fichier `config.json`

## Fichiers du Projet

### auto_roi_create.py
Script qui :
- Charge la configuration depuis `config.json`
- Convertit le point IJK en coordonnées RAS à partir du volume de référence
- Crée un nœud ROI avec le nom (`RoiName`) et la taille (`RoiSize`) spécifiés
- Positionne le centre initial du ROI sur le point converti

### auto_roi_center.py
Script qui :
- Recharge la configuration depuis `config.json`
- Récupère le nœud ROI par son nom
- Calcule un nouveau centre pour le ROI en fonction de la face à aligner (définie par `RoiCenteringFace`)
- Met à jour la position du ROI

### config.json
Fichier de configuration contenant les paramètres d'exécution. Exemple de contenu :

```json
{
    "VolumeBaseName": "2: A PERFORANTES",
    "InitialPointIJK": [252, 148, 294],
    "RoiName": "MyCustomROI",
    "RoiSize": [20, 35, 20],
    "RoiCenteringFace": "front"
}
```

#### Paramètres de configuration
- **VolumeBaseName** : Nom du volume de référence (il doit être chargé dans Slicer)
- **InitialPointIJK** : Point d'intérêt en coordonnées IJK dans le volume
- **RoiName** : Nom attribué au nœud ROI
- **RoiSize** : Taille de la ROI en millimètres sous la forme `[largeur, hauteur, profondeur]`
- **RoiCenteringFace** : Face sur laquelle centrer le ROI ("none", "top", "bottom", "front", "back", "right", "left")

### readme.md
Ce fichier de documentation.

## Prérequis

- 3D Slicer (version 5.8.0 testée)
- Le module Python intégré (VTK est fourni avec Slicer)
- Les fichiers du projet doivent être placés dans un répertoire accessible (par exemple, `C:\projects\slicer_auto_roi\`)

## Utilisation

### 1. Création de la ROI

1. Ouvrez 3D Slicer et chargez le volume référencé (dont le nom doit correspondre à `VolumeBaseName` dans `config.json`)
2. Ouvrez la console Python (menu **View → Python Interactor** ou utilisez le raccourci `Ctrl+3` / `Cmd+3`)
3. Exécutez le script de création en tapant dans la console :

```python
exec(open(r"C:\projects\slicer_auto_roi\auto_roi_create.py").read())
```

Ce script va :
- Charger la configuration
- Convertir le point IJK en coordonnées RAS
- Créer le nœud ROI avec le nom et la taille définis
- Positionner initialement le ROI sur le point converti

### 2. Ajustement (Centrage) de la ROI

Une fois la ROI créée et visible dans la scène de Slicer, vous pouvez ajuster son positionnement pour aligner une face précise.

Dans la console Python, exécutez :

```python
exec(open(r"C:\projects\slicer_auto_roi\auto_roi_center.py").read())
```

Ce script va :
- Recharger la configuration
- Récupérer le nœud ROI à partir du nom (`RoiName`)
- Calculer le décalage nécessaire pour centrer la face spécifiée (par exemple "front")
- Mettre à jour le centre du ROI

## Dépannage

### ROI ou volume introuvable
- Vérifiez que le volume et la ROI existent dans la scène et que leurs noms correspondent exactement à ceux définis dans `config.json`
- Pour lister les nœuds disponibles, utilisez dans la console :

```python
print([node.GetName() for node in slicer.util.getNodesByClass("vtkMRMLMarkupsROINode")])
print([node.GetName() for node in slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode")])
```

### Erreur de conversion IJK → RAS
- Assurez-vous que le volume possède bien une matrice de transformation IJK-to-RAS et que le point IJK est correct

### Problèmes de chemin
- Vérifiez que les chemins spécifiés dans les appels `open()` correspondent à l'emplacement réel de vos fichiers

### Crash de Slicer
- Consultez la console Python pour obtenir des messages d'erreur détaillés et assurez-vous que tous les nœuds nécessaires existent dans la scène