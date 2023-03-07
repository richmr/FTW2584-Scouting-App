from typing import List
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


# from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey, PickleType
# from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

class scoring_base(DeclarativeBase):
    pass

class Teams(scoring_base):
    __tablename__ = "Teams"

    team_number: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str]
    team_game_actions: Mapped[List["Observed_Actions"]] = relationship()
    # pictures: Mapped[List["Robot_Pics"]] = relationship()

# class Robot_Pics(scoring_base):
#     __tablename__ = "Robot_Pics"

#     rowID:Mapped[int] = mapped_column(primary_key=True)
#     team_number: Mapped[int] = mapped_column(ForeignKey("Teams.team_number"))
#     image: Mapped

class Game_Modes(scoring_base):
    __tablename__ = "Game_Modes"

    modeID: Mapped[int] = mapped_column(primary_key=True)
    mode_name: Mapped[str]

class Possible_Actions(scoring_base):
    __tablename__ = "Possible_Actions"

    actionID: Mapped[int] = mapped_column(primary_key=True)
    action_description: Mapped[str]
    requires_precondition: Mapped[bool]
    # precondition_action: Mapped[int] = mapped_column(insert_default=None)

class Follow_Actions(scoring_base):
    __tablename__ = "Follow_Actions"

    rowID: Mapped[int] = mapped_column(primary_key=True)
    initial_action: Mapped[int] = mapped_column(ForeignKey("Possible_Actions.actionID"))
    final_action: Mapped[int] = mapped_column(ForeignKey("Possible_Actions.actionID"))

class Matches(scoring_base):
    __tablename__ = "Matches"

    matchID: Mapped[int] = mapped_column(primary_key=True)
    match_name: Mapped[str]
    red_1: Mapped[int] = mapped_column(ForeignKey("Teams.team_number"))
    red_2: Mapped[int] = mapped_column(ForeignKey("Teams.team_number"))
    red_3: Mapped[int] = mapped_column(ForeignKey("Teams.team_number"))
    blue_1: Mapped[int] = mapped_column(ForeignKey("Teams.team_number"))
    blue_2: Mapped[int] = mapped_column(ForeignKey("Teams.team_number"))
    blue_3: Mapped[int] = mapped_column(ForeignKey("Teams.team_number"))

class Observed_Actions(scoring_base):
    __tablename__ = "Observed_Actions"

    rowID: Mapped[int] = mapped_column(primary_key=True)
    matchID: Mapped[int] = mapped_column(ForeignKey("Matches.matchID"))
    team_number: Mapped[int] = mapped_column(ForeignKey("Teams.team_number"))
    action_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    actionID: Mapped[int] = mapped_column(ForeignKey("Possible_Actions.actionID"))

        