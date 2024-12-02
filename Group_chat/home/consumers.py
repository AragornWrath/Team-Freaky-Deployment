import json
from channels.generic.websocket import AsyncWebsocketConsumer
import hashlib
from pymongo import MongoClient
from asgiref.sync import async_to_sync
import html

db = MongoClient("mongo")
collection = db['users']
accounts = collection['accounts']
trips = collection['trips']
messages = collection['messages']
class LikeConsumer(AsyncWebsocketConsumer):
    username = 'Guest'
    async def connect(self):
        auth_token = find_auth_token(self.scope["headers"])
        print("auth token found: ", auth_token, flush=True)
        user = findUser(auth_token)
        self.username = 'Guest'
        if user != None:
            self.username = user['username']
        print("username: ", self.username, flush=True)

        #adding users to channel layer group to broadcast to all users
        await self.accept()

        self.room_group_name = 'likes'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        # await self.send(text_data=json.dumps({
        #     'type': 'connection_established',
        #     'message': 'you are now connected! :)',
            
        # }))

    async def receive(self, text_data):
        print("instance username: ", self.username, flush=True)
        like_data_json = json.loads(text_data)
        like_type = like_data_json["type"]
        tripID = like_data_json["tripID"]
        # print("like data: ", like_data_json, flush=True)
        return_like_data = None
        if like_type == "add_like":
            return_like_data = ws_add_likes(tripID, self.username)
        elif like_type == "delete_like":
            return_like_data = ws_delete_likes(tripID, self.username)
        # await self.send(text_data=json.dumps(return_like_data))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": 'send_like_data',
                "message": json.dumps(return_like_data),
            }
        )
        # print("Like data sent to websocket", flush=True)
#Make sure if you want to print something you use flush=True
    async def send_like_data(self, event):
        message = event["message"]
        await self.send(text_data=message)
        

class SchemeConsumer(AsyncWebsocketConsumer):
    username = 'Guest'
    async def connect(self):
        auth_token = find_auth_token(self.scope["headers"])
        print("auth token found: ", auth_token, flush=True)
        user = findUser(auth_token)
        self.username = 'Guest'
        if user != None:
            self.username = user['username']
        print("username: ", self.username, flush=True)

        #adding users to channel layer group to broadcast to all users
        await self.accept()

        self.room_group_name = 'scheme'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        print("\nCONNECTED AND READY TO SCHEME!\n", flush=True)

    async def receive(self, text_data):
        print("instance username: ", self.username, flush=True)
        scheme_data_json = json.loads(text_data)
        print("\nSCHEME DATA::::", flush=True)
        print(scheme_data_json, flush=True)

        user_message = scheme_data_json.get('message', '')
        user_message_dict = {'message': html.escape(user_message), 'username': self.username}
        
        messages.insert_one(user_message_dict.copy())

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": 'send_message',
                "message": json.dumps(user_message_dict),
            }
        )

    async def send_message(self, event):
        message = event["message"]
        await self.send(text_data=message)



def find_auth_token(headers):
    #call with the headers from self.scope["headers"]
    for header_tuple in headers:
            if b'cookie' in header_tuple:
                cookies = header_tuple[1]
                string_cookies = cookies.decode()
                cookie_list = string_cookies.split()
                for cookie in cookie_list:
                    if cookie.startswith('token='):
                        cookie = cookie.replace(';', '')
                        token_split = cookie.split('=', 1)
                        token = token_split[1]
                        #print("token: ", token, flush=True)
                        return token
    return 'no_auth_token'


def ws_delete_likes(tripID, username):
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        return {"likes": [], "tripID": tripID}
    
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
        "likes": likes_copy,
        "tripID": tripID
    }
    return response



def ws_add_likes(tripID, username):
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        print("no trip found", flush=True)
        return {"likes": [], "tripID": tripID}
    
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
        "likes": likes_copy,
        "tripID": tripID
    }
    return response


def findUser(token) :
    # REPLACE OR REMOVE
    query = {'token' : hashlib.sha256(token.encode()).digest()}
    account = accounts.find_one(query)
    if account != None :
        return account
    return None