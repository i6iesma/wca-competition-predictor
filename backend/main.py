import mysql.connector as connector
from classes import User
#Connection with the db named wca_dev
connection = connector.connect(
    host = "localhost",
    user = "inigo",
    password = "123456"
)
#Commands in order to use wca_dev db
cursor = connection.cursor(buffered=True)
cursor.execute("use wca_dev")
#Get all of the events from the database
cursor.execute("select id from Events;")
events = []
for event in list(cursor.fetchall()):
    events.append(str(event)[2:][:-3])



def get_all_users(competition_id):
    #Get all of the people ids on a give competition
    get_users_ids_query = "SELECT user_id FROM registrations WHERE competition_id ='" + competition_id + "' AND accepted_at IS NOT NULL AND deleted_at IS NULL;"
    cursor.execute(get_users_ids_query)
    users_ids = cursor.fetchall()
    users = []
    for id in users_ids:
        str_id = (str(id)[:-2][1:])
        #FIND NAME

        cursor.execute("select name from users where id='" + str_id + "'")
        name = str(cursor.fetchall())[3:][:-4]
        #FIND WCAID

        cursor.execute("select wca_id from users where id='" + str_id + "'")
        wca_id = str(cursor.fetchall())[3:][:-4]
        this_user = User(name, wca_id)
        for event in events:
            #Find single
            event_pb_single = ""
            cursor.execute("select best from RanksSingle where personId ='" + wca_id +  "' and eventId = '"+ event + "';")
            event_pb_single= str(cursor.fetchall())[2:][:-3]
            # #Some people may not have a result so this filters removing the entry completely
            if event_pb_single == '' :
                continue
            event_pb_single_int = int(event_pb_single)
            exec("this_user.pb_single_" + event + " = " + str(event_pb_single_int))
            exec("this_user.pb_single_" + event + " = " + "int(this_user.pb_single_" + event + ")")
            #Find avg 
            cursor.execute("select best from RanksAverage where personId ='" + wca_id +  "' and eventId = '"+ event + "';")
            event_pb_avg = ""
            event_pb_avg= str(cursor.fetchall())[2:][:-3]
            # #Some people may not have a result so this filters removing the entry completely
            if event_pb_avg == '':
                continue
            event_pb_avg_int = int(event_pb_single)
            exec("this_user.pb_avg_" + event + " = " + str(event_pb_avg_int))
            exec("this_user.pb_avg_" + event + " = " + "int(this_user.pb_avg_" + event + ")")
        users.append(this_user)


    return users
def clean_0_users(users):
    for i, o in enumerate(users):
        if o.pb_single_333 == -1:
            print("got to delete with user: " + o.name)
            del users[i]
            users.pop(i)
    # print(users[0].pb_avg_333bf)
    return users
            
    return users
def sort_users(event, format, users):
    #Sort all of the users based on their pb results on the event specified
    exec("users.sort(key=lambda user: user.pb_" + format + "_" + event + ")")
    return users

# sorted_users = sort_users("333", "avg", get_all_users("GetafeContinua2023"))
all_users = sort_users("333", "single", clean_0_users(get_all_users("LazarilloOpen2023")))


# for user in all_users:
#     print(user.name, user.pb_single_333)
