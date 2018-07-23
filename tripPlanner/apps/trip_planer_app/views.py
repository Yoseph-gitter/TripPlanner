from django.shortcuts import render, redirect, HttpResponse
import bcrypt
import re
from django.contrib import messages
from .models  import User, Trip

def index(request):
    if 'email' in request.session:
        return redirect("/travels")
    return render(request, "trip_planer_app/index.html")

def travels(request):
    if 'email' not in request.session:
        return redirect("/register")

    userEmails = request.session['email']
    #  grab the list of trips the current user joines till now
    try:
        your_trips = User.objects.get(email=userEmails).joined_trips.values()
        # User.objects.get(email='mollaTenkolu@gmail.com').joined_trips.values()
    except TypeError:
        print("User with the mentioned email deoes not exist!")
        return
    # flag trips that are created by current user as they are displayed differently in the template
    currentUser = User.objects.get(email=request.session['email'])
    flagged_trips = []
    for trip in your_trips:
        user_trip = {}
        if trip['created_id'] == currentUser.id :
            user_trip['is_created'] = True
        else:
            user_trip['is_created'] = False
        user_trip['trip'] = trip
        flagged_trips.append(user_trip)
    # filtering trips created

    allTrips_excluding_currentUser = Trip.objects.exclude(id__in=(currentUser.joined_trips.values('id')))
    context ={
        'flagged_trips' : flagged_trips ,
        'trips_created':  allTrips_excluding_currentUser
        # Trip.objects.exclude(id__in=[currentUser.joined_trips.values().keys())
    }
    return render(request, "trip_planer_app/travels.html", context )
 
def login(request):
    # validate 
    if request.method == "POST" :
        # Validate User Here atleast the email is correct
        errors = User.objects.validate_userInputs_For_LoggedInUsers(request.POST)
        if ( errors ):
            for key, value in errors.items() :
                messages.error(request , value)
                return redirect("/")
        else:
            # No validation Errors
            # check user in db error out if they are new
            # This loggin validator checks for 
            # 1 - if user does not exist , INFO message is logged and redirect to login page
            # 2 - else if user is new , we register it for the first time
            # 3 - else an existing user so logged him in and save loggedin state in session
            user = User.objects.filter(email = request.POST['email'])
            if (user.count() == 0 ):
                messages.info(request, "User Does Not Exist in the system, Please register !" )
                return redirect("/")

            elif bcrypt.checkpw(request.POST['password'].encode() , user.values()[0]['password'].encode() ):
                messages.success(request , "Successfully logged in!")
                # request.session['first_name'] = user.values[0]['first_name']
                request.session['email'] = request.POST['email']
            else:
                messages.error(request , "Wrong Password, try relogging again !")
                return redirect("/")

    return redirect("/travels")

def logout(request):
    del request.session['email'] 
    messages.success(request, "Successfully logged out !")
    return redirect("/")

def join(request, trip_id):
    # Add existing user to the group of trip_joiners
    trips = Trip.objects.get(id=trip_id)
    currentUser = User.objects.get(email=request.session['email'])
    trips.joined_users.add(currentUser)

    return redirect("/travels")
        
def register(request):
    # what happens if a non-logged in user tries to login with out first_name/last_name
    errors = User.objects.validate_userInputs_NoneLoggedInUser(request.POST)
    if ( errors ):
        for key, value in errors.items() :
            messages.error(request , value)
            return redirect("/")
    else:
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        request.session['email'] = request.POST['email']
        messages.success(request, "Successfully registered !")
    return redirect("/travels")  

def createPlan(request):
    return render(request, "trip_planer_app/addTrip.html")

def show(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=trip.created_id) 
    # User.objects.get(email=request.session['email'])
    # request.session['trip_id'] = trip
    other_users = trip.joined_users.values().exclude(id__exact=user.id)
    context = {
        'user' : user ,
        'trip' : trip,
        'other_users' : other_users
   }
    return render(request, "trip_planer_app/success.html", context)

def create(request):
    return redirect("/travels")

#  users creation will go below
def trips(request):
    return redirect("/travels")

def createTrips(request):
    errors = {}
    if request.method == "POST" :
        # validate user input 
        errors = Trip.objects.validate_trip_info(request.POST)
        if( errors ):
            for key, value in errors.items() :
                messages.error(request , value)
            return redirect("/createPlan")

        # otherwise no validation error : process normally
        userEmail = request.session['email']
        loggedInUser = User.objects.get(email= userEmail)

        tripOne = Trip.objects.create(
            destination = request.POST['tripName'],
            desc = request.POST['tripDesc'],
            travelDateFrom = request.POST['travelStartDate'],
            travelDateTo = request.POST['travelDateTo'],
            created = loggedInUser
        )

        tripOne.joined_users.add(loggedInUser)
        tripOne.save()

    return redirect("/trips")

def delete(request, trip_id):
    # Trip.objects.get(id=8).joined_users.get(email='yosepharegay4@yahoo.com').delete()
    # trip = Trip.objects.get(id=trip_id)
    # trip.joined_users.get(email= request.session['email']).delete()
    User.objects.get(email= request.session['email']).joined_trips.get(id=trip_id).delete()

    return redirect("/travels")
def cancel(request, trip_id):

    trips = Trip.objects.get(id=trip_id)
    trips.joined_users.remove(User.objects.get(email=request.session['email']))
    # add it to the others list

    return redirect("/travels")

def back(request):
    return redirect("/travels")


