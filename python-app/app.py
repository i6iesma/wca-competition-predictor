from flask import Flask, render_template, request
import sys
sys.path.insert(1, './backend')
import main as backend
app = Flask(__name__)
application = app
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template('index.html', users=[], event="", format="", len_users = 0)
    elif request.method == "POST":
        url = request.form.get('url')
        format = request.form.get('format')
        event = request.form.get('event')
        mode = request.form.get('mode')
        print("event is " + str(event))
        #Get the users from the backend
        #Filter the competition id from url like this https://www.worldcubeassociation.org/competitions/LazarilloOpen2023
        competition_id = str(url).strip("https://www.worldcubeassociation.org/competitions/")
        #Get all the users already sorted
        users = backend.main(competition_id, event, format, mode) 
        len_users = len(users)
        return render_template('index.html', users=users, event=event, format=format, len_users=len_users)

        

@app.route("/competition_ranking", methods=["POST", "GET"])
def competition_ranking():
    url = request.form.get('url')
    format = request.form.get('format')
    event = request.form.get('event')
    #Get the users from the backend
    #Filter the competition id from url like this https://www.worldcubeassociation.org/competitions/LazarilloOpen2023
    competition_id = str(url).strip("https://www.worldcubeassociation.org/competitions/")
    #Get all the users already sorted
    users = backend.main(competition_id, event, format, "pb")
    len_users = len(users)
     

    return render_template('competition_ranking.html', users=users, event=event, format=format, len_users=len_users)


if __name__ == "__main__":
    app.run(debug=True)
