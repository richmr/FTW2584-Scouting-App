from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from sqlalchemy.exc import IntegrityError, NoResultFound

from typing import Union, List
from enum import Enum

from appsecrets import user_site_key, admin_site_key, all_key, app_mode, sqlAConnectionString
from appdata import appdata
from datamodels import Teams

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

# teaminfo(key: ValidKeys, id: Union[List[int]] = Query(default=None)):
@app.get("/{key}/api/team/results")
def teamresults(key: ValidKeys, 
                team_numbers: Union[List[int], None] = Query(default=None),
                stats_type: StatSummaryTypes = Query(default=None),
                group_by_mode: bool = False,
                return_key: Union[str, None] = Query(default=None)
    ):
    """
    Returns a variety of responses.

    stats_type = total

    Set return_key to desired value to place it in a dictionary like {return_key: data}
    """
    if key is not ValidKeys.admin:
        raise HTTPException(status_code=401, detail="Please use admin key to access this API")

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
