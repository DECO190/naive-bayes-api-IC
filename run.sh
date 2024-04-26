#!/bin/bash
docker run -d -p 5500:5500 -it --name naivebayes-container --mount type=bind,source=.,target=/home/USER/naivebayes naivebayes-image:latest
