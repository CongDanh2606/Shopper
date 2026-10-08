from django.db import models
from django.conf import settings

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Rate(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='raitings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    class Meta: 
        unique_together = ('blog', 'user')

    def __str__(self):
        return f"{self.user} đánh giá {self.blog}: {self.rate} sao tại {self.created_at}"

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cmt = models.TextField()
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Coment {self.id} by {self.user.username}"