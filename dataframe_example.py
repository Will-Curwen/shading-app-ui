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
import traitlets as tr

class ApertureParameters(BaseModel):
    "Parameters for an Aperture"
    aperture_name: str = Field(
        default="window1",
        json_schema_extra=dict(column_width=150),
    )
    room_face: int = Field(
        default=3,
        description="Face of room that aperture is placed in. 0 is facing in the positive x direction (by default East) and goes clockwise as value is increased to 3",
        ge=0,
        le=3,
        json_schema_extra=dict(column_width=100),
    )
    frame_thickness: float = Field(
        default=0.05,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
        json_schema_extra=dict(column_width=150),
    )
    aperture_offset: float = Field(
        default=0,
        description="(m)",
        json_schema_extra=dict(column_width=150),
    )
    aperture_width: float = Field(
        default=1,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
        json_schema_extra=dict(column_width=150),
    )
    sill_height: float = Field(
        default=1.1,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
        json_schema_extra=dict(column_width=90),
    )
    aperture_height: float = Field(
        default=1.5,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
        json_schema_extra=dict(column_width=150),
    )
    extra_reveal_depth: float = Field(
        default=0,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
        json_schema_extra=dict(column_width=170),
    )


APERTURES_DEFAULT = [
    {
        "aperture_name": "window1",
        "room_face": 3,
        "frame_thickness": 0.05,
        "aperture_offset": 0.0,
        "aperture_width": 1.0,
        "sill_height": 1.1,
        "aperture_height": 1.5,
        "extra_reveal_depth": 0.0,
    }
]


class Apertures(BaseModel):
    "Array of aperture parameters - each item is a new aperture"
    apertures: list[ApertureParameters] = Field(
        default=APERTURES_DEFAULT,
        json_schema_extra=dict(format="DataFrame", global_decimal_places=2),
    )

class ApertureInputUi(w.VBox):
    _value = tr.Dict()

    def __init__(self):
        self.aperture_params = AutoObject.from_pydantic_model(Apertures)

        super().__init__(
            [
                self.aperture_params
            ]
        )

    @property
    def value(self):
        self._value = (
            self.aperture_params.value
        )
        return self._value

    @value.setter
    def value(self, inputs):
        """Pass key value pair and check if the value is associated to
        a certain widget. If so, then set the value."""
        for key, value in inputs.items():
            is_value_set = False
            for child in self.children:
                if key in child.di_widgets.keys():
                    child.di_widgets[key].value = value
                    is_value_set = True
                    break
            if not is_value_set:
                raise ValueError(f"'{key}' does not exist")    