from django.db import models
from django.contrib.auth.models import User

class institution(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)

    institution_ID = models.IntegerField( null=True,)
    name = models.CharField(null=True,  max_length=255)
    location = models.CharField(null=True, max_length=255)

    def __str__(self):
        return (f"{self.name}  " )

class County_Health_Worker(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)

    workerID = models.IntegerField( null=True,)
    fullName = models.CharField(max_length=255)
    designation = models.CharField(null=True, max_length=255)

    def __str__(self):
        return (f"{self.fullName} + \n + {self.designation}" )

class medication_package(models.Model):
    STATUS = (
        ("Pending", 'pending'),
        ("Delivered", 'Delivered')
    )
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='created_packages')
    county_Health_Worker = models.ForeignKey(County_Health_Worker, null=True, on_delete=models.SET_NULL)
    medicationName = models.CharField(null=True, max_length=255)
    batchNumber = models.CharField(null=True, max_length=255)
    expiryDate = models.DateField(null=True)
    quantity = models.IntegerField(null=True)
    status = models.CharField(null=True, max_length=255, choices=STATUS)

    def __str__(self):
        return f"{self.medicationName}"
        return f"{self.quantity}"
        return f"{self.packageID}"
        return f"{self.expiryDate}"


class MedicationDistribution(models.Model):
    creator1 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='Created_packages')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    package = models.ForeignKey(medication_package, on_delete=models.CASCADE,null=True,)
    institution = models.ForeignKey(institution, on_delete=models.CASCADE,null=True,)
    quantity = models.IntegerField(null=True,)

    def __str__(self):
        return f"{self.package.medicationName} to {self.institution.name}"




class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True,)
    message = models.TextField(null=True,)
    package = models.ForeignKey(MedicationDistribution, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True,)
    is_read = models.BooleanField(default=False, null=True,)

    def __str__(self):
        return self.message

class auditor(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE,)

    auditorID = models.IntegerField(null=True, )
    auditorName = models.CharField(max_length=255,null=True,)
    designation = models.CharField(null=True, max_length=255)