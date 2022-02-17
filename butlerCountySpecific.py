# This contains functions specific only to Butler County data. It's in a separate file
# for when we ultimately use this for other counties.
import copy


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
