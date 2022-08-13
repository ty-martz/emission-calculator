import pandas as pd
import math

def load_airport_data(path='data/airports.csv'):
    airports = pd.read_csv(path)
    airp = airports[['iata_code', 'latitude_deg', 'longitude_deg']]
    airp = airp.dropna(axis=0)
    return airp

def deg_to_rad(deg):
    return deg*(math.pi/180)

def calculate_distance(from_iata,to_iata):
    '''
    parameters
        from_iata: iata code of departure airport
        to_iata: iata code of arrival airport
    returns distance in miles between coordinates
    '''

    # load airport data
    airp = load_airport_data()

    # using airports.csv get the lat/long from iata_codes
    from_airp = tuple(airp[airp['iata_code'] == from_iata][['latitude_deg', 'longitude_deg']].values[0])
    to_airp = tuple(airp[airp['iata_code'] == to_iata][['latitude_deg', 'longitude_deg']].values[0])

    #distance calculation according to Haversine formula
    R = 6371 # radius of Earth in miles
    dis_lat = deg_to_rad(to_airp[0] - from_airp[0])
    dis_lon = deg_to_rad(to_airp[1] - from_airp[1])
    a = math.sin(dis_lat/2)**2 + math.cos(deg_to_rad(from_airp[0]) * math.cos(deg_to_rad(to_airp[0]))) * math.sin(dis_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    d = R * c
    return d
