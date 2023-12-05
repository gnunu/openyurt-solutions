#!/usr/bin/env bash

openvino_version=$1

case ${openvino_version} in
	"2023.1" )
		openvino_package="l_openvino_toolkit_ubuntu22_2023.1.0.12185.47b736f63ed_x86_64" ;;
	"2023.2")
		openvino_package="l_openvino_toolkit_ubuntu22_2023.2.0.13089.cfd42bd2cb0_x86_64" ;;
	* )
		echo "invalid openvino version" && exit ;;
esac

echo docker buildx build -t openvino:${openvino_version} --platform=linux/amd64 --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} --build-arg openvino_version=${openvino_version} --build-arg openvino_package=${openvino_package} .
docker buildx build -t openvino:${openvino_version} --platform=linux/amd64 --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} --build-arg openvino_version=${openvino_version} --build-arg openvino_package=${openvino_package} .
