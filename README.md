Description
===================
Internet of things (IoT) and Wireless Network (WN) 

##Requirments
1. Linux OS (preferred)
2. Docker
3. Contiki-NG OS

## Install Docker in Ubuntu (x86_64) Bionic 18.04 (LTS)

**Install using the repository**

Link : https://docs.docker.com/engine/install/ubuntu/

1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:


    
        $ sudo apt update

        $ sudo apt install \
                apt-transport-https \
                ca-certificates \
                curl \
                gnupg-agent \
                software-properties-common

2. Add Docker’s official GPG key:

        $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    Verify that you now have the key with the fingerprint 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88, by searching for the last 8 characters of the fingerprint.

        $ sudo apt-key fingerprint 0EBFCD88

        pub   rsa4096 2017-02-22 [SCEA]
            9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
        uid           [ unknown] Docker Release (CE deb) <docker@docker.com>
        sub   rsa4096 2017-02-22 [S]

3. Use the following command to set up the stable repository. To add the nightly or test repository, add the word nightly or test (or both) after the word stable in the commands below

        $ sudo add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"

4. Create Docker group and add "your user"

        a. Create docker group 
        $ sudo groupadd docker

        b. add your user to docker group
        $ sudo usermod -aG docker $USER

5. Change permission of docker folder to run smoothly everything 

        $ chmod -R 775 /home/faiz/.docker

6. Some commands 

        $ docker ps    

        This will present you with a list of container IDs. Select the ID of the container you wish to open a terminal for and then

        $ docker exec -it <the ID> /bin/bash

7. Docker compose 

        $ sudo apt install docker-compose

## Contiki-NG image 

Help : https://github.com/contiki-ng/contiki-ng/wiki/Docker

        $ docker pull contiker/contiki-ng

**Chechout Contiki-NG**

        $ git clone https://github.com/contiki-ng/contiki-ng.git
        $ cd contiki-ng
        $ git submodule update --init --recursive

Then, it is a good idea to create an alias that will help start docker with all required options. On Linux, you can add the following to ~/.profile or similar, for instance, to ~/.bashrc:

        $ vim ~/.bashrc 
        and 
        $ vim ~/.profile

        add the following lines 

        export CNG_PATH=/home/faiz/contiki-ng
        alias contiker="docker run --privileged --sysctl net.ipv6.conf.all.disable_ipv6=0 --mount type=bind,source=$CNG_PATH,destination=/home/user/contiki-ng -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/bus/usb:/dev/bus/usb -ti contiker/contiki-ng"

        run following commands 

        $ source ~/.bashrc
        and 
        $ source ~/.bashrc


**Run and Execute Contiker**

Disable access control 

        $ xhost +

Run contiker bash

        $ contiker 

Run cooja from contiker bash

        $ sudo cooja



       