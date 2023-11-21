ARG http_proxy
ARG https_proxy

FROM ubuntu:22.04 as ubuntu

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y curl gpg software-properties-common vim


FROM ubuntu as ov

# install openvino
RUN mkdir /opt/intel
COPY l_openvino_toolkit_ubuntu22_2023.1.0.12185.47b736f63ed_x86_64.tgz /tmp
RUN cd /opt/intel && tar xf /tmp/l_openvino_toolkit_ubuntu22_2023.1.0.12185.47b736f63ed_x86_64.tgz && mv l_openvino_toolkit_ubuntu22_2023.1.0.12185.47b736f63ed_x86_64 openvino_2023.1.0 && rm /tmp/l_openvino_toolkit_ubuntu22_2023.1.0.12185.47b736f63ed_x86_64.tgz
RUN cd /opt/intel/openvino_2023.1.0 && ./install_dependencies/install_openvino_dependencies.sh -y && python3 -m pip install -r ./python/requirements.txt
RUN ln -s /opt/intel/openvino_2023.1.0 /opt/intel/openvino_2023


FROM scratch as base

COPY --from=ov / /

RUN useradd -ms /bin/bash -u 1000 -G video openvino

# OpenVINO environment variables
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino_2023
ENV OpenVINO_DIR="$INTEL_OPENVINO_DIR/runtime/cmake"
ENV InferenceEngine_DIR="$INTEL_OPENVINO_DIR/runtime/cmake"
ENV ngraph_DIR="$INTEL_OPENVINO_DIR/runtime/cmake"
ENV LD_LIBRARY_PATH="$INTEL_OPENVINO_DIR/runtime/lib/intel64:$LD_LIBRARY_PATH"
ENV PYTHONPATH="$INTEL_OPENVINO_DIR/python:$INTEL_OPENVINO_DIR/python/python3:$PYTHONPATH"


FROM base

ARG OV_HOME=/home/openvino

COPY models ${OV_HOME}/models
COPY infer_face_detect.py ${OV_HOME}
RUN chown -R openvino:openvino ${OV_HOME}

USER openvino
WORKDIR ${OV_HOME}
