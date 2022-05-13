from cProfile import Profile
from django.contrib import admin
from .models import *
# Register your models here.

class SuperAdmin(admin.ModelAdmin):
    admin.site.site_header = admin.site.site_title ='Food App' 


all_models = (Master, Profile, FoodItem, UserFavourite, Cart, Category)

for model in all_models:
    admin.site.register(model, SuperAdmin)


##you can aslo do like below
# admin.site.register(Master)
# admin.site.register(Category)