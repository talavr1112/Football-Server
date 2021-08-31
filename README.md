
Running guidelines:
---------------------
1) Open cmd
2) Navigate to project directory
3) Run: python football_server.py 
4) Open browser and navigate to http://localhost:8080

To get list of matches by team enter url:
    http://localhost:8080/?team=<team_name>
To get list of matches by team filtered by status enter url: 
    http://localhost:8080/?team=<team_name>&status=<status>

To get list of matches by tournament enter url: 
    http://localhost:8080/?tournament=<tournament>
To get list of matches by tournament filtered by status enter url: 
    http://localhost:8080/?tournament=<tournament>&status=<status>
    
Running examples:
-------------------
To get list of matches of "Sutton united" team:
    http://localhost:8080/?team=Sutton United
To get list of matches of "premier-league" tournament filtered by status "upcoming":
    http://localhost:8080/?tournament=premier-league&status=upcoming
    
Result:
----------
Please see result on the web browser which contains the response for the "get" request in json format.
Recommendation: Add JSONView or other chrome extension for a nicer json display :)

Please see attached file "RunningExamples.pdf" for examples.
