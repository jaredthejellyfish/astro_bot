from datetime import datetime
import csv
import time

class Location:
    # Initialize transaction and add values to self.
    def __init__(self, chat_id, lat, lon):
        self.chat_id = chat_id
        self.time = int(time.time())
        self.lat = lat 
        self.lon = lon 

    # Return all values from transaction as a dictionarty object.
    def as_dict(self):
        return {'CHAT_ID': self.chat_id, 'TIME': self.time, 'LAT': str(self.lat), 'LON': self.lon}
    
    # Representation method
    def __repr__(self):
        return 'Location for user {} at {} is {}, {}'.format(self.chat_id, self.time, self.lat, self.lon)

class Database:
    def __init__(self, chat_id):
        # Generate the filename for the database file.
        fname = 'database.csv'

        try:
            f = open(fname)
            print('opened')
        except:
            f = open(fname, 'w+')
            writer = csv.writer(f)
            writer.writerow(['CHAT_ID', 'TIME', 'LAT', 'LON'])
        
        f.close
        self.filename = fname
    
dab = Database('123333211')