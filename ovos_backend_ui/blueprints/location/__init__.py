from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user

from ovos_local_backend.configuration import CONFIGURATION
from ovos_local_backend.utils.geolocate import Geocoder
from ovos_utils.json_helper import merge_dict

from .static.scripts.info import INSTRUCTIONS
from .static.scripts.codes import STATE_CODES


location = Blueprint("location", __name__, template_folder="templates", static_folder="static")

@location.route("/<last_page>")
def index(last_page):
    data = {
        "navbar_button_title": "BACK",
        "navbar_button_url": url_for(last_page),
        "navbar_button_icon": "icon_edit-reset",
        "anonymous": current_user.is_authenticated,
        "page_title": "LOCATION",
        "last_page": last_page
            }
    page_data = merge_dict(data, parse_default_location())
    print(data['timezone'])
    return render_template("location.html", **page_data)

@location.route("/search/<parent_page>", methods=["POST", "GET"])
def search(parent_page):
    data = {
        "navbar_button_title": "BACK",
        "navbar_button_url": url_for("location.index", last_page=parent_page),
        "navbar_button_icon": "icon_edit-reset",
        "anonymous": current_user.is_authenticated,
        "page_title": "SEARCH FOR LOCATION",
        "parent_page": parent_page,
        "instructions": INSTRUCTIONS
        }
    if request.method == "POST":
        location = Geocoder().get_location(request.form.get("enter_location"))
        print(location)
        city_list = location["city"]["code"].split(", ")
        # print(city_list)
        # print(len(city_list))
        parse_searched_location(location)
        return redirect(url_for(parent_page))

    return render_template("search_location.html", **data)

def parse_default_location():
    def_loc = CONFIGURATION['default_location']
    loc = {}
    for k in def_loc:
        if k == "city":
            loc["city"] = def_loc[k]["code"]
            loc["state"] = def_loc[k]["state"]["name"]
            loc["country"] = def_loc[k]["state"]["country"]["name"]
        if k == "coordinate":
            loc["lat"] = def_loc[k]["latitude"]
            loc["lon"] = def_loc[k]["longitude"]
        if k == "timezone":
            loc["timezone"] = def_loc[k]["name"]
    return loc

def parse_searched_location(location):
    city_location = location["city"]["code"].split(", ")
    new_location = {}
    if city_location[0].isnumeric():
        address = f"{city_location[0]} {city_location[1]}"
        city_location.pop(0)
        city_location.pop(0)
    else:
        address = ""
    new_location = {
                "default_location": {
                    "city": {
                        "address": address,
                        "code": city_location[0],
                        "name": city_location[0],
                        "state": {
                            "code": get_code_from_state(city_location[2]),
                            "name": city_location[2],
                            "country": {
                                "code": get_code_from_country(city_location[-1]),
                                "name": city_location[-1]
                                }
                            }
                        },
                    "coordinate": location["coordinate"],
                    "timezone": location["timezone"]
                    }
                }
    if not new_location["default_location"]["timezone"]["name"]:
        print("no name for timezone")
        new_location["default_location"]["timezone"]["name"] = new_location["default_location"]["timezone"]["code"]
    new_location = CONFIGURATION.merge(new_location)
    print(CONFIGURATION["default_location"])
    CONFIGURATION.store()


def get_code_from_state(state):
    # TODO: add state code parser
    return state

def get_code_from_country(country):
    # TODO: add country code parser
    return country
