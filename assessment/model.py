
from assessment.extensions import db

class Status(db.Model):
        status_id = db.Column(db.Integer, primary_key = True) #the id for this specific status update, primary key
        device_id = db.Column(db.String)
        timestamp = db.Column(db.String)
        battery_level = db.Column(db.Integer, db.CheckConstraint('battery_level >= 0 AND battery_level <= 100'))
        rssi = db.Column(db.Integer)
        online = db.Column(db.Boolean)

        def __init__(self, device_id, timestamp, battery_level, rssi, online):
                self.device_id = device_id
                self.timestamp = timestamp
                self.battery_level = battery_level
                self.rssi = rssi
                self.online = online

        def __repr__(self):
               return f'Status of {self.device_id} at {self.timestamp} \nBattery Level: {self.battery_level} \nRSSI: {self.rssi} \nOnline:{self.online}'