import django_filters
from .models import *


class institutionfilter(django_filters.FilterSet):
    class Meta:
        model = institution
        fields = ['location']

class filterauditor(django_filters.FilterSet):
    class Meta:
        model = institution
        fields = ['location']
