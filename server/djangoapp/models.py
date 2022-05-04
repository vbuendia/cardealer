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
    def __init__(self, address, city, id, lat, long, st, zip):
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

    def __str__(self):
        return "Dealer: " + self.address

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    dealer = models.ForeignKey(
        CarDealer,
        on_delete=models.CASCADE,
     )    
    description = models.CharField(max_length=2000)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return "Reviewer: " + self.reviewer + "," + \
               "Dealer: " + self.dealer + "," + \
               "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
     car_makes = models.ManyToManyField(CarMake)
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
                "Type :" + self.model_type + \
                "Date: " + self.year.strftime("%Y")
            


