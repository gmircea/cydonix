Installation guide
=================

   This is a step by step guide to configure Raspberry Pi and run the cydonix-agent script.

1. So, as the first step is to get a Raspberry PI!
1. Download Raspbian Wheezy from internet through torrent or directly as a [ZIP file](http://www.raspberrypi.org/downloads/).
1. Installing Raspbian Wheezy on a SD card:
     * on **Ubuntu**:
       * insert the SD card and mount it;
       * run in Terminal the ***df*** command; find the device in */dev* directory.
       * unmount the SD card with the following command:
      ``` 
      $ umount /media/sdcardname 
      ```
       * format the SD card in FAT32 :
      ``` 
      # mkdosfs -F 32 -v /dev/mmcblk0 
      ```
       * copy the .img file to the SD card using dd command:
      ```
      # dd bs=1M if="full_path_to_img" of=path_to_sdcard 
      ```
       * when it is ready you can unplug and use the SD card with Raspberry Pi.
     * on **Windows**:
       * download [Win32 Disk Imager](http://sourceforge.net/projects/win32diskimager/)
       * Select the Raspbian image and target device;
       * Push the write button and wait until it has finished;
1. Now you can put the SD card into Raspberry Pi and turn it on. You need to plug in the HDMI display, mouse and keyboard to the Raspberry Pi to make the first setup.

1. Configuring Raspberry Pi :
   After booting up you will see a menu where you can do the following:
     * *expand_rootfs* - to  use the whole SD card;
     * *configure_keyboard* - configure keyboard layout;
     * *change_timezone* ;
     * *ssh* - enable ssh server ;
     * *boot_behaviour* - you can choose yes if you want to boot it on GUI interface , or no if you exclusively use the command line; we will login to Raspberry Pi through SSH;
    
   For more information you have this [tutorial](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-2-first-time-configuration/overview) for a better understanding.

1. Connect through SSH to the Raspberry Pi with PuTTY (on Windows) or ssh (Ubuntu).
   * for **Windows** : 
     * download [PuTTY](http://www.putty.org/).
     * enter Raspberry Pi's IP address and Open;
     * enter the username and password :
          * username: pi ;
          * password: raspberry (DEFAULT);
   * for **Ubuntu** :
     * install OpenSSH through Terminal :

       ``` 
       # apt-get install openssh-server openssh-client 
       ```
     * connect to Raspberry Pi:
   
       ``` 
        $ ssh pi@ipaddress_of_raspberry 
       ```
       

1. Installing RPi.GPIO with the following command lines:
    ```
    # apt-get update
    ```
    ```
    # apt-get install python-dev
    ```
    ```
    # apt-get install python-rpi.gpio
    ```

1. Installing pip :
    ``` 
    # apt-get install python-pip 
    ```

1. Installing sleekxmpp package through pip : 
    ```
    # pip install sleekxmpp 
    ```

1. Installing hipi to enable i2c on Raspberry Pi :
    ``` 
    # apt-get update 
    ```
    ``` 
    $ wget http://raspberry.znix.com/hipifiles/hipi-install 
    ```
    ``` 
    $ perl hipi-install 
    ```

1. Enabling secondary i2c at each boot :
  Write the following line in the */etc/rc.local* file:
   ``` 
   /usr/local/bin/hipi-i2c e 0 1 
   ```
  You can access the file as :
   ``` 
   # nano /etc/rc.local 
   ```

1. You can test the connected device :
   ``` 
   # i2cdetect -y 0 
   ```
   or 
   ``` 
   # i2cdetect -y 1 
   ```

   depends on which version of Raspberry Pi you use.   

1. Reboot Raspberry Pi:
    ``` 
    # reboot
    ```
    and login again through SSH.  

1. Installing git :
    ``` 
    # apt-get install git-core 
    ```

1. Installing and using the Adafruit BMP Python Library:
    ``` 
    # apt-get update 
    ```
    ``` 
    # apt-get install git build-essential python-dev python-smbus 
    ```
    ```
    $ git clone https://github.com/adafruit/Adafruit_Python_BMP.git 
    ```
    ```
    $ cd Adafruit_Python_BMP 
    ```
    ```
     # python setup.py install
    ```

1. Create configuration file and save it somewhere.
1. Clone git repository :
    ``` 
    $ git clone https://github.com/vitheia/cydonix.git 
    ```

1. Go to the cydonix/agent directory and copy the script to */usr/bin* directory. 

1. Add execute rights with the following command :
    ```
    # chmod u+x cydonix-agent 
    ```

1. If you want to test the script you can go to the directory you saved and run it in Terminal:
   ```
   # python cydonix-agent -c config_file.ini -l log_file.log 
   ```
   At least a configuration file is needed to be specified with ***-c*** option ( you have to put the relative path, or full path if it is situated in other directory than cydonix agent). The log file is optional, you only need to add that option if you want to have a log file with the message stanzas sent or received through XMPP. 

1. Copy the *debian/init.d/cydonix-agent* script file to init.d directory.
 

Enjoy!
