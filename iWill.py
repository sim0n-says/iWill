import os
import re
from PyQt5.QtWidgets import (
    QFileDialog, QVBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QCheckBox, QProgressBar, QLineEdit, QDockWidget, QWidget
)
from PyQt5.QtCore import Qt
from datetime import datetime
from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes

class ShapefileLoader(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inspecteur Will")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        
        self.init_ui()
        
    def init_ui(self):
        # Bouton pour sélectionner un répertoire
        self.select_button = QPushButton("Sélectionner un répertoire")
        self.select_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.select_button)
        
        # Checkbox pour afficher le type de géométrie
        self.show_geometry_type_checkbox = QCheckBox("Afficher le type de géométrie")
        self.layout.addWidget(self.show_geometry_type_checkbox)
        
        # Barre de recherche pour filtrer les fichiers
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un fichier...")
        self.search_bar.textChanged.connect(self.filter_files)
        self.layout.addWidget(self.search_bar)
        
        # Liste des fichiers avec 5 colonnes
        self.file_list = QTreeWidget()
        self.file_list.setColumnCount(5)
        self.file_list.setHeaderLabels(["Nom du fichier", "Date de modification", "Répertoire", "Type de géométrie", "Extension"])
        self.file_list.setSortingEnabled(True)  # Activer le tri
        self.file_list.sortItems(1, Qt.AscendingOrder)  # Trier par date par défaut
        self.file_list.setSelectionMode(QTreeWidget.MultiSelection)  # Permettre la sélection multiple
        self.file_list.itemSelectionChanged.connect(self.update_checkboxes)  # Connecter l'événement de changement de sélection
        self.layout.addWidget(self.file_list)
        
        # Bouton pour charger les couches sélectionnées
        self.load_button = QPushButton("Charger les couches sélectionnées")
        self.load_button.clicked.connect(self.load_selected_layers)
        self.layout.addWidget(self.load_button)
        
        # Barre de progression pour afficher l'état du traitement des fichiers
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)  # Centrer le texte
        self.layout.addWidget(self.progress_bar)
        
        self.all_files = []  # Stocker tous les fichiers pour le filtrage
    
    def select_directory(self):
        # Ouvrir une boîte de dialogue pour sélectionner un répertoire
        directory = QFileDialog.getExistingDirectory(self, "Sélectionner un répertoire")
        if directory:
            self.list_shapefiles(directory)
    
    def list_shapefiles(self, directory):
        # Lister tous les fichiers shapefiles dans le répertoire sélectionné
        self.file_list.clear()
        self.all_files.clear()
        show_geometry_type = self.show_geometry_type_checkbox.isChecked()
        supported_extensions = [".shp", ".gpkg", ".geojson", ".kml", ".csv", ".xlsx", ".xls", ".gdb", ".dbf"]
        files_to_process = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in supported_extensions):
                    file_path = os.path.join(root, file)
                    if os.name == 'nt' and len(file_path) > 256:
                        file_path = f"\\\\?\\{os.path.abspath(file_path)}"
                    files_to_process.append((root, file))
        
        total_files = len(files_to_process)
        self.progress_bar.setMaximum(total_files)
        
        for index, (root, file) in enumerate(files_to_process):
            file_path = os.path.join(root, file)
            if os.name == 'nt' and len(file_path) > 256:
                file_path = f"\\\\?\\{os.path.abspath(file_path)}"
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
            file_extension = os.path.splitext(file)[1]
            geometry_type = ""
            if show_geometry_type and file_extension == ".shp":
                layer = QgsVectorLayer(file_path, file, "ogr")
                if layer.isValid():
                    geometry_type = QgsWkbTypes.displayString(layer.wkbType())
            
            file_info = {
                "file": file,
                "file_path": file_path,
                "file_mtime": file_date,
                "root": root,
                "geometry_type": geometry_type,
                "file_extension": file_extension
            }
            self.all_files.append(file_info)
            self.add_file_item(file_info)
            
            # Mettre à jour la barre de progression
            self.progress_bar.setValue(index + 1)
            percentage = ((index + 1) / total_files) * 100
            self.progress_bar.setFormat(f"Fichiers traités: {index + 1}/{total_files} ({percentage:.2f}%)")
            self.update_progress_bar_color(index + 1, total_files)
    
    def add_file_item(self, file_info):
        # Ajouter un élément de fichier à la liste des fichiers
        file_item = QTreeWidgetItem([file_info["file"], file_info["file_mtime"], file_info["root"], file_info["geometry_type"], file_info["file_extension"]])
        file_item.setData(0, 1, file_info["file_path"])
        file_item.setData(1, Qt.UserRole, file_info["file_mtime"])  # Stocker l'horodatage pour le tri
        file_item.setCheckState(0, 0)  # Ajoute une case à cocher
        self.file_list.addTopLevelItem(file_item)
    
    def update_progress_bar_color(self, value, total):
        # Mettre à jour la couleur de la barre de progression en fonction du pourcentage
        percentage = (value / total) * 100
        if percentage < 50:
            color = "red"
        elif percentage < 80:
            color = "yellow"
        else:
            color = "green"
        self.progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
    
    def filter_files(self):
        # Filtrer les fichiers en fonction du texte de recherche
        search_text = self.search_bar.text().lower()
        search_text = search_text.replace('*', '.*')  # Remplacer le wildcard * par .*
        self.file_list.clear()
        for file_info in self.all_files:
            if re.search(search_text, file_info["file"].lower()):
                self.add_file_item(file_info)
    
    def update_checkboxes(self):
        # Mettre à jour les cases à cocher en fonction de la sélection multiple
        for i in range(self.file_list.topLevelItemCount()):
            item = self.file_list.topLevelItem(i)
            if item.isSelected():
                item.setCheckState(0, Qt.Checked)
            else:
                item.setCheckState(0, Qt.Unchecked)
    
    def load_selected_layers(self):
        # Charger les couches sélectionnées dans QGIS
        for i in range(self.file_list.topLevelItemCount()):
            item = self.file_list.topLevelItem(i)
            if item.checkState(0) == Qt.Checked:  # Vérifie si la case est cochée
                file_path = item.data(0, 1)
                layer = QgsVectorLayer(file_path, os.path.basename(file_path), "ogr")
                if not layer.isValid():
                    print(f"Layer {file_path} failed to load!")
                else:
                    QgsProject.instance().addMapLayer(layer)

# Pour ouvrir la fenêtre de l'outil de manière non modale
def open_shapefile_loader():
    loader = ShapefileLoader()
    loader.setWindowModality(Qt.NonModal)  # fenêtre est non modale
    loader.show()

def initGui(self):
    self.dock_widget = ShapefileLoader()
    self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

def unload(self):
    self.iface.removeDockWidget(self.dock_widget)

open_shapefile_loader()