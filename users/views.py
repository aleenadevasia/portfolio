from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, UserProfileForm, ProjectForm, WorkExperienceForm, EducationForm, CertificationForm
from django.contrib import messages
from .models import UserProfile, Project, WorkExperience, Education, Certification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger






# def create_user(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST, request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password'])
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#             messages.success(request, 'User and profile data have been successfully submitted.')
#             return redirect('/')
#         else:
#             messages.error(request, 'There was an error processing your request. Please check the form and try again.')
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#     return render(request, 'create_user.html', {'user_form': user_form, 'profile_form': profile_form})

def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'User and profile data have been successfully submitted.')
            return redirect('/')
        else:
            messages.error(request, 'There was an error processing your request. Please check the form and try again.')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'create_user.html', {'user_form': user_form, 'profile_form': profile_form})


# def user_list(request):
#     users = UserProfile.objects.all()
#     # users = get_object_or_404(UserProfile, pk=user_id)
#
#     return render(request, 'user_list.html', {'users': users})
def user_list(request):
    search_query = request.GET.get('search')
    users = UserProfile.objects.all()
    if search_query:
        users = users.filter(person__icontains=search_query)
    page_number = request.GET.get('page')
    paginator = Paginator(users, 10)  # Show 10 users per page
    try:
        users = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)
    return render(request, 'user_list.html', {'users': users})


def admin_view(request):
    users = UserProfile.objects.all()
    # users = get_object_or_404(UserProfile, pk=user_id)

    return render(request, 'admin_view.html', {'users': users})

# def edit_user(request, user_profile_id):
#     user_profile = get_object_or_404(UserProfile, id=user_profile_id)
#     # Assuming 'user_profile_id' is the field in the Project model that links to UserProfile
#     projects = Project.objects.filter(user_profile_id=user_profile.id)
#     work_experiences = WorkExperience.objects.filter(user_profile=user_profile)
#     educations = Education.objects.filter(user_profile=user_profile)
#     certifications = Certification.objects.filter(user_profile=user_profile)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'User profile has been updated successfully.')
#             return redirect('user_list')
#     else:
#         form = UserProfileForm(instance=user_profile)
#     return render(request, 'edit_user.html', {'user_profile': user_profile, 'projects': projects, 'work_experiences': work_experiences, 'educations': educations, 'certifications': certifications, 'form': form})

def edit_user(request, user_profile_id):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    projects = Project.objects.filter(user_profile=user_profile)
    work_experiences = WorkExperience.objects.filter(user_profile=user_profile)
    educations = Education.objects.filter(user_profile=user_profile)
    certifications = Certification.objects.filter(user_profile=user_profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile has been updated successfully.')
            return redirect('edit_user',user_profile_id=user_profile.id)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_user.html', {'user_profile': user_profile, 'projects': projects, 'work_experiences': work_experiences, 'educations': educations, 'certifications': certifications, 'form': form})


def delete_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, pk=user_id)
    if request.method == 'POST':
        user_profile.user.delete()
        messages.success(request, 'User profile has been deleted successfully.')
        return redirect('admin_view')
    return render(request, 'delete_user.html', {'user_profile': user_profile})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)  # Retrieve UserProfile object
                messages.success(request, f'Welcome, {username}. You are now logged in.')
                # Redirect to edit_user page after successful login
                return redirect('edit_user', user_profile_id=user_profile.id)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the user profile for the current user
            user_profile = request.user.userprofile

            # Create a new project associated with the user profile
            project = form.save(commit=False)
            project.user_profile = user_profile
            project.save()

            messages.success(request, 'Project has been created successfully.')
            return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile.id}))
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})


def project_detail(request, project_id):
    # Retrieve the Project object corresponding to the project_id
    project = get_object_or_404(Project, pk=project_id)

    # Render the template with the project details
    return render(request, 'project_detail.html', {'project': project})


def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Retrieve the associated UserProfile using the user_profile_id field
    user_profile = project.user_profile

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project has been updated successfully.')
            return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile.id}))
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project, 'user_profile': user_profile})


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        # Perform deletion logic
        project.delete()
        messages.success(request, 'Project has been deleted successfully.')
        # Redirect to edit_user page after deletion
        return redirect(reverse('edit_user', kwargs={'user_profile_id': project.user_profile.id}))

    # Render delete.html when HTTP method is GET
    return render(request, 'delete.html', {'project': project})






def create_work_experience(request):
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            user_profile = request.user.userprofile  # Corrected
            work_experience = form.save(commit=False)
            work_experience.user_profile = user_profile  # Assign the current user's profile
            work_experience.save()
            messages.success(request, 'Work experience has been created successfully.')
            return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile.id}))
    else:
        form = WorkExperienceForm()
    return render(request, 'create_work_experience.html', {'form': form})



def edit_work_experience(request, work_experience_id):
    work_experience = get_object_or_404(WorkExperience, pk=work_experience_id)
    user_profile = work_experience.user_profile

    if request.method == 'POST':
        form = WorkExperienceForm(request.POST, instance=work_experience)
        if form.is_valid():
            form.save()
            return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile.id}))
    else:
        form = WorkExperienceForm(instance=work_experience)
    return render(request, 'edit_work_experience.html', {'form': form, 'work_experience': work_experience})


# def delete_work_experience(request, work_experience_id):
#     work_experience = get_object_or_404(WorkExperience, pk=work_experience_id)
#     user_id = work_experience.user_profile_id
#     if request.method == 'POST':
#         work_experience.delete()
#         return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile.id}))
#     return render(request, 'delete_work_experience.html', {'work_experience': work_experience})

def delete_work_experience(request, work_experience_id):
    work_experience = get_object_or_404(WorkExperience, pk=work_experience_id)
    # user_id = work_experience.user_profile_id
    user_profile = work_experience.user_profile
    if request.method == 'POST':
        work_experience.delete()
        return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile.id}))
    return render(request, 'delete_work_experience.html', {'work_experience': work_experience})


def create_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user_profile = request.user.userprofile  # Assign the current user's profile
            education.save()
            messages.success(request, 'Education record has been created successfully.')
            return redirect(reverse('edit_user', kwargs={'user_profile_id': request.user.userprofile.id}))  # Corrected
    else:
        form = EducationForm()
    return render(request, 'create_education.html', {'form': form})



def edit_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            # Retrieve the user profile associated with the education
            user_profile_id = education.user_profile_id
            return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile_id}))
    else:
        form = EducationForm(instance=education)
    return render(request, 'edit_education.html', {'form': form, 'education': education})



def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    user_profile_id = education.user_profile_id
    if request.method == 'POST':
        education.delete()
        return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile_id}))
    return render(request, 'delete_education.html', {'education': education})




def create_certification(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.user_profile = request.user.userprofile  # Assign the current user's profile
            certification.save()
            messages.success(request, 'Certification record has been created successfully.')
            # Retrieve the user_profile_id from the current user
            user_profile_id = request.user.userprofile.id
            return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile_id}))
    else:
        form = CertificationForm()
    return render(request, 'create_certification.html', {'form': form})


def edit_certification(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)

    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            # Retrieve the user_profile_id from the edited certification
            user_profile_id = certification.user_profile.id
            return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile_id}))
    else:
        form = CertificationForm(instance=certification)
    return render(request, 'edit_certification.html', {'form': form, 'certification': certification})

def delete_certification(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)
    user_profile_id = certification.user_profile_id
    if request.method == 'POST':
        certification.delete()
        return redirect(reverse('edit_user', kwargs={'user_profile_id': user_profile_id}))
    return render(request, 'delete_certification.html', {'certification': certification})



def base_view(request, user_profile_id):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    projects = Project.objects.filter(user_profile=user_profile)
    work_experiences = WorkExperience.objects.filter(user_profile=user_profile)
    educations = Education.objects.filter(user_profile=user_profile)
    certifications = Certification.objects.filter(user_profile=user_profile)

    context = {
        'user_profile': user_profile,
        'projects': projects,
        'work_experiences': work_experiences,
        'educations': educations,
        'certifications': certifications,
        'skills': user_profile.skills.split(",") if "," in user_profile.skills else [
            user_profile.skills] if user_profile.skills else [],
    }


    return render(request, 'base.html', context)
# Create your views here.
