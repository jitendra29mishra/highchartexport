#!/usr/bin/env python3

"""
Highchart Export
"""

from json import dumps as __dumps__
import requests

VERSION = "v0.0.4"

BASIC_CONFIG = None


def set_basic_config():
    """
    set_basic_config
    ----------------

    BASIC_CONFIG is global variable of type dict.
    """
    global BASIC_CONFIG   # pylint: disable=W0603
    BASIC_CONFIG = {
        "infile": "",
        "width": False,
        "scale": False,
        "constr": "Chart",
        "styledModel": False,
        "type": "image/png",
        "asyncRendering": False,
        "async": False,
    }


def __check_basic_config__(func):
    def wrap(*args, **kwargs):
        if BASIC_CONFIG is None:
            set_basic_config()
        ret = func(*args, **kwargs)
        return ret

    return wrap


def __get_content__(data):
    """
    __get_content__
    ---------------
    """
    highchart_export_url = "https://export.highcharts.com/"
    highchart_headers = {
        "Content-type": "application/json",
        "Cookie": "__cfduid=d2e2782a64847f0a58f714fa5ab68939e1613642479",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
                "(KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    }
    resp = requests.request(
        "POST", highchart_export_url, headers=highchart_headers, data=data
    )
    content = resp.content
    if not isinstance(content, bytes):
        if content[-4:] == ".png":
            resp = requests.get(highchart_export_url + content)
            content = resp.content
        else:
            raise Exception("Something went wrong")
    return content


def __create_chart_file__(data, filename):
    """
    __create_chart_file__
    ---------------------
    """
    __content__ = __get_content__(data)
    with open(filename, "bw") as _f:
        _f.write(__content__)


@__check_basic_config__
def __basic_config__(config: dict):
    """
    Highchart configuration
    """
    BASIC_CONFIG["infile"] = __dumps__(config) if isinstance(config, dict) else config


@__check_basic_config__
def __set_type__(file_type: str):
    """
    Image file format
    * PNG
    * JPEG
    * SVG
    * PDF
    """
    BASIC_CONFIG["type"] = file_type


def __png__():
    """
    PNG format image file.
    """
    __set_type__("image/png")


def __jpeg__():
    """
    JPEG format image file.
    """
    __set_type__("image/jpeg")


def __svg__():
    """
    SVG format image file.
    """
    __set_type__("image/svg+xml")


def __pdf__():
    """
    PDF format image file.
    """
    __set_type__("application/pdf")


@__check_basic_config__
def __save__(filename):
    """
    __save__
    --------
    """
    data = __dumps__(BASIC_CONFIG)
    __create_chart_file__(data, filename)


@__check_basic_config__
def __scale__(scale: int):
    """
    A scaling factor for a higher image resolution.
    Maximum scaling is set to 4x.  Remember that the width
    parameter has a higher precedence over scaling.
    """
    BASIC_CONFIG["scale"] = str(scale)


@__check_basic_config__
def __width__(width: int):
    """
    The exact pixel width of the exported image.
    Defaults to chart.width or 600px. Maximum width is 2000px.
    """
    BASIC_CONFIG["width"] = str(width)


@__check_basic_config__
def __constr__(constr: str):
    """
    Either Chart or StockChart depending on what product you use.
    """
    BASIC_CONFIG["constr"] = constr


def __save_as_type__(func):
    """
    __save_as_type__
    ----------------
    Decorator function
    """
    def wrap(config: dict, filename: str, **kwargs):
        """
        wrap
        ----
        """
        func(config, filename)
        __basic_config__(config)

        if "constr" in kwargs:
            __constr__(kwargs["constr"])

        if "width" in kwargs:
            __width__(kwargs["width"])

        if "scale" in kwargs:
            __scale__(kwargs["scale"])

        __save__(filename=filename)

    return wrap


@__save_as_type__
def save_as_png(config: dict, filename: str, **kwargs) -> None:
    """
    save_as_png
    -----------
    """
    __png__()


@__save_as_type__
def save_as_jpeg(config: dict, filename: str, **kwargs) -> None:
    """
    save_as_png
    -----------
    """
    __jpeg__()


@__save_as_type__
def save_as_svg(config: dict, filename: str, **kwargs) -> None:
    """
    save_as_svg
    -----------
    """
    __svg__()


@__save_as_type__
def save_as_pdf(config: dict, filename: str, **kwargs) -> None:
    """
    save_as_pdf
    -----------
    """
    __pdf__()


def chart():
    """
    chart
    """
    __constr__("Chart")


def stockChart():  # pylint: disable=C0103
    """
    stockChart

    Create StockChart in highchart
    """
    __constr__("StockChart")


def mapChart():   # pylint: disable=C0103
    """
    mapChart

    Create map chart in highchart
    """
    __constr__("Map")


def save(config: dict, filename: str, file_type: str = "png", **kwargs):
    """
    save
    ----
    """
    if file_type.lower() == "png":
        save_as_png(config=config, filename=filename, **kwargs)
    elif file_type.lower() == "jpeg":
        save_as_jpeg(config=config, filename=filename, **kwargs)
    elif file_type.lower() == "svg":
        save_as_svg(config=config, filename=filename, **kwargs)
    elif file_type.lower() == "pdf":
        save_as_pdf(config=config, filename=filename, **kwargs)
    else:
        __basic_config__(config)
        __set_type__(file_type)
        __save__(filename)


# To reset basic config variable content
reset_basic_config = set_basic_config
