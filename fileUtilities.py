import csv


def loadCountyMap(baseDirectory, fileName):
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


def outputResultsToCSVFile(results, baseDirectory, fileName):
    # Writes the passed in list of dictionaries to a CSV file
    fullFileName = baseDirectory + fileName

    with open(fullFileName, 'w', newline='') as csvfile:
        fieldNames = results[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)

        writer.writeheader()
        for x in results:
            writer.writerow(x)

