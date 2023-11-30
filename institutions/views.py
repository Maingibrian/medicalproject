from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django.contrib.auth.decorators import login_required
from reportlab.platypus import TableStyle

from members.decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from members.forms import *
from members.models import institution

from django.http import FileResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from members.filters import *


@login_required(login_url="members/login")
@admin_only
@allowed_users(allowed_roles=["county workers"])
def main (request):
    institutions = institution.objects.all()
    template = loader.get_template("main_page.html")
    myFilter = institutionfilter(request.GET, queryset=institutions)
    institutions = myFilter.qs
    context = {
        "myFilter": myFilter,
        "institutions": institutions,
    }
    return HttpResponse(template.render(context, request))
def institutions(request):
    institutions = institution.objects.all()
    template = loader.get_template('institutionTable.html')
    myFilter = institutionfilter(request.GET, queryset=institutions)
    institutions = myFilter.qs
    context = {
        "myFilter": myFilter,
        "institutions": institutions,
    }
    return HttpResponse(template.render(context, request))



def Home2 (request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user, is_read=False)
    institutions = institution.objects.all().values()
    med = MedicationDistribution.objects.all()
    mymeds = medication_package.objects.all()
    template = loader.get_template("Home2.html")
    myFilter2 = filterauditor(request.GET, queryset=institutions)
    institutions = myFilter2.qs

    if request.method == 'POST':
        form = MedicationDistributionForm(request.POST)
        if form.is_valid():
            distribution = form.save(commit=False)
            package = distribution.package
            if distribution.quantity > package.quantity:
                # Handle error here, quantity exceeds recorded quantity
                pass
            else:
                # Set the creator before saving
                form.instance.creator = request.user
                distribution.save()
                # Update the quantity in the medication package
                package.quantity -= distribution.quantity
                package.save()
                return redirect("Home2")
    else:
        form = MedicationDistributionForm()
    context = {
        'notifications': notifications,
        "myFilter2": myFilter2,
        "med": med,
        "institutions": institutions,
        "mymeds": mymeds,
        "form": form,
    }
    return HttpResponse(template.render(context, request))


@allowed_users(allowed_roles=["auditor"])
def auditorHome (request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user, is_read=False)
    institutions = institution.objects.all().values()
    med = MedicationDistribution.objects.all()
    mymeds = medication_package.objects.all()
    template = loader.get_template("auditorHome.html")
    myFilter2 = filterauditor(request.GET, queryset=institutions)
    institutions = myFilter2.qs

    if request.method == 'POST':
        form = MedicationDistributionForm(request.POST)
        if form.is_valid():
            distribution = form.save(commit=False)
            package = distribution.package
            if distribution.quantity > package.quantity:
                # Handle error here, quantity exceeds recorded quantity
                pass
            else:
                distribution.save()
                # Update the quantity in the medication package
                package.quantity -= distribution.quantity
                package.save()
                return redirect("auditorHome")
    else:
        form = MedicationDistributionForm()
    context = {
        'notifications': notifications,
        "myFilter2": myFilter2,
        "med": med,
        "institutions": institutions,
        "mymeds": mymeds,
        "form": form,
    }
    return HttpResponse(template.render(context, request))

def delete_med_distribution(request, pk):
    package = MedicationDistribution.objects.get(id=pk)
    if request.method == 'POST':
        package.delete()
    context = { "package": package}
    return render(request, "deletemed.html", context)

def institution_details(request, pk):
    Institution = institution.objects.get(id=pk)

    info = institution.MedicationDistribution_set.all()
    context = {
        "Institution": Institution,
        "info": info
    }
    return  render(request,"institution_details.html", context)


@login_required(login_url="members/login")

def new_institution (request):
    form = institutionForm()
    if request.method == 'POST':
        form = institutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("institutions")

    context = {"form": form}
    return render(request, "institutionForm.html", context)


@login_required(login_url="members/login")

def update_institution(request, pk):

    package = institution.objects.get(id=pk)
    form = institutionForm(instance=package)
    if request.method == 'POST':
        form = institutionForm(request.POST,instance=package )
        if form.is_valid():
            form.save()
            return redirect("institutions")

    context = {"form": form}
    return render(request, "institutionForm.html", context)

@login_required(login_url="members/login")

def delete_institution(request, pk):
    package = institution.objects.get(id=pk)
    if request.method == 'POST':
        package.delete()
        return redirect("institutions")
    context = { "item": package}
    return render(request, "delete_institution.html", context)

@login_required(login_url="members/login")
def admin_report(request):
    buf = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buf, pagesize=letter)

    # Create a list to store data for the table
    data = []

    # Define table headers
    table_headers = ["Ofiicer Name",  "Package ID", "Medication Name", "Batch Number", "Quantity", "Status"]

    # Add the headers as the first row in the data list
    data.append(table_headers)

    medication_packages = medication_package.objects.all()

    for package in medication_packages:
        # Append different types of data to the data list
        row = [
            package.creator,
            str(package.id),
            package.medicationName,
            package.batchNumber,
            str(package.quantity),
            package.status,
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
    response = FileResponse(buf, as_attachment=True, filename='admin_report.pdf')
    return response
