#! /usr/bin/bash
curl -X POST -H 'Content-Type: application/json' -d '{"src": "rtspsrc", "user-id": "admin", "user-pw":"intel123", "url": "rtsp://10.238.157.61:554/Streaming/Channels/101", "model": "horizontal-text-detection-0001.xml", "dev": "AUTO", "rtmpsink": "rtmp://10.238.158.178:1935/live/test"}' http://10.238.156.124:55555/pipeline
