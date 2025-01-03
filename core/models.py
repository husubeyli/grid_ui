from django.db import models


class TestCase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    github_url = models.URLField()
    status = models.CharField(max_length=20, default='Pending')
    execution_result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
