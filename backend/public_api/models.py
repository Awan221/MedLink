from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class DiseaseCategory(models.Model):
    """Catégorie de maladies (ex: Cardiologie, Neurologie, etc.)"""
    name = models.CharField(_('Nom de la catégorie'), max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    icon = models.CharField(_('Icône'), max_length=50, blank=True, 
                          help_text="Nom de l'icône (ex: 'heart' pour une icône de cœur)")
    
    class Meta:
        verbose_name = _('Catégorie de maladie')
        verbose_name_plural = _('Catégories de maladies')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Disease(models.Model):
    """Modèle représentant une maladie ou pathologie"""
    SEVERITY_CHOICES = [
        ('L', _('Léger')),
        ('M', _('Modéré')),
        ('S', _('Sévère')),
    ]
    
    name = models.CharField(_('Nom de la maladie'), max_length=200)
    scientific_name = models.CharField(_('Nom scientifique'), max_length=200, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(
        DiseaseCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='diseases',
        verbose_name=_('Catégorie')
    )
    
    # Informations générales
    short_description = models.TextField(_('Description courte'), max_length=300)
    description = models.TextField(_('Description détaillée'))
    
    # Symptômes
    main_symptoms = models.TextField(_('Symptômes principaux'), 
                                   help_text="Un symptôme par ligne")
    other_symptoms = models.TextField(_('Autres symptômes'), blank=True)
    
    # Causes et facteurs de risque
    causes = models.TextField(_('Causes'), blank=True)
    risk_factors = models.TextField(_('Facteurs de risque'), blank=True)
    
    # Diagnostic et traitement
    diagnosis = models.TextField(_('Méthodes de diagnostic'), blank=True)
    treatment = models.TextField(_('Traitements possibles'), blank=True)
    
    # Prévention et pronostic
    prevention = models.TextField(_('Méthodes de prévention'), blank=True)
    prevention_details = models.TextField(_('Détails de prévention'), blank=True)
    when_to_see_doctor = models.TextField(_('Quand consulter un médecin'), blank=True)
    useful_links = models.TextField(_('Liens utiles'), blank=True)
    prognosis = models.TextField(_('Pronostic'), blank=True)
    
    # Gravité et urgence
    severity = models.CharField(
        _('Niveau de gravité'), 
        max_length=1, 
        choices=SEVERITY_CHOICES, 
        default='M'
    )
    is_emergency = models.BooleanField(
        _('Urgence médicale ?'), 
        default=False,
        help_text="Cocher si cette condition nécessite des soins d'urgence"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(_('Date de création'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Dernière mise à jour'), auto_now=True)
    is_published = models.BooleanField(_('Publié'), default=True)
    
    class Meta:
        verbose_name = _('Maladie')
        verbose_name_plural = _('Maladies')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DiseaseResource(models.Model):
    """Ressources supplémentaires pour une maladie (liens, documents, etc.)"""
    RESOURCE_TYPES = [
        ('LINK', _('Lien externe')),
        ('DOCUMENT', _('Document')),
        ('VIDEO', _('Vidéo')),
        ('IMAGE', _('Image')),
    ]
    
    disease = models.ForeignKey(
        Disease, 
        on_delete=models.CASCADE, 
        related_name='resources',
        verbose_name=_('Maladie')
    )
    title = models.CharField(_('Titre'), max_length=200)
    resource_type = models.CharField(
        _('Type de ressource'), 
        max_length=20, 
        choices=RESOURCE_TYPES
    )
    url = models.URLField(_('URL ou chemin'), max_length=500, blank=True)
    file = models.FileField(
        _('Fichier'), 
        upload_to='disease_resources/', 
        blank=True, 
        null=True
    )
    description = models.TextField(_('Description'), blank=True)
    
    class Meta:
        verbose_name = _('Ressource')
        verbose_name_plural = _('Ressources')
    
    def __str__(self):
        return f"{self.get_resource_type_display()} - {self.title}"
