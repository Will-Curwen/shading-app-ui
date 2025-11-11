from pydantic import BaseModel, Field, PositiveFloat, model_validator
from ipyautoui.autoobject import AutoObject

import pathlib
import json
import os
import sys
import ipywidgets as w
import uuid
import datetime
import pathlib
import typing as ty
import numpy as np
from enum import Enum
from collections import OrderedDict
import pandas as pd

from shading_model_ui import ShadingModelInputUi

"""
This set of functions is to create and save a json file with the parameters for the shading model
"""


def save_json(json_data: dict, name: str, fdir=pathlib.Path(".").parent):
    """
    saves json file under given name
    """
    filename = str(name) + ".json"
    filepath = os.path.join(fdir, filename)

    with open(filepath, "w") as outfile:
        json.dump(json_data, outfile)
    return filepath


def folder_creation(parent_fpath, fname, input_json_data):
    """
    Creates a folder structure if it doesn't exist and saves data into files
    """
    fpath = os.path.join(parent_fpath, fname)
    inputs_fpath = os.path.join(fpath, "in")
    outputs_fpath = os.path.join(fpath, "out")
    pathlib.Path(fpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(inputs_fpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(outputs_fpath).mkdir(parents=True, exist_ok=True)
    fp = save_json(input_json_data, fname, inputs_fpath)
    return fp


def single_parameter_variation(parent_folder, parameter_name, start_value, end_value, step, global_params):
    """
    Could make this into a multiple param varation thing - need to tidy this 
    """
    ui = ShadingModelInputUi()
    ui.value = global_params
    param_array = np.linspace(
        start_value, end_value, int(round((end_value - start_value) / step, 0) + 1)
    ).round(decimals=3)
    names_list = []
    filename_list = []
    filepath_list = []
    for i, param_val in enumerate(param_array):
        fname = str(uuid.uuid4())
        ui.value = {parameter_name: param_val}
        fp = folder_creation(parent_folder, fname, ui.value)
        names_list.append(fname)
        filepath_list.append(fp)
    return names_list, filepath_list

def read_json(path, filename=""):
    if filename:
        filepath = os.path.join(path, filename)
    else:
        filepath = os.path.join(path)
    f = open(filepath, "r")
    return json.load(f, object_pairs_hook=OrderedDict)

if __name__ == "__main__":
    APERTURES_ARRAY = [
        {
            "aperture_name":"window1",
            "room_face":3,
            "frame_thickness":0.05,
            "aperture_offset":0.0,
            "aperture_width":1.0,
            "sill_height":1.1,
            "aperture_height":1.5,
            "extra_reveal_depth":0.0,
        },
        {
            "aperture_name":"window2",
            "room_face":2,
            "frame_thickness":0.05,
            "aperture_offset":0.0,
            "aperture_width":1.0,
            "sill_height":1.1,
            "aperture_height":1.5,
            "extra_reveal_depth":0.0,
        },
    ]
    ui = ShadingModelInputUi()
    fname = str(uuid.uuid4())
    ui.value = {"apertures":APERTURES_ARRAY}
    fpath = folder_creation("test_results", fname, ui.value)
    #fpath, fname = save_json(ui.value, "default_model_inputs")
    print(fpath)