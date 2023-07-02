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
        #FIND 333 PB SINGLE

        cursor.execute("select best from RanksSingle where personId ='" + wca_id +  "' and eventId = '333';")
        pb_single_333 = str(cursor.fetchall())[2:][:-3]

        #FIND 333 PB AVG
        cursor.execute("select best from RanksAverage where personId ='" + wca_id +  "' and eventId = '333';")
        pb_avg_333 = str(cursor.fetchall())[2:][:-3]
   
        #CREATE CLASS WITH INFO
        users.append(User(name, wca_id, pb_single_333, pb_avg_333))


    return users


print(get_all_users('GetafeContinua2023')[3].pb_single_333)
