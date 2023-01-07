import os
import math
import http.client, urllib.parse
import json
import requests
from configparser import ConfigParser


def user_input():
    
    #Geting initial user input (location of a ground station)
    print("=======USER INPUT======")
    print("Ground station location details: ")
    country_input = input("Enter country: ")
    city_input = input("Enter city name: ")
    country = country_input.title()
    city = city_input.title()
    #parsing data to geo_location funtion
    geo_location(country, city)

def geo_location(country, city):
    #Open http.client connection
    conn = http.client.HTTPConnection('geocode.xyz')
    #Read config file (api keys)
    config_obj = ConfigParser()
    config_obj.read("sat_config.ini")
    user_info = config_obj["USERINFO"]
    geo_api = user_info["geo_api"]
    n2yo_api = user_info["n2yo_api"]
    dec_api = user_info["dec_api"]
    #Join location data into string
    location = country + ' , ' + city
    #Preparing api request data
    params = urllib.parse.urlencode({
        'auth': geo_api,
        'locate': location,
        'json': 1,
        })
    #Sending request to geocode.xyz
    conn.request('GET', '/?{}'.format(params))

    #Formating json response
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)

    print("\n=======RESULTS=======")
    print("Ground station location:")
    #longitude and latitude variable initialization
    float_long = 0.0
    float_latt = 0.0
    
    #iterate json response and updating variable values
    for key, value in result.items():
        if key == 'longt':
            float_long = float(value)
            
            
        if key == 'latt':
            float_latt = float(value)
            
            
    #api request for magnetic declination
    dec_resp = requests.get("https://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination?lat1={}&lon1={}&key={}&resultFormat=json".format(float_latt,float_long,dec_api))
    dec_result = dec_resp.json()
    #magnetic declination variable initialization
    float_dec = 0.0
    #iterarte json response and updating variable values
    for i in dec_result['result']:
        float_dec=i['declination']
    
    #Print ground station details
    print("Country: "+ country + "\n" + "City: " + city + "\nLongitude: "+ str(round(float_long, 2))+"\nLatitude: " + str(round(float_latt, 2)) + "\nMagnetic declination: "+ str(round(float_dec, 2)))
    #Parse data to sat_above function
    sat_above(float_dec,float_long,float_latt,n2yo_api)

def sat_above(float_dec,float_long,float_latt,n2yo_api):
    print("----------------------------------------------------------")
    #Optional user input for narrowing the satellite searching scope
    usr_input = input("\nEnter the first few characters of the satellite name you are searching for (OPTIONAL): ")
    select = usr_input.upper()
    #api request to n2yo - select every geostationary satellite above the horizon
    response = requests.get("https://api.n2yo.com/rest/v1/satellite/above/{}/0/0/90/10/&apiKey={}".format(float_latt,n2yo_api))
    result = response.json()
    #Initialize satnames,satlongs and norad id lists
    satnames = []
    satlongs = []
    satnorad = []
    #Iterate json response and append results into lists
    for i in result['above']:
        satnames.append(i['satname'])
        satlongs.append(i['satlng'])
        satnorad.append(i['satid'])
     
     
    #Iterate satname list with user input 'select'
    starts = [n for n, l in enumerate(satnames) if l.startswith(select)]
    #Printing combined result from lists
    for n in starts:
        z = n
        print("\nNORAD ID: " + str(satnorad[z]) + " Name: " + satnames[z] + " Longitude: " + str(satlongs[z]))
    #User input with satellite NORAD ID
    usr_sat_choice = input("\nEnter NORAD ID of the satellite you want to track: ")

    #Getting index of element in satnorad list
    match = satnorad.index(int(usr_sat_choice))
    print("\n======= SELECTED satellite =======\n" + "NORAD ID: " + str(satnorad[match]) + " Name: " + satnames[match] + " Longitude: " + str(satlongs[match]))
    #Match norad id with satellite longitude value
    satlong = satlongs[match]
    #Parsing data for final calculations
    az_elev(satlong, float_dec, float_long, float_latt)     
    
def az_elev(satlong, float_dec, float_long, float_latt):        
    #Initialize 1 radian in degrees 2*pi*rad = 360
    r=57.29578
    #calculte difference betwen sat longitude and ground station longitude
    g_value = satlong - float_long


   
    #calculate values in radians with math library
    radiansL = float_latt/r
    radiansG = g_value/r
    elevRadG = math.cos(radiansG)
    elevRadL = math.cos(radiansL)

    #calculate azimuth angle in radians
    #The math.atan() method returns the arc tangent of a number (x) as a numeric value between -PI/2 and PI/2 radians.
    #Arc tangent is also defined as an inverse tangent function of x, where x is the value of the arc tangent is to be calculated.
    
    def az1():
        return (3.14159-(math.atan((math.tan(radiansG)/math.sin(radiansL)))))
    #convert azimuth angle from radians to degrees
    def azimuth():
        return az1()*r
    #calculate azimuth angle with magnetic declination
    def az_dec():
        return azimuth()+float_dec
    #calculate elevation anlge in radians
    #-.1512 constant value
    def elev1():
        return math.atan((elevRadG*elevRadL-.1512)/(math.sqrt(1-(elevRadG*elevRadG)*(elevRadL*elevRadL))))
    def elevation():
        return elev1()*r
    
    #Print results with sugested magnetic declination correction

    print("\n========== GROUND STATION CONFIG ===============")
    #For proper communication elevation must be over 7 degrees
    if elevation() > 7:
        print("Azimuth angle (true north): {}".format(round(azimuth(),2)))
        print("Azimuth angle with magnetic declination correction: {}".format(round(az_dec(),2)))
        print("Elevation angle: {}".format(round(elevation(),2)))
    else:
        print("Satellite is unreachable from your location")


def main():
    #clear terminal screen before running a script
    os.system('cls' if os.name == 'nt' else 'clear')
    user_input()
   

if __name__ == '__main__':
    main()