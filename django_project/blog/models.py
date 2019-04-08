from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    hit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_posted']

    def approved(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.author.username
