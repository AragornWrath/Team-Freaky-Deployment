let chatMessages = {};
function dropdown(){
    if (document.getElementById("dropdown").className == "dropdown-hidden"){
        document.getElementById("dropdown").className = "dropdown-show";
    }
    else {
        document.getElementById("dropdown").className = "dropdown-hidden";
    }
}

function addTripPopUp(){
    if (document.getElementById("addTripCard").className == "dropdown-hidden"){
        document.getElementById("addTripCard").className = "add-trip-card";
    }
    else {
        document.getElementById("addTripCard").className = "dropdown-hidden";
    }
}

/* Ajax for creating a trip */
/* trip date will be sent as 'yyyy-mm-dd' */

function addTrip(){
    const tripNameTextBox = document.getElementById("trip-name-text-box");
    const tripName = tripNameTextBox.value;
    tripNameTextBox.value = "";

    const tripDestinationTextBox = document.getElementById("trip-destination-text-box");
    const tripDestination = tripDestinationTextBox.value;
    tripDestinationTextBox.value = "";

    // const dateBox = document.getElementById("date-box");
    // const date = dateBox.value;

    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            addTripToHTML(this.response);
            console.log(this.response);
        }
    }
    const tripJSON = {"tripName": tripName, "tripDestination": tripDestination};

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    request.open("POST", "add-trip/");
    request.setRequestHeader("X-CSRFToken", csrftoken)
    request.send(JSON.stringify(tripJSON));
}



//ADDING FRIENDS TO TRIP
function addFriend(i, tripID){
    console.log("ADD FRIEND IS CALLED ON JAVASCRIPT")
    const friendNameTextBox = document.getElementById("add-friends-text-box"+i);
    const friendName = friendNameTextBox.value;
    friendNameTextBox.value = "";
    console.log("FRIEND'S NAME ON JS:")
    console.log(friendName)
    console.log("TRIPID:")
    console.log(tripID)


    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            //implement this part
            //addFriendToHTML(friendName);
        }
    }
    const friendJSON = {"friendName": friendName};

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    request.open("POST", "add-friend/"+tripID);
    request.setRequestHeader("X-CSRFToken", csrftoken)
    request.send(JSON.stringify(friendJSON));
}


function addTask(i, tripID){
    console.log("ADD TASK IS CALLED ON JAVASCRIPT")
    const taskNameTextBox = document.getElementById("add-task-text-box"+i);
    const taskName = taskNameTextBox.value;
    taskNameTextBox.value = "";


    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            //implement this part
            //addFriendToHTML(friendName);
        }
    }
    const taskJSON = {"task": taskName};

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    request.open("POST", "add-task/"+tripID);
    request.setRequestHeader("X-CSRFToken", csrftoken)
    request.send(JSON.stringify(taskJSON));
}


//When adding a trip use "afterbegin" so that way the add trip button is pushed to the end
function addTripToHTML(response){
    const trips = document.getElementById("tripsTable");
    const parsed_response = JSON.parse(response);
    const trips_list = parsed_response["trips"];
    for (let trip of trips_list){
        const tripName = trip["tripname"];
        const tripDestination = trip["destination"];
        trips.insertAdjacentHTML("afterbegin", createTripHTML(tripName, tripDestination));
    }
}
//work on this
function addFriendToHTML(friendName){
    const friends = document.getElementById("friends-list");
    friends.insertAdjacentHTML("afterbegin", friendItemHTML(friendName))
}

function friendItemHTML(friendName){
    let html = '<li>'+friendName+'</li>';
    return html
}

function createTripHTML(tripName, tripDestination){
    let html = '<div class="trip"> <div class="trip-header"> <b class="trip-title">' + tripName + '</b> </div> <b class="trip-destination">' + tripDestination + '</b>  </div>';
    return html;
}


function updateGallery(){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updateGalleryItems(JSON.parse(this.response));
        }
    }
    request.open("GET", "media-uploads/");
    request.send();
}

// play around
function updateGalleryItems(tripPhotos){
    console.log('UPDATE GALLERY CALLED')
    let serverIndex = 0
    let localIndex = 0;

    while (serverIndex < serverMessages.length && localIndex < chatMessages.length) {
        let fromServer = serverMessages[serverIndex];
        let media = chatMessages[localIndex];
        if (fromServer["id"] !== media["id"]) {
            // this message has been deleted
            const messageElem = document.getElementById("media_" + media["id"]);
            messageElem.parentNode.removeChild(messageElem);
            localIndex++;
        } else {
            serverIndex++;
            localIndex++;
        }
    }

    while (localIndex < chatMessages.length) {
        let localMessage = chatMessages[localIndex];
        const messageElem = document.getElementById("media_" + localMessage["id"]);
        messageElem.parentNode.removeChild(messageElem);
        localIndex++;
    }

    while (serverIndex < serverMessages.length) {
        addPhotoToGallery(serverMessages[serverIndex]);
        serverIndex++;
    }
    chatMessages = serverMessages;
}

function addPhotoToGallery(messageJSON) {
    const gallery = document.getElementById("Gallery");
    gallery.insertAdjacentHTML("afterbegin", galleryItemHTML(messageJSON))
    // chatMessages.scrollIntoView(false);
    // chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}


function galleryItemHTML(messageJSON){
    console.log('YO')
    console.log(messageJSON)
    let html = '<div class="photo"> <div img src=""alt="alternative description" class="trip-header" > </div>';
    return html
}

/* Model ajax from jesse*/