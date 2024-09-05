## Branch 3.5.1


# Odoonix IoT in Odoo 

The Internet of Things (IoT) box makes you connect easily to your Odoo database with external devices. IoT enhances productivity and boosts easiness. For building the IoT integration, you need no technical expertise. Yes, it is simple, customizable, and highly securable to increase productivity in your business by fully integrating the IoT box with your existing business processes.

The impact of using IoT boxes has excelled in different business sectors like manufacturing, hospitality industries, hospitals, education sectors, eCommerce, warehouse and storage units, to meet up with the advanced IoT technologies which have developed in the Artificial Intelligence and Machine Learning fields most of them use this tool for advance improvement of their business processes.

The odoonix IoT box connects with your external devices like attendece,printer, scanner, Wifi and ethernet cable, etc. Also, it acts as a mediator with the IoT box. 




# How to configure a Cubitruck embedded linux:


## Scafolding

- create a folder with name .vw-gateway
- create a git directory


	mkdir .vw-gateway
	mkdir git

``` bash

${VW_HOME: /root}
├── git
│   └── odoo-iot
│       ├── docs
│       ├── .git
│       ├── .gitignore
│       ├── readme.md
│       ├── ubuntu
│       ├── .vscode
│       ├── vw-gateway
│       └── vw-iot
├── .ssh
│   ├── authorized_keys
│   ├── id_rsa
│   ├── id_rsa.pub
│   ├── known_hosts
│   └── known_hosts.old
└── .vw-gateway
    ├── conf.yaml
    ├── connected_devices.json
    ├── json_files
    │   ├── cups.json
    │   └── zktec.json
    └── statistics.json
```


## Get codes

- add device public key to github
- clone the following project into the git directory.
	```
	cd ~/git
	git clone https://github.com/odoonix/iot.git --branch 3.5.1
	cd ..
	```

## Manuall installation 

- Install pre-requirenemnt based on your os
- install package dependencies
	```
	cd ~/git/iot/vw-gateway
	python3 -m pip install -r requirements.txt
	cd ~
	```

### OpenSuse Thumbelweed Python 3.11:

	zypper install \
	    python311-ply \
	    python311-paho-mqtt \
	    python311-protobuf \
	    python311-pycups\
	    python311-regex\
	    python311-pycparser\
	    python311-pip \
	    python311-cffi \
	    python311-setuptools-wheel \
	    python311-cryptography \
	    python311-future \
	    python311-jsonpath-rw \
	    python311-PyYAML \
	    python311-simplejson \
	    python311-requests \
	    python311-PyInquirer \
	    python311-termcolor \
	    python311-grpcio \
	    python311-cachetools \
	    python311-charset-normalizer \
	    python311-idna \
	    python311-urllib3 \
	    python311-certifi \
	    python311-Pygments \
	    python311-prompt-toolkit \
	    python311-wcwidth


### Ubuntu server 22.04 LTS

	sudo apt-get install \
	    python3-ply \
	    python3-paho-mqtt \
	    python3-protobuf \
	    python3-regex\
	    python3-pycparser\
	    python3-pip \
	    python3-cffi \
	    python3-cryptography \
	    python3-future \
	    python3-jsonpath-rw \
	    python3-simplejson \
	    python3-requests \
	    python3-termcolor \
	    python3-grpcio \
	    python3-cachetools \
	    python3-charset-normalizer \
	    python3-idna \
	    python3-urllib3 \
	    python3-certifi \
	    python3-prompt-toolkit \
	    python3-wcwidth


## Configuration


- copy a template configuration

```
	cp ~/git/iot/vw-gateway/ubuntu/configs/* ~/.vw-gateway/ -fR
	cd ~/.vw-gateway
	nano conf.json
	nano json_files/zktec.json
```
	
then update all device configuration
```
	mkdir -p ~/bin
	cp ~/git/odoo-iot/ubuntu/vw-gateway.sh ~/bin
	chmod +x ~/bin/vw-gateway.sh
	
	cp ~/git/odoo-iot/ubuntu/vw-gateway.service /etc/systemd/system
	systemctl status vw-gateway
	systemctl enable vw-gateway
	systemctl start vw-gateway
```

## Create service for Ubuntu server 22.04 LTS

Add WorkingDirectory in vw-gateway and Change ExecStart in service

For Example

Change according to the address of the Python file
```
cat << 'EOF' > vw-gateway.service
[Unit]
Description=My test service
After=multi-user.target
[Service]
Type=simple
Restart=always
WorkingDirectory=/root/.vw-gateway
ExecStart=/usr/bin/python3 "/root/git/odoo-iot/vw-gateway/main.py" --extension "/root/git/odoo-iot/vw-gateway/extensions"  --config "/root/.vw-gateway/conf.yaml"
[Install]
WantedBy=multi-user.target
EOF
```

- systemctl daemon-reload

- systemctl restart vw-gateway 

- systemctl enable vw-gateway

- Create logs Folder in WorkingDirectory

- Create logs.conf file

