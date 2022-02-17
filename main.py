# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from butlerCountySpecific import *
import csv

# general variables
baseDirectory = "C:\\Users\\parag\\Documents\\BCDems\\ElectionData\\"


def loadCountyMap(fileName):
    # Loads in a map of county names to county numbers

    countyMap = []
    fullFileName = baseDirectory + fileName
    with open(fullFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for row in reader:
            countyMap.append(row)

    # print("load_county_map() finished")

    # print(countyMap)

    return countyMap


def loadElectionData(fileName):
    # Comment
    fullFileName = baseDirectory + fileName
    electionData = []
    # print("Hello, ", {fullFileName})
    with open(fullFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        counter = 0
        for row in reader:
            counter = counter + 1
            electionData.append(row)
            # print(row['FirstName'], row['LastName'])
    # print("load_election_data(): Read in " + str(counter) + " lines\n")

    # This is a list of dictionary items, with the keys being the top row of the CSV file
    return electionData


def filterResultsByCounty(electionData, countyData, countyName):
    # Takes in a list of dictionaries of election data, returns a map of all
    # election data specific to that county only

    # filter the county dictionary list to find the passed in county name
    # countyDict = list(filter(lambda county: county['County'] == countyName, electionData))
    countyDict = next(item for item in countyData if item['County'] == str(countyName))
    countyNumber = countyDict['Code']

    # filteredResult = next(item for item in electionData if item['CountyCode'] == str(countyNumber))
    filteredResult = list(filter(lambda county: county['CountyCode'] == countyNumber, electionData))

    # print("county name = " + countyName + " county number = " + str(countyNumber))

    # print(filteredResult)
    return filteredResult


def filterResultsByCandidateLastName(electionData, lastName, firstName):
    # NOTE - This assumes last name filter only
    # TODO: update for first and last name filtering

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


# Iterate over the first dictionary list, pull out precinct and votes, search
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


def outputResultsToCSVFile(results, fileName):
    # Writes the passed in list of dictionaries to a CSV file
    fullFileName = baseDirectory + fileName

    with open(fullFileName, 'w', newline='') as csvfile:
        fieldNames = results[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)

        writer.writeheader()
        for x in results:
            writer.writerow(x)


# This will compare general election performance of two candidates, and write the
# results out to a CSV file - sorted by precinct
def compareCandidatesSameYear(candidate1, first1, candidate2, first2, electionData, outputFileName):

    # First, we take our entire general election data file, and pull out all data specific to
    # a single candidate
    candidate1Results = filterResultsByCandidateLastName(electionData, candidate1, first1)
    candidate2Results = filterResultsByCandidateLastName(electionData, candidate2, first2)

    c1PrecinctResults = getResultsByPrecinct(candidate1Results)
    c1PrecinctResultsCombined = combineButlerCongressionalDistrictData(c1PrecinctResults)
    # print(str(len(c1FilteredResults)))
    c2PrecinctResults = getResultsByPrecinct(candidate2Results)
    c2PrecinctResultsCombined = combineButlerCongressionalDistrictData(c2PrecinctResults)
    # print(str(len(c2FilteredResults)))

    combinedResults = combineResultsByPrecinct(c1PrecinctResultsCombined, candidate1,
                                               c2PrecinctResultsCombined, candidate2)

    outputResultsToCSVFile(combinedResults, outputFileName)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # This will load in a map that maps county names to county numbers - required to search for
    # county-specific election results
    countyMap = loadCountyMap('CountyMap.csv')
    # This will load in all of 2020's general election results
    generalElectionResults2020 = loadElectionData('ElectionReturns_2020_General_PrecinctReturns.csv')

    # Now we'll filter out only the Butler County results. Can put any county name in here
    butlerCountyGeneralElection2020 = filterResultsByCounty(generalElectionResults2020, countyMap, 'Butler')

    print("main(): Read in " + str(len(generalElectionResults2020)) + " election records")
    print("Received " + str(len(butlerCountyGeneralElection2020)) + " county-specific results")

    compareCandidatesSameYear('BIDEN', 'JOSEPH', 'SHAPIRO ', 'JOSHUA',
                              butlerCountyGeneralElection2020, "BidenVShapiro2020General.csv")
    compareCandidatesSameYear('BIDEN', 'JOSEPH', 'LAMB', 'CONOR',
                              butlerCountyGeneralElection2020, "BidenVLamb2020General.csv")
    compareCandidatesSameYear('SMITH', 'DANIEL', 'METCALFE', 'DARYL',
                              butlerCountyGeneralElection2020, "SmithVMetcalfe2020General.csv")

    # Now, let's pull out all the Biden 2020 results from Butler County
    # bidenResults = filterResultsByCandidateLastName(butlerCountyGeneralElection2020, 'BIDEN')
    # Note - had to add an extra space after SHAPIRO for Butler county only because that's how the data is
    # shapiroResults = filterResultsByCandidateLastName(butlerCountyGeneralElection2020, 'SHAPIRO ')

    # Create version that only has desired data (precinct code, last name, first name, vote total)
    # bidenFilteredResults = getResultsByPrecinct(bidenResults)
    # shapiroFilteredResults = getResultsByPrecinct(shapiroResults)

    # combinedResults = combineResultsByPrecinct(bidenFilteredResults, "Biden", shapiroFilteredResults, "Shapiro")
    # print("Received " + str(len(bidenResults)) + " Biden-specific results")
    # print("Received " + str(len(shapiroResults)) + " Shapiro-specific results")

    # outputResultsToCSVFile(combinedResults, "BidenVShapiro2020General.csv")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
