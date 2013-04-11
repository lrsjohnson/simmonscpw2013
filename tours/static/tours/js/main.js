
function newRequest() {
    $.ajax({
	url: "new",
	success: function( data ) {location.reload();}
    });
}

function claimRequest() {
    $.ajax({
	url: "claim",
	success: function( data ) {location.reload();}
    });
2
}
function checkNotify() {
    $.ajax({
	url: "notify",
	success: function( data ) {}
    });
}


/*
Keys to Functions
*/

function onA(evt) {
    newRequest();
}

function onW(evt) {
    claimRequest();
}

function onS(evt) {
}

function onD(evt) {
}


function checkkey(evt)
{
    var evt  = (evt) ? evt : ((event) ? event : null); 
    if ((evt.keyCode == 119)){onW(evt);}
    else if (evt.keyCode == 97) {onA(evt);}
    else if (evt.keyCode == 115)  {onS(evt);}
    else if (evt.keyCode == 100)  {onD(evt);}
}

$(document).ready(function(){
    $('#IDofTextInput').bind('keyup',checkkey);
});

window.setInterval(function(){
    window.reload();
}, 600000);

