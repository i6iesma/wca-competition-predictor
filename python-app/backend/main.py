import mysql.connector as connector
import datetime

def get_all_competitions():
    # Connection with the db named wca_dev
    connection = connector.connect(
        host="localhost",
        user="u625102952_mysqluser",
        ssl_disabled=True,
        password="MysqlUser1",
    )
    # Commands in order to use wca_dev db
    cursor = connection.cursor(buffered=True)
    cursor.execute("use u625102952_wca_dev")
    #This function gets all competitions returning the name and id of the comp
    #in order to index it in the search function
    cursor.execute("SELECT id,name from Competitions")
    ids_names = cursor.fetchall()
    ids = []
    names = []
    for id_name in ids_names:
        ids.append(id_name[0])
        names.append(id_name[1])
    return ids, names 
    connection.close()
def get_all_users(competition_id,  cursor):
    # Get all the people ids

    cursor.execute("SELECT user_id FROM registrations WHERE competition_id=%(competition_id)s AND accepted_at IS NOT NULL AND deleted_at IS NULL;", {
                   'competition_id': competition_id})
    users_ids = cursor.fetchall()
    users = []
    for user_id in users_ids:
        str_id = (str(user_id)[:-2][1:])

        # Find names
        cursor.execute("select name from users where id='" + str_id + "'")
        name = str(cursor.fetchall())[3:][:-4]
        # Find wca_ids
        cursor.execute("select wca_id from users where id='" + str_id + "'")
        wca_id = str(cursor.fetchall())[3:][:-4]

        user = {
            "name": name,
            "wca_id": wca_id,
            # Ranking is set to 1 temporarely so that it is changed later in sort_users()
            "ranking": 1,
            #Result is the number which is desplayed on the web 
            #and is set to an empty string for now, this will turn into wathever
            #result the prediction is making
            "result": ''
        }
        users.append(user)
    return users
def get_smart_prediction(users, event, format, competitionId, cursor):
    new_users = []
    for user in users:
        #First get the last competition the competitor competed in that event
        sql_insert_query = "select competitionId from Results where personId=%s and eventId=%s order by id desc limit 1;" 
        sql_parameters = (user["wca_id"], event)
        cursor.execute(sql_insert_query, sql_parameters)
        last_comp = str(cursor.fetchall())[3:][:-4]
        if format == "single":
            sql_insert_query = "select best from Results where personId='" + user["wca_id"] + "' and eventId=%s and competitionId=%s;"
        if format == "avg":
            sql_insert_query = "select average from Results where personId='" + user["wca_id"] + "' and eventId=%s and competitionId=%s;"


        sql_parameters = (event, last_comp)
        cursor.execute(sql_insert_query, sql_parameters)
        averages = cursor.fetchall()
        if averages == []:
            continue
        new_averages = []
        for average in averages:
            average = str(average)[1:][:-2]
            new_averages.append(int(average))

        #Find the average of the averages
        if new_averages == [-1]:
            continue
        result = sum(new_averages) // len(new_averages)
        user["result"] = str(result) 
        if user["result"] != '':
            new_users.append(user)
    return new_users
def get_comp_id(comp_name, cursor):
    print(comp_name)
    cursor.execute("select id from Competitions where name='" + comp_name + "';")
    comp_id = str(cursor.fetchall())[3:][:-4]
    print(str(comp_id))
    return comp_id

    
def get_pb(users, event, format, cursor):
    new_users = []
    # Find pb single at the event and format specified
    for user in users:

        if format == "single":
            cursor.execute("select best from RanksSingle where personId='" +
                           user["wca_id"] + "' and eventId=%(event)s;", {'event': event})
            event_pb_format = str(cursor.fetchall())[2:][:-3]
        elif format == "avg":
            cursor.execute("select best from RanksAverage where personId='" +
                           user["wca_id"] + "' and eventId=%(event)s;", {'event': event})
            event_pb_format = str(cursor.fetchall())[2:][:-3]
        if event_pb_format != '':
            new_user = {
             "name": user["name"],
            "wca_id": user["wca_id"],
            # Ranking is set to 1 temporarely so that it is changed later in sort_users()
            "ranking": 1,
            "result": event_pb_format
            }
            new_users.append(new_user)

    return new_users

            
            
    

def sort_users(users):
    users.sort(key=lambda user: float(user["result"]))
    # Set ranking now so that it is according to the sorted list
    ranking = 0
    for user in users:
        ranking = ranking + 1
        user["ranking"] = ranking
    return users


def fix_centiseconds(users, event, format):
    # This function will change the centiseconds format to a minutes/seconds/centiseconds format
    if event == "333mbf":
        multiblind_formatting(users, event)
        return users
    if event == "333fm":
        if format == "single":
            return users
        else:
            for user in users:
                print(user["result"])
                user["result"] = str(int(user["result"]) / 100 )
            return users

    for user in users:
        cs_pb = int(user["result"])

        seconds = int(cs_pb) / 100
        minutes = seconds // 60
        remainder_seconds = seconds - (60*minutes)
        # Sometimes python has a weird thing where it adds many decimals so this rounds it
        if len(str(remainder_seconds)) > 5:
            remainder_seconds = round(remainder_seconds, 2)

        if int(minutes) == 0:
            final_str = str(remainder_seconds)

        else:
            final_str = str(int(minutes)) + ":" + str(remainder_seconds)
        user["result"] = final_str
    return users


def multiblind_formatting(users, event):
    multiblind = "333mbf"
    for user in users:
        result = str(user["result"])
        # new: DDTTTTTMM
        # difference    = 99 - DD
        # timeInSeconds = TTTTT (99999 means unknown)
        # missed        = MM
        # solved        = difference + missed
        # attempted     = solved + missed
        # This is an example of how data is showed 36/38 58:23
        # I only extract solved attempted and time in seconds becouse
        # is the only thing needed to show like in wca website
        if result != '':
            difference = str(99 - int(result[:2]))
            time_in_seconds = str(result[2:][:-2])
            time_in_minutes_and_seconds = str(
                datetime.timedelta(seconds=int(time_in_seconds)))
            missed = str(result[7:])
            solved = str(int(difference) + int(missed))
            attempted = str(int(solved) + int(missed))
            formatted_result = solved + "/" + attempted + " " + time_in_minutes_and_seconds
            user["result"] = formatted_result

    return users
def debug_user_status(users, previous_function):
    for user in users:
        print("this user has a result of " + user["result"] + " and this was called from " + previous_function)
#Competition id is written with camelCase because of the way it is in the wca db
def main(competition_name, event, format):
    # Connection with the db named wca_dev

    connection = connector.connect(
        host="localhost",
        user="u625102952_mysqluser",
        password="MysqlUser1",
        ssl_disabled=True
    )
    # Commands in order to use wca_dev db
    cursor = connection.cursor()
    cursor.execute("use u625102952_wca_dev")
    competitionId = get_comp_id(competition_name, cursor)
    #Example code for getting user data in the pb mode
    users = get_all_users(competitionId, cursor)
    #Both modes are calcultated in advance so you can change them without reloading the page

    pb_users = get_pb(users, event, format, cursor)
    pb_users = sort_users(pb_users)
    pb_users = fix_centiseconds(pb_users, event, format)
    results_connection = connector.connect(
            host="localhost",
            user="u625102952_mysqlresults",
            password="MysqlUser1",
            ssl_disabled=True)

    results_cursor = results_connection.cursor()
    results_cursor.execute("use u625102952_wca_results")

    smart_prediction_users = get_smart_prediction(users, event, format, competitionId, results_cursor)
    smart_prediction_users = sort_users(smart_prediction_users)
    smart_prediction_users = fix_centiseconds(smart_prediction_users, event, format)
    # Close the connection
    connection.close()
    results_connection.close()
    return pb_users, smart_prediction_users


