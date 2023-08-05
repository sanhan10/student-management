from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Registration
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.core import serializers

def index(request):
    return render(request, "index.html")

@login_required(login_url='adminlogin')  # Redirect unauthenticated users to adminlogin page
def adminclick_view(request):
    return redirect('admin-dashboard')

def afterlogin_view(request):
    return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    return render(request, 'admin/dashboard.html')

@login_required(login_url='adminlogin')
def add_registration_view(request):
    if request.method == 'POST':
        # Retrieve the form data from the POST request
        name = request.POST.get('name')
        address = request.POST.get('address')
        father_name = request.POST.get('father_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')
        class_field = request.POST.get('class')
        remarks = request.POST.get('remarks')

        # Create a Registration object and save it to the database
        registration = Registration(
            name=name,
            address=address,
            father_name=father_name,
            date_of_birth=date_of_birth,
            gender=gender,
            contact_number=contact_number,
            class_field=class_field,
            remarks=remarks,
        )
        registration.save()

        # Show SweetAlert after successful form submission
        messages.success(request, 'Registration successfully added!')

        # Redirect to the same page to clear the form data
        return redirect('add-registration')

    else:
        return render(request, 'admin/add-registration.html')

@login_required(login_url='adminlogin')
def list_registration_view(request):
    # Retrieve all the registrations from the database
    registrations = Registration.objects.all()

    # Get the selected number of entries per page from the 'entries' query parameter
    entries_per_page = int(request.GET.get('entries', 5))  # Default to 5 if not provided

    # Create a Paginator object
    paginator = Paginator(registrations, entries_per_page)

    # Get the current page number from the 'page' query parameter
    page_number = request.GET.get('page')

    # Get the page object for the current page number
    current_page = paginator.get_page(page_number)

    # Search query
    search_query = request.GET.get('q')

    if search_query:
        # Filter registrations based on the search query
        registrations = registrations.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(father_name__icontains=search_query) |
            Q(date_of_birth__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(contact_number__icontains=search_query) |
            Q(class_field__icontains=search_query) |
            Q(remarks__icontains=search_query)
        )

        # Update the Paginator object with the filtered registrations
        paginator = Paginator(registrations, entries_per_page)
        current_page = paginator.get_page(page_number)

    # If it's not an AJAX request, render the template as usual
    return render(request, 'admin/list-registration.html', {'registrations': current_page})
@login_required(login_url='adminlogin')
def update_registration_view(request, registration_id):
    # Retrieve the registration instance
    registration = get_object_or_404(Registration, pk=registration_id)

    if request.method == 'POST':
        # Process the form data and update the registration
        registration.name = request.POST.get('name')
        registration.address = request.POST.get('address')
        registration.father_name = request.POST.get('father_name')

        # Validate and convert the date_of_birth to the correct format
        date_of_birth_str = request.POST.get('date_of_birth')
        try:
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
            registration.date_of_birth = date_of_birth.date()
        except ValueError:
            # Handle the case of an invalid date format
            # You can choose to show an error message or handle it based on your requirements
            pass

        registration.gender = request.POST.get('gender')
        # ... and so on for other form fields ...
        registration.save()
        return redirect('list-registration')

    # Pass the registration data to the template for prefilling the form
    return render(request, 'admin/update-registration.html', {'registration': registration})
@login_required(login_url='adminlogin')
def delete_registration_view(request, registration_id):
    # Retrieve the registration instance
    registration = get_object_or_404(Registration, pk=registration_id)

    if request.method == 'POST':
        # Delete the registration
        registration.delete()
        return redirect('list-registration')

    # Pass the registration data to the template to confirm deletion
    return render(request, 'admin/delete-registration.html', {'registration': registration})

def delete_multiple_registrations_view(request):
    if request.method == 'POST':
        selected_ids = request.POST.get('selected_ids')
        selected_ids = json.loads(selected_ids) if selected_ids else []

        # Delete the selected registrations
        Registration.objects.filter(pk__in=selected_ids).delete()

        # Redirect to the list-registration page
        return redirect('list-registration')
    else:
        return JsonResponse({'message': 'Invalid request method.'})



def forgot_password_view(request):
    return render(request, 'admin/forgot-password.html')

def admin_404(request):
    return render(request, 'admin/404.html')

def admin_password_reset(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        new_password = request.POST['new_password']




        try:
            # Check if the username_or_email exists in the User model (you can customize this to your actual user model)
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            # If the user is not found, show an error message
            messages.error(request, 'Admin not found with the provided username or email.')
            return redirect('admin_password_reset')




        # Update the user's password
        user.set_password(new_password)
        user.save()




        messages.success(request, 'Password reset successful.')
        return redirect('adminlogin')  # Redirect to login page or any other appropriate page




    return render(request, 'admin/forgot-password.html')
