from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.forms import  UserCreationForm
from .forms import CreateUserForm
from .models import  *
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.template import loader
from .models import institution
from django.contrib.auth.decorators import login_required
from members.decorators import *
from django.contrib.auth.models import Group
from django.http import FileResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from reportlab.lib.pagesizes import letter


def login_user(request):

        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/home")
            else:
                messages.success(request, "There was an error logging in. Try again!")
                return redirect('login')
        else:
            return render(request, 'registration/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out")
    return redirect('login')

@login_required(login_url="members/login")
@allowed_users(allowed_roles=["county workers"])
def register_user(request):
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)  # Process the custom form
            if form.is_valid():
                # Create the user
                user = form.save()

                # Associate the user with the selected institution
                institution_id = form.cleaned_data['institution'].id
                institution_obj = institution.objects.get(id=institution_id)
                institution_obj.user = user
                institution_obj.save()

                username = form.cleaned_data['username']

                group = Group.objects.get(name="Medical institution workers")
                user.groups.add(group)
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, "Registration is successful, " + username)
                return redirect('login')
        else:
            form = CreateUserForm()

        return render(request, "registration/register_user.html" , {
        'form': form,
    })


@login_required(login_url="members/login")
@allowed_users(allowed_roles=["county workers"])
def medication (request):
    mymeds = medication_package.objects.all().values()
    template = loader.get_template('medication.html')
    context = {
        "mymeds": mymeds,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url="members/login")

def new_med(request):
    form = medication_packageForm()
    if request.method == 'POST':
        form = medication_packageForm(request.POST)
        if form.is_valid():
            # Set the creator before saving
            form.instance.creator = request.user
            form.save()

    context = {"form": form}
    return render(request, "new_medForm.html", context)

@login_required(login_url="members/login")

def update_med(request, pk):
    package = medication_package.objects.get(id=pk)
    form = medication_packageForm(instance=package)
    if request.method == 'POST':
        form = medication_packageForm(request.POST, instance=package)  # Use medication_packageForm here
        if form.is_valid():
            form.save()
            return redirect("medication")

    context = {"form": form}
    return render(request, "new_medForm.html", context)

@login_required(login_url="members/login")
def delete_med(request, pk):
    package = medication_package.objects.get(id=pk)
    if request.method == 'POST':
        package.delete()
        return redirect("medication")
    context = { "item": package}
    return render(request, "deletemed.html", context)
@login_required(login_url="members/login")
def delete_med_distributed(request, pk):
    package = MedicationDistribution.objects.get(id=pk)
    if request.method == 'POST':
        package.delete()
        return redirect("Home2")
    context = { "item": package}
    return render(request, "delete_distributed.html", context)


@login_required(login_url="members/login")
@allowed_users(allowed_roles=["Medical institution workers"])
def user_page(request):
    try:
        # Access the user's institution using the OneToOneField
        user_institution = request.user.institution

        # Fetch the medications associated with the user's institution
        user_medication_packages = MedicationDistribution.objects.filter(institution=user_institution)

    except ObjectDoesNotExist:
        user_institution = None
        user_medication_packages = None

    context = {
        "user_institution": user_institution,
        "user_medication_packages": user_medication_packages,
    }
    return render(request, "user_page.html", context)

@login_required(login_url="members/login")
@allowed_users(allowed_roles=["Medical institution workers"])
def user_report(request):
    buf = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buf, pagesize=letter)

    # Create a list to store data for the table
    data = []

    # Define table headers
    table_headers = ["Medication Name", "expiryDate ", "Quantity", "batchNumber","status"]

    # Add the headers as the first row in the data list
    data.append(table_headers)

    # Retrieve the medication packages associated with the current user
    user = request.user  # Get the current user
    medication_packages = MedicationDistribution.objects.filter(institution__user=user)

    for venue in medication_packages:
        # Append different types of data to the data list
        row = [
            venue.package.medicationName,
            venue.package.expiryDate,
            str(venue.quantity),
            venue.package.batchNumber,
            venue.package.status,
        ]
        data.append(row)

    # Create the table
    table = Table(data)

    # Define the style for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)

    # Build the PDF document
    elements = []
    elements.append(table)
    doc.build(elements)

    buf.seek(0)

    # Return the PDF as a response
    response = FileResponse(buf, as_attachment=True, filename='user_report.pdf')
    return response

@login_required(login_url="members/login")
@allowed_users(allowed_roles=["Medical institution workers"])
def user_update_med(request, pk):
    packager = medication_package.objects.get(id=pk)
    form = userForm(instance=packager)
    if request.method == 'POST':
        form = userForm(request.POST, instance=packager)
        if form.is_valid():
            if packager.quantity < 5:
                institution = packager.Institution.name
                message = f"Low stock at {institution}: {packager.medicationName} is running low. The Current quantity is: {packager.quantity}."
                users = User.objects.all()
                for user in users:
                    notification = Notification(recipient=user, message=message, package=packager)
                    notification.save()
            form.save()
            return redirect("user_page")

    else:
        form = userForm(instance=packager)

    context = {
        'form': form,
        'packager': packager,
    }

    return render(request, "userForm.html", context)


@login_required(login_url="members/login")

def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user, is_read=False)

    context = {
        'notifications': notifications
    }
    return render(request, 'notifications.html', context)

@login_required(login_url="members/login")

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)

    # Check if the notification belongs to the logged-in user
    if notification.recipient == request.user:
        notification.is_read = True
        notification.save()
        return render(request, 'mark_notification_as_read.html')


@login_required(login_url="members/login")
def user_update_distribution(request, pk):
    distribution = get_object_or_404(MedicationDistribution, id=pk)
    form = MedicationDistributionFormUser(instance=distribution)

    if request.method == 'POST':
        form = MedicationDistributionFormUser(request.POST, instance=distribution)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']

            # Check if the new quantity is within acceptable bounds
            if 0 <= new_quantity <= distribution.package.quantity:
                # Check if the new quantity does not exceed the allocated quantity for the institution
                form.save()

                # Check if the quantity is below 5 and trigger a notification
                if new_quantity < 5:
                    institution = distribution.institution.name
                    message = f"Low stock at {institution}: {distribution.package.medicationName} is running low. The Current quantity is: {new_quantity}."
                    users = User.objects.all()
                    for user in users:
                        notification = Notification(recipient=user, message=message, package=distribution)
                        notification.save()

                return redirect("user_page")
            else:
                form.add_error('quantity', 'Quantity must be between 0 and the preallocated quantity.')

    context = {
        'form': form,
        'distribution': distribution,
    }

    return render(request, "userForm.html", context)
