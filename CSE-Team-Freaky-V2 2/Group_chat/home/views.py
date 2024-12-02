import os
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader, RequestContext
from pymongo import MongoClient
from bcrypt import hashpw, gensalt
from home.generateToken import generateToken, generateImageToken
import hashlib
from .models import userModel
from django.http import JsonResponse
from django.http import HttpResponseForbidden

from django.views.generic import ListView
from .models import TripItem
from django.core.exceptions import ObjectDoesNotExist
import json
import logging
import uuid
import html
import os
from PIL import Image
from PIL import ImageFile
from io import BytesIO


db = MongoClient("mongo")
collection = db['users']
accounts = collection['accounts']
trips = collection['trips']
pictures = collection['pictures']
messages = collection['messages']
#{'username': username, 'tripname': tripname, 'date': date}

# Create your views here.

def view_likes(request: HttpRequest):
    print("\n\n******response******\n\n")
    print(request, flush=True)
    decoded_body = json.loads(request.body.decode())
    tripID = decoded_body["tripID"]
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        return HttpResponseForbidden()
    likes = trip.get('likes', [])
    response = {
        "likes": likes
        }
    return JsonResponse(response)

def delete_like(request: HttpRequest):
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL': 
        return HttpResponseForbidden()
    
    decoded_body = json.loads(request.body.decode())
    tripID = decoded_body["tripID"]
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        return HttpResponseForbidden()
    
    likes = trip.get('likes', [])
    likes_copy = likes.copy()
    trip_copy = trip.copy()
    if username in likes:
        likes_copy.remove(username)
    trip_copy["likes"] = likes_copy

    # updates = {'$set' : {'likes' : likes}}
    trips.replace_one(trip, trip_copy)

    trip_copy.pop("_id")
    
    response = {
        "likes": likes_copy
    }
    return JsonResponse(response)
    


def add_like(request: HttpRequest):
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL': 
        return HttpResponseForbidden()
    
    decoded_body = json.loads(request.body.decode())
    tripID = decoded_body["tripID"]
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        return HttpResponseForbidden()
    
    likes = trip.get('likes', [])
    likes_copy = likes.copy()
    trip_copy = trip.copy()
    if username not in likes:
        likes_copy.append(username)
    trip_copy["likes"] = likes_copy

    # updates = {'$set' : {'likes' : likes}}
    trips.replace_one(trip, trip_copy)

    trip_copy.pop("_id")
    
    response = {
        "likes": likes_copy
    }

    return JsonResponse(response)


def all_trips(request: HttpRequest):
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    #If users auth token is not found in the db -> invalid request
    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL':
        return HttpResponseForbidden()
    
    trips_cursor = trips.find({})
    trips_list = []
    for trip in trips_cursor:
        trip.pop("_id")
        trips_list.append(trip)
    context = {
        "trips": trips_list,
        "username": username
    }
    print("***** ALL TRIPS *****")
    print(context, flush=True)
    return render(request, "all_trips.html", context)

#TODO: GET USERNAME 
def index_trips(request: HttpRequest):
    # print("\n\n***REQUEST START***\n")
    # print(request)
    # print("\n***REQUEST END***\n\n")
    # print("\n\n***REQUEST BODY START***\n")
    # print(request.body)
    # print("\n\n***REQUEST END***\n\n")

    #Getting the user's auth token
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    #If users auth token is not found in the db -> invalid request
    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL':
        return HttpResponseForbidden()
    
    tripscontext = trips.find({'username': username})

    context = {
        'trips' : tripscontext,
    }


    return render(request, 'trips.html', context)

def add_trip(request: HttpRequest):
    # print("\n\n***REQUEST START***\n")
    # print(request)
    # print("\n***REQUEST END***\n\n")
    # print("\n\n***REQUEST BODY START***\n")
    # print(request.body)
    # print("\n\n***REQUEST END***\n\n")
    #Getting the user's auth token
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    #If users auth token is not found in the db -> invalid request
    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL': 
        return HttpResponseForbidden()
    decoded_body = json.loads(request.body.decode())
    #print("\n\n **** decoded body start *****\n")
    #print(decoded_body, flush=True)
    #print("\n **** decoded body end *****\n\n", flush=True)

    # rbody = rbody.decode()
    tripname = html.escape(decoded_body["tripName"])
    if tripname == '':
        return HttpResponseForbidden()
    destination = html.escape(decoded_body["tripDestination"])
    if destination == '':
        return HttpResponseForbidden()
    trip = {'username': username, 'tripname': tripname, 'destination': destination, 'tripID': str(uuid.uuid1())}
    trips.insert_one(trip)
    
    # tripscontext = trips.find_one({'username': username})
    # l = []
    # for i in tripscontext:
    #     i.pop("_id")
    #     l.append(i)

    trip.pop("_id")
    response = {
        "trips": [trip]
    }

    return JsonResponse(response)

def index(request: HttpRequest):
    messages_list = []
    messages_cursor = messages.find({})
    for message in messages_cursor:
        message.pop("_id")
        messages_list.append(message)
    context = {
        'logged_out' : True,
        'messages': messages_list
    }
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token'].encode()
        currToken = hashlib.sha256(token).digest()
        print(currToken)
        entry = accounts.find_one({'token' : currToken})
        if entry != None :
            print('Logging In')
            logged_out = False
            user = entry['username']
            context['username'] = user
            context['logged_out'] = False
            return render(request,"index2.html",context)
    return render(request, "index2.html", context)

def register(request: HttpRequest):
    if request.method == 'POST' :
        print(request)
        body = request.body
        print(body)
        body = body.split(b'&')         #Assuming the body is urlencoded
        username = html.escape(body[1].split(b'=')[1].decode())
        password = html.escape(body[2].split(b'=')[1].decode())
        query = {'username' : username}
        newAcc = accounts.find_one(query)

        if (username == "" or password == "") :
            return invalidRegister()
        
        if (newAcc != None) :
            return invalidRegister()
        
        salt = generateToken(20)
        combined = (password + salt).encode()
        hashed = hashlib.sha256(combined).digest()

        newEntry = {
            'username' : username,
            'password' : hashed,
            'salt' : salt,
            'token' : None
        }
        accounts.insert_one(newEntry)
    
    return HttpResponseRedirect('/')

def login(request: HttpRequest):
    invalid = False
    print("LOGIN")
    if request.method == 'POST' :
        #print(request)
        body = request.body
        body = body.split(b'&')                             #Assuming the body is urlencoded
        username = html.escape(body[1].split(b'=')[1].decode())
        password = html.escape(body[2].split(b'=')[1].decode())
        if username == "" or password == "" :
            return invalidLogin()
        entry = accounts.find_one({'username': username})
        print("Finding User")
        if entry != None :
            print("Found User")
            salt = entry['salt']
            combined = (password + salt).encode()
            attempt = hashlib.sha256(combined).digest()

            if attempt == entry['password']:
                token = generateToken(15)
                hashed = hashlib.sha256(token.encode()).digest()
                updates = {'$set' : {'token' : hashed}}
                accounts.update_one(entry, updates)
                #entry['token'] = hashed
                redirect = HttpResponseRedirect('/')
                print('SUCCESS')
                redirect.set_cookie('token', token, httponly=True)
                redirect.set_cookie('username', username, httponly=True)
                return redirect
            else:
                return invalidLogin()
        else:
            return invalidLogin()

def invalidLogin() :
    #print("Invalid")
    redirect = HttpResponseRedirect('/serveLoginFailed/')
    redirect.context = {'invalid' : True}
    return redirect

def invalidRegister() :
    #print("Invalid")
    redirect = HttpResponseRedirect('/serveRegister/')
    return redirect

def logout (request: HttpRequest) :
    
    token = request.COOKIES['token']
    user = findUser(token)
    if user != None :
        updates = {'$set' : {'token' : None}}
        accounts.update_one(user, updates)
    redirect = HttpResponseRedirect('/')
    if 'token' in request.COOKIES :
        redirect.delete_cookie('token')
    return redirect

def findUser(token) :
    # REPLACE OR REMOVE
    query = {'token' : hashlib.sha256(token.encode()).digest()}
    account = accounts.find_one(query)
    if account != None :
        return account
    return None

def uploadImage(request: HttpRequest, trip_id) :
    print("***trip_id***")
    print(trip_id, flush=True)
    #   Outline
    #
    #   Take the image as a request, Create a new file 
    #   and save it to whatever folder you may create
    #   that persists data :)

    cur_path = os.path.realpath(__file__)
    #   This breaks the image upload at the moment, not sure why.
    # dir = os.path.dirname(cur_path)
    # dir = dir.replace('util', 'public')
    dir = "/root/home/static/home/userImages/"
    print(request.FILES, flush= True)
    print("CONTENT TYPE IS: ", request.content_type, flush= True)

    imageType = request.FILES.get('upload', None)
    if imageType == None:
        return HttpResponseRedirect('/trips/')
    
    imageType = imageType.content_type.split("/")[1]
    print('IMAGE TYPE IS: ', imageType, flush=True)
    imageID = generateImageToken(20)
    path = dir + imageID + "." + imageType
    image = request.FILES.get('upload', None)
    if image == None:
        return HttpResponseRedirect('/trips/')
    image = image.read()

    image_display= ""
    # save file on disk
    with open(path, 'wb') as newImage :
        width_and_height= resize_this_image(image,path)
        image_display=message_image(path, width_and_height[0], width_and_height[1])
        # newImage.write(image)
        newImage.close()
        # resize the image
    
    uploaded_image= open(path, "rb").read()
    path = 'home/userImages/' + imageID + '.' + imageType
    photo = {'imageID': imageID, 'path': path, 'image': uploaded_image}
    pictures.insert_one(photo)


    #Instead of redirecting back to home page find a way to call updateMessages()
    
    response = HttpResponseRedirect('/trips/')

    trip = trips.find_one({"tripID": trip_id})
    if trip == None:
        return response
    
    tripCopy = trip.copy()
    imagePaths = trip.get("imagePaths", [])
    imagePathsCopy = imagePaths.copy()
    imagePathsCopy.append(path)
    tripCopy["imagePaths"] = imagePathsCopy
    trips.replace_one(trip, tripCopy)

    return response

# def serveMedia(request: HttpRequest, trip_id):
    
#     return 

def load_trip_by_id(request,trip_id):
    # Generates a new page for each individual trip.

    #Unfinished.
    currTrips = trips.find_one({'tripID' : trip_id})

    if currTrips == None:
        return HttpResponseNotFound
    else :
        newContext = {'creator' : currTrips['username'], 'tripID': currTrips['tripID'], 'destination' : currTrips['destination'], 'name' : currTrips['tripname']}
        #response = HttpResponseRedirect('newTrip.html')
        #response.context = newContext
        
        return render(request,'newTrip.html', newContext)


def resize_this_image(image_bytes, path):
    im = Image.open(BytesIO(image_bytes))
    width, height = im.size

    new_width = 0
    new_height = 0

    if width > height:
        new_width += 240
        ratio = 240/width
        new_height += height*ratio
    else:
        new_height += 240
        ratio = 240/height
        new_width += width*ratio

    im = im.resize((int(new_width), int(new_height)))
    im.save(path)

    return tuple((int(new_width), int(new_height)))

def message_image(path,width, height):
    return f'<img src="{path}"alt="alternative description" width={width} height={height}/>'

def index2(request: HttpRequest):
    return render(request, "index2.html")

def login2(request: HttpRequest):
    pass


def serveRegister(request: HttpRequest):
    return render(request, "register.html")

def serveLogin(request: HttpRequest):
    return render(request, "login.html")


def serveLoginFailed(request: HttpRequest):
    return render(request, "loginFailed.html")

