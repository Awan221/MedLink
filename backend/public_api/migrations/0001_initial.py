# Generated by Django 5.2.1 on 2025-06-14 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom de la catégorie')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('icon', models.CharField(blank=True, help_text="Nom de l'icône (ex: 'heart' pour une icône de cœur)", max_length=50, verbose_name='Icône')),
            ],
            options={
                'verbose_name': 'Catégorie de maladie',
                'verbose_name_plural': 'Catégories de maladies',
            },
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nom de la maladie')),
                ('scientific_name', models.CharField(blank=True, max_length=200, verbose_name='Nom scientifique')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('short_description', models.TextField(max_length=300, verbose_name='Description courte')),
                ('description', models.TextField(verbose_name='Description détaillée')),
                ('main_symptoms', models.TextField(help_text='Un symptôme par ligne', verbose_name='Symptômes principaux')),
                ('other_symptoms', models.TextField(blank=True, verbose_name='Autres symptômes')),
                ('causes', models.TextField(blank=True, verbose_name='Causes')),
                ('risk_factors', models.TextField(blank=True, verbose_name='Facteurs de risque')),
                ('diagnosis', models.TextField(blank=True, verbose_name='Méthodes de diagnostic')),
                ('treatment', models.TextField(blank=True, verbose_name='Traitements possibles')),
                ('prevention', models.TextField(blank=True, verbose_name='Méthodes de prévention')),
                ('prognosis', models.TextField(blank=True, verbose_name='Pronostic')),
                ('severity', models.CharField(choices=[('L', 'Léger'), ('M', 'Modéré'), ('S', 'Sévère')], default='M', max_length=1, verbose_name='Niveau de gravité')),
                ('is_emergency', models.BooleanField(default=False, help_text="Cocher si cette condition nécessite des soins d'urgence", verbose_name='Urgence médicale ?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publié')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diseases', to='public_api.diseasecategory', verbose_name='Catégorie')),
            ],
            options={
                'verbose_name': 'Maladie',
                'verbose_name_plural': 'Maladies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DiseaseResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('resource_type', models.CharField(choices=[('LINK', 'Lien externe'), ('DOCUMENT', 'Document'), ('VIDEO', 'Vidéo'), ('IMAGE', 'Image')], max_length=20, verbose_name='Type de ressource')),
                ('url', models.URLField(blank=True, max_length=500, verbose_name='URL ou chemin')),
                ('file', models.FileField(blank=True, null=True, upload_to='disease_resources/', verbose_name='Fichier')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='public_api.disease', verbose_name='Maladie')),
            ],
            options={
                'verbose_name': 'Ressource',
                'verbose_name_plural': 'Ressources',
            },
        ),
    ]
