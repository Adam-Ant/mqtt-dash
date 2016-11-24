# Amazon Dash Button to MQTT Bridge

Sends an MQTT message when an Amazon Dash button press is detected.

Dash detection code based on [sejnub/docker-amazon-dash-sniff](https://github.com/sejnub/docker-amazon-dash-sniff)

## Dash Button Setup
3. Go through the normal Dash button setup in the Amazon app, but when asked to select a product, simply exit out of the setup process.

4. Find the mac address of the Amazon button. This can usually be achieved through your router. If in doubt, use a [MAC address vendor checker](https://macvendors.com/) to make sure the MAC is reigstered to "Amazon Technologies inc."

5. (Optional) Block the button from accessing the internet. Different routers have different ways of achieving this, but typically a simple IPTables rule will achieve this.

## Usage
1. Install Python (>= 2.7), as well as scapy, configparser and paho-mqtt from pip.

2. Clone this repo

3. Run main.py to generate the example config.

4. Edit the config provided to include your MQTT host, as well as the MAC addresses of the button and the corresponding MQTT channels to message. (See the config for examples.)

5. Run main.py

** OR **
1. Run the docker image:
``` docker run -d --net=host --name="mqtt-dash" -v $YOUR_CONFIG_DIRECTORY:/config adamant/mqtt-amazon-dash```

2. Edit the config provdided by the program.

3. Start the container again:
``` docker start mqtt-dash ```
