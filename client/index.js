var connection = null;
var bulb = false;
var close;
var BOSH_SERVICE;
var jid;
var pass;
var pubsubserver;
var pubsubnode;
var msg;
var discomsg;
var msgto;
var splitmsg;
var finalmsg;
var msgtoserver;
var msgfromserver;
var splitdiscomsg;
var finaldiscomsg;
var historyvalue = '';
var sensors;
var sensor_value;
var devices = {};
var sensors = new Array();

function Login() {
    var networkState = navigator.network.connection.type;
    var states = {};
    states[Connection.UNKNOWN] = 'Unknown connection';
    states[Connection.ETHERNET] = 'Ethernet connection';
    states[Connection.WIFI] = 'WiFi connection';
    states[Connection.CELL_2G] = 'Cell 2G connection';
    states[Connection.CELL_3G] = 'Cell 3G connection';
    states[Connection.CELL_4G] = 'Cell 4G connection';
    states[Connection.NONE] = 'No network connection';
    var state = states[networkState];
    if (state == 'No network connection') {
        navigator.notification.alert('No network connection', null, 'Error', 'Done');
    }

    msgto = document.getElementById('messto').value;
    navigator.notification.vibrate(100);
    console.logger.level(console.logger.DEBUG);
    BOSH_SERVICE = document.getElementById('bosh').value;
    connection = new Strophe.Connection(BOSH_SERVICE);
    connection.RawInput = RawInput;
    connection.RawOutput = RawOutput;

    jid = document.getElementById('user').value + '@' + document.getElementById('domain').value + '/' + device.uuid;
    pass = document.getElementById('pwd').value;
    document.getElementById("ResultTable").innerHTML = "";
    connection.connect(jid, pass, onConnect);
}

function Logout() {
    try {
        document.getElementById("app").style.display = "table";
        document.getElementById("logged").style.display = "none";
        navigator.notification.vibrate(100);
        connection.disconnect(onConnect);
    } catch (err) {
        console.error("Error: " + err);
    }
}

function Send() {
    if (bulb == false) {
        connection.send($msg({
            to : msgto,
            from : jid,
            type : 'chat'
        }).c("body").t('SET switch=True'));
        bulb = true;
    } else if (bulb == true) {
        connection.send($msg({
            to : msgto,
            from : jid,
            type : 'chat'
        }).c("body").t('SET switch=False'));
        bulb = false;
    }
}

function RawInput(data) {
    console.debug('RECV: ' + data);
    var message = data;
}

function RawOutput(data) {
    console.debug('SENT: ' + data);
}

function onConnect(status) {
    if (status == Strophe.Status.CONNECTING) {
        console.debug('Strophe is connecting.');
    } else if (status == Strophe.Status.CONNFAIL) {
        console.debug('Strophe failed to connect.');
    } else if (status == Strophe.Status.DISCONNECTING) {
        console.debug('Strophe is disconnecting.');
    } else if (status === Strophe.Status.AUTHFAIL) {
        alert('Authentication failed!');
    } else if (status == Strophe.Status.DISCONNECTED) {
        console.debug('Strophe is disconnected.');
        navigator.notification.beep(1);
        close = true;
        document.getElementById("stopimg").style.display = "none";
        document.getElementById("goimg").style.display = "none";
        document.getElementById("ResultTable").innerHTML = "";
        UnSubscribe();
    } else if (status == Strophe.Status.CONNECTED) {
        try {
            console.debug('Strophe is connected.');
            close = false;
            connection.send($pres());
            document.getElementById("app").style.display = "none";
            document.getElementById("logged").style.display = "table";
            navigator.notification.beep(1);
            BuildMap();
            Subscribe();
        } catch (err) {
            console.error("Error: " + err);
        }
    }
}

function onLoad() {
    document.addEventListener("deviceready", onDeviceReady, false);
    console.debug('On Load');
}

function onDeviceReady() {
    document.addEventListener("backbutton", onBackKeyDown, false);
    console.debug('Device ready');
    close = false;
}

function onBackKeyDown() {
    if (close == true) {
        navigator.app.exitApp();
    } else {
        connection.disconnect(onConnect);
        document.getElementById("logged").style.display = "none";
        document.getElementById("app").style.display = "table";
    }
}
function Subscribe() {
    pubsubserver = document.getElementById('pubsubs').value;
    pubsubnode = document.getElementById('pubsubn').value;
    connection.pubsub.subscribe(connection.jid, pubsubserver, pubsubnode, [], null, null);
    connection.addHandler(Modified, null, 'message', 'headline', null, null, null);
    connection.addHandler(function() {
        document.getElementById("stopimg").style.display = "initial";
        document.getElementById("goimg").style.display = "none";
        document.getElementById("ResultTable").innerHTML = "";
    }, null, 'presence', 'unavailable', null, null, null);
}

function Modified() {
    document.getElementById("stopimg").style.display = "none";
    document.getElementById("goimg").style.display = "initial";
    BuildMap();
}

function UnSubscribe() {
    connection.pubsub.unsubscribe(connection.jid, pubsubserver, pubsubnode, [], null, null);
}

function RealTime() {
    document.getElementById("ResultTable").style.display = "table";
    document.getElementById("HistoryTable").style.display = "none";
    document.getElementById("HistoryResult").style.display = "none";
}

function History() {
    document.getElementById("ResultTable").style.display = "none";
    document.getElementById("HistoryResult").style.display = "none";
    document.getElementById("HistoryResult").innerHTML = "";
    document.getElementById("HistoryTable").style.display = "table";
}

function CreateLayout(message) {
    connection.send($msg({
        to : msgto,
        from : jid,
        type : 'chat'
    }).c("body").t('GET temperature pressure altitude soc_temp arm_freq core_freq core_volt sdram_volt'));

    try {
        connection.addHandler(OnMessage, null, 'message', 'chat', null, null, null);
        connection.addHandler(function() {
            document.getElementById("stopimg").style.display = "initial";
            document.getElementById("goimg").style.display = "none";
            document.getElementById("ResultTable").innerHTML = "";
        }, null, 'message', 'error', null, null, null);
    } catch (err) {
        console.error("Error: " + err);
    }
}

function OnMessage(message) {
    try {
        document.getElementById("goimg").style.display = "initial";
        document.getElementById("stopimg").style.display = "none";
        document.getElementById("ResultTable").innerHTML = "";
        document.getElementById("ResultTable").align = "center";
        var table = document.getElementById("ResultTable");
        msg = Strophe.getText(message.getElementsByTagName('body')[0]);
        splitmsg = msg.split(" ");
        for (j = 0; j < splitmsg.length; j++) {
            finalmsg = splitmsg[j].split("=");
            console.log('Final msg : ' + finalmsg);
            var row = table.insertRow(0);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            cell1.innerHTML = devices[finalmsg[0]][2];
            cell2.innerHTML = finalmsg[1];
            cell3.innerHTML = devices[finalmsg[0]][0];
        }
    } catch (err) {
        console.error('Error : ' + err);
    }
}

function SendToServer() {
    try {
        sensors = document.getElementsByName('sensors');
        for ( var i = 0; i < sensors.length; i++) {
            if (sensors[i].checked) {
                sensor_value = sensors[i].value;
            }
        }
        msgtoserver = sensor_value + '?begin=' + document.getElementById("fromdate").value + ':00Z' + '&end='
                + document.getElementById("todate").value + ':00Z&offset=' + document.getElementById("offset").value
                + '&count=' + document.getElementById("count").value;
        msgtoserver = msgtoserver.replace(/-/g, "");
        msgtoserver = msgtoserver.replace(/:/g, "");
        console.log('Message to server :' + msgtoserver);
        var url = "http://193.231.162.26:8000/portal/" + msgtoserver;
        var client = new XMLHttpRequest();
        client.onload = ReqListener;
        client.open("GET", url, true);
        client.send(msgtoserver);
    } catch (err) {
        console.error('Error : ' + err);
    }
}

function ReqListener() {
    try {
        document.getElementById("HistoryTable").style.display = "none";
        document.getElementById("HistoryResult").style.display = "table";
        var table = document.getElementById("HistoryResult");
        historyvalue = '';
        historytimestamp = '';
        console.log('Response :' + this.responseText);
        msgfromserver = JSON.parse(this.responseText);
        var row = table.insertRow(0);
        var cell11 = row.insertCell(0);
        var res = '';
        for ( var i = 0; i < msgfromserver.length; i++) {
            var row1 = table.insertRow(1);
            var cell1 = row1.insertCell(0);
            var cell2 = row1.insertCell(1);
            historyvalue = msgfromserver[i].value + ' ' + devices[sensor_value][0];
            historytimestamp = msgfromserver[i].timestamp;
            res = historytimestamp.substr(0, 4) + '/' + historytimestamp.substr(4, 2) + '/'
                    + historytimestamp.substr(6, 2) + '  ' + historytimestamp.substr(9, 2) + ':'
                    + historytimestamp.substr(11, 2) + ':' + historytimestamp.substr(13, 2) + '->';
            cell1.innerHTML = res;
            cell2.innerHTML = historyvalue;
        }
    } catch (err) {
        console.error('Error :' + err);
    }
}

function BuildMap(message) {
    connection.send($msg({
        to : msgto,
        from : jid,
        type : 'chat'
    }).c("body").t('DISCO'));
    try {
        connection.addHandler(OnRecv, null, 'message', 'chat', null, null, null);
        connection.addHandler(function() {
            document.getElementById("stopimg").style.display = "initial";
            document.getElementById("goimg").style.display = "none";
            document.getElementById("ResultTable").innerHTML = "";
        }, null, 'message', 'error', null, null, null);
    } catch (err) {
        console.error("Error: " + err);
    }
    return true;
}

function OnRecv(message) {
    try {
        discomsg = Strophe.getText(message.getElementsByTagName('body')[0]);
        console.log('DISCO MESSAGE ' + discomsg);
        splitdiscomsg = discomsg.split(";");
        for ( var j = 0; j < splitdiscomsg.length; j++) {
            var finaldiscomsg1 = splitdiscomsg[j].split("|");
            console.log('Final Disco message : ' + finaldiscomsg1);
            devices[finaldiscomsg1[0]] = [ finaldiscomsg1[1], finaldiscomsg1[2], finaldiscomsg1[3] ];
        }
        console.log('Devices : ' + devices);
        CreateLayout();
        Subscribe();
    } catch (err) {
        console.error('Disco Error :' + err);
    }
}