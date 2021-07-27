var timeoutID;
var timeout = 1000;
var flag = false;

function setup() {
	document.getElementById("button1").addEventListener("click", makePost, true);
	timeoutID = window.setTimeout(poller, timeout);
}

function makePost() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Cannot create an XMLHTTP instance');
		return false;
	}
	var forumName = document.getElementById("forumName").innerHTML;
	var message = document.getElementById("message").value;
	httpRequest.onreadystatechange = function() { handlePost(httpRequest, message) };
	
	httpRequest.open("POST", "/new_message");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data;
	data = "message=" + message + "&forumName=" + forumName;
	
	httpRequest.send(data);
}

function handlePost(httpRequest, row) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			addRow(row);
			clearInput();
		} else {
			alert("There was a problem with the post request.");
		}
	}
}

function poller() {
	var httpRequest = new XMLHttpRequest();
	var forumName = document.getElementById("forumName").innerHTML;
	if (!httpRequest) {
		alert('Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { handlePoll(httpRequest) };
	httpRequest.open("GET", "/messages?forumName=" + forumName);
	httpRequest.send();
}

function handlePoll(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			var tab = document.getElementById("table1");
			while (tab.rows.length > 0) {
				tab.deleteRow(0);
			}			
			var rows = JSON.parse(httpRequest.responseText);
			if(flag && rows.length === 0){
				alert("This forum was deleted by the host! Now exiting:")
				window.location = "/hostEnd/";
			}
			for (var i = 0; i < rows.length; i++) {
				addRow(rows[i]);
			}
			
			timeoutID = window.setTimeout(poller, timeout);
			
		} else {
			alert("There was a problem with the poll request, refresh the page to recieve updates again!");
		}
	}
}

function clearInput() {
	document.getElementById("message").value = "";
}

function addRow(row) {
	flag = true;
	var tableRef = document.getElementById("table1");
	var newRow   = tableRef.insertRow();

	var newCell, newText;
	newCell  = newRow.insertCell();
	newText  = document.createTextNode(row);
	newCell.appendChild(newText);
}

window.addEventListener("load", setup, true);


