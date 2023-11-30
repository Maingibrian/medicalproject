from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class medication_packageForm(ModelForm):
    class Meta:
        model = medication_package
        fields = ['medicationName', "batchNumber", "expiryDate","quantity","status"]

class CreateUserForm(UserCreationForm):
    institution = forms.ModelChoiceField(queryset=institution.objects.all(), required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('institution',)

class  institutionForm(ModelForm):
    class Meta:
        model = institution
        fields = ['institution_ID', 'name', "location"]

class userForm(ModelForm):
    class Meta:
        model = medication_package
        fields = ['quantity', 'status']




class MedicationDistributionForm(forms.ModelForm):
    class Meta:
        model = MedicationDistribution
        fields = ['package', 'institution', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        package = self.cleaned_data['package']

        # Check if the entered quantity is below 0
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be below 0.")

        # Check if the entered quantity exceeds the available quantity in the package
        if quantity > package.quantity:
            raise forms.ValidationError(f"Quantity exceeds available quantity in the package ({package.quantity}).")

        return quantity



from django import forms
from django.core.exceptions import ValidationError

class MedicationDistributionFormUser(forms.ModelForm):
    class Meta:
        model = MedicationDistribution
        fields = ['quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity is not None:
            if quantity < 0:
                raise ValidationError('Quantity must be greater than or equal to 0.')
            if quantity > self.instance.quantity:
                raise ValidationError('Quantity must be less than or equal to the preallocated quantity.')

        return quantity


