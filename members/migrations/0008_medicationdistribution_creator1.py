# Generated by Django 4.1.7 on 2023-11-28 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0007_remove_medication_package_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicationdistribution',
            name='creator1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Created_packages', to=settings.AUTH_USER_MODEL),
        ),
    ]
