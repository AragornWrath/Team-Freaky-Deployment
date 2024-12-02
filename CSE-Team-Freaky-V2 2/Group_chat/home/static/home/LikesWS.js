{/* <script type="text/javascript">
            let url = 'ws://' + window.location.host + '/ws/socket-server'
            const socket = new WebSocket(url)

            socket.onmessage = function(e){
                let data = JSON.parse(e.data)
                console.log("Data:", data)
            }
        </script> */}

function welcome() {

    initWS();

}

function initWS(){
    // added the wss here
    let url = 'wss://' + window.location.host + '/all_trips/websocket';
    const socket = new WebSocket(url);

    socket.onmessage = function (ws_message) {
        console.log(JSON.parse(ws_message.data));
    };
}
