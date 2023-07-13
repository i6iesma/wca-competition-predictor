from flask import Flask, render_template, request
import sys
sys.path.insert(1, './backend')
import main as backend
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/competition_ranking", methods=["POST", "GET"])
def competition_ranking():
    url = request.form.get('url')
    format = request.form.get('format')
    event = request.form.get('event')
    #Get the users from the backend
    #Filter the competition id from url like this https://www.worldcubeassociation.org/competitions/LazarilloOpen2023
    competition_id = str(url).strip("https://www.worldcubeassociation.org/competitions/")
    #Get all the users already sorted
    users = backend.main(competition_id, event, format)
    len_users = len(users)
     

    return render_template('competition_ranking.html', users=users, event=event, format=format, len_users=len_users)


if __name__ == "__main__":
    app.run(debug=True)
