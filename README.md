Hello! This is Morgan Yang's solution for the Ubiety Technical Assessment!

To get started, download the file and change directory into 'ubietyTechAssessment'.
Next, type 'python -m venv .venv' into the terminal and hit enter to set up our virtual enviornment.
Then start up the virtual enviornment with '.venv/Scripts/activate' and enter.
Next, install nessesary dependencies to the enviornment with 'pip install -r requirements.txt' and hit enter.

To run the app, make sure you are in the 'ubietyTechAssessment' directory and type 'python -m assessment.app'
I am using the Postman plugin on VScode to feed GET and POST requests to the API.
When the app starts running, there should be a line in the terminal telling what its address is.
Use address from the step above and append the routes in 'routes.py' in postman to use GET and POST features.
Included is 'example.JSON', which can be pasted into Postman and fed into the app's DB through POST 'address/status'.

To run the app's tests, simply run 'pytest' in the 'ubietyTechAssessment' directory.
This will run the unit tests in 'test_unit.py' and the integration test in 'test_integration.py'.
Refer to comments for test context.

When writing up the app, I wanted to use the Application Factory approach, where I define the creation of the app in a function and register blueprints
connected to the endpoints. This allows easy implementation of pytest with a test application. For the design of the app itself, I have the database keep
all statuses stored so that any historical status can be accessed, while other routes use queries to find get specific data.

As for the tests, I didn't do much test writing in pytest prior to this, so reading up methodology and documentation was quite a fun experience!
I have the SQLAlchemy URI set to 'sqlite://' which creates the database in memory and tears it down automatically at the end of the test.

For unit tests, there are 6 tests, which in order test the following.
1. 'test_working' tests if the app can run an instance
2. 'test_status_post' tests if POST '/status' creates a database entry and the the data matches what was entered
3. 'test_status_post_battery_OOB' tests that the database does not take a batter status not from 0-100. I chose to include 0 since sometimes devices will say they are at 0% when they are near, but it is simple to set the constraint to not include 0.
4. 'test_status_given_device_recent' tests that '/status/<device_id>' returns the most recent status of the given device
5. 'test_status_given_device_history' tests that '/status/<device_id>/history' returns all statuses of the given device
6. 'test_status_summary_recent' tests that 'status/summary' returns all devices, but only their most recent status

As for the integration test, 'test_post_and_get_statuses' tests if all the /GET endpoints of the API return the correct data after it is fed through /POST

For the bonus features, I implemented the historical updates. The database keeps all statuses posted to it, and in its /summary and 
/device_id routes, returns the latest with a sorted query. Returning historical updates just requires returning all rows after filtering 
for a specific device_id column. 

I did want to implement containerization bonus using Docker to easily and seamlessly spin up the app
across different evniornments, but Docker Desktop was not being very cooperative and was not recognizing my WSL installation.
During our next meeting I would love to talk a little about this as well as learn more about Docker-Compose implementation!

I did not get around to implementing the authentication bonus, but I did read up on different methods. I think given more time it would be neat to try and implement a login system where the backend keeps a database of users and passwords, and requires login to view endpoints that contain device status. 