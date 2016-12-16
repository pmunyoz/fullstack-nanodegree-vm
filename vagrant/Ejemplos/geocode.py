import httplib2
import json

def getGeocodeLocation(inputString):
    google_api_key = "AIzaSyBXijzBsvT-L3s4lURv2qgAjjZkSXr8n7A"
    locationString = inputString.replace(" ","+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    latitud = result['results'][0]['geometry']['location']['lat']
    longitud = result['results'][0]['geometry']['location']['lng']
    return (latitud, longitud)
