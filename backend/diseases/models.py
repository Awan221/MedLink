from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class DiseaseCategory(models.Model):
    """Catégorie pour classer les maladies"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icône Font Awesome ou autre")
    
    class Meta:
        verbose_name = "Catégorie de maladie"
        verbose_name_plural = "Catégories de maladies"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Disease(models.Model):
    """Modèle pour les fiches de pathologies"""
    SEVERITY_CHOICES = [
        ('low', 'Faible'),
        ('moderate', 'Modérée'),
        ('high', 'Grave'),
        ('severe', 'Très grave'),
    ]
    
    # Informations de base
    name = models.CharField(max_length=200, verbose_name="Nom de la maladie")
    scientific_name = models.CharField(max_length=200, blank=True, verbose_name="Nom scientifique")
    slug = models.SlugField(max_length=220, unique=True)
    category = models.ForeignKey(
        DiseaseCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='diseases',
        verbose_name="Catégorie"
    )
    
    # Description
    short_description = models.TextField(verbose_name="Description courte")
    description = models.TextField(verbose_name="Description détaillée")
    causes = models.TextField(verbose_name="Causes", blank=True)
    risk_factors = models.TextField(verbose_name="Facteurs de risque", blank=True)
    
    # Symptômes
    main_symptoms = models.TextField(verbose_name="Symptômes principaux")
    other_symptoms = models.TextField(verbose_name="Autres symptômes", blank=True)
    when_to_see_doctor = models.TextField(verbose_name="Quand consulter un médecin", blank=True)
    
    # Diagnostic et traitement
    diagnosis = models.TextField(verbose_name="Diagnostic", blank=True)
    treatment = models.TextField(verbose_name="Traitement", blank=True)
    prevention = models.TextField(verbose_name="Prévention", blank=True)
    
    # Métadonnées
    severity = models.CharField(
        max_length=20, 
        choices=SEVERITY_CHOICES, 
        default='moderate',
        verbose_name="Gravité"
    )
    is_contagious = models.BooleanField(default=False, verbose_name="Contagieux")
    is_chronic = models.BooleanField(default=False, verbose_name="Maladie chronique")
    
    # Champs de recherche
    search_vector = SearchVectorField(null=True, blank=True)
    
    # Métadonnées administratives
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_reviewed = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Maladie"
        verbose_name_plural = "Maladies"
        ordering = ['name']
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['severity']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class DiseaseSymptom(models.Model):
    """Symptômes spécifiques liés aux maladies"""
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='symptoms_list')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_common = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Symptôme"
        verbose_name_plural = "Symptômes"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.disease.name})"

class DiseaseTreatment(models.Model):
    """Traitements spécifiques pour les maladies"""
    TREATMENT_TYPES = [
        ('medication', 'Médicament'),
        ('surgery', 'Chirurgie'),
        ('therapy', 'Thérapie'),
        ('lifestyle', 'Mode de vie'),
        ('other', 'Autre'),
    ]
    
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='treatments')
    name = models.CharField(max_length=200)
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPES)
    description = models.TextField()
    effectiveness = models.PositiveSmallIntegerField(
        help_text="Efficacité sur une échelle de 1 à 10",
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Traitement"
        verbose_name_plural = "Traitements"
        ordering = ['treatment_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_treatment_type_display()}) pour {self.disease.name}"
