# Slicer Auto ROI

## Ajuster les paramètres du script

Renseigner les paramètres suivants dans le fichier config.json : 

```json
{
    "VolumeBaseName": "MonVolume",
    "InitialPointIJK": [10, 20, 30],
    "RoiName": "MaRoi",
    "RoiSize": [50, 50, 50]
}
```

* VolumeBaseName est le nom du volume sur lequel on va travailler
* InitialPointIJK est le point d'intérêt pour débuter le travail de segmentation
* RoiName est le nom que l'on veux donner à la nouvelle ROI (Region of Interest)
* RoiSize est la taille en millimètre de la nouvelle ROI

## Lancer le script dans slicer

Pour lancer le script dans slicer il faut ouvrir la console python puis taper la commande suivante : 

```bash
exec(open(r"C:\projects\slicer_auto_roi\main.py").read())
```