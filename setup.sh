#!/bin/bash
#Creating the docker container...
docker run -d --name wca_competition_predictor_container wca_competition_predictor
#Setup the app, this might take a few minutes
docker exec -it wca_competition_predictor_container /bin/bash
./setup.sh
#Finished!
