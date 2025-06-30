#!/usr/bin/env python
import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import pydicom
from datetime import datetime

# Ajouter le répertoire du projet au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from django.conf import settings
from ai_diagnostic.models import AIModel

def preprocess_dicom_images(dicom_dir, target_size=(224, 224)):
    """Prétraiter les images DICOM pour l'entraînement."""
    images = []
    labels = []
    
    # Parcourir les sous-répertoires (classes)
    for class_name in os.listdir(dicom_dir):
        class_dir = os.path.join(dicom_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
        
        # Attribuer un label numérique à chaque classe
        if class_name == "normal":
            label = 0
        elif class_name == "pneumonia":
            label = 1
        else:
            continue
        
        # Parcourir les fichiers DICOM dans le répertoire de classe
        for filename in os.listdir(class_dir):
            if not filename.endswith('.dcm'):
                continue
            
            file_path = os.path.join(class_dir, filename)
            
            try:
                # Lire le fichier DICOM
                dicom = pydicom.dcmread(file_path)
                
                # Convertir les données de pixel en tableau numpy
                img = dicom.pixel_array
                
                # Normaliser les valeurs de pixel
                img = img / np.max(img)
                
                # Redimensionner l'image
                img = tf.image.resize(img[..., np.newaxis], target_size).numpy()
                
                # Ajouter l'image et le label aux listes
                images.append(img)
                labels.append(label)
            except Exception as e:
                print(f"Erreur lors du traitement de {file_path}: {str(e)}")
    
    return np.array(images), np.array(labels)

def build_model(input_shape=(224, 224, 1), num_classes=2):
    """Construire un modèle CNN pour la classification d'images médicales."""
    model = Sequential([
        # Première couche de convolution
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        
        # Deuxième couche de convolution
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Troisième couche de convolution
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Aplatir les caractéristiques
        Flatten(),
        
        # Couches entièrement connectées
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    # Compiler le modèle
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model(model_name, target_disease, dicom_dir):
    """Entraîner un modèle d'IA pour le diagnostic médical."""
    print(f"Début de l'entraînement du modèle {model_name} pour {target_disease}...")
    
    # Prétraiter les images DICOM
    images, labels = preprocess_dicom_images(dicom_dir)
    
    if len(images) == 0:
        print("Aucune image DICOM trouvée pour l'entraînement.")
        return None
    
    print(f"Nombre d'images chargées: {len(images)}")
    
    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels, test_size=0.2, random_state=42
    )
    
    # Augmentation des données
    datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Construire le modèle
    model = build_model(input_shape=images[0].shape)
    
    # Résumé du modèle
    model.summary()
    
    # Entraîner le modèle
    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=32),
        epochs=20,
        validation_data=(X_test, y_test),
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=3,
                restore_best_weights=True
            )
        ]
    )
    
    # Évaluer le modèle
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Précision du modèle sur l'ensemble de test: {accuracy:.4f}")
    
    # Sauvegarder le modèle
    model_dir = os.path.join(settings.MEDIA_ROOT, 'ai_models')
    os.makedirs(model_dir, exist_ok=True)
    
    model_filename = f"{model_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.h5"
    model_path = os.path.join(model_dir, model_filename)
    
    model.save(model_path)
    print(f"Modèle sauvegardé à {model_path}")
    
    # Enregistrer le modèle dans la base de données
    ai_model = AIModel.objects.create(
        name=model_name,
        description=f"Modèle de classification pour {target_disease}",
        model_type="CLASSIFICATION",
        version=datetime.now().strftime('%Y%m%d'),
        file_path=f"ai_models/{model_filename}",
        target_disease=target_disease,
        accuracy=float(accuracy),
        training_date=datetime.now().date(),
        status="ACTIVE"
    )
    
    print(f"Modèle enregistré dans la base de données avec l'ID {ai_model.id}")
    
    return ai_model

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python ai_model_training.py <model_name> <target_disease> <dicom_dir>")
        sys.exit(1)
    
    model_name = sys.argv[1]
    target_disease = sys.argv[2]
    dicom_dir = sys.argv[3]
    
    train_model(model_name, target_disease, dicom_dir)