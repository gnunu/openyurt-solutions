#!/usr/bin/env python3

import os
from flask import Flask, request

'''
    pipeline server run with dlstreamer
    port: 55555
'''

workDir = "/home/dlstreamer/"
videoDir = workDir + "openyurt-solutions/onvif/tests/"
modelDir = workDir + "models/"

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/pipeline-kill', methods=['POST'])
def pipeline_kill():
    kill_cmd = f"pkill gst-launch-1.0"
    os.system(kill_cmd)

@app.route('/pipeline', methods=['POST'])
def pipeline():
    src = "rtspsrc"
    url = ""
    dev = "CPU"
    model = "horizontal-text-detection-0001.xml"
    userid = ""
    userpw = ""
    sink = "fakesink async=false"
    framerate = "queue"

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        if "url" in json:
            url = json["url"]
        else:
            return "url must not be null"
        if "src" in json:
            src = json["src"]
        if "framerate" in json:
            rate = json["framerate"]
            framerate = f"videorate ! video/x-raw,framerate={rate}/1 ! queue"
        if "dev" in json:
            dev = json["dev"]
        if "model" in json:
            model = json["model"]
        if "user-id" in json:
            userid = json["user-id"]
        if "user-pw" in json:
            userpw = json["user-pw"]
        if "rtmpsink" in json:
            sts = json["rtmpsink"]
            sink = f"queue ! gvawatermark ! videoconvert ! vaapih264enc ! h264parse ! flvmux ! rtmp2sink location={sts}"

        if src == "rtspsrc":
            if userid != "":
                src += f' user-id="{userid}" user-pw="{userpw}" '

        pipeline_cmd = create_pipeline(src=src, url=url, framerate=framerate, model=model, dev=dev, sink=sink)
        return pipeline_cmd + " created"
    else:
        return 'Content-Type not supported!'

def create_pipeline(src, url, framerate, model, dev, sink):
    model = modelDir + model
    if src == "filesrc":
        url = videoDir + url

    pipeline_cmd = f'gst-launch-1.0 -v {src} location={url} ! decodebin ! {framerate} ! gvadetect model-instance-id=nunu model={model} device={dev} ! gvafpscounter ! {sink}'
    pid = os.fork()
    if pid == 0:
        os.system(pipeline_cmd)
    return pipeline_cmd

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=55555)
