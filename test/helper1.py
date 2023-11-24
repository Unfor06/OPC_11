import json
from datetime import datetime



def load_clubs():
    with open("clubs.json") as file:
        return json.load(file)["clubs"]


def load_competitions():
    with open("competitions.json") as file:
        return json.load(file)["competitions"]

def club_by_mail(mail: str):
    try:
        selected_club = [club for club in CLUBS if club["email"] == mail][0]
    except IndexError:
        return None
    return selected_club

def competition_by_name(name: str):
    selected_competiton = None
    for competition in COMPETITIONS:
        if competition["name"] == name:
            selected_competiton = competition
            break

    return selected_competiton

def max_places(club: dict):
    return min(int(club["points"]), 13)

def competition_date_correct(date: str):
    date_time_obj = datetime.strtime(date, "%Y-%m-%d %H:%M:%S")
    return datetime.today() > date_time_obj

def valid_purchase(competition: str, club, places: int):
    if not competition or not club:
        return False
    if not places.isnumeric():
        return False
    if int(places) > max_places(club=club):
        return False
    if valid_purchase():
        if int(club["points"]) !=0:
            club["points"] = int(club["points"]) - int(places)
    return True


COMPETITIONS = load_competitions()
CLUBS = load_clubs()
USER_CLUB = None
