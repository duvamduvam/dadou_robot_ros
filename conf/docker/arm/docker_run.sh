  #!/bin/bash
  #docker run -u=$(id -u $USER):$(id -g $USER) -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v $(pwd)/app:/app --rm nodes-helloworld
  docker container run -u=$(id -u $USER):$(id -g $USER) -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v $HOME/.Xauthority:/root/.Xauthority:rw -v $(pwd)/app:/app --rm ros-helloworld
