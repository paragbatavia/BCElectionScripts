# This contains election data filtering utilities that work across various
# types of election data (general returns and voter registration


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

