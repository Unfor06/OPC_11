from flask import Flask,render_template,request,redirect,flash,url_for
import helper1 as helper


app = Flask(__name__)
app.secret_key = 'something_special'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    selected_club = helper.club_by_mail(mail=request.form["email"])
    clubs = helper.loadClubs()

    if selected_club is None:
        print("Not Found")
        flash("Email wasn't found")
        return  render_template("index.html")

    if selected_club:
        helper.USER_CLUB = selected_club
        print("Found")
        return render_template(
            "welcome.html",
            club=helper.USER_CLUB,
            competitions=helper.COMPETITIONS, all_clubs=clubs
        )
    flash("Email adress not found")
    return render_template("index.html")

@app.route('/book/<competition>/<club>')
def book(competition,club):
    selected_club = helper.get_club_by_name(name=club)
    selected_competition = helper.get_competition_by_name(name=competition)

    if selected_competition and selected_club:
        max_place = helper.get_max_place(club=selected_club)
        return render_template('booking.html', club=selected_club, competition=selected_competition, max_place=max_place)

    flash("Something went wrong-please try again")
    return render_template('welcome.html', club=helper.USER_CLUB, competitions=helper.COMPETITIONS)


@app.route('/purchasePlaces',methods=['POST'])

def purchasePlaces():
    selected_competition = helper.get_my_competition_by_name(name=request.form["competition"])
    selected_club = helper.get_my_club_by_name(name=request.form["club"])
    places_required = request.form['places']

    purchase_is_valid = helper.is_purchase_is_valid(competition=selected_competition, club=selected_club, places=places_required)

    if purchase_is_valid:

        selected_competition['numberOfPlaces'] = int(selected_competition['numberOfPlaces'])-places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=selected_club, competitions=helper.COMPETITIONS)

    flash("Nombre de places maximum par competition depassée")
    return render_template("welcome.html", club=helper.USER_CLUB, competition=helper.COMPETITIONS)

@app.route("/points_display")
def points_display():
    clubs = helper.loadClubs()
    return render_template("competition.html", competition=helper.COMPETITIONS, all_clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))