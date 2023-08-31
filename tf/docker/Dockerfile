ARG http_proxy
ARG https_proxy

FROM ubuntu:22.04 as base

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y curl gpg software-properties-common

# install compute libs
RUN curl -fsSL https://repositories.intel.com/graphics/intel-graphics.key | gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/graphics/ubuntu `. /etc/os-release && echo ${UBUNTU_CODENAME}` arc" | tee /etc/apt/sources.list.d/intel-graphics.list

ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-opencl-icd=${ICD_VER} \
    intel-level-zero-gpu=${LEVEL_ZERO_GPU_VER} \
    level-zero=${LEVEL_ZERO_VER} \
    clinfo && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

# install oneapi runtime
RUN curl -fsSL https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor --output /usr/share/keyrings/intel-sw-products.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/intel-sw-products.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/intel-oneapi.list

ARG DPCPP_VER
ARG MKL_VER

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-oneapi-runtime-dpcpp-cpp=${DPCPP_VER} \
    intel-oneapi-runtime-mkl=${MKL_VER}

ARG PYTHON
RUN apt-get update && apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-cache policy $PYTHON && apt-get update && apt-get install -y \
    --no-install-recommends --fix-missing $PYTHON

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    ${PYTHON} lib${PYTHON} python3-pip ${PYTHON}-distutils && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

RUN pip --no-cache-dir install --upgrade \
    pip \
    setuptools

RUN ln -sf $(which ${PYTHON}) /usr/local/bin/python && \
    ln -sf $(which ${PYTHON}) /usr/local/bin/python3 && \
    ln -sf $(which ${PYTHON}) /usr/bin/python && \
    ln -sf $(which ${PYTHON}) /usr/bin/python3

RUN pip install tensorflow==2.13.0
RUN pip install --upgrade intel-extension-for-tensorflow[gpu]
RUN pip install notebook
RUN pip install keras-cv tensorflow-datasets
RUN pip install matplotlib ipywidgets

RUN useradd -ms /bin/bash -u 1000 -G video tensor


FROM base

ARG TF_HOME=/home/tensor

WORKDIR ${TF_HOME}
USER tensor
