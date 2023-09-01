docker buildx build -t dlstreamer-onvif --platform=linux/amd64 --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} .
