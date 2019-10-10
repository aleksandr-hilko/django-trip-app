# Django Trip App

App that allow customers to collaborate being moved around the city by either creating or searching relevant trips.

## What's used

* Docker + Docker Compose
* Django + Django REST Framework
* Postgres

## Setup Steps

1. Install Docker: `https://docs.docker.com/install/linux/docker-ce/ubuntu/` (check the menu on the left for other OS-s)
2. Install Docker Compose: `https://docs.docker.com/compose/install/`
3. Clone the current repo somewhere.

4. Go to the `{project_name}`:<br/>

    `cd {project_name}`

5. To run the tests you should type:

* `make test` - this will build a test Docker image and run the tests automatically.

6. Run `docker-compose -f docker-compose.yaml -f docker-compose.setup.yaml up` if you have
   you have dependencies updated / model migrations changed, otherwise run `docker-compose up'

    You can check that your server is now working in a browser:
        `http://127.0.0.1:8000/api/accounts/`
    Press `Ctrl+C` when completed to stop the services.
    
 ## Description of API endpoints
 
 #### 1. POST api/trips/ -  Create a new trip.
 
 * Description - As being a driver who wants to create a trip and accept passengers
 on board you can create this via specified endpoint.
 * Request body parameters (* - required parameters):
 ```
   {
        dep_time*: datetime,
        start_point*: str (see comment below),
        dest_point*: str (see comment below),
        price: positive int,
        num_seats*: positive int,
        description: str,
        is_active: bool (default False),
        man_approve: bool (default True)
    }
 ```

Comment: start_point and dest_point parameters represent geo coordinates of start point and 
endpoint of a trip, therefore the string input should consist of 2 floats the first is longitude and
the second is latitude of a point. Supported formats are: 
 "23.5 23.5", "[23.5 23.5]", "[23.5, 23.5]", "(23.5, 23.5)", "23.5, 23.5"

 #### 2. GET api/trips/ -  Get trips.
 
 * Description:
       As being a person who wants to commute to a certain address you are interested 
 in searching for trips with specific start and destination coordinates, departure time, etc... This
 endpoint should help you to do this.
 
 * Query string parameters available:
 
    /api/trips/?time1={time1}&time2={time2}&sp={sp}&dp={sp}
    
    * time1 and time2 - you expect the trip to start between time1 and time2. So say you want to
      leave from your work between 15.00 and 15.30 on 7 October, then the parameters passed should be
      ```time1=2019-11-07%2015:00:00&time2=2019-11-08%2015:30:00```
    * sp and dp - stands for start point and destination point accordingly. These parameters represent 
    geo coordinates that you can take from a google map for example. The string input should consist of 2 floats 
    the first is longitude and the second is latitude of a point. Example:
    ```sp=53.914356%2027.602271&dp=53.928330%20%2027.630353```
  
  - Response:
  
      After you send the request with interested query params, you should get the list of trips
  that are relevant. The list should be sorted in the ascending order by the sum of dist1 and dist2
  parameters (see the example below). What it really means: dist1 - the distance between your desired 
  departure point trip departure time, and the dist2 distance between your and trip end point.
  The example of a response returned:
   ```
   {
            "id": 7,
            "driver": "user0",
            "passengers": [],
            "dep_time": "10/08/2019 08:03:40",
            "start_point": "-17.881069 -108.188611",
            "dest_point": "-64.691651 -56.982846",
            "price": 484,
            "free_seats": 2,
            "man_approve": false,
            "description": "False",
            "is_active": true,
            "dist1": "123.3040071 m",
            "dist2": "142.3964066 m
    }
 ```

#### 3. GET api/trips/{trip_id} -  Get a trip
   
   Permission: Authenticated user
   
#### 4. PUT api/trips/{trip_id} -  Update a trip

   Permission: Authenticated driver of a trip or admin

#### 5. DELETE api/trips/{trip_id} -  Delete a trip

   Permission: Authenticated driver of a trip or admin

#### 6. POST trips/{trip_id}/reserve - Reserve a place in a trip 

 * Description: As being a passenger who found the relevant trip and wants to reserve a place 
    in it you should do a request to this endpoint. Few rules take place here:
    * If the trip you are interested in assumes automatic acceptance of incoming requests
      then you will be instantly added to the passengers list
    * If the trip you are interested in assumes manual approve from the driver side your request would
      be sent to the driver, and the driver is able to approve/decline it. 
    
  * Response:
  
      Depending on the fact whether the trip requires manual approval from the driver or it is automatic
      you should get 200 response with the body containing either TripRequest created or Trip where the passenger
      is added to the passengers list.
      
      400 Request is sent in two cases:
      * when the user who is attempting to reserve the trip is a driver of this trip.
      * when you send the request for the trip in which there are now free seats.
 
 
#### 7. GET trips/{trip_id}/requests - Get a list of requests for a specific trip
   
