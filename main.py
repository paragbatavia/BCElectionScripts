# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from butlerCountySpecific import *
from compareCandidates import *
from generalElectionDataUtilities import *
from fileUtilities import *

# general variables
baseDirectory = "C:\\Users\\parag\\Documents\\BCDems\\ElectionData\\"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # This will load in a map that maps county names to county numbers - required to search for
    # county-specific election results
    countyMap = loadCountyMap(baseDirectory, 'CountyMap.csv')
    # This will load in all of 2020's general election results
    generalElectionResults2020 = loadElectionData(baseDirectory, 'ElectionReturns_2020_General_PrecinctReturns.csv')

    # Now we'll filter out only the Butler County results. Can put any county name in here
    butlerCountyGeneralElection2020 = filterResultsByCounty(generalElectionResults2020, countyMap, 'Butler')

    print("main(): Read in " + str(len(generalElectionResults2020)) + " election records")
    print("Received " + str(len(butlerCountyGeneralElection2020)) + " county-specific results")

    compareCandidatesSameYear('BIDEN', 'JOSEPH', 'SHAPIRO ', 'JOSHUA',
                              butlerCountyGeneralElection2020, baseDirectory,
                              "BidenVShapiro2020General.csv")
    compareCandidatesSameYear('BIDEN', 'JOSEPH', 'LAMB', 'CONOR',
                              butlerCountyGeneralElection2020, baseDirectory,
                              "BidenVLamb2020General.csv")
    compareCandidatesSameYear('SMITH', 'DANIEL', 'METCALFE', 'DARYL',
                              butlerCountyGeneralElection2020, baseDirectory,
                              "SmithVMetcalfe2020General.csv")

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
