# SpaPi

Use a RaspberryPi to control your sauna (On/Off and temperature) and disperse water on your heater automatically 
with a fully customizable timetable and adjustable amount of water.
<br />
<br />

## Settings:

All settings can be defined in a _config_ file:
  - To have the freedom of creating your own electrical circuit with other peripherals, you can specify the In- and Outputs in the *config* file:
    In- / Output | Function
    ------------ | -------------
    Output | Sauna On / Off
    Output | Water Pump On / Off
    Input | Thermometer
    Input | Hygrometer
    Multi | Display (HMI)

  - You can specify the interface and port SpaPi will listen on for REST API HTTP requests.
  - An Graphical User Interface can be chosen to replace the standard one.
<br />

## REST API:

**SpaPi** uses a REST API server to make it possible for other developers to create their own App / Graphical User Interface for controlling **SpaPi**.
For example: [SpaAssist](https://github.com/appiekap653/SpaAssist) is an other project of mine to intergrate SpaPi into [HomeAssistant](https://www.home-assistant.io/).
<br />
<br />

## Components I'm using:
I'm using the following components in my setup to control my sauna and to automaticly disperse water on my heater.

Sauna Control | Waterflow | Thermometer | Hygrometer | Display
--- | --- | --- | --- | ---
2x Relais (Spoel: DC5V 760mA, Load: 250VAC 30A), one is used for the heater* , the other for the water pump. | Micro Water Pump 120L/H DC2.5-6V 130-220mA, Low Noise Brushless Motor | DS18B20, Temperature range: -55°C to +125°C | DHT22 AM2302, Humidity range: 0-100% RH, Temperature range: -40 to +80°C | Inside the sauna: 1.8" Serial SPI 128x160 Color TFT LCD. Showing Temperature and Humidity values

**\* make sure the _load_ covers your _heater ratings_!**
<br />
<br />

My water disperse system is still a work in progress.<br />
At the moment i'm using a bucket with the water pump on the bottom, the hose leads to an aquarium outlet with small holes and is placed offset of my heater with an aluminium plate to cover the gap.<br />
I'm planning on manufacturing some simular construction made of stainless steel

![Image of water disperse setup](https://github.com/appiekap653/SpaPi/blob/development/resources/water_disperse_setup.png)

![Image of display setup](https://github.com/appiekap653/SpaPi/blob/development/resources/display_setup.png)

