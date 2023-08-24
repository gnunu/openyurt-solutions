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
$ curl -X POST -H 'Content-Type: application/json' -d '{"src": "rtspsrc", "user-id": "admin", "user-pw":"passwd", "url": "rtsp://<camera-ip>:554/Streaming/Channels/101", "model": "horizontal-text-detection-0001.xml", "dev": "AUTO", "rtmpsink": "rtmp://<rtmp-service-ip>:1935/live/test"}' http://<openvino-service-ip>:55555/pipeline

```

Note: to use pushing stream feature (rtmp sink), GPU is used (vaapih264enc), so at least an iGPU should be present on the worker node.

### deploy in k8s cluster:
to use GPU, for video encoding and AI inference, intel-gpu-plugin should be deployed.

```sh
Install to nodes with NFD (Node Feature Disvovery), Monitoring and Shared-dev
$ kubectl apply -k 'https://github.com/intel/intel-device-plugins-for-kubernetes/deployments/nfd?ref=v0.27.1'
$ kubectl apply -k 'https://github.com/intel/intel-device-plugins-for-kubernetes/deployments/nfd/overlays/node-feature-rules?ref=v0.27.1'
$ kubectl apply -k 'https://github.com/intel/intel-device-plugins-for-kubernetes/deployments/gpu_plugin/overlays/monitoring_shared-dev_nfd/?ref=v0.27.1'

```
to deploy workload and a nodeport service for access from outside:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: onvif-demo
  labels:
    app: onvif-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: onvif-demo
  template:
    metadata:
      labels:
        app: onvif-demo
    spec:
      containers:
      - name: onvif-demo
        image: aibox03.bj.intel.com:5000/dlstreamer-onvif:latest
        imagePullPolicy: IfNotPresent
        command: [ "/home/dlstreamer/openyurt-solutions/onvif/pipeline.py" ]
        securityContext:
          # note render group is not stable
          runAsGroup: 105
        resources:
          limits:
            gpu.intel.com/i915: 1
        ports:
        - containerPort: 55555
---
apiVersion: v1
kind: Service
metadata:
  name: onvif-demo
spec:
  selector:
    app: onvif-demo
  type: NodePort
  ports:
  - name: http
    port: 55555
    targetPort: 55555
    nodePort: 30036
    protocol: TCP

```
