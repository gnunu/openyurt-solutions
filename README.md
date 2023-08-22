# openyurt-solutions

## onvif
### build container image:
```sh
$ git clone https://github.com/gnunu/openyurt-solutions.git

$ cd openyurt-solutions/docker
$ docker buildx build -t dlstreamer-onvif --platform=linux/amd64 --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} .

test:
start the pipeline server:
$ docker run --rm -p 55555:55555 dlstreamer-onvif:latest
or with gpu access:
$ docker run --rm -p 55555:55555 --device /dev/dri --group-add=$(stat -c "%g" /dev/dri/render* | uniq) dlstreamer-onvif:latest
(render group is not static, so we need to add it on deployment)

on client side:
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "filesrc", "url": "bbc-fish.mp4", "model": "horizontal-text-detection-0001.xml", "dev": "CPU"}' http://<openvino-service-ip>:55555/pipeline
to use GPU:
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "filesrc", "url": "bbc-fish.mp4", "model": "horizontal-text-detection-0001.xml", "dev": "GPU"}' http://<openvino-service-ip>:55555/pipeline
or,
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "filesrc", "url": "bbc-fish.mp4", "model": "horizontal-text-detection-0001.xml", "dev": "AUTO"}' http://<openvino-service-ip>:55555/pipeline

send a rtsp stream:
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "rtspsrc", "user-id": "admin", "user-pw":"passwd", "url": "rtsp://<camera-ip>:554/Streaming/Channels/101", "model": "horizontal-text-detection-0001.xml", "dev": "AUTO"}' http://<openvino-service-ip>:55555/pipeline

```

### deploy rtmp server
```sh
$ docker run -d -p 1935:1935 -p 8080:8080 alqutami/rtmp-hls
(this one has fast response than the nginx one)

to test in our container:
$ gst-launch-1.0 \
rtspsrc user-id="user-id" user-pw="user-pw" location=rtsp://<camera-ip>/stream1 ! decodebin ! \
gvainference model=/home/dlstreamer/models/horizontal-text-detection-0001.xml device=AUTO ! queue ! \
gvafpscounter ! gvawatermark ! videoconvert ! vaapih264enc ! h264parse ! flvmux ! rtmp2sink location=rtmp://<rtmp-service-ip>:1935/live/test

use rest api (json):
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "rtspsrc", "user-id": "admin", "user-pw":"passwd", "url": "rtsp://<camera-ip>:554/Streaming/Channels/101", "model": "horizontal-text-detection-0001.xml", "dev": "AUTO", "rtmp2sink": "rtmp://<rtmp-service-ip>:1935/live/test"}' http://<openvino-service-ip>:55555/pipeline

```

### deploy in k8s cluster:
<<TODO>>


