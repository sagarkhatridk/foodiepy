from email import message
import profile
from django.shortcuts import redirect, render
from .models import *
import os
from django.conf import settings
from django.core.mail import send_mail
from random import randint
# Create your views here.

default_data = {
    'app_name' : 'food Delivery',
    'no_header_pages' : ['index', 'register_page','otp_page']
}

def index(request):
    if 'email' in request.session:
        return redirect(profile_page)
    default_data['current_page'] = 'index'
    return render(request, 'food_admin/login_page.html', default_data)

def dashboard_page(request):
    default_data['current_page'] = 'dashboard_page'
    return render(request, 'food_admin/dashboard_page.html', default_data)
    
def register_page(request):
    default_data['current_page'] = 'register_page'
    return render(request, 'food_admin/register_page.html', default_data)

def otp_page(request):
    default_data['current_page'] = 'otp_page'
    return render(request, 'food_admin/otp_page.html', default_data)

def profile_page(request):
    default_data['current_page'] = 'profile_page'

    if 'email' not in request.session:
        return redirect(index)

    load_food_items()    
    profile_data(request) # call the profile_data method to collect profile data
    return render(request, 'food_admin/profile_page.html', default_data)


###profile data###

def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)

    default_data['profile_data'] = profile

#OTP create and send to email#
def create_otp(request):

    email_to_list = [request.session['reg_data']['email'],]
    subject = 'OTP varification for FoodDelivery'
    otp = randint(1000, 9999)

    print('OTp is: ',  otp)

    request.session['otp'] = otp

    message = f"Your One Time Password for Varification is: {otp}"

    email_from = settings.EMAIL_HOST_USER

    # sent_mail is imported from django.core.mail
    send_mail(subject, message, email_from, email_to_list)

# Verifu OTP
def verify_otp(request):
    otp = int(request.POST['otp']) 

    if otp == request.session['otp']:
        master = Master.objects.create(
                    Email = request.session['reg_data']['email'],
                    Password = request.session['reg_data']['password'],
                    IsActive = True,
                    )

        Profile.objects.create(
                Master = master,
            )
        
        del request.session['otp']
        del request.session['reg_data']
        print('OTP verify success')

        return redirect(index)
    else:
        print('Invalid OTP')
    
    return redirect(register_page)

##profile update
def profile_update(request):
    
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)

    profile.FullName = request.POST['full_name']
    profile.City = request.POST['city']
    profile.State = request.POST['state']
    profile.Pincode = request.POST['pincode']
    profile.Gender = request.POST['gender']
    profile.Address = request.POST['address']
    

    dob = request.POST['dob'].split("-")
    profile.DOB = ("-").join(dob)


    profile.save()

    return redirect(profile_page)

def login(request):
    print(request.POST)
    try:
        master = Master.objects.get(Email = request.POST['email'])
        if master.Password == request.POST['password']:
            request.session['email'] = master.Email
            return redirect(profile_page)
        else:
            print("Incorrect Password.")
    except Master.DoesNotExist as err:
        print(err)
        return redirect(index)
    
    return redirect(index)


def load_food_items():
    default_data['food_items'] = FoodItem.objects.all()
 
def logout(request):
    if 'email' in request.session:
            del request.session['email']
    return redirect(index)

def registration(request):

    request.session['reg_data'] = {
        'email' : request.POST['email'],
        'password' : request.POST['password'],
    }

    create_otp(request)


    # master = Master.objects.create(
    #     Email = request.POST['email'],
    #     Password = request.POST['password']
    # )

    # Profile.objects.create(
    #     Master = master,
    # )
    
    print(request.POST)
    return redirect(otp_page)

# profile_image_upload

# def profile_image_upload(request):


#     master = Master.objects.get(Email = request.session['email'])
#     profile = Profile.objects.get(Master = master)

#     # if 'profile_image' in request.FILES:    #uncomment it when you want image in option
#     profile.ProfileImage = request.FILES['profile_image']

#     profile.save()
#     return redirect(profile_page)




# # profile image upload

# ## this code of profile picture upload will remove duplicate picture from the upload folder
def profile_image_upload(request):
    
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)

    image = request.FILES['profile_image']
    
    image_name = image.name
    image_path = os.path.join(settings.MEDIA_ROOT, 'images/users')
    images = os.listdir(image_path)

    image_extension = image_name.split('.')[-1]

    new_image_name = f"{profile.id}_{master.Email.split('@')[0]}.{image_extension}"
    image.name = new_image_name

    
    print('image name:', image_name)
    print('new name:', new_image_name)
    print('image path:', images)

    if new_image_name in images:
        os.remove(os.path.join(image_path, new_image_name))

    profile.ProfileImage = image

    profile.save()

    return redirect(profile_page)

