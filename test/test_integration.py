from datetime import datetime, timedelta
import unittest
from helper1 import club_by_mail, valid_purchase,competition_date_correct, \
    competition_by_name, load_competitions, load_clubs
from server import app


#  test une partie d'un programme ( plusieurs fonctions à la fois )

class TestFormBooking(unittest.TestCase):

    def setUp(self):
        self.club = {"name": "She Lifts",
                     "email": "kate@shelifts.co.uk",
                     "points": "8"
                     }
        self.competition = {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }

        self.clients = app.test_client()

    # test pour s'assurer que les places demandées ne dépasse pas les points du club
    def test_exception_is_raised_if_places_required_are_greater_than_points_club(self):
        self.assertEqual(valid_purchase(self.competition, self.club, "10"), False)

    # test pour s'assurer que les places demandées ne dépasse pas les points de la compétitions
    def test_exception_is_raised_if_places_required_are_greater_than_competition_places(self):
        self.assertEqual(valid_purchase()(None, self.club, "16"), False)

    # test pour s'assurer que les places demandées ne dépasse pas les points du club et de la compétitions
    def test_return_if_places_required_are_less_or_equal_than_points_club_and_competition_places(self):
        self.assertEqual(valid_purchase(self.competition, None, "16"), False)

    # test qui retourne une exception si les places demandées ne dépasse pas la limite de la compétitions
    def test_exception_is_raised_if_places_required_are_greater_than_limit_booking_places(self):
        self.assertEqual(valid_purchase(self.competition, self.club, "8"), True)

    # test si la compétition est valide
    def test_exception_is_raised_if_competition_is_closed(self):
        date = datetime.now() - timedelta(days=1)
        str_date = date.strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(competition_date_correct(str_date), True)

    # test si la compétition n'est pas validé
    def test_exception_not_raised_if_competition_is_not_closed(self):
        date = datetime.now() + timedelta(days=1)
        str_date = date.strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(competition_date_correct(str_date), False)

    # test de la page d'acceuil
    def test_get_home_page(self):
        reponse = self.clients.get("/", follow_redirects=True)
        self.assertEqual(b"<h1>Welcome to the GUDLFT Registration Portal!</h1>" in reponse.data, True)
        self.assertEqual(reponse.status_code, 200)

    # test show summary
    def test_show_summary(self):
        reponse = self.clients.post("/showSummary", data={"email": "a@gmail.com"}, follow_redirects=True)
        self.assertEqual(b"Sorry, that email" in reponse.data, True)
        self.assertEqual(reponse.status_code, 200)

    # test booking
    def test_booking(self):
        reponse = self.clients.get("/book/<competition>/<club>", follow_redirects=True)
        self.assertEqual(b"book" in reponse.data, True)
        self.assertEqual(reponse.status_code, 200)

    def test_logout(self):
        reponse = self.clients.get("/logout", follow_redirects=True)

        self.assertEqual(reponse.status_code, 200)


if __name__ == '__main__':
    unittest.main()