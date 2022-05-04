from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarMake

class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)