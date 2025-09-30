from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Entry(models.Model):
    MOOD_CHOICES = [
    ('happy', 'Happy'),
    ('sad', 'Sad'),
    ('angry', 'Angry'),
    ('anxious', 'Anxious'),
    ('neutral', 'Neutral'),
    ('excited', 'Excited'),
    ('relaxed', 'Relaxed'),
    ('tired', 'Tired'),
    ('confused', 'Confused'),
    ('bored', 'Bored'),
    ('love', 'Love')
]


    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
        default='neutral'
    )
    def __str__(self):
        return self.title