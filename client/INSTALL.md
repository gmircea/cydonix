Installation
--------------

Step 1 : Install Cordova    
Step 2 : Create Cordova project :
```sh
cordova create sensormonitoringclient com.vitheia.cordova.sensorclient SensorMonitoringClient
``` 
Step 3 : Add android platform : 
```sh
cordova platform add android
``` 
Step 4 : Install cordova plugins : 

```sh
cordova plugin add https://git-wip-us.apache.org/repos/asf/cordova-plugin-device.git    
cordova plugin add https://git-wip-us.apache.org/repos/asf/cordova-plugin-splashscreen.git    
cordova plugin add https://git-wip-us.apache.org/repos/asf/cordova-plugin-vibration.git
cordova plugin add https://git-wip-us.apache.org/repos/asf/cordova-plugin-dialogs.git
cordova plugin add https://git-wip-us.apache.org/repos/asf/cordova-plugin-network-information.git
```
Step 5 :
#### Add files to :
##### SensorMonitoringClient/www

* index.html

##### SensorMonitoringClient/www/js

* strophe.js
* strophe.pubsub.js
* index.js

##### SensorMonitoringClient/www/css

* index.css

##### SensorMonitoringClient/www/img

* stop.png
* go.png

Step 6 : Prepare cross-platform sources for android.

```sh
cordova prepare android
cordova compile android
```