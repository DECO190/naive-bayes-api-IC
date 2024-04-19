#!/bin/bash
docker run -d -p 5500:5500 -it --name nb --mount type=bind,source=.,target=/home/deco/naivebayes naive-bayes:latest 
