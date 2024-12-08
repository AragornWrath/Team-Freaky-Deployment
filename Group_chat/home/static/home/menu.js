let socket = null;


function dropdown(){
    if (document.getElementById("dropdown").className == "dropdown-hidden"){
        document.getElementById("dropdown").className = "dropdown-show";
    }
    else {
        document.getElementById("dropdown").className = "dropdown-hidden";
    }
}

function welcome(){
    initWS();

    document.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            sendChat();
        }
    });
}

function initWS(){
    let url = 'ws://' + window.location.host + '/scheme'
    socket = new WebSocket(url)

    socket.onmessage = function (ws_message) {
        message_data = JSON.parse(ws_message.data)
        // console.log("likes data ->")
        // console.log(likes_data)
        message = message_data["message"]
        username = message_data["username"]
        // console.log(JSON.parse(ws_message.data))
        updateChat(message, username)
    }
}

function updateChat(message, username){
    console.log(message)
    console.log(username)
    let messageHTML = createMessageHTML(message, username)
    addMessageToChat(messageHTML)
}

function addMessageToChat(messageHTML){
    const chatMessages = document.getElementById("chat-messages")
    chatMessages.insertAdjacentHTML("beforeend", messageHTML)
}

function createMessageHTML(message, username){
    let messageHTML = "<div> <b>" + username + ": " + message + "</b> </div>"
    return messageHTML
}

function sendChat(){
    const chatTextBox = document.getElementById("chat-text-box");
    const message = chatTextBox.value;
    chatTextBox.value = "";

    const timeBox = document.getElementById("time");
    const time = timeBox.value;
    timeBox.value = "";

    socket.send(JSON.stringify({'message': message, 'time': time}))
    chatTextBox.focus();
}
