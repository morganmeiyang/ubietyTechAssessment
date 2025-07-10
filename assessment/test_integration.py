from assessment.extensions import db
from assessment.model import Status

def test_post_and_get_statuses(client, app): #tests if posted data is able to be accessed by the various GET endpoints
    input1 = {"device_id": "sensor-abc-123", "timestamp": "2025-06-09T14:00:00Z", "battery_level": 76, "rssi": -60, "online": True}
    input2 = {"device_id": "sensor-abc-123", "timestamp": "2025-06-07T14:00:00Z", "battery_level": 86, "rssi": -60, "online": True}
    input3 = {"device_id": "sensor-XYZ-321", "timestamp": "2025-07-07T14:00:00Z", "battery_level": 86, "rssi": -60, "online": True}
    input4 = {"device_id": "sensor-XYZ-321", "timestamp": "2025-07-08T14:00:00Z", "battery_level": 86, "rssi": -60, "online": True}
    with app.app_context():
        client.post('/status', json = input1)
        client.post('/status', json = input2)
        client.post('/status', json = input3)
        client.post('/status', json = input4)
        response_status_abc = client.get('/status/sensor-abc-123')
        response_status_abc_history = client.get('/status/sensor-abc-123/history')
        response_summary = client.get('/status/summary')

        assert b"sensor-abc-123" in response_status_abc.data            #the correct sensor is present in /status/<device_id>
        assert b"2025-06-09T14:00:00Z" in response_status_abc.data      #only the most recent status is present
        assert b"sensor-XYZ-321" not in response_status_abc.data
        assert b"2025-06-07T14:00:00Z" not in response_status_abc.data  #the incorrect status is not

        assert b"sensor-XYZ-321" not in response_status_abc_history.data        #Checks other sensor isnt present, then checks that both timestamps are present
        assert b"sensor-abc-123" in response_status_abc_history.data
        assert b"2025-06-09T14:00:00Z" in response_status_abc_history.data
        assert b"2025-06-07T14:00:00Z" in response_status_abc_history.data

        assert b"sensor-abc-123" in response_summary.data               #both sensors present in summary
        assert b"sensor-XYZ-321" in response_summary.data
        assert b"2025-06-09T14:00:00Z" in response_summary.data         #both most recent timestamps present
        assert b"2025-07-08T14:00:00Z" in response_summary.data
        assert b"2025-06-07T14:00:00Z" not in response_summary.data         #both least recent timestamps absent
        assert b"2025-07-07T14:00:00Z" not in response_summary.data
        

        