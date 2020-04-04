// Initialize variables and user info
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const user_name = JSON.parse(document.getElementById('user-name').textContent);
var letter = user_name[0].toUpperCase();
var colour = random_rgba();
var online = [user_name];
var viewing = {};
var curr_user = {};
viewing[user_name] = Date.now().toString();
online_elements = document.querySelector('#online-users');
history_elements = document.querySelector('#viewed-user-list');


online_elements.innerHTML = `<div onmouseover="showUserDetails('${user_name}')" onmouseout="hideUserDetails('${user_name}')" class="row" id="online-row-${user_name}">\n` +
    `            <span class="circle" id="logo-${user_name}"></span>\n` +
    `        </div>`;
document.querySelector(`#logo-${user_name}`).style.backgroundColor = colour;
document.querySelector(`#logo-${user_name}`).innerHTML = letter;

// creating the user-detail div that will contain the username details of the user
createCustomUserDetailDiv(user_name);

const chatSocket = new WebSocket(`ws://${window.location.host}/ws/docs/${roomName}/`);

chatSocket.onmessage = function (e) {

    // obtain info from message
    const data = JSON.parse(e.data);
    switch (data.message_type) {
        case "ping": {
            // Obtain info of users
            let name = data.message.name;
            let date = data.message[name];
            let u_colour = data.message['colour'];
            let u_letter = data.message['letter'];

            // Update viewing users timestamps
            viewing[name] = date;

            // insert new people
            if (!online.includes(name)) {
                online.push(name);
                online_elements.innerHTML += `<div onmouseover="showUserDetails('${name}')" onmouseout="hideUserDetails('${name}')" class="row" id="online-row-${name}">\n` +
                    `            <span class="circle" id="logo-${name}"></span>\n` +
                    `        </div>`;

                // creating the user-detail div that will contain the username details of the user
                createCustomUserDetailDiv(name);

                document.querySelector('#logo-' + name).style.backgroundColor = u_colour;
                document.querySelector('#logo-' + name).innerHTML = u_letter;
            }
            break;
        }

        case 'viewing_history': {
            history_elements.innerHTML = '<div id="viewed-user-list"></div>';
            for (var key in data.message) {
                history_elements.innerHTML += '<div class="row">\n' +
                    '            <span class="history" id="history-' + key + '">' + key + ': ' + data.message[key] + '</span>\n' +
                    '        </div>';
            }
        }

    }
};

chatSocket.onclose = function (e) {
    // Socket disconnect message
    console.error('Chat socket closed unexpectedly');
};

// ping server with user info (name and timestamp)
window.setInterval(pingSocket, 1000);

// check for disconnected users
window.setInterval(removeIdle, 1000);


function showUserDetails(username) {
    // show the user details(triggered on hovering of mouseover)
    let user_details_element = document.getElementById(`user-details-${username}`);
    user_details_element.innerHTML = username;
    user_details_element.style.display = 'block';
}


function hideUserDetails(username) {
    // hide the user details(triggered on hovering of mouseout)
    document.getElementById('user-details-' + username).style.display = 'none';
}


function createCustomUserDetailDiv(username) {
    // dynamically create the user-detail div that will be hidden until mouseover of the parent element
    var user_details = document.createElement('div');
    user_details.setAttribute('class', 'user-details');
    user_details.setAttribute('id', `user-details-${username}`);
    document.getElementById(`online-row-${username}`).appendChild(user_details);
}


function toggleShowViewedHistory() {
    // toggle display and text for the user viewed history block
    if (history_elements.style.display == "") {
        history_elements.style.display = 'block';
        document.getElementById('history-title').innerHTML = 'Hide Visit History'
    } else if (history_elements.style.display == 'block') {
        history_elements.style.display = "";
        document.getElementById('history-title').innerHTML = 'Show Visit History'
    }
}


function pingSocket() {
    // Ping server with user info
    curr_user['message_type'] = 'ping';
    curr_user[user_name] = new Date().toString();
    curr_user['name'] = user_name;
    curr_user['colour'] = colour;
    curr_user['letter'] = letter;
    chatSocket.send(JSON.stringify(curr_user));
}


function removeIdle() {
    // Remove idle users
    for (index = 0; index < online.length; index++) {
        now = new Date().getTime();
        date = new Date(viewing[online[index]]).getTime();
        if (now - date > 10000) {
            row = document.querySelector('#online-row-' + online[index]);
            row.parentNode.removeChild(row);
            online.splice(index, 1);
        }
    }
}


function random_rgba() {
    // Random colour generator
    var o = Math.round, r = Math.random, s = 255;
    return 'rgba(' + o(r() * s) + ',' + o(r() * s) + ',' + o(r() * s) + ',' + r().toFixed(1) + ')';
}