# Urban4Cast
## Forecasting Parking Availability and Traffic Flow
The project is based on Prophet separated into three main python files: `parking4cast.py`, `parking4cast_bystreet.py` and `trafficflow.py`.

### Parking Availability 

The `parking4cast.py` script accepts a CSV (comma-delimited file) with columns: 
  - TimeStamp (renamed as `ds`) (with format yyyy-mm-dd hh:mm:ss);
  - AvailableSpots (renamed as `y`) - this can be changed and use Occupancy as the `y` column;
  - And 6 more columns (e.g., OccupiedSpotsNo, OccupiedDuration, AvailabilityDuration, Occupancy, OccupiedDurationPerSpot and OccupiedDurationPercentage)

This file works with a pre-defined 10 periods and a frequency of 15 minutes.

The `parking4cast_bystreet.py` script accepts a CSV (comma-delimited file) with columns: 
  - Time (rennamed as `ds`) (with format yyyy-mm-dd hh:mm:ss);
  - Latitude, Longitude, ID and Value:
    - The ID represents the sensor identifier;
    - The Value is the sensor's binary result (0, 1).

After removing all the duplicated results and resorting to GeoPandas, the script should find all the street names of each sensor and add this information to a dictionary. Then, apply the dictionary to the initial dataframe and create a second dataframe by defining the **street name**.
This file works with a pre-defined 10 periods and a frequency of 10 minutes.

**When running Prophet, there needs to be two defined columns, `ds` and `y`.**

### Traffic Flow

This solution is based on historical data obtained on the open-source data from [Paris Data](#https://parisdata.opendatasoft.com/explore/dataset/comptages-routiers-permanents/).

The `trafficflow.py` script accepts a CSV (comma-delimited file) with columns: 
  - Time (rennamed as `ds`) (with format yyyy-mm-dd hh:mm:ss);
  - "Etat_traffic" (renamed as `y`)
  - And 3 more columns (q - Throughput (number of vehicles counted during the hour), k - Occupancy rate (as a percentage of the time the measuring station is occupied by vehicles per hour) and etat_barre - Open state or not (barred, unknown or invalid) to the circulation)

Similarly to `parking4cast_bystreet.py`, it can also be defined by road by adding a sixth column which defines the label of the track observed (libelle)
This file works with a pre-defined 10 periods and a frequency of 2 hours.


# Using the docker image

In order to use the project as a docker container, you can use the provided docker-compose configuration.

First, you have to build the image, using `docker-compose build`. Please note that the Python packages required for this project might take a long time to install.

After this, running `docker-compose run --rm urban4cast` will start the container and run the `parking4cast.py` script for generating parking forecasts. The forecasts are placed in the root directory, which is shared as a volume between the host and the docker container.
