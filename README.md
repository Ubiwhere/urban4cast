# Using the docker image

In order to use the project as a docker container, you can use the provided docker-compose configuration.

First, you have to build the image, using `docker-compose build`. Please note that the Python packages required for this project might take a long time to install.

After this, running `docker-compose run --rm urban4cast` will start the container and run the `parking4cast.py` script for generating parking forecasts. The forecasts are placed in the root directory, which is shared as a volume between the host and the docker container.
