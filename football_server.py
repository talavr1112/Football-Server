import pandas as pd
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json

# CONSTANTS

PLAYED_FILE_PATH = "input_data/result_played.csv"
UPCOMING_FILE_PATH = "input_data/result_upcoming.csv"
HOME_TEAM_IDENTIFIER = "home_team"
AWAY_TEAM_IDENTIFIER = "away_team"
TOURNAMENT_IDENTIFIER = "tournament"
STATUS_IDX = 3
NUM_OF_ARGUMENTS = 4
GET_BY_IDX = 1
FILTER_ARG_IDX = 2

PLAYED = "played"
UPCOMING = "upcoming"

# GLOBAL VARS

host_name = "localhost"
server_port = 8080
result_played = pd.read_csv(PLAYED_FILE_PATH)
result_played = result_played.assign(status=PLAYED)  # adding status column to the result

result_upcoming = pd.read_csv(UPCOMING_FILE_PATH)
result_upcoming = result_upcoming.assign(status=UPCOMING)


class FootballGameServer(BaseHTTPRequestHandler):
    """
    This class implements football game server which clients can use to get the fixtures (upcoming
    matches) and the results of football matches.
    """

    def do_GET(self):

        res = ""
        query_components = parse_qs(urlparse(self.path).query)
        query_contain_team = 'team' in query_components
        query_contain_tournament = 'tournament' in query_components
        query_contain_status = 'status' in query_components

        if len(query_components) == 1:
            if query_contain_team:
                res = FootballGameServer.get_by_team(query_components['team'][0])
            elif query_contain_tournament:
                res = FootballGameServer.get_by_tournament(query_components['tournament'][0])
        elif len(query_components) == 2:
            if query_contain_team and query_contain_status:
                res = FootballGameServer.get_by_team_and_status(query_components['team'][0],
                                                                query_components['status'][0])
            elif query_contain_tournament and query_contain_status:
                res = FootballGameServer.get_by_tournament_and_status(query_components['tournament'][0],
                                                                      query_components['status'][0])

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(res.encode(encoding='utf_8'))

    # STATIC METHODS

    @staticmethod
    def get_by_team(team_name):
        """
        This method returns list of matched by team.
        :param team_name: team name to filter by
        :return:  list of matched by team, in json format
        """
        played_by_team_json = FootballGameServer.get_json_by_team(result_played, team_name)
        upcoming_by_team_json = FootballGameServer.get_json_by_team(result_upcoming, team_name)

        json_dict_played = json.loads(played_by_team_json)
        json_dict_upcoming = json.loads(upcoming_by_team_json)

        merged_dict = json_dict_played + json_dict_upcoming

        # string dump of the merged dict
        return json.dumps(merged_dict)

    @staticmethod
    def get_by_team_and_status(team_name, status):
        """
        This method returns list of matches by team filtered by status.
        :param team_name: team name to filter by
        :param status: "played", "upcoming"
        :return: list of matches by team filtered by status, in json format
        """
        response_data = result_played if status == PLAYED else result_upcoming
        response_data = FootballGameServer.get_json_by_team(response_data, team_name)
        return response_data

    @staticmethod
    def get_by_tournament(tournament):
        """
        This method returns list of matches by tournament.
        :param tournament: tournament to filter by
        :return:  list of matched by tournament, in json format
        """
        played_by_tournament_json = FootballGameServer.get_json_tournament(result_played, tournament)
        upcoming_by_tournament_json = FootballGameServer.get_json_tournament(result_upcoming, tournament)

        json_dict_played = json.loads(played_by_tournament_json)
        json_dict_upcoming = json.loads(upcoming_by_tournament_json)

        merged_dict = json_dict_played + json_dict_upcoming

        return json.dumps(merged_dict)

    @staticmethod
    def get_by_tournament_and_status(tournament, status):
        """
        This method returns list of matches by tournament, filtered by status.
        :param status: "played", "upcoming"
        :param tournament: tournament to filter by
        :return: ist of matched by tournament filtered by status, in json format
        """
        response_data = result_played if status == PLAYED else result_upcoming
        response_data = FootballGameServer.get_json_tournament(response_data, tournament)
        return response_data

    @staticmethod
    def get_json_by_team(df, team_name):
        """
        This method filter the given data frame by given team name.
        :param df: pandas data frame
        :param team_name: team name
        :return: filtered data frame
        """
        return df.loc[(df[HOME_TEAM_IDENTIFIER] == team_name) | (df[AWAY_TEAM_IDENTIFIER] == team_name)].to_json(
            orient="records", indent=4)

    @staticmethod
    def get_json_tournament(df, tournament):
        """
        This method filter the given data frame by given tournament.
        :param df: pandas data frame
        :param tournament:
        :return: filtered data frame
        """
        return df.loc[(df[TOURNAMENT_IDENTIFIER] == tournament)].to_json(orient="records", indent=4)


if __name__ == "__main__":
    server_address = (host_name, server_port)
    webServer = HTTPServer(server_address, FootballGameServer)
    print("Football server started http://%s:%s" % (host_name, server_port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
