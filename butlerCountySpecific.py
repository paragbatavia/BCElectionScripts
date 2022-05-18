# This contains functions specific only to Butler County data. It's in a separate file
# for when we ultimately use this for other counties.
import copy
from typing import *
from dataTypes import *


# This function combines vote totals for specific precincts that are split between two
# congressional districts. For Butler County, that means:
# Cranberry East 2 (C16 and C17)
# Cranberry East 3 (C16 and C17)
# Cranberry West 1 (C16 and C17)
# Cranberry West 2 (C16 and C17)
# Jefferson 1 (C15 and C16)
# Jefferson 2 (C15 and C16)
#
# IMPORTANT: This function only works if the election data that is passed in is
# only contains data for a single precinct - do not use this on an aggregate
# imported CSV election data file. Run getResultsByPrecinct() first!

def combineButlerCongressionalDistrictDataByName(electionData, inputName1, inputName2, outputName, newPrecinctCode):
    CE2_C16 = next((item for item in electionData if item['MunicipalityName'] == inputName1),
                   None)
    CE2_C17 = next((item for item in electionData if item['MunicipalityName'] == inputName2),
                   None)
    # We have three different possibilities here - both Cong districts exist in the data, or only one of the two
    # exist in the data. We need to handle each of these cases. In the case where both exist, we add votes
    # and rename. In the case where only one exists, we don't need to add votes - we just copy, rename the
    # district, and update the (false) precinct code.
    if CE2_C16 and CE2_C17:
        # The data exists, so we need to combined them
        # print(CE2_C16)
        # print(CE2_C17)
        CE2_C16_Vote = int(CE2_C16['VoteTotal'])
        CE2_C17_Vote = int(CE2_C17['VoteTotal'])
        CE2 = copy.deepcopy(CE2_C16)
        # Need to manually update a few fields now
        CE2['VoteTotal'] = CE2_C16_Vote + CE2_C17_Vote
        CE2['PrecinctCode'] = str(newPrecinctCode)
        CE2['MunicipalityName'] = outputName
        # print(CE2)
        # Now we need to delete both elements from the list - lambda might be a better way - but I
        # want to do this in place
        for i in range(len(electionData)):
            if electionData[i]['MunicipalityName'] == inputName1:
                del electionData[i]
                break
        for i in range(len(electionData)):
            if electionData[i]['MunicipalityName'] == inputName2:
                del electionData[i]
                break
        electionData.append(CE2)
        # print("\n\n******")
        # print(electionData)
    elif CE2_C16:
        # We may need to also delete the original dictionary item - but should be fine if we don't. Same below.
        CE2 = copy.deepcopy(CE2_C16)
        CE2['MunicipalityName'] = outputName
        CE2['PrecinctCode'] = str(newPrecinctCode)
        electionData.append(CE2)
    elif CE2_C17:
        CE2 = copy.deepcopy(CE2_C17)
        CE2['MunicipalityName'] = outputName
        CE2['PrecinctCode'] = str(newPrecinctCode)
        electionData.append(CE2)

    return electionData


def combineButlerCongressionalDistrictData(electionData):
    electionData = combineButlerCongressionalDistrictDataByName(electionData, "CRANBERRY X EAST X 2 (Cong 16)",
                                                                "CRANBERRY X EAST X 2 (Cong 17)",
                                                                "CRANBERRY X EAST X 2", 8000)

    electionData = combineButlerCongressionalDistrictDataByName(electionData, "CRANBERRY X EAST X 3 (Cong 16)",
                                                                "CRANBERRY X EAST X 3 (Cong 17)",
                                                                "CRANBERRY X EAST X 3", 8001)

    electionData = combineButlerCongressionalDistrictDataByName(electionData, "CRANBERRY X WEST X 1 (Cong 16)",
                                                                "CRANBERRY X WEST X 1 (Cong 17)",
                                                                "CRANBERRY X WEST X 1", 8002)

    electionData = combineButlerCongressionalDistrictDataByName(electionData, "CRANBERRY X WEST X 2 (Cong 16)",
                                                                "CRANBERRY X WEST X 2 (Cong 17)",
                                                                "CRANBERRY X WEST X 2", 8003)

    electionData = combineButlerCongressionalDistrictDataByName(electionData, "JEFFERSON X I (Cong 15)",
                                                                "JEFFERSON X I (Cong 16)",
                                                                "JEFFERSON X I", 8004)

    electionData = combineButlerCongressionalDistrictDataByName(electionData, "JEFFERSON X II (Cong 15)",
                                                                "JEFFERSON X II (Cong 16)",
                                                                "JEFFERSON X II", 8005)

    return electionData


def combineButlerVoterRegistrationDataByPrecinctCodes(registrationData: List[RegisteredVoterData],
                                                      precinct1: int, precinct2: int,
                                                      outputPrecinct: int) -> List[RegisteredVoterData]:
    """
    Voter Registration data from the DoS is split by congressional district in some cases. The data
    from other sources, like VoteBuilder for turnout data, isn't. So, we need to combine the
    congressional district registration totals into one.

    :param registrationData:
    :param precinct1:
    :param precinct2:
    :param outputPrecinct:
    :return:
    """

    # search registration data for precinct 1 and remove from list
    regTotal1 = regTotal2 = 0
    precinct1Name = "a"
    precinct2Name = "b"
    year = 0

    for i in range(len(registrationData)):
        if int(registrationData[i]['PrecinctNumber']) == precinct1:
            print("Found precinct1")
            regTotal1 = registrationData[i]['RegisteredDems']
            precinct1Name = registrationData[i]['PrecinctName']
            year = registrationData[i]['Year']
            del registrationData[i]
            break

    # search registration data for precinct 2 and remove from list
    for i in range(len(registrationData)):
        if int(registrationData[i]['PrecinctNumber']) == precinct2:
            regTotal2 = registrationData[i]['RegisteredDems']
            precinct2Name = registrationData[i]['PrecinctName']
            del registrationData[i]
            break

    # add up the registered voters number
    regTotal = int(regTotal1) + int(regTotal2)
    entry: RegisteredVoterData = {'PrecinctNumber': outputPrecinct,
                                  'PrecinctName': precinct1Name,
                                  'Year': year,
                                  'RegisteredDems': regTotal}

    # Add a new entry for this, using outputPrecinct number
    registrationData.append(entry)

    return registrationData


def combineButlerRegistrationData(registrationData: List[RegisteredVoterData]) -> List[RegisteredVoterData]:
    """
    This combines voter registration data from Cranberry Twp and Jefferson
    precincts which are split into different congressional districts in
    DoS data.

    :param registrationData:
    :return:
    """

    # Cranberry Twp
    registrationData = combineButlerVoterRegistrationDataByPrecinctCodes(registrationData, 370, 371, 370)
    registrationData = combineButlerVoterRegistrationDataByPrecinctCodes(registrationData, 375, 376, 375)
    registrationData = combineButlerVoterRegistrationDataByPrecinctCodes(registrationData, 380, 381, 380)
    registrationData = combineButlerVoterRegistrationDataByPrecinctCodes(registrationData, 410, 411, 410)

    # Jefferson
    registrationData = combineButlerVoterRegistrationDataByPrecinctCodes(registrationData, 544, 545, 544)
    registrationData = combineButlerVoterRegistrationDataByPrecinctCodes(registrationData, 554, 555, 554)

    return registrationData


