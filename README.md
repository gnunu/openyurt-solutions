# openyurt-solutions

## onvif
```sh
$ git clone https://github.com/gnunu/openyurt-solutions.git

build container image:
$ cd openyurt-solutions/docker
$ docker buildx build -t dlstreamer-onvif --platform=linux/amd64 --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} .

to test:
start the pipeline server:
$ docker run --rm -p 55555:55555 dlstreamer-onvif:latest
or with gpu access:
$ docker run --rm -p 55555:55555 --device /dev/dri --group-add=$(stat -c "%g" /dev/dri/render* | uniq) dlstreamer-onvif:latest
(render group is not static, so we need to add it on deployment)

on client side:
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "filesrc", "url": "bbc-fish.mp4", "model": "horizontal-text-detection-0001.xml", "dev": "CPU"}' http://localhost:55555/pipeline
to use GPU:
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "filesrc", "url": "bbc-fish.mp4", "model": "horizontal-text-detection-0001.xml", "dev": "GPU"}' http://localhost:55555/pipeline
or,
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "filesrc", "url": "bbc-fish.mp4", "model": "horizontal-text-detection-0001.xml", "dev": "AUTO"}' http://localhost:55555/pipeline

send a rtsp stream:
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "rtspsrc", "user-id": "admin", "user-pw":"passwd", "url": "rtsp://10.238.157.61:554/Streaming/Channels/101", "model": "horizontal-text-detection-0001.xml", "dev": "AUTO"}' http://localhost:55555/pipeline

to deploy in k8s cluster:
<<TODO>>


```
