from django.contrib import admin
from .models import *

admin.site.register(institution)

admin.site.register(County_Health_Worker)

admin.site.register(medication_package)

admin.site.register(MedicationDistribution)