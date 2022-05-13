


from tabnanny import verbose
from unicodedata import category
from django.db import models

# Create your models here.



class Master(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)

    class Meta:
        db_table = 'master'


gender_choices = (
    ('m', 'male'),
    ('f', 'female'),
)

class Profile(models.Model):

    Master = models.ForeignKey(Master, on_delete=models.CASCADE)

    ProfileImage = models.FileField(upload_to="images/users", default="images/user.png")


    FullName = models.CharField(max_length=30, default="")
    DOB = models.DateField(auto_created=True, default="2022-01-01")
    City = models.CharField(max_length=40, default="")
    State = models.CharField(max_length=40, default="")
    Pincode = models.CharField(max_length=6, default="")
    Gender = models.CharField(max_length=10, choices=gender_choices)
    Address = models.TextField(max_length=500, default="")

    class Meta:
        db_table = 'profile'

class Category(models.Model):
    Category = models.CharField(max_length=30) 

    class Meta:
        db_table = 'Category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.Category 

food_type_choices = (
    ("veg","veg"),
    ("eg","egg"),
    ("nveg","non-veg"),
    
)
class FoodItem(models.Model):
    FoodImage = models.FileField(upload_to="images/fooditems", default="images/food.png")
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Type = models.CharField(max_length=10,choices=food_type_choices)
    Price = models.FloatField()
    Description = models.TextField(max_length=250)

    class Meta:
        db_table = 'FoodItem'

class UserFavourite(models.Model):
    FoodItem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UserFavourite'

class Cart(models.Model):
    FoodItem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)
    TotalPrice = models.FloatField()

    class Meta:
        db_table = 'Cart'
