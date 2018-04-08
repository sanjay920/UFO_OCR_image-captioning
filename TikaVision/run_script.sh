#!/bin/sh
#!/bin/bash

#For Images and Videos
git clone https://github.com/USCDataScience/tika-dockers.git && cd tika-dockers 
docker build -f InceptionVideoRestDockerfile -t uscdatascience/inception-video-rest-tika .
docker run -p 8764:8764 -it uscdatascience/inception-video-rest-tika

#For Images 
#git clone https://github.com/USCDataScience/tika-dockers.git && cd tika-dockers
#docker build -f InceptionRestDockerfile -t uscdatascience/inception-rest-tika .
#docker run -p 8764:8764 -it uscdatascience/inception-rest-tika

