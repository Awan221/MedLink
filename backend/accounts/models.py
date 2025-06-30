class UserDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=[
        ('LICENCE', 'Licence médicale'),
        ('CERTIFICAT', 'Certificat de spécialité'),
        ('AUTRE', 'Autre document')
    ])
    file = models.FileField(upload_to='user_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.document_type}"

    def clean(self):
        if not self.file:
            raise ValidationError("Le document est requis")
        if self.file.size > 5 * 1024 * 1024:  # 5MB
            raise ValidationError("Le fichier ne doit pas dépasser 5MB")
        if not self.file.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            raise ValidationError("Format de fichier non supporté. Utilisez PDF, JPG, JPEG ou PNG")

    class Meta:
        verbose_name = "Document utilisateur"
        verbose_name_plural = "Documents utilisateur" 