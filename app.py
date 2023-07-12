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
    #sort users based on event and format
    users = backend.sort_users(event, format, backend.get_all_users(competition_id))
     
    pbs = []
    names = []
    #Filter the pbs that are -1 becouse they have not competed in that event
    for user in users:
        print(user.pb_avg_333, user.name)    
        exec("if user.pb_" + format + "_" + event + " != -1: pbs.append(user.pb_" + format + "_" + event + ")")
        exec("if user.pb_" + format + "_" + event + " != -1: names.append(user.name)")

    users_len = len(pbs)
    return render_template('competition_ranking.html', names=names, pbs=pbs, event=event, format=format,   users_len=users_len)


if __name__ == "__main__":
    app.run(debug=True)
