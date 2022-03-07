from generalElectionDataUtilities import *
from butlerCountySpecific import *
from fileUtilities import *


# This will compare general election performance of two candidates, and write the
# results out to a CSV file - sorted by precinct
def compareCandidatesSameYear(candidate1, first1, candidate2, first2, electionData, baseDirectory,
                              outputDirectory, outputFileName):

    # First, we take our entire general election data file, and pull out all data specific to
    # a single candidate
    candidate1Results = filterResultsByCandidateName(electionData, candidate1, first1)
    candidate2Results = filterResultsByCandidateName(electionData, candidate2, first2)

    c1PrecinctResults = getResultsByPrecinct(candidate1Results)
    c1PrecinctResultsCombined = combineButlerCongressionalDistrictData(c1PrecinctResults)
    # print(str(len(c1FilteredResults)))
    c2PrecinctResults = getResultsByPrecinct(candidate2Results)
    c2PrecinctResultsCombined = combineButlerCongressionalDistrictData(c2PrecinctResults)
    # print(str(len(c2FilteredResults)))

    combinedResults = combineResultsByPrecinct(c1PrecinctResultsCombined, candidate1,
                                               c2PrecinctResultsCombined, candidate2)

    outputResultsToCSVFile(combinedResults, outputDirectory, outputFileName)




