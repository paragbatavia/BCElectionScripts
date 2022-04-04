# Define data types used across functions

from typing import TypedDict


class CountyMap(TypedDict):
    CountyNumber: int
    CountyName: str


class PrecinctMap(TypedDict):
    """
    This structure holds mappings from precinct code to precinct name
    In addition, the mapping of codes to names is different depending
    on the data source (PA DoS Voter Registration Data vs. Vote Builder
    Turnout data. Therefor we maintain both mappings, so we can
    search for data in both data sources based on index
    """
    RegisteredDataPrecinctNumber: int
    RegisteredDataPrecinctName: str
    VoteBuilderPrecinctNumber: int
    VoteBuilderPrecinctName: str


class TurnoutData(TypedDict):
    """ Representation of turnout data taken from VoteBuilder """
    PrecinctNumber: int
    PrecinctName: str
    Year: int
    DemTurnout: int


class RegisteredVoterData(TypedDict):
    """ Representation of voter registration data taken from VoteBuilder """
    PrecinctNumber: int
    PrecinctName: str
    Year: int
    RegisteredDems: int


class CandidateComparison(TypedDict):
    PrecinctCode: int
    PrecinctName: str
    Candidate1Name: str
    Candidate1Votes: int
    Candidate2Name: str
    Candidate2Votes: int


class TurnoutComparison(TypedDict):
    PrecinctCode: int
    PrecinctName: str
    Y1Year: int
    Y1DemsRegistered: int
    Y1DemsVoted: int
    Y1TurnoutPercentage: float
    Y2Year: int
    Y2DemsRegistered: int
    Y2DemsVoted: int
    Y2TurnoutPercentage: float
    Y1Y2RegistrationChangePercentage: float
    Y1Y2TurnoutChangePercentage: float

