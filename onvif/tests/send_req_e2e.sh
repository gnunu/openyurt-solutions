#! /usr/bin/bash
curl -X POST -H 'Content-Type: application/json' -d '{"src": "rtspsrc", "user-id": "admin", "user-pw":"intel123", "url": "rtsp://10.238.157.73:554/Streaming/Channels/101", "framerate": "3", "model": "horizontal-text-detection-0001.xml", "dev": "AUTO", "rtmpsink": "rtmp://10.238.156.107:1935/live/test"}' http://10.238.156.107:55555/pipeline
