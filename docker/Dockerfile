ARG http_proxy
ARG https_proxy

FROM ubuntu:22.04 as base

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y curl gpg software-properties-common

# install dlstreamer
RUN curl -fsSL https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor --output /usr/share/keyrings/intel-sw-products.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-sw-products.gpg] https://apt.repos.intel.com/openvino/2022 `. /etc/os-release && echo ${UBUNTU_CODENAME}` main" | tee /etc/apt/sources.list.d/intel-openvino-2022.list
RUN curl -fsSL https://repositories.intel.com/graphics/intel-graphics.key | gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/graphics/ubuntu `. /etc/os-release && echo ${UBUNTU_CODENAME}` arc" | tee /etc/apt/sources.list.d/intel-graphics.list
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y intel-dlstreamer-dev

RUN /opt/intel/dlstreamer/install_dependencies/install_mqtt_client.sh
RUN /opt/intel/dlstreamer/install_dependencies/install_kafka_client.sh

# install openvino
RUN /opt/intel/dlstreamer/install_dependencies/install_openvino.sh

# install oneapi runtime
RUN echo "deb [signed-by=/usr/share/keyrings/intel-sw-products.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/intel-oneapi.list
RUN apt-get update && apt-get install -y intel-level-zero-gpu level-zero intel-dlstreamer-dpcpp

RUN apt-get install -y vim clinfo vainfo git

RUN pip3 install flask

ARG DLS_HOME=/home/dlstreamer
ARG PYTHON_VERSION=python3.10
ENV DLSTREAMER_DIR=/opt/intel/dlstreamer
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino_2022

# OpenVINO environment variables
ENV OpenVINO_DIR="$INTEL_OPENVINO_DIR/runtime/cmake"
ENV InferenceEngine_DIR="$INTEL_OPENVINO_DIR/runtime/cmake"
ENV ngraph_DIR="$INTEL_OPENVINO_DIR/runtime/cmake"
ENV HDDL_INSTALL_DIR="$INTEL_OPENVINO_DIR/runtime/3rdparty/hddl"
ENV TBB_DIR="$INTEL_OPENVINO_DIR/runtime/3rdparty/tbb/cmake"
ENV LD_LIBRARY_PATH="$INTEL_OPENVINO_DIR/tools/compile_tool:$INTEL_OPENVINO_DIR/runtime/3rdparty/tbb/lib:$INTEL_OPENVINO_DIR/runtime/3rdparty/hddl/lib:$INTEL_OPENVINO_DIR/runtime/lib/intel64:$LD_LIBRARY_PATH"
ENV PYTHONPATH="$INTEL_OPENVINO_DIR/python/${PYTHON_VERSION}:$PYTHONPATH"

# DL Streamer environment variables
ENV GSTREAMER_DIR=${DLSTREAMER_DIR}/gstreamer
ENV GST_PLUGIN_PATH="${DLSTREAMER_DIR}/lib/gstreamer-1.0:${GSTREAMER_DIR}/lib/gstreamer-1.0:${GST_PLUGIN_PATH}"
ENV LIBRARY_PATH="/usr/lib:${DLSTREAMER_DIR}/lib:${DLSTREAMER_DIR}/lib/gstreamer-1.0:${LIBRARY_PATH}"
ENV LD_LIBRARY_PATH="/usr/lib:${DLSTREAMER_DIR}/lib:${DLSTREAMER_DIR}/lib/gstreamer-1.0:${LD_LIBRARY_PATH}"
ENV PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig:${DLSTREAMER_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}"
ENV MODELS_PATH="${MODELS_PATH:-${DLS_HOME}/models}"
ENV LC_NUMERIC="C"

# if USE_CUSTOM_GSTREAMER set, add GStreamer build to GST_PLUGIN_SCANNER and PATH
ARG USE_CUSTOM_GSTREAMER=yes
ENV GST_PLUGIN_SCANNER=${USE_CUSTOM_GSTREAMER:+${GSTREAMER_DIR}/bin/gstreamer-1.0/gst-plugin-scanner}
ENV GI_TYPELIB_PATH=${USE_CUSTOM_GSTREAMER:+${GSTREAMER_DIR}/lib/girepository-1.0}
ENV PATH=${USE_CUSTOM_GSTREAMER:+${GSTREAMER_DIR}/bin:}${PATH}
ENV PKG_CONFIG_PATH=${USE_CUSTOM_GSTREAMER:+${GSTREAMER_DIR}/lib/pkgconfig:}${PKG_CONFIG_PATH}
ENV LIBRARY_PATH=${USE_CUSTOM_GSTREAMER:+${GSTREAMER_DIR}/lib:}$LIBRARY_PATH
ENV LD_LIBRARY_PATH=${USE_CUSTOM_GSTREAMER:+${GSTREAMER_DIR}/lib:}$LD_LIBRARY_PATH
ENV PYTHONPATH=${USE_CUSTOM_GSTREAMER:+${GSTREAMER_DIR}/lib/python3/dist-packages:}$PYTHONPATH

# DPC++ runtime
ENV DPCPP_DIR="/opt/intel/oneapi/compiler/latest/linux"
ENV PATH="${PATH}:${DPCPP_DIR}/lib:${DPCPP_DIR}/compiler/lib/intel64_lin"
ENV LIBRARY_PATH="${LIBRARY_PATH}:${DPCPP_DIR}/lib:${DPCPP_DIR}/compiler/lib/intel64_lin"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${DPCPP_DIR}/lib:${DPCPP_DIR}/lib/x64:${DPCPP_DIR}/compiler/lib/intel64_lin"

RUN useradd -ms /bin/bash -u 1000 -G video dlstreamer


FROM base

ARG DLS_HOME=/home/dlstreamer

WORKDIR ${DLS_HOME}
USER dlstreamer

ARG foo=
# download models
RUN curl -L --create-dir https://storage.openvinotoolkit.org/repositories/open_model_zoo/2022.1/models_bin/2/horizontal-text-detection-0001/FP32/horizontal-text-detection-0001.bin -o ${DLS_HOME}/models/horizontal-text-detection-0001.bin https://storage.openvinotoolkit.org/repositories/open_model_zoo/2022.1/models_bin/2/horizontal-text-detection-0001/FP32/horizontal-text-detection-0001.xml -o ${DLS_HOME}/models/horizontal-text-detection-0001.xml

ARG bar=
RUN cd ${DLS_HOME} \
    && git clone https://github.com/gnunu/openyurt-solutions.git

CMD ["/home/dlstreamer/openyurt-solutions/onvif/pipeline.py"]
