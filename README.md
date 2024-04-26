## SETUP THE DEVELOPMENT ENVIRONMENT

First, make sure you follow the instructions to [install Docker](https://docs.docker.com/desktop/install/linux-install/).

Then, proceed to build the development environment image.

```docker
docker build . -t naive-bayes --build-arg USERNAME="YOUR_USER_NAME"
```

This will setup a development environment with:

- All dependencies installed via pip
- All development files (already linked to git) are in: /home/$USER/naivebayes 

## RUNNING THE DEVELOPMENT CONTAINER

The development container is based in a bind port between the OS and the container. I also binded the code source with the container.

```docker
docker run -d -p 5500:5500 -it --name naivebayes-container --mount type=bind,source=.,target=/home/USER/naivebayes naivebayes-image:latest
```

## STOP (hard turn off) THE CONTAINER

To stop the container (will kill the process, like shutting down the machine)
```docker
docker stop naivebayes-container
```

And, conversely, to start again, use:
```
docker start naivebayes-container
```
