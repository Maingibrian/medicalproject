from django.db import models



class institution(models.Model):

    institution_ID = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    location =models.CharField(null=True, max_length=255)

    def __str__(self):
        return f"{self.name}"
