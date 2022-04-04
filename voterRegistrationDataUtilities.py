# The utilities in this file are used to process voter registration data
from filterUtilities import *


def extractDemRegisteredByPrecinct(registrationData):
    """
    This will create a simple list of dictionaries with the following entries:
    - Municipality Code
    - Municipality Name
    - Registered Dems
    :param registrationData:
    :return:
    """

    desiredKeys = {'PrecinctCode', 'MunicipalityName', 'DemRegistered'}

    filteredResult = []
    for x in registrationData:
        filteredResult.append({newKey: x[newKey] for newKey in desiredKeys})

    # print(filteredResult)

    return filteredResult


def extractTurnoutByPrecinct(electionData):
    """
    *** DEPRECATED - DO NOT USE ***
    So, our approach here is to look at Democratic turnout only in the US Presidential
    election - this may not reflect full turnout - it misses the cases where Dems may
    have voted in the presidential election for a different candidate than in a
    down-ballot election. The 'right' way to do this would be to look at all Dem
    votes across all elections, and take the maximum.
    NOTE: We assume the passed in electionData is already filtered by County

    :param electionData:
    :return:
    """

    # Create a list of dictionaries that is filtered by the following
    #  - OfficeCode == 'USP' (US President)
    #  - PartyCode == 'DEM' (Democrat)
    filteredResult = list(filter(lambda name: name['OfficeCode'] == 'USP' and name['PartyCode'] == 'DEM',
                                 electionData))

    # Now filter this to return a list that only includes the following elements
    #  - Municipality Code
    #  - Municipality Name
    #  - Dem Turnout
    desiredKeys = {'PrecinctCode', 'MunicipalityName', 'VoteTotal'}
    finalResult = []
    for x in filteredResult:
        finalResult.append({newKey: x[newKey] for newKey in desiredKeys})

    return finalResult


def combineRegistrationAndElectionDataByPrecinct(demRegistered, demTurnout, titlePrefix: str):
    """
    *** DEPRECATED - DO NOT USE ***
    This takes in two lists of dictionaries - both filtered by County, one
    which contains dem voter registration data, and one which contains
    dem turnout data (for a specific election, usually US President),
    and combines it into a new list of dictionaries that contains the following
     - Precinct Code
     - Municipality Name
     - Dems Registered
     - Dems Voted
     - % of dems registered who voted

    :param demRegistered:
    :param demTurnout:
    :param titlePrefix:
    :return:
    """

    precinctKey = "PrecinctCode"
    precinctNameKey = "PrecinctName"
    registeredKey = titlePrefix + "_DemsRegistered"
    votedKey = titlePrefix + "_DemsVoted"
    turnoutKey = titlePrefix + "_TurnoutPercentage"

    combined = []
    for x in demRegistered:
        demsRegistered = x['DemRegistered']
        precinct = x['PrecinctCode']
        # Now, we've pulled a precinct code from a list element in demRegistered - look for the
        # same precinct code entry in the list demTurnout
        dict2 = next((item for item in demTurnout if item['PrecinctCode'] == str(precinct)), None)
        # This would only happen if we have registered dems in a precinct, but no one voted for the
        # dem candidate in that precinct - in that case, dict2 would be Null
        if not dict2:
            continue
        demsVoted = dict2['VoteTotal']
        municipalityName = dict2['MunicipalityName']

        if float(demsRegistered) >= 1:
            turnout = float(demsVoted) / float(demsRegistered)
        else:
            turnout = 0.0

        newItem = {precinctKey: precinct, precinctNameKey: municipalityName, registeredKey: demsRegistered,
                   votedKey: demsVoted, turnoutKey: str(turnout)}

        # print(newItem)
        combined.append(newItem)

    return combined


def combineVoterTurnoutByYearByPrecinct(turnoutData1, turnoutData2):
    """
    This routine takes in two lists of dictionaries, each of which contains turnout information,
    and combines them.

    :param turnoutData1: voter turnout data for first comparison year
    :param turnoutData2: voter turnout data for second comparison year
    :return: single list of dictionaries that merges the (key,values) of both passed in dictionaries
    """

    turnoutKeys1 = turnoutData1[0].keys()
    turnoutKeys2 = turnoutData2[0].keys()

    combined = []
    for x in turnoutData1:
        precinct = x['PrecinctCode']
        dict2 = next((item for item in turnoutData2 if item['PrecinctCode'] == str(precinct)), None)
        if not dict2:
            continue
        # Now = we need to combine x and dict2 into a single dictionary
        newDict = {}
        newDict.update(x)
        newDict.update(dict2)

        combined.append(newDict)

    return combined


def extractVoterRegistrationTurnoutByPrecinct(registrationData, electionData, countyData, prefixTitle):
    """
    This function takes in registration data and results data, pulls out all the Butler county
    data, and then creates a single output list of dictionaries that only includes the following
    keys:
    - Precinct Code
    - Municipality Name
    - Dems Registered
    - Dems Voted
    - % of dems registered who voted-

    :param registrationData: list of dictionaries of registration data
    :param electionData: list of dictionaries of election results data
    :param countyData: list of dictionaries of county mapping data
    :param prefixTitle: string that contains prefix to add to return value dictionary keys
    :return: a list of dictionaries that combines selected data from both data sets
    """

    countyOnlyRegistrationResults = filterResultsByCounty(registrationData, countyData, 'Butler')
    countyOnlyElectionResults = filterResultsByCounty(electionData, countyData, 'Butler')

    demRegistered = extractDemRegisteredByPrecinct(countyOnlyRegistrationResults)
    demTurnout = extractTurnoutByPrecinct(countyOnlyElectionResults)

    combinedData = combineRegistrationAndElectionDataByPrecinct(demRegistered, demTurnout, prefixTitle)

    return combinedData


def processVoterTurnoutComparison(voter1, election1, prefix1, voter2, election2, prefix2, countyMap):
    """
    This is a top-level routine to process and compare voter turnout information across two different
    sets of data.

    Args:
        voter1: list of dictionaries of registration data
        election1: list of dictionaries of election results data
        prefix1 (str): text prefix to be applied to output columns, typically denotes data year
        voter2: list of dictionaries of registration data for second year
        election2: list of dictionaries of election results data for second year
        prefix2 (str): text prefix to be applied to output columns, typically denotes data year
        countyMap: list of dictionaries that maps county number to county name, used for filtering data

    Returns:
        List of dictionaries that combines turnout data with election results data across two
        comparison years.

    """

    processed1 = extractVoterRegistrationTurnoutByPrecinct(voter1, election1, countyMap, prefix1)

    processed2 = extractVoterRegistrationTurnoutByPrecinct(voter2, election2, countyMap, prefix2)

    finalData = combineVoterTurnoutByYearByPrecinct(processed1, processed2)
    # print(finalData)

    return finalData
