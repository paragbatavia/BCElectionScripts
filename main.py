# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from dataTypes import *
from butlerCountySpecific import *
from compareCandidates import *
from generalElectionDataUtilities import *
from voterRegistrationDataUtilities import *
from voterTurnoutDataUtilities import *
from fileUtilities import *


# general variables
baseDirectory = "C:\\Users\\parag\\Documents\\BCDems\\ElectionData\\"
outputDirectory = "C:\\Users\\parag\\Documents\\BCDems\\Results\\"


# This will process 2020 general election results and generate three CSV files:
# A comparison of Biden v. Shapiro results by precinct
# A comparison of Biden v. Lamb results by precinct
# A comparison of Dan Smit v. Metcalfe results by precinct
def process2020GeneralElectionResults(countyMap):
    # This will load in all of 2020's general election results
    generalElectionResults2020 = loadElectionData(baseDirectory, 'ReturnData\\2020\\ElectionReturns_2020_General_PrecinctReturns.csv')

    # Now we'll filter out only the Butler County results. Can put any county name in here
    butlerCountyGeneralElection2020 = filterResultsByCounty(generalElectionResults2020, localCountyMap, 'Butler')

    print("main(): Read in " + str(len(generalElectionResults2020)) + " election records")
    print("Received " + str(len(butlerCountyGeneralElection2020)) + " county-specific results")

    compareCandidatesSameYear('BIDEN', 'JOSEPH', 'SHAPIRO ', 'JOSHUA',
                              butlerCountyGeneralElection2020, baseDirectory, outputDirectory,
                              "BidenVShapiro2020General.csv")
    compareCandidatesSameYear('BIDEN', 'JOSEPH', 'LAMB', 'CONOR',
                              butlerCountyGeneralElection2020, baseDirectory, outputDirectory,
                              "BidenVLamb2020General.csv")
    compareCandidatesSameYear('SMITH', 'DANIEL', 'METCALFE', 'DARYL',
                              butlerCountyGeneralElection2020, baseDirectory, outputDirectory,
                              "SmithVMetcalfe2020General.csv")


# This will generate a CSV file with the following results, by precinct
#  - 2016 Dems Registered (Primary data only available)
#  - 2016 Dems Voted (Primary data only available)
#  - 2016 % Turnout
#  - 2016 Raw vote count
#  - 2020 Dems Registered (Based on general election registration data)
#  - 2020 Dems Registered (Based on general election registration data)
#  - 2020 % Turnout
#  - 2020 Raw vote count
#  - Delta in turnout
def processVoterTurnoutComparison2016v2020(countyMap):

    voterRegistration2016 = loadElectionData(baseDirectory,
                                             'ReturnsData\\2016\\VoterRegistration_2016_Primary_Precinct.csv')
    electionData2016 = loadElectionData(baseDirectory,
                                        'ReturnsData\\2016\\ElectionReturns_2016_General_PrecinctReturns.csv')
    voterRegistration2020 = loadElectionData(baseDirectory,
                                             'ReturnsData\\2020\\VoterRegistration_2020_General_Precinct.csv')
    electionData2020 = loadElectionData(baseDirectory,
                                        'ReturnsData\\2020\\ElectionReturns_2020_General_PrecinctReturns.csv')

    finalData = processVoterTurnoutComparison(voterRegistration2016, electionData2016, "2016",
                                              voterRegistration2020, electionData2020, "2020",
                                              countyMap)

    outputResultsToCSVFile(finalData, outputDirectory, "Turnout2016v2020.csv")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # This will load in a map that maps county names to county numbers - required to search for
    # county-specific election results
    localCountyMap = loadCountyMap(baseDirectory, 'CountyMap.csv')
    precinctMap = loadPrecinctMap(baseDirectory, 'VoterRolls\\Butler_Zone_Codes.csv')


    # process2020GeneralElectionResults(localCountyMap)
    # processVoterTurnoutComparison2016v2020(localCountyMap)

    # Test stuff for voter turnout calculations
    fileName2020 = 'VoteBuilderData\\DemTurnoutByYear2020.csv'
    fileName2016 = 'VoteBuilderData\\DemTurnoutByYear2016.csv'
    registeredFileName2020 = 'ReturnsData\\2020\\VoterRegistration_2020_General_Precinct.csv'
    registeredFileName2016 = 'ReturnsData\\2016\\VoterRegistration_2016_Primary_Precinct.csv'
    voterTurnout2020 = loadVoterTurnoutData(baseDirectory, fileName2020, 2020)
    voterTurnout2016 = loadVoterTurnoutData(baseDirectory, fileName2016, 2016)
    # Butler county is 10
    registeredDems2020 = loadVoterRegistrationData(baseDirectory, registeredFileName2020, 10)
    registeredDems2016 = loadVoterRegistrationData(baseDirectory, registeredFileName2016, 10)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
