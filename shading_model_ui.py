# %load_ext lab_black

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


def check_date(month: int, day: int):
    datetime.date(1900, month, day)

class SimulationParameters(BaseModel):
    "These are simulation parameters relating to the calculation."
    run_irradiance_calc: bool = Field(default=True)
    run_df_calc: bool = Field(default=True)
    run_climate_based_dl_model: bool = Field(default=False)
    run_BSEN17037_calc: bool = Field(default=False)

    epw_filepath: str = Field(
        default=r"J:\J7356\Calcs\DaylightOverheatingTool\02_InputData\00_Defaults\00_WeatherData\London_LHR_DSY1_2020High50.epw"
    )
    bearing: float = Field(
        default=0,
        description="degrees, bearing of glazed facade from North",
        ge=0,
        max=360,
    )

    start_month: int = Field(
        default=1, description="Numerical date for start month", ge=1, le=12
    )
    start_day: int = Field(
        default=1, description="Numerical date for start day", ge=1, le=31
    )
    start_hour: int = Field(default=0, description="Start hour of day", ge=0, le=23)

    end_month: int = Field(
        default=12, description="Numerical date for end month", ge=1, le=12
    )
    end_day: int = Field(
        default=31, description="Numerical date for end day", ge=1, le=31
    )
    end_hour: int = Field(default=23, description="", ge=0, le=23)
    timestep: int = Field(default=1, enum=[1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60])

    window_grid_offset_distance: float = Field(
        default=-0.05, description="(m), negative is inside room"
    )
    window_grid_size: float = Field(
        default=0.1,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )

    working_plane_grid_size: float = Field(
        default=0.1,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    working_plane_height: float = Field(
        default=0.8,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    calc_surface_offset: float = Field(
        default=0,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    radiance_parameters_detail_level: int = Field(
        default=0,
        ge=0,
        le=2,
        description="Number to specify the accuracy of the calculation. 0 is the lowest, 2 is the highest.",
    )

    @model_validator(mode="after")
    def check_dates(self) -> "SimulationParameters":
        check_start_date = check_date(month=self.start_month, day=self.start_day)
        check_end_date = check_date(month=self.end_month, day=self.end_day)
        return self


class RoomParameters(BaseModel):
    "These parameters determine the size and properties of the test room"
    height_above_ground_level: float = Field(default=0, description="(m)")
    x_offset: float = Field(default=0, description="(m)")
    y_offset: float = Field(default=0, description="(m)")
    room_name: str = Field(default="parametric_room")
    room_width: float = Field(
        default=3,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    room_depth: float = Field(
        default=4,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    room_height: float = Field(
        default=3,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    wall_thickness: float = Field(
        default=0.3,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    slab_thickness: float = Field(
        default=0.4,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    internal_floor_reflectance: float = Field(default=0.2, description="", ge=0, le=1)
    internal_wall_reflectance: float = Field(default=0.5, description="", ge=0, le=1)
    internal_ceiling_reflectance: float = Field(default=0.7, description="", ge=0, le=1)
    external_wall_reflectance: float = Field(default=0.2, description="", ge=0, le=1)
    external_roof_reflectance: float = Field(default=0.2, description="", ge=0, le=1)
    external_soffit_reflectance: float = Field(default=0.2, description="", ge=0, le=1)
    reveal_reflectance: float = Field(default=0.4, description="", ge=0, le=1)


class GlazingParameters(BaseModel):
    "Parameters that determine the glazing properties"
    glazing_u_value: float = Field(
        default=0.8,
        description="(W/m²K)",
        ge=0,
        max=sys.float_info.max,
    )
    glazing_g_value: float = Field(
        default=0.4,
        ge=0,
        max=sys.float_info.max,
        # autoui="AutoWidgetBoundedFloatText"
    )
    glazing_vlt: float = Field(
        default=0.7,
        ge=0,
        max=sys.float_info.max,
        # autoui="AutoWidgetBoundedFloatText"
    )


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

class OverhangParameters(BaseModel):
    "Parameters that determine the size of the overhang."
    toggle_overhang: bool = Field(default=False)
    overhang_width: float = Field(
        default=1,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    overhang_depth: float = Field(
        default=1,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    overhang_height_above_window: float = Field(
        default=0,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    overhang_offset: float = Field(default=0, description="(m)")
    overhang_reflectance: float = Field(
        default=0.5,
        description="",
        ge=0,
        le=1,
        # autoui="AutoWidgetBoundedFloatText"
    )
    overhang_angle: float = Field(
        default=0,
        description="deg, rotation angle of overhang, positive drops the overhang below the window",
        ge=-360,
        le=360,
    )


class LouvreFinParameters(BaseModel):
    "Parameters to toggle and vary the dimensions of fins or louvres"
    toggle_louvre_creation: bool = Field(default=False)
    toggle_fins_or_louvres: bool = Field(
        default=False,
        description="Set to True for fins, otherwise will produce Louvres",
    )
    blade_depth: float = Field(
        default=0.3,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    number_of_shades: int = Field(default=3, ge=0, le=100, description="Number of ")
    distance_between_shades: float = Field(
        default=0.2,
        description="(m)",
        ge=0,
        max=sys.float_info.max,
    )
    blade_angle: float = Field(
        default=0,
        description="degrees",
        ge=0,
        max=360,
    )
    blade_reflectance: float = Field(
        default=0.35,
        description="",
        ge=0,
        max=1,
        # autoui="AutoWidgetBoundedFloatText"
    )
    louvre_offset_distance: float = Field(
        default=0,
        description="(m), distance from window to inner edge of louvre/fin blades.",
        ge=0,
        max=sys.float_info.max,
    )
    extra_blade_width: float = Field(
        default=0,
        description="(m), distance that the louvre extends past the edge of the window",
        ge=0,
        max=sys.float_info.max,
    )


class WindowBlindParameters(BaseModel):
    "Create a diffusive vertical blind based on a percentage window covering."
    toggle_blind: bool = Field(default=False)
    blind_percentage_cover: float = Field(
        default=50,
        description="% of Window Covered",
        ge=0,
        max=100,
    )
    blind_offset: float = Field(
        default=0,
        description="(m). Distance from glazing to blind, positive is external",
        ge=0,
        max=sys.float_info.max,
    )
    blind_solar_reflectance: float = Field(
        default=0.5,
        description="Total solar reflectance",
        ge=0,
        le=1,
    )
    blind_visible_reflectance: float = Field(
        default=0.5,
        description="Visible light reflectance. Assumes perfectly diffuse",
        ge=0,
        le=1,
    )
    blind_diffusive_transmittance: float = Field(
        default=0.2,
        description="Visible diffuse transmittance",
        ge=0,
        le=1,
    )
    blind_specular_transmittance: float = Field(
        default=0.04,
        description="Default for most blinds is about 4%",
        ge=0,
        le=1,
    )
    toggle_opaque_blind: bool = Field(
        default=False,
        description="True is perfectly opaque blind, false is translucent",
    )
    toggle_perforated_blind: bool = Field(
        default=False,
        description="True sets circular perforations, keep as False unless absolutely necessary!",
    )
    blind_perforation_spacing: float = Field(
        default=0.04,
        description="(m), c/c distance between holes.",
        ge=0,
        max=sys.float_info.max,
    )
    blind_perforation_radius: float = Field(
        default=0.01,
        description="(m), perforation hole radius.",
        ge=0,
        max=sys.float_info.max,
    )
    toggle_horizontal_blind: bool = Field(
        default=False,
        description="True sets the blind to generate horizontally across the window from left to right",
    )
    toggle_reverse_blind_direction: bool = Field(
        default=False,
        description="True reverses the direction of blind generation (WIP)",
    )


class CustomShadeParameters(BaseModel):
    "Imports Custom HBJson Shade files from a file and adds to model."
    toggle_custom_shading: bool = Field(default=False)
    custom_shade_filepath: str = Field(
        default=r"J:\J7356\Calcs\DaylightOverheatingTool\02_InputData\00_Defaults\02_DefaultCustomShading\examples\venetian_blinds\venetian_blinds.json"
    )


# +
class VerticalFinParameters(BaseModel):
    "Creates a vertical fin that is exterior to the window boundary"
    toggle_external_vertical_fin: bool = Field(default=False)
    vertical_fin_height: float = Field(
        default=1.5,
        description="(m), height of vertical fin.",
        ge=0,
        max=sys.float_info.max,
    )
    vertical_fin_depth: float = Field(
        default=0.5,
        description="(m), depth of vertical fin.",
        ge=0,
        max=sys.float_info.max,
    )
    reverse_fin_side: bool = Field(
        default=False,
        description="Default is for fin to be generated to the right of the window (from an external view). Set to True to move to the left",
    )
    fin_window_offset: float = Field(
        default=0.1,
        description="(m), distance of vertical fin from edge of window.",
    )
    fin_vertical_offset: float = Field(
        default=0,
        description="(m), offset centre of fin from centre of window.",
    )
    vertical_fin_reflectance: float = Field(
        default=0.35,
        description="Reflectance of shade material",
        ge=0,
        le=1,
    )


class ContextParameters(BaseModel):
    "Sets parameters for suroundings and context to the room"
    toggle_ground_plane: bool = Field(default=False)
    toggle_context: bool = Field(default=False)
    context_filepath: str = Field(
        default=r"J:\J7356\Calcs\DaylightOverheatingTool\02_InputData\00_Defaults\01_Default Context\defaultContextShade.json"
    )


# -

class Main(BaseModel):
    simulation_params: SimulationParameters = SimulationParameters()

# +
import traitlets as tr


class ShadingModelInputUi(w.VBox):
    _value = tr.Dict()

    def __init__(self):
        self.simulation_params = AutoObject.from_pydantic_model(SimulationParameters)
        self.room_params = AutoObject.from_pydantic_model(RoomParameters)
        self.glazing_params = AutoObject.from_pydantic_model(GlazingParameters)
        self.aperture_params = AutoObject.from_pydantic_model(Apertures)
        self.overhang_params = AutoObject.from_pydantic_model(OverhangParameters)
        self.louvre_fin_params = AutoObject.from_pydantic_model(LouvreFinParameters)
        self.window_blind_params = AutoObject.from_pydantic_model(WindowBlindParameters)
        self.custom_shade_params = AutoObject.from_pydantic_model(CustomShadeParameters)
        self.vertical_fin_params = AutoObject.from_pydantic_model(VerticalFinParameters)
        self.context_params = AutoObject.from_pydantic_model(ContextParameters)

        super().__init__(
            [
                self.simulation_params,
                self.room_params,
                self.glazing_params,
                self.aperture_params,
                self.overhang_params,
                self.louvre_fin_params,
                self.window_blind_params,
                self.custom_shade_params,
                self.vertical_fin_params,
                self.context_params,
            ]
        )
        self._update_show_hide_fins()
        self._show_hide_fins("")

    def _update_show_hide_fins(self):
        self.vertical_fin_params.observe(self._show_hide_fins, "_value")

    def _show_hide_fins(self, on_change):
        if self.vertical_fin_params.value["toggle_external_vertical_fin"]:
            self.vertical_fin_params.order = list(
                self.vertical_fin_params.di_widgets.keys()
            )
        else:
            self.vertical_fin_params.order = ["toggle_external_vertical_fin"]

    @property
    def value(self):
        self._value = (
            self.simulation_params.value
            | self.room_params.value
            | self.glazing_params.value
            | self.aperture_params.value
            | self.overhang_params.value
            | self.louvre_fin_params.value
            | self.window_blind_params.value
            | self.custom_shade_params.value
            | self.vertical_fin_params.value
            | self.context_params.value
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


# -

# ui.traits()

ui = ShadingModelInputUi()

ui

# +
order = list(ui.vertical_fin_params.di_widgets.keys())

self = ui


def _update_show_hide_controls(self):
    self.vertical_fin_params.di_widgets["toggle_external_vertical_fin"].observe(
        _show_hide, "value"
    )


def _show_hide(self, on_change):
    if self.vertical_fin_params.di_widgets["toggle_external_vertical_fin"]:
        self.vertical_fin_params.order = list(
            self.vertical_fin_params.di_widgets.keys()
        )
    else:
        self.vertical_fin_params.order = ["toggle_external_vertical_fin"]


_update_show_hide_controls(self)
# -

order = ["toggle_external_vertical_fin"]
ui.vertical_fin_params.order = order

self = ui
self.vertical_fin_params.order = list(self.vertical_fin_params.di_widgets.keys())

ui.value


