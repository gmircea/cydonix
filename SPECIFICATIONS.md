Cydonix project
===============

The project consists of the following modules:

* **agent** - server application providing sensor data
* **portal** - server application storing the history of sensor data
* **client** - client application used as a front end interface

Agent
-----

The agent application will run on a RaspberryPi and provide the following sensor data:

* **pressure** in bars
* **temperature** in centigrades (Celsius)
* **altitude** in meters

The agent communicates with outside world using XMPP protocol, acting as an XMPP user.
It accepts requests as XMPP *message* stanza containing the requested sensor name
and respond with a *message* stanza containing the sensor value.


Request from an XMPP user for temperature:

 ```
 <message from="john@example.com" to="agent@example.com">
   <body>get temperature</body>
 </message>
```

Response containing the sensor value:

```
 <message from="agent@example.com" to="john@example.com">
   <body>temperature=37</body>
 </message>
```


Portal
------

The portal application must run a script which periodically (e.g. each 10
seconds - this must be configurable) request sensors data from the agent
and store them in database.

The portal will provide the stored data using the following REST API:
* request using GET method:
```
GET /temperature?begin=&end=&offset=&count=
```
* the response will JSON formatted data:
TODO

The portal will be implemented using [Django](https://www.djangoproject.com/) framework.


Client
------

The client will provide the following features

* retrieve the current value of one of the sensors from the agent using an XMPP
connection
* retrieve the history from the portal by providing date/time interval and
using pagination.

The client will be implemented as a Cordova application.

Misc
----

Recommended XMPP libraries:

* for Python - [SleekXMPP](https://github.com/fritzy/SleekXMPP)
* for JavaScript - [Strophe](http://strophe.im/)
