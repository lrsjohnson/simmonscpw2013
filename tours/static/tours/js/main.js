
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

function onR(evt) {
    newRequest();
}

function onC(evt) {
    claimRequest();
}

function checkkey(evt)
{
    var evt  = (evt) ? evt : ((event) ? event : null);
    console.log(evt.keyCode);
    if ((evt.keyCode == 67)){onC(evt);}
    else if (evt.keyCode == 82) {onR(evt);}
}

$(document).ready(function(){
    $('body').bind('keyup',checkkey);
});

window.setInterval(function(){
    location.reload();
}, 30000);

