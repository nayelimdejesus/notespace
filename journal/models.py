from django.db import models

# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title