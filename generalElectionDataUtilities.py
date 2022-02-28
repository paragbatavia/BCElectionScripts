# Takes in a list of dictionaries of election data, returns a map of all
# election data specific to that county only
def filterResultsByCounty(electionData, countyData, countyName):

    # filter the county dictionary list to find the passed in county name
    # countyDict = list(filter(lambda county: county['County'] == countyName, electionData))
    countyDict = next(item for item in countyData if item['County'] == str(countyName))
    countyNumber = countyDict['Code']

    # filteredResult = next(item for item in electionData if item['CountyCode'] == str(countyNumber))
    filteredResult = list(filter(lambda county: county['CountyCode'] == countyNumber, electionData))

    # print("county name = " + countyName + " county number = " + str(countyNumber))

    # print(filteredResult)
    return filteredResult


# Takes in election data structure, and returns a list of dictionary elements
# that only have data for the specified candidate.
def filterResultsByCandidateName(electionData, lastName, firstName):
    # NOTE - This assumes last name filter only

    filteredResult = list(filter(lambda name: name['LastName'] == lastName and name['FirstName'] == firstName,
                                 electionData))

    return filteredResult


# This will take data filtered by county by candidate, and create a dictionary with the following entries
# PrecinctCode, LastName, FirstName, VoteTotal
def getResultsByPrecinct(electionData):

    desiredKeys = {'PrecinctCode', 'LastName', 'FirstName', 'VoteTotal', 'MunicipalityName'}

    filteredResult = []
    for x in electionData:
        filteredResult.append({newKey: x[newKey] for newKey in desiredKeys})

    # print(filteredResult)

    return filteredResult


# The purpose of this function is to take in two election data sets (represented
# as lists of dictionaries) which are already pre-filtered by county and by candidate name,
# and combine them into a single new data structure which is also a list of dictionaries,
# where data from the same precinct for each candidate is added to each list item
# (dictionary entry).
# It works by iterating over the first dictionary list, pulls out precinct and votes, search
# over second dictionary list for same precinct, pull out results two, combine
# into a new dictionary and append to results list.
# Note - this assumes that precincts may be arbitrarily ordered between the two
# lists, when in reality they always seem to be in the same order.
def combineResultsByPrecinct(results1, title1, results2, title2):

    precinctKey = "PrecinctCode"
    precinctNameKey = "PrecinctName"
    votes1Key = title1 + "Votes"
    votes2Key = title2 + "Votes"

    combined = []
    for x in results1:
        votes1 = x['VoteTotal']
        precinct = x['PrecinctCode']
        dict2 = next((item for item in results2 if item['PrecinctCode'] == str(precinct)), None)
        if not dict2:
            continue
        votes2 = dict2['VoteTotal']
        municipalityName = dict2['MunicipalityName']

        newItem = {precinctKey: precinct, precinctNameKey: municipalityName, votes1Key: votes1, votes2Key: votes2}

        # print(newItem)
        combined.append(newItem)

    return combined

