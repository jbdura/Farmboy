# gallery/models.py
from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.

class Image(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = CloudinaryField('image')

    def save(self, *args, **kwargs):
        if not self.title and self.image:
            self.title = self.image.name.split('/')[-1]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
