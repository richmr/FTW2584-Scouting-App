from datetime import datetime
import json
from pprint import pprint
import re
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import func, select, distinct

from typing import Union, List, Dict
from enum import Enum
import traceback

from appsecrets import user_site_key, admin_site_key, app_mode, sqlAConnectionString, static_key
from appdata import appdata
from datamodels import Teams, Observed_Actions, Matches

app = None
if app_mode == "test":
    app = FastAPI()
else:
    app = FastAPI(openapi_url=None)

app.mount(f"/{static_key}/static", StaticFiles(directory="static"), name="static")

class ValidKeys(str, Enum):
    user = user_site_key
    admin = admin_site_key

# Initialize appdata
appdata(sqlAConnectionString)

################ APIS ######################

## Team APIs

# Get Teams
@app.get("/{key}/api/team/allteams")
def allteams(key: ValidKeys, return_key: Union[str, None] = Query(default=None)):
    """
    Returns list of {team_number, team_name}

    Set return_key to desired value to place it in a dictionary like {return_key: data}
    """
    with appdata.getSQLSession() as dbsession:
        res = dbsession.query(Teams)
        toreturn = [{"team_number":row.team_number, "team_name":row.team_name} for row in res]
        return {"data":toreturn}

# Add Team
class TeamModel(BaseModel):
    team_number: int
    team_name: str

@app.post("/{key}/api/team/addteam")
def addteam(key: ValidKeys, team_data: TeamModel, return_key: Union[str, None] = Query(default=None)):
    """
    Adds a team
    Returns: {
        team_number:
        team_name:
    }

    Set return_key to desired value to place it in a dictionary like {return_key: data}
    """
    if key is not ValidKeys.admin:
        raise HTTPException(status_code=401, detail="Please use admin key to access this API")
    
    with appdata.getSQLSession() as dbsession:
        # Attempt to add
        try:
            toreturn = team_data.dict()
            print(toreturn)
            newteam = Teams().fromDict(toreturn)
            dbsession.add(newteam)
            dbsession.commit()
        except IntegrityError as badnews:
            raise HTTPException(status_code=422, detail=f"Team {team_data.team_number} already exists")
        except Exception as badnews:
            raise HTTPException(status_code=500, detail=f"{badnews}")
        
    if return_key is not None:
        toreturn = {return_key:toreturn}
    return {"data":[toreturn]}

# Modify Team
@app.post("/{key}/api/team/modify")
def modifyteam(key: ValidKeys, team_data: TeamModel, return_key: Union[str, None] = Query(default=None)):
    """
    Modifies team data in the database
    Returns: {
        team_number:
        team_name:
    }

    Set return_key to desired value to place it in a dictionary like {return_key: data}
    """
    if key is not ValidKeys.admin:
        raise HTTPException(status_code=401, detail="Please use admin key to access this API")
    
    with appdata.getSQLSession() as dbsession:
        try:
            toreturn = team_data.dict()
            # Find the object
            team_db = dbsession.query(Teams).filter_by(team_number = team_data.team_number).one()
            # update it
            team_db.fromDict(toreturn)
            dbsession.commit()
        except NoResultFound:
            raise HTTPException(status_code=400, detail=f"No team {team_data.team_number} exists")
        except Exception as badnews:
            raise HTTPException(status_code=500, detail=f"{badnews}")
        
    if return_key is not None:
        toreturn = {return_key: toreturn}
    return {"data":[toreturn]}

# Delete Team
class JustTeamNumber(BaseModel):
    team_number: int

@app.post("/{key}/api/team/delete")
def deleteteam(key: ValidKeys, team_data: JustTeamNumber):
    """
    deletes team data in the database
    
    """
    if key is not ValidKeys.admin:
        raise HTTPException(
            status_code=401, detail="Please use admin key to access this API")

    with appdata.getSQLSession() as dbsession:
        try:
            toreturn = []
            # Find the object
            team_db = dbsession.query(Teams).filter_by(team_number=team_data.team_number).one()
            # delete it
            dbsession.delete(team_db)
            dbsession.commit()
        except NoResultFound:
            raise HTTPException(
                status_code=400, detail=f"No team {team_data.team_number} exists")
        except Exception as badnews:
            raise HTTPException(status_code=500, detail=f"{badnews}")

    
    return {"data":[toreturn]}

# Get Team results
class StatSummaryTypes(str, Enum):
    total = "total"
    by_placement = "by_placement"

class SummaryResults(BaseModel):
    scored_cone = 0
    scored_cube = 0
    balanced_charging_station = 0
    robot_broke = 0

class AverageResults(BaseModel):
    scored_cone = 0.0
    scored_cube = 0.0
    balanced_charging_station = 0.0
    robot_broke = 0.0


class TeamMatchResults(BaseModel):
    team_number: int
    team_name: str
    matches_played: int
    preference: int
    Auton = SummaryResults()
    Tele = SummaryResults()
    total = SummaryResults()
    avg = AverageResults()

class AllResults(BaseModel):
    data:List[TeamMatchResults]

# teaminfo(key: ValidKeys, id: Union[List[int]] = Query(default=None)):
@app.get("/{key}/api/team/results")
def teamresults(key: ValidKeys) -> AllResults:
    """
    Returns dictionary with list of team results behind the "data" key 
    """
    with appdata.getSQLSession() as dbsession:
        try:
            teamResultsDict = {}
            allTeams_q = dbsession.query(Teams)
            team_data_dict = {r.team_number: {"team_name": r.team_name}
                            for r in allTeams_q}
            stmt = select(Observed_Actions.team_number, func.count(distinct(
                Observed_Actions.matchID)).label("matches_played")).group_by(Observed_Actions.team_number)
            for row in dbsession.execute(stmt):
                team_data_dict[row.team_number]["matches_played"] = row.matches_played

            stmt = select(Observed_Actions.team_number,
                        Observed_Actions.mode_name,
                        Observed_Actions.action_label,
                        func.sum(Observed_Actions.count_seen).label("total")).group_by(Observed_Actions.team_number, Observed_Actions.mode_name, Observed_Actions.action_label)
            res = dbsession.execute(stmt)
            for r in res:
                if r.team_number not in teamResultsDict.keys():
                    teamResultsDict[r.team_number] = TeamMatchResults(team_number=r.team_number,
                                                                    team_name=team_data_dict[r.team_number]["team_name"],
                                                                    matches_played=team_data_dict[r.team_number]["matches_played"],
                                                                    preference=99) # Place holder preference
                tr = teamResultsDict[r.team_number]
                m = getattr(tr, r.mode_name, None)
                # Set by mode
                if m is not None:
                    if hasattr(m, r.action_label):
                        setattr(m, r.action_label, getattr(
                            m, r.action_label) + r.total)

                # Set by total
                if hasattr(tr.total, r.action_label):
                    setattr(tr.total, r.action_label, getattr(
                        tr.total, r.action_label) + r.total)

                # Add count to avg ( do math later )
                if hasattr(tr.avg, r.action_label):
                    setattr(tr.avg, r.action_label, getattr(
                        tr.avg, r.action_label) + r.total)

            for n, (k, v) in enumerate(teamResultsDict.items()):
                # Calculate averages
                if v.matches_played > 0:
                    for attr in v.avg.__fields__.keys():
                        setattr(v.avg, attr, round(
                            getattr(v.avg, attr)/v.matches_played, 1))
                        
            return AllResults(data=list(teamResultsDict.values()))
        except Exception as badnews:
            detail = f"{badnews}"
            if app_mode == "test":
                print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=detail) 

def generate_csv_header_list(in_dict:dict, lead_in="") -> list:
    toreturn = []
    if not isinstance(in_dict, dict):
        return []
    for n, (key, val) in enumerate(in_dict.items()):
        if isinstance(val, dict):
            toreturn += generate_csv_header_list(val, lead_in=f"{lead_in}_{key}")
        else:
            toreturn += [f"{lead_in}_{key}"]
    return toreturn

def generate_csv_line_list_from_dict(in_dict:dict) -> list:
    toreturn = []
    for n, (key, val) in enumerate(in_dict.items()):
        if isinstance(val, dict):
            toreturn += generate_csv_line_list_from_dict(val)
        else:
            toreturn += [val]
    return toreturn

@app.get("/{key}/api/team/resultscsv")
def resultscsv(key: ValidKeys):
    try:
        results = teamresults(key).dict()["data"]
        if len(results) == 0:
            return Response(content="", media_type="text/csv")
        header_list = [str(data) for data in generate_csv_header_list(results[0])]
        csv_data = ",".join(header_list) + "\n"
        for entry in results:
            this_list = [str(data) for data in generate_csv_line_list_from_dict(entry)]
            csv_data += ",".join(this_list) + "\n"
        return Response(content=csv_data, media_type="text/csv")
    except Exception as badnews:
        if app_mode == "test":
            print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"{badnews}")

## Match API
class SingleMatchData(BaseModel):
    matchID = -1
    match_name: str
    red_1: int
    red_2: int
    red_3: int
    blue_1: int
    blue_2: int
    blue_3: int

class MatchList(BaseModel):
    data: List[SingleMatchData]

def cleanString(in_str: str) -> str:
    """
    Removes all but letters, numbers, and spaces from a string
    """
    out_str = re.sub("[^A-Z\s\d]", "", in_str, 0, re.IGNORECASE)
    return out_str

# Get All Matches
@app.get("/{key}/api/match/all")
def allmatch(key: ValidKeys) -> MatchList:
    try:
        with appdata.getSQLSession() as dbsession:
            res = dbsession.query(Matches)
            return MatchList(data=[SingleMatchData(**r.toDict()) for r in res])
    except Exception as badnews:
        raise HTTPException(status_code=500, detail=f"{badnews}")



    
# Add Match
@app.post("/{key}/api/match/add")
def addmatch(key: ValidKeys, match_data:SingleMatchData):
    if key is not ValidKeys.admin:
        raise HTTPException(
            status_code=401, detail="Please use admin key to access this API")

    try:
        with appdata.getSQLSession() as dbsession:
            # need to pop out the matchID
            md = match_data.dict()
            md.pop("matchID", -1)
            md["match_name"] = cleanString(md["match_name"])
            newmatch = Matches().fromDict(md)
            dbsession.add(newmatch)
            dbsession.commit()
            return {"data":[SingleMatchData(**newmatch.toDict())]}
    except Exception as badnews:
        raise HTTPException(status_code=500, detail=f"{badnews}")

# Modify Match
@app.post("/{key}/api/match/modify")
def modify_match(key: ValidKeys, match_data:SingleMatchData):
    if key is not ValidKeys.admin:
        raise HTTPException(
            status_code=401, detail="Please use admin key to access this API")

    with appdata.getSQLSession() as dbsession:
        try:
            toreturn = match_data.dict()
            # Find the object
            team_db = dbsession.query(Matches).filter_by(matchID = match_data.matchID).one()
            # update it
            team_db.fromDict(toreturn)
            dbsession.commit()
        except NoResultFound:
            raise HTTPException(status_code=400, detail=f"No match {match_data.matchID} exists")
        except Exception as badnews:
            raise HTTPException(status_code=500, detail=f"{badnews}")
        
    return {"data":[toreturn]}

# Delete Match
@app.get("/{key}/api/match/delete")
def delete_match(key: ValidKeys, matchID:int):
    if key is not ValidKeys.admin:
        raise HTTPException(
            status_code=401, detail="Please use admin key to access this API")
    
    with appdata.getSQLSession() as dbsession:
        try:
            toreturn = {}
            # Find the object
            match = dbsession.query(Matches).filter_by(matchID = matchID).one()
            # update it
            dbsession.delete(match)
            dbsession.commit()
            return {"data":[toreturn]}
        except NoResultFound:
            raise HTTPException(status_code=400, detail=f"No match {matchID} exists")
        except Exception as badnews:
            raise HTTPException(status_code=500, detail=f"{badnews}")


## Observed Actions

# Add action

class NewObsAction(BaseModel):
    matchID: int
    mode_name: str
    team_number: int
    #action_timestamp: datetime
    action_label: str
    count_seen: int

# class ObsActions(BaseModel):
#     actions: List[NewObsAction]

class SmallObsActions(BaseModel):
    mode_name: str
    action_label: str
    count_seen: int

class ScoredActions(BaseModel):
    matchID: int
    team_number: int
    scored_items: List[SmallObsActions]

@app.post("/{key}/api/actions/addaction")
def addaction(key:ValidKeys, action_data: NewObsAction) -> dict:
    # Need logic to prevent multi balances
    with appdata.getSQLSession() as dbsession:
        dbsession.add(Observed_Actions().fromDict(action_data.dict()))
        dbsession.commit()

@app.get("/{key}/api/actions/addmanyactions")
def addmanyactions_get(key:ValidKeys, action_obj: str):
    """
    action_obj is a string like:
    match_id|team_number|action_label|mode|count_seen...
    ex: 1|606|team_competed|Tele|1|robot_broke|Tele|1

    Exists to allow for QR code style data submits
    """
    data_recvd = action_obj.split("|")
    matchID = int(data_recvd[0])
    team_number = int(data_recvd[1])
    scored_items = []
    for index in range(2,len(data_recvd),3):
        scored_items.append(
            SmallObsActions(
                mode_name=data_recvd[index],
                action_label=data_recvd[index+1],
                count_seen=data_recvd[index+2]
            )
        )
    actions = ScoredActions(
        matchID=matchID,
        team_number=team_number,
        scored_items=scored_items
    )
    success = addmanyactions(key, actions)
    # If we get here it must have been successful
    response = f"""
    <html>
        <head>
            <title>Data received</title>
        </head>
        <body>
            <h2>Match data for team {team_number} received</h2>
        </body>
    </html>
    """
    return HTMLResponse(content=response, status_code=200)

@app.post("/{key}/api/actions/addmanyactions")
def addmanyactions(key:ValidKeys, actions: ScoredActions):
    with appdata.getSQLSession() as dbsession:
        try:
            # Check for this team and match already submitted.
            exist_count = dbsession.query(Observed_Actions).filter_by(matchID = actions.matchID, team_number = actions.team_number).count()
            if exist_count > 0:
                raise HTTPException(status_code=400, detail=f"Match data for team {actions.team_number} already submitted for this match")
            for action in actions.scored_items:
                # Check for this team and match already submitted.
                dbsession.add(Observed_Actions(matchID=actions.matchID, team_number=actions.team_number).fromDict(action.dict()))
            dbsession.commit()
            return {}
        except HTTPException as http_badnews:
            raise http_badnews
        except Exception as badnews:
            if app_mode == "test":
                print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"{badnews}")
    

# Modify action

# Delete action
