from flask import request, Blueprint
from sqlalchemy import desc

from assessment.extensions import db

from assessment.model import Status

main = Blueprint("main", __name__)

@main.route('/')
def start():
        return('working')

@main.route('/status',  methods = ['POST']) #Adds a new row to the DB
def add_status():
        status = Status(device_id = request.json['device_id'], \
                        timestamp = request.json['timestamp'], \
                        battery_level = request.json['battery_level'], \
                        rssi = request.json['rssi'], \
                        online = request.json['online'])
        db.session.add(status)
        db.session.commit() 
        return {'device_id': status.device_id, \
                'timestamp': status.timestamp, \
                'battery_level': status.battery_level, \
                'rssi': status.rssi, \
                'online': status.online} #this chunk just shows you the data you sent to the database
        

@main.route('/status/summary') #returns each unique device's most recent status by timestamp
def get_all_statuses():
        statuses = Status.query.order_by(desc(Status.timestamp)).all() #fetches all statuses, ordered by most recent timestamp
        output = []
        firstPass = True
        for status in statuses:
             if firstPass == True: #since we ordered by timestamp, the first status will always be the most recent from whatever device it is
                status_data = [] #I initially tried dict, but order of keys is not preserved when returning the output, even in ordereddict, so instead I am preserving the order of output using a list of lists
                status_data.append('Device ID: ' + status.device_id)
                status_data.append('Time of last update: ' + status.timestamp)
                status_data.append('Battery level: ' + str(status.battery_level))
                status_data.append('Online status: ' + str(status.online))
                firstPass = False #now we set this to false because we need to check every status thereafter to make sure its not a device already present
                output.append(status_data)
             else:
                noDupe = True
                for item in output:       #simple loop to prevent a device having more than 1 status
                        if (('Device ID: ' + status.device_id) in item):
                                noDupe = False
                        
                if noDupe == True: #to touch on an earlier mentioned idea - the first instance of a device will contain its status with the most recent timestamp
                        status_data = []
                        status_data.append('Device ID: ' + status.device_id)
                        status_data.append('Time of last update: ' + status.timestamp)
                        status_data.append('Battery level: ' + str(status.battery_level))
                        status_data.append('Online status: ' + str(status.online))
                        output.append(status_data)
        return output

@main.route('/status/<device_id>') #retrieves most recent status of device in route
def get_device_status(device_id):
        status = Status.query.filter(Status.device_id == device_id).order_by(desc(Status.timestamp)).first() #uses similar methodology as summary, but with only the rows that have matching device id column
        status_data = []
        status_data.append('Device ID: ' + status.device_id)
        status_data.append('Time of last update: ' + status.timestamp)
        status_data.append('Battery level: ' + str(status.battery_level))
        status_data.append('RSSI: ' + str(status.rssi))        
        status_data.append('Online status: ' + str(status.online))        
        return(status_data)

@main.route('/status/<device_id>/history')
def get_device_status_history(device_id):
       status = Status.query.filter(Status.device_id == device_id).order_by(desc(Status.timestamp)).all() #fetches all rows (statuses) in the DB with device id that matches the route
       outputs = []
       for item in status:
                output = []
                output.append('Device ID: ' + item.device_id)
                output.append('Time of last update: ' + item.timestamp)
                output.append('Battery level: ' + str(item.battery_level))
                output.append('RSSI: ' + str(item.rssi))        
                output.append('Online status: ' + str(item.online))    
                print(item.device_id)

                outputs.append(output)

       return outputs

