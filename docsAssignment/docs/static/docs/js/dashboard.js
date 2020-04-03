// Reroute to entered document
document.querySelector('#doc-name-input').focus();
document.querySelector('#doc-name-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#doc-name-submit').click();
    }
};

document.querySelector('#doc-name-submit').onclick = function (e) {
    var roomName = document.querySelector('#doc-name-input').value;
    window.location.pathname = '/docs/' + roomName + '/';
};