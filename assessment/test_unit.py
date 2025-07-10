from assessment.extensions import db
from assessment.model import Status

def test_working(client): #tests if the app is actually running and returns working
    response = client.get('/')
    assert b"working" in response.data 

def test_status_post(client, app): #tests that posting to /status fills the DB correctly
    input = {"device_id": "sensor-abc-123", "timestamp": "2025-06-09T14:00:00Z", "battery_level": 76, "rssi": -60, "online": True}
    with app.app_context():
        client.post('/status', json = input)
        checkthis = str(Status.query.first())
        assert Status.query.count() == 1 #check if there is a single row in our database
        assert "sensor-abc-123" in checkthis #ensures the data is accurate
        assert "2025-06-09T14:00:00Z" in checkthis
        assert "76" in checkthis
        assert "True" in checkthis

def test_status_post_battery_OOB(client, app): #tests tthat posting a battery level outside of the 0-100 range throws error 500, while ensuring DB accepts at 0 and 100
    input_over = {"device_id": "sensor-abc-123", "timestamp": "2025-06-09T14:00:00Z", "battery_level": 101, "rssi": -60, "online": True}
    input_under = {"device_id": "sensor-abc-123", "timestamp": "2025-06-09T14:00:00Z", "battery_level": -1, "rssi": -60, "online": True}
    input_100 = {"device_id": "sensor-abc-123", "timestamp": "2025-06-09T14:00:00Z", "battery_level": 100, "rssi": -60, "online": True}
    input_0 = {"device_id": "sensor-abc-123", "timestamp": "2025-06-09T14:00:00Z", "battery_level": 0, "rssi": -60, "online": True}
    with app.app_context():
        response_over = client.post('/status', json = input_over)
        assert response_over.status_code == 500

    with app.app_context():    
        response_under = client.post('/status', json = input_under)
        assert response_under.status_code == 500

    with app.app_context():
        response_100 = client.post('/status', json = input_100)
        assert response_100.status_code == 200

        response_0 = client.post('/status', json = input_0)              
        assert response_0.status_code == 200
    

def test_status_given_device_recent(client, app): #tests that /status/<device_id> returns only the most recent of the device's statuses
    with app.app_context():
        status = Status("VERYWRONG", "2025-06-10T14:00:00Z", 76, -60, True)
        db.session.add(status)
        status = Status("sensor-abc-123", "2025-07-03T14:00:00Z", 76, -60, True) #mock up database with 2 sensors and our target with 3 unique timestamps to check it returns most recent status of the given sensor
        db.session.add(status)
        status = Status("sensor-abc-123", "2025-07-07T14:00:00Z", 76, -60, True)
        db.session.add(status)
        status = Status("sensor-abc-123", "2025-06-09T14:00:00Z", 76, -60, True)
        db.session.add(status)
        status = Status("VERYWRONG", "2025-06-11T14:00:00Z", 76, -60, True)
        db.session.add(status)
        db.session.commit()
        response = client.get('/status/sensor-abc-123')
        assert b"sensor-abc-123" in response.data
        assert b"2025-07-07T14:00:00Z" in response.data   #ensure most recent is in the response, but exclude all others
        assert b"2025-07-03T14:00:00Z" not in response.data
        assert b"2025-06-09T14:00:00Z" not in response.data
        assert b"VERYWRONG" not in response.data
        

def test_status_given_device_history(client, app): #tests that /status/<device_id>/history returns all statuses of a given device
    with app.app_context():
        status = Status("VERYWRONG", "2025-06-10T14:00:00Z", 76, -60, True) #mock up database with 2 sensors with our target having 3 unique timestamps and check it returns all for given sensor
        db.session.add(status)
        status = Status("sensor-abc-123", "2025-07-03T14:00:00Z", 76, -60, True)
        db.session.add(status)
        status = Status("sensor-abc-123", "2025-07-07T14:00:00Z", 76, -60, True)
        db.session.add(status)
        status = Status("sensor-abc-123", "2025-06-09T14:00:00Z", 76, -60, True)
        db.session.add(status)
        status = Status("VERYWRONG", "2025-06-11T14:00:00Z", 76, -60, True)
        db.session.add(status)
        db.session.commit()
        response = client.get('/status/sensor-abc-123/history')
        assert b"sensor-abc-123" in response.data
        assert b"2025-07-07T14:00:00Z" in response.data   #ensure all of device status are present
        assert b"2025-07-03T14:00:00Z" in response.data
        assert b"2025-06-09T14:00:00Z" in response.data
        assert b"VERYWRONG" not in response.data

def test_status_summary_recent(client, app): #tests that /status/summary returns only the most recent of each device's statuses
    with app.app_context():
        status = Status("sensor-abc-123", "2025-07-03T14:00:00Z", 76, -60, True) #mock up database with 3 sensors each with 2 timestamps and assert that only the 3 most recent ones are in output
        db.session.add(status)
        status = Status("sensor-abc-123", "2025-07-07T14:00:00Z", 76, -60, True)
        db.session.add(status)

        status = Status("sensor-xyz-321", "2025-06-08T14:00:00Z", 76, -60, True)
        db.session.add(status)
        status = Status("sensor-xyz-321", "2025-06-03T14:00:00Z", 76, -60, True)
        db.session.add(status)
        
        status = Status("sensor-AAA-314", "2025-06-07T14:00:08Z", 76, -60, True)
        db.session.add(status)
        status = Status("sensor-AAA-314", "2025-06-07T14:00:00Z", 76, -60, True)
        db.session.add(status)
        
        db.session.commit()
        response = client.get('/status/summary')
        assert b"sensor-abc-123" in response.data
        assert b"2025-07-07T14:00:00Z" in response.data   #ensure most recent of each device is present, exclude others
        assert b"2025-07-03T14:00:00Z" not in response.data
        
        assert b"sensor-xyz-321" in response.data
        assert b"2025-06-08T14:00:00Z" in response.data
        assert b"2025-06-03T14:00:00Z" not in response.data

        assert b"sensor-AAA-314" in response.data
        assert b"2025-06-07T14:00:08Z" in response.data
        assert b"2025-06-07T14:00:00Z" not in response.data

