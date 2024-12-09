from django import template

register = template.Library()

@register.simple_tag
def tripName(trip):
    return trip["tripname"]

@register.simple_tag
def tripDestination(trip):
    return trip["destination"]

@register.simple_tag
def tripUsername(trip):
    return trip["username"]

@register.simple_tag
def tripLikes(trip):
    numberOfLikes = trip.get("likes", [])
    return len(numberOfLikes)

@register.simple_tag
def tripID(trip):
    return trip.get("tripID", "none")

@register.simple_tag
def checkLikeStatus(trip, username):
    likers = trip.get("likes", [])
    if username in likers:
        return "clicked"
    else:
        return "unclicked"

@register.simple_tag
def checkLikeStatusIcon(trip, username):
    likers = trip.get("likes", [])
    if username in likers:
        return "/static/home/icons/red_heart.svg"
    else:
        return "/static/home/icons/empty_heart.svg"
    

@register.simple_tag
def getImagePaths(trip):
    return trip.get("imagePaths", [])

@register.simple_tag
def getMessage(message):
    return message.get('message', '')


@register.simple_tag
def getUsername(message):
    return message.get('username', 'Guest')