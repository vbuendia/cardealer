from django.db import models
from django.utils.timezone import now

from django.conf import settings

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
     name =  models.CharField(max_length=200, default="Car Make")
     description =  models.CharField(max_length=200, default="Description")
     
     def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, id, lat, long, st, zip, short_name, full_name):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
        self.short_name = short_name
        self.full_name = full_name

    def __str__(self):
        return "Dealer: " + self.short_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self,dealership, name, purchase, review, purchase_date, car_make,car_model, car_year,sentiment, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment
        self.id=id

    def __str__(self):
        return "Dealer: " + self.name + \
            " sentiment: " + self.sentiment


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
     make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)  
     dealer_id = models.IntegerField(default=0)
     name = models.CharField(max_length=200, default="Car Model Name")
     SEDAN = 'Sedan'
     SUV = 'SUV'
     WAGON = 'WAGON'
     TYPE_CHOICES = [
        (SEDAN , 'Sedan'),
        (SUV , 'SUV'),
        (WAGON , 'WAGON')        
     ]
     model_type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
     )
     year = models.DateField(null=True)

     def __str__(self):
        return "Name: " + self.name + "," + \
                "Type :" + self.model_type 
            


