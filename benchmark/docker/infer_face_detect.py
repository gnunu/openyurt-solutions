#!/usr/bin/env python3

import numpy as np
from pathlib import Path
import time
import openvino as ov

model_name = "face-detection-retail-0005"
model_xml_name = f'{model_name}.xml'
model_bin_name = f'{model_name}.bin'

base_artifacts_dir = Path('./models').expanduser()
model_xml_path = base_artifacts_dir / model_xml_name

core = ov.Core()
model = core.read_model(model=model_xml_path)
compiled_model = core.compile_model(model=model, device_name="CPU")
output_layer = compiled_model.output(0)

input_image = np.random.randint(0, 255, size=(1, 3, 300, 300))

while True:
    i = 0
    start_time_s = time.time()
    while i < 10:
        i = i + 1
        compiled_model([input_image])[output_layer]
    print("--- %s ms --- per 10 infer" % ((time.time() - start_time_s) * 1000))
