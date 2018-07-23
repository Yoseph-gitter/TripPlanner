from django.db import models
import re
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware
import pytz


class UserManager(models.Manager):
    def validate_userInputs_NoneLoggedInUser(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 :
            errors['first_name'] = "First Name should be greater than 5"
        if len(postData['last_name']) < 2  :
            errors['last_name'] = "Last Name should be greater than 5"
        if not ( self.validateEmail( postData['email'] )) :
            errors['email']  = "Email is not valid , could you correct and submit!"
        if len(postData['password']) < 8 :
            errors['password'] = "Password can not be less than 8 chars"
       
        if len(postData['password']) != len(postData['password_confirmation']) or ( postData['password'] != postData['password_confirmation'] ):
                errors['password_confirmation'] = "Password is not same as passwordConfirmation"

        return errors
    
    def validateEmail(self, email):
        if len(email) > 6:
            if re.match('[\w\.-]+@[\w\.-]+\.\w{2,4}', email) != None:
                return True
        return False
    
    def validate_userInputs_For_LoggedInUsers(self, postData):
        errors = {}
       
        if not ( self.validateEmail( postData['email'] )) :
            errors['email']  = "Email is not valid , could you correct and submit!"
        if len(postData['password']) < 8 :
            errors['password'] = "Password can not be less than 8 chars"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255, unique = True)
    password = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # associating it to the manager objects
    objects = UserManager()


class TripManager(models.Manager):

    def validate_trip_info(self, postData):

        errors = {}
        if len(postData['tripName']) < 2 :
            errors['tripName'] = "tripName should be greater than 2"
        if len(postData['tripDesc']) < 2 :
            errors['tripDesc'] = "tripDesc should be greater than 2"

        if len ( postData['travelStartDate'] ) == 0 or len (postData['travelDateTo'])== 0 :
            errors['date_empty'] = "Date is Empty"

        else:
           
            travelStartDate_aware = make_aware(datetime.strptime(postData['travelStartDate'], '%Y-%m-%d'))
            travelDateTo_aware = make_aware(datetime.strptime(postData['travelDateTo'], '%Y-%m-%d'))
            
            timezone = travelStartDate_aware.tzinfo

            # Current datetime for the timezone of your variable
            now_in_timezone = datetime.now(timezone)

            # Now you can do a fair comparison, both datetime variables have the same time zone
            if (travelStartDate_aware)  < now_in_timezone :
                errors['travelStartDate'] = "travelStartDate can't be in the PAST"

            if (travelDateTo_aware) < now_in_timezone  :
                errors['travelDateTo'] = "travelDateTo can't be in the PAST"

            if  travelDateTo_aware <  travelStartDate_aware :
                errors['travelDateTo_travelStartDate'] = "travelDateTo can't be before travelStartDate"
    
        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    desc = models.TextField()
    travelDateFrom = models.DateTimeField(auto_now_add=True)
    travelDateTo = models.DateTimeField(auto_now=True)
    created = models.ForeignKey(User, related_name="created_trips")
    joined_users = models.ManyToManyField(User, related_name="joined_trips")

    objects = TripManager()

    
    
