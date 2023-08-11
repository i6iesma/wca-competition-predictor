import mysql.connector as connector
import datetime


def get_all_users(competition_id, event, format, cursor):
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
        # Find pb single at the event and format specified
        if format == "single":
            cursor.execute("select best from RanksSingle where personId='" +
                           wca_id + "' and eventId=%(event)s;", {'event': event})
            event_pb_format = str(cursor.fetchall())[2:][:-3]
        elif format == "avg":
            cursor.execute("select best from RanksAverage where personId='" +
                           wca_id + "' and eventId=%(event)s;", {'event': event})
            event_pb_format = str(cursor.fetchall())[2:][:-3]
        # Filter out people without a result
        if event_pb_format != '':
            # Save the user as a dictionary
            user = {
                "name": name,
                "wca_id": wca_id,
                "event_pb": int(event_pb_format),
                # Ranking is set to 1 temporarely so that it is changed later in sort_users()
                "ranking": 1
            }
            users.append(user)

    return users


def sort_users(users):
    users.sort(key=lambda user: user["event_pb"])
    # Set ranking now so that it is according to the sorted list
    ranking = 0
    for user in users:
        ranking = ranking + 1
        user["ranking"] = ranking
    return users


def fix_centiseconds(users, event):
    # This function will change the centiseconds format to a minutes/seconds/centiseconds format
    if event == "333mbf":
        multiblind_formatting(users, event)
        return users
    if event == "333fm":
        return users

    for user in users:
        cs_pb = user["event_pb"]

        seconds = cs_pb / 100
        minutes = seconds // 60
        remainder_seconds = seconds - (60*minutes)
        print(int(minutes))
        if int(minutes) == 0:
            user["event_pb"] = remainder_seconds
        else:
            # Sometimes python has a weird thing where it adds many decimals so this rounds it
            if len(str(remainder_seconds)) > 5:
                remainder_seconds = round(remainder_seconds, 2)
            final_str = str(int(minutes)) + ":" + str(remainder_seconds)
            user["event_pb"] = final_str
    return users


def multiblind_formatting(users, event):
    multiblind = "333mbf"
    for user in users:
        result = str(user["event_pb"])
        # new: DDTTTTTMM
        # difference    = 99 - DD
        # timeInSeconds = TTTTT (99999 means unknown)
        # missed        = MM
        # solved        = difference + missed
        # attempted     = solved + missed
        # This is an example of how data is showed 36/38 58:23
        # I only extract solved attempted and time in seconds becouse
        # is the only thing needed to show like in wca website
        difference = str(99 - int(result[:2]))
        time_in_seconds = str(result[2:][:-2])
        time_in_minutes_and_seconds = str(
            datetime.timedelta(seconds=int(time_in_seconds)))
        missed = str(result[7:])
        solved = str(int(difference) + int(missed))
        attempted = str(int(solved) + int(missed))
        formatted_result = solved + "/" + attempted + " " + time_in_minutes_and_seconds
        user["event_pb"] = formatted_result

    return users


def main(competition_id, event, format):
    # Connection with the db named wca_dev
    connection = connector.connect(
        host="localhost",
        user="python_script_user",
        password="python_script_user"
    )
    # Commands in order to use wca_dev db
    cursor = connection.cursor(buffered=True)
    cursor.execute("use wca_dev")
    users = get_all_users(competition_id, event, format, cursor)
    users = sort_users(users)
    users = fix_centiseconds(users, event)
    for user in users:
        print(user["event_pb"])
    # Close the connection
    connection.close()
    return users


main("LazarilloOpen2023", "333mbf", "single")
