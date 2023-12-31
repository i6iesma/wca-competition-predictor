import mysql.connector as connector
#Connection with the db named wca_dev
connection = connector.connect(
    host = "localhost",
    user = "inigo",
    password = "123456"
)
#Commands in order to use wca_dev db
cursor = connection.cursor(buffered=True)
cursor.execute("use wca_dev")


def get_all_users(competition_id, event, format):
    #Get all the people ids
    
    get_users_ids_query = "SELECT user_id FROM registrations WHERE competition_id ='" + competition_id + "' AND accepted_at IS NOT NULL AND deleted_at IS NULL;"
    cursor.execute(get_users_ids_query)
    users_ids = cursor.fetchall()
    users = []
    for user_id in users_ids:
        str_id = (str(user_id)[:-2][1:])
        
        #Find names
        cursor.execute("select name from users where id='" + str_id + "'")
        name = str(cursor.fetchall())[3:][:-4]
        #Find wca_ids 
        cursor.execute("select wca_id from users where id='" + str_id + "'")
        wca_id = str(cursor.fetchall())[3:][:-4]
        #Find pb single at the event and format specified
        if format == "single":
            cursor.execute("select best from RanksSingle where personId ='" + wca_id +  "' and eventId = '"+ event + "';")
            event_pb_format= str(cursor.fetchall())[2:][:-3]
        elif format == "avg":
            cursor.execute("select best from RanksAverage where personId ='" + wca_id +  "' and eventId = '"+ event + "';")
            event_pb_format= str(cursor.fetchall())[2:][:-3]
        #Filter out people without a result
        if event_pb_format != '':
            #Save the user as a dictionary
            user = {
            "name": name,
            "wca_id": wca_id,
            "event_pb": int(event_pb_format),
            #Ranking is set to 1 temporarely so that it is changed later in sort_users()
            "ranking": 1
            }
            users.append(user)

        
    return users 

def sort_users(users):
    users.sort(key=lambda user: user["event_pb"])
    #Set ranking now so that it is according to the sorted list
    ranking = 0
    for user in users:
        ranking = ranking + 1
        user["ranking"] = ranking
    return users 

def fix_centiseconds(users):
    #TODO Add exceptions to multiblind and similar categories
    #This function will change the centiseconds format to a minutes/seconds/centiseconds format
    for user in users:
        cs_pb = user["event_pb"] 
        seconds = cs_pb / 100
            
        minutes = seconds // 60
        remainder_seconds = seconds - (60*minutes)
        print(int(minutes))
        if int(minutes) == 0:
            user["event_pb"] = remainder_seconds 
        else:
            #Sometimes python has a weird thing where it adds many decimals so this rounds it
            if len(str(remainder_seconds)) > 5:
                remainder_seconds = round(remainder_seconds, 2)
            final_str = str(int(minutes)) + ":" + str(remainder_seconds)
            user["event_pb"] = final_str
    return users
            


def main(competition_id, event, format):
    users = get_all_users(competition_id, event, format)
    users = sort_users(users)
    users = fix_centiseconds(users) 
    for user in users:
        print(user["event_pb"])
    return users 

main("LazarilloOpen2023", "444", "single")
