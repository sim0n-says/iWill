# Plugin QGIS - Inspecteur Will

## Vue d'ensemble
iWill est un plugin QGIS conçu pour faciliter la rechercher et le chargement des fichiers "shapefile" etc. 
Il offre une interface conviviale pour sélectionner des répertoires, filtrer des fichiers et charger les couches sélectionnées dans l'environnement QGIS.

## Fonctionnalités
- Sélectionner un répertoire pour parcourir les fichiers shapefile.
- Filtrer les fichiers à l'aide d'une barre de recherche.
- Afficher les détails des fichiers, y compris la date de modification, le type de géométrie et l'extension du fichier.
- Charger les fichiers shapefile sélectionnés dans QGIS.
- Barre de progression pour indiquer l'état de chargement.

## Installation
1. Cloner le dépôt ou télécharger les fichiers du plugin.
2. Placer le dossier `iWill` dans le répertoire des plugins de QGIS. Il est généralement situé à :
   - **Windows:** `C:\Users\<VotreNomUtilisateur>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
   - **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
   - **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`
3. Ouvrir QGIS et naviguer vers le menu Plugins.
4. Sélectionner "Gérer et installer les plugins".
5. Trouver `iWill` dans la liste et cliquer sur "Installer".

## Utilisation
- Après l'installation, vous verrez l'icône iWill dans la barre d'outils de QGIS.
- Cliquez sur l'icône pour ouvrir la boîte de dialogue iWill.
- Utilisez le bouton "Sélectionner un répertoire" pour choisir un répertoire contenant des fichiers shapefile.
- Utilisez la barre de recherche pour filtrer les fichiers affichés.
- Cochez la case "Afficher le type de géométrie" pour voir les types de géométrie.
- Sélectionnez les fichiers shapefile souhaités et cliquez sur "Charger les couches sélectionnées" pour les charger dans QGIS.

## Exigences
- QGIS 3.x
- Python 3.x
- PyQt5

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
