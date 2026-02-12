from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.file_name
    
    def is_image(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
        return any(self.file_name.lower().endswith(ext) for ext in image_extensions)
    
    class Meta:
        ordering = ['-uploaded_at']
