from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import func, select, distinct

from typing import Union, List, Dict
from enum import Enum
import traceback

from appsecrets import user_site_key, admin_site_key, all_key, app_mode, sqlAConnectionString
from appdata import appdata
from datamodels import Teams, Observed_Actions

app = None
if app_mode == "test":
    app = FastAPI()
else:
    app = FastAPI(openapi_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

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
        if return_key is not None:
            toreturn = {return_key:toreturn}
        return toreturn

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
    return toreturn   

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
    return toreturn

# Delete Team
@app.get("/{key}/api/team/delete")
def deleteteam(key: ValidKeys, team_number: int, return_key: Union[str, None] = Query(default=None)):
    """
    Modifies team data in the database
    Returns: {
        team_number:
        team_name:
    }

    Set return_key to desired value to place it in a dictionary like {return_key: data}
    """
    if key is not ValidKeys.admin:
        raise HTTPException(
            status_code=401, detail="Please use admin key to access this API")

    with appdata.getSQLSession() as dbsession:
        try:
            toreturn = []
            # Find the object
            team_db = dbsession.query(Teams).filter_by(team_number=team_number).one()
            # delete it
            dbsession.delete(team_db)
            dbsession.commit()
        except NoResultFound:
            raise HTTPException(
                status_code=400, detail=f"No team {team_number} exists")
        except Exception as badnews:
            raise HTTPException(status_code=500, detail=f"{badnews}")

    if return_key is not None:
        toreturn = {return_key: toreturn}
    return toreturn

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
                        func.count(Observed_Actions.rowID).label("total")).group_by(Observed_Actions.team_number, Observed_Actions.mode_name, Observed_Actions.action_label)
            res = dbsession.execute(stmt)
            for r in res:
                if r.team_number not in teamResultsDict.keys():
                    teamResultsDict[r.team_number] = TeamMatchResults(team_number=r.team_number,
                                                                    team_name=team_data_dict[r.team_number]["team_name"],
                                                                    matches_played=team_data_dict[r.team_number]["matches_played"])
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
                    
        
## Match API
# Get All Matches

# Get Match Data

# Add Match

# Modify Match

# Delete Match

## Observed Actions

# Add action

# Modify action

# Delete action
