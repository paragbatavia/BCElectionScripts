import csv
import io
from dataTypes import *
from typing import *


def loadCountyMap(baseDirectory: str, fileName: str):
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


def loadPrecinctMap(baseDirectory: str, fileName: str) -> List[PrecinctMap]:

    precinctMap = []

    fullFileName = baseDirectory + fileName
    with open(fullFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for row in reader:
            rzone = int(row['RegisteredDataPrecinctCode'])
            rtitle = row['RegisteredDataPrecinctName']
            vzone = int(row['VoteBuilderPrecinctCode'])
            vtitle = row['VoteBuilderPrecinctName']
            mapItem = {'RegisteredDataPrecinctNumber': rzone,
                       'RegisteredDataPrecinctName': rtitle,
                       'VoteBuilderPrecinctNumber': vzone,
                       'VoteBuilderPrecinctName': vtitle}
            precinctMap.append(mapItem)

    return precinctMap


def loadElectionData(baseDirectory, fileName):
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


def loadVoterRegistrationData(baseDirectory: str, fileName: str, county: int) -> List[RegisteredVoterData]:
    """
    Read in voter registration data from file, returns a list of structs / dictionaries
    :param baseDirectory:
    :param fileName:
    :param county:
    :return: list of RegisteredVoterData structures
    """

    fullFileName = baseDirectory + fileName
    registeredVoterData = []
    with open(fullFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for row in reader:
            if int(row['CountyCode']) == county:
                # We've found data from our county - start populating a data element
                # print(row)
                year = int(row['ElectionYear'])
                precinctcode = int(row['PrecinctCode'])
                precinctname = row['MunicipalityName']
                dems = int(row['DemRegistered'])
                voterItem = {'PrecinctNumber': precinctcode,
                             'PrecinctName': precinctname,
                             'Year': year,
                             'RegisteredDems': dems}
                registeredVoterData.append(voterItem)

    return registeredVoterData


def loadVoterTurnoutData(baseDirectory: str, fileName: str, year: int) -> List[TurnoutData]:
    """
    Read in turnout data spreadsheet from file, and returns a list of structs.
    This turnout data comes from VoteBuilder, and is already filtered by Butler County already,
    so no need to further filter the data.
    :param year:
    :param baseDirectory:
    :param fileName:
    :return: list of TurnoutData structures
    """

    fullFileName = baseDirectory + fileName
    turnoutData = []
    with open(fullFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for row in reader:
            pnumber = int(row["PrecinctCode"])
            pname = row["Precinct"]
            newyear = year
            voted = int(row["Turnout"])
            turnoutItem = {'PrecinctNumber': pnumber,
                           'PrecinctName': pname,
                           'Year': newyear,
                           'DemTurnout': voted}
            turnoutData.append(turnoutItem)

    # print(turnoutData)

    return turnoutData


def outputResultsToCSVFile(results: List, baseDirectory: str, fileName: str, header: List = None):
    # Writes the passed in list of dictionaries to a CSV file
    fullFileName = baseDirectory + fileName

    with open(fullFileName, 'w', newline='') as csvfile:
        fieldNames = results[0].keys()
        # writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer = csv.writer(csvfile)

        if not header:
            # writer.writeheader()
            print('Hello')
        else:
            writer.writerow(dict(zip(header, header)))
        for x in results:
            # writer.writerow(x)
            writer.writerow([x[k] for k in fieldNames])

