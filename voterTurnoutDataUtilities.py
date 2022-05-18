# This file contains utility functions to read in voter turnout information
# This information is generated from votebuilder

import csv
import io
from dataTypes import *
from typing import *
from fileUtilities import *
from butlerCountySpecific import *


def compareYoYDemTurnout(baseDirectory: str, precinctMap: List[PrecinctMap]) -> List[TurnoutComparison]:
    """
    This function compares voter turnout over 2 years.
    TODO: Parameterize the years being compared instead of hardcoding them
    TODO: as 2016 and 2020.

    :param baseDirectory: Base directory where election data is held
    :param precinctMap: List of precincts
    :return: List of TurnoutComparison structures, ready for further analysis or written to file
    """

    # Test stuff for voter turnout calculations
    fileName2020 = 'VoteBuilderData\\DemTurnoutByYear2020.csv'
    fileName2016 = 'VoteBuilderData\\DemTurnoutByYear2016.csv'
    registeredFileName2020 = 'ReturnsData\\2020\\VoterRegistration_2020_General_Precinct.csv'
    registeredFileName2016 = 'ReturnsData\\2016\\VoterRegistration_2016_Primary_Precinct.csv'
    voterTurnout2020 = loadVoterTurnoutData(baseDirectory, fileName2020, 2020)
    voterTurnout2016 = loadVoterTurnoutData(baseDirectory, fileName2016, 2016)
    # Butler county is 10
    registeredDems2020 = loadVoterRegistrationData(baseDirectory, registeredFileName2020, 10)
    registeredDems2020 = combineButlerRegistrationData(registeredDems2020)
    registeredDems2016 = loadVoterRegistrationData(baseDirectory, registeredFileName2016, 10)
    registeredDems2016 = combineButlerRegistrationData(registeredDems2016)

    # ToDo: Iterate over every zone code in the precinct / zone map, and search both the
    # ToDo: registered voter maps and voter turnout maps for data for those zones. For
    # ToDo: any that have data in all four maps, create a TurnoutComparison type and add to a list
    # ToDo: After the basic data is added in, write a function to post process by calculating teh
    # ToDo: various percentage changes over time, etc.

    turnoutComparison = []
    for item in precinctMap:
        turnoutPrecinctCode = item['VoteBuilderPrecinctNumber']
        registeredPrecinctCode = item['RegisteredDataPrecinctNumber']
        print("Searching " + str(turnoutPrecinctCode) + " ," + str(registeredPrecinctCode))
        # Search 2016 data for voter turnout information
        turnout1 = next((x for x in voterTurnout2016 if x['PrecinctNumber'] == turnoutPrecinctCode), None)
        # Search 2020 data first for voter turnout information
        turnout2 = next((x for x in voterTurnout2020 if x['PrecinctNumber'] == turnoutPrecinctCode), None)
        # Search registered dems info for 2016 number of registered dems
        registered1 = next((x for x in registeredDems2016 if x['PrecinctNumber'] == registeredPrecinctCode), None)
        # Search registered dems info for 2020 number of registered dems
        registered2 = next((x for x in registeredDems2020 if x['PrecinctNumber'] == registeredPrecinctCode), None)
        # Now, assuming we got valid data for this precinct, add it to a new TurnoutComparison struct and add to a list
        if turnout1 and turnout2 and registered1 and registered2:
            # Calculate some basic statistics
            Y1DemTurnout = float(turnout1['DemTurnout'])
            Y2DemTurnout = float(turnout2['DemTurnout'])
            Y1RegisteredDems = float(registered1['RegisteredDems'])
            Y2RegisteredDems = float(registered2['RegisteredDems'])
            if Y1RegisteredDems > 0.01:
                Y1TurnoutPercentage = Y1DemTurnout / Y1RegisteredDems
                Y1Y2RegisteredPercentage = Y2RegisteredDems / Y1RegisteredDems
            else:
                Y1TurnoutPercentage = 0.0
                Y1Y2RegisteredPercentage = 0.0

            if Y2RegisteredDems > 0.01:
                Y2TurnoutPercentage = Y2DemTurnout / Y2RegisteredDems
            else:
                Y2TurnoutPercentage = 0.0

            if Y1DemTurnout > 0.01:
                Y1Y2TurnoutPercentage = Y2DemTurnout / Y1DemTurnout
            else:
                Y1Y2TurnoutPercentage = 0.0

            compare: TurnoutComparison = {'PrecinctCode': turnoutPrecinctCode,
                                          'PrecinctName': item['VoteBuilderPrecinctName'],
                                          'Y1Year': 2016, 'Y1DemsRegistered': registered1['RegisteredDems'],
                                          'Y1DemsVoted': turnout1['DemTurnout'],
                                          'Y1TurnoutPercentage': Y1TurnoutPercentage,
                                          'Y2Year': 2020, 'Y2DemsRegistered': registered2['RegisteredDems'],
                                          'Y2DemsVoted': turnout2['DemTurnout'],
                                          'Y2TurnoutPercentage': Y2TurnoutPercentage,
                                          'Y1Y2RegistrationChangePercentage': Y1Y2RegisteredPercentage,
                                          'Y1Y2TurnoutChangePercentage': Y1Y2TurnoutPercentage
                                          }
            turnoutComparison.append(compare)
        else:
            print("Didn't find all data for " + str(turnoutPrecinctCode) + " (" + item['VoteBuilderPrecinctName'] + ")")
            newstr = "Missing"
            if not turnout1:
                newstr += " Turnout2016"
            if not turnout2:
                newstr += " Turnout2020"
            if not registered1:
                newstr += " Returns2016"
            if not registered2:
                newstr += " Returns2020"
            print("   " + newstr)

    return turnoutComparison

