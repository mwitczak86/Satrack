# Satrack - azimuth and elevation angle calculator.
A Python application that calculates the azimuth and elevation angles for pointing a satellite antenna towards a specific geostationary satellite. The calculation takes into account the location of the antenna and the magnetic declination at that location. The list of available geostationary satellites is obtained using the N2YO API.

![Azimuth_and_elevation_angles](/Demo_images/satrack.jpg)

## How does it work?
#### Azimuth equation:

$A = 180 + \arctan[\frac{\tan(G)}{\sin(L)}]$

<br>$A$ = azimuth of antenna in degrees
<br>$S$ = satellite longitude in degrees
<br>$N$ = ground station longitude in degrees
<br>$L$ = ground station latitude in degrees
<br><b>G=S-N</b>

#### Elevation equation:

$E = \arctan[\frac{\cos(G)\cos(L)-.1512}{\sqrt{1-cos^{2}(G)cos^{2}(L)}}]$
   

    
<br>$E$ = elevation of antenna in degrees
<br>$S$ = satellite longitude in degrees
<br>$N$ = ground station longitude in degrees
<br>$L$ = ground station latitude in degrees
<br><b>G=S-N</b>

#### Why you should include magnetic declination in your configuration?:
Magnetic declination, also known as magnetic variance, is the angle between true north and magnetic north. It is important because compasses, which are used for navigation, are based on the Earth's magnetic field and not true north. If the declination is not taken into account, the compass will give an incorrect reading and lead to an incorrect destination. In some areas, the declination can be quite large and can cause significant errors if not accounted for.

For example, if the declination in a particular location is 15 degrees east of true north, the equation would be:

<b>Declination = (Magnetic North - True North) + East
= (Magnetic North - True North) + 15 degrees</b>


This means that if you are facing magnetic north with a compass, you will need to add 15 degrees to your bearing in order to get your true bearing.

![Azimuth_and_elevation_calculator](/Demo_images/satrack.gif)

## Requirements
1. Install Python 
1. Register on https://www.n2yo.com/api/ get your own API key for geostationary satellites list
2. Register on https://geocode.xyz/api get your own API key for geographic coordinates
3. Register on https://www.ngdc.noaa.gov/ get your own API key needed to calculate magnetic declination
4. Put your API keys into sat_config.ini file
5. Tested on Windows 10 OS.

## Inspiration
https://tiij.org/issues/issues/3_2/3_2e.html

## License
This project is licensed under the ISC License - see the LICENSE.md file for details

### Author
M.Witczak