docker buildx build --platform=linux/amd64 \
                 --build-arg http_proxy=$http_proxy \
                 --build-arg https_proxy=$https_proxy \
                 --build-arg PYTHON=python3.10 \
                 --build-arg ICD_VER=23.17.26241.33-647~22.04 \
                 --build-arg LEVEL_ZERO_GPU_VER=1.3.26241.33-647~22.04 \
                 --build-arg LEVEL_ZERO_VER=1.11.0-647~22.04 \
                 --build-arg DPCPP_VER=2023.2.1-16 \
                 --build-arg MKL_VER=2023.2.0-49495 \
                 --build-arg PYTHON=python3.10 \
                 -t itex:latest \
                 .
