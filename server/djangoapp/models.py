from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    Name = models.CharField(null=False, max_length=20, default='')
    Description = models.CharField(max_length=1000)
    def __str__(self):
        return self.Name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    CarMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    Name = models.CharField(max_length=1000)
    # DealerId = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    DealerId = models.IntegerField(default=0)
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    TYPE_CHOICES = [
        (SEDAN, "SEDAN"),
        (SUV, "SUV"),
        (WAGON, "WAGON"),
    ]
    Type = models.CharField(max_length=1000, choices=TYPE_CHOICES, default=SEDAN)
    Year = models.DateField(null=True)
    def __str__(self):
        return self.Name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
