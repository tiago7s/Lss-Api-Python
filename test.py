__author__ = 'tiagosalvador'

# ------------------------------------------------------------------
# -------------- parse command line  -------------------------------
# ------------------------------------------------------------------
from api.LSS_USDL_API_Extended import ServiceSystem

if __name__ == "__main__":

    """inputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hf:",["file="])
    except getopt.GetoptError:
        print 'LSS-USDL_API.py -f <service_system_file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'LSS-USDL_API.py -f <service_system_file>'
            sys.exit()
        elif opt in ("-f", "--file"):
            inputfile = arg"""

    listOfFiles = [
        "../../../../Users/tiagosalvador/Documents/University/GSI_Project_TiagoSalvador"
        + "/TurtleServices/ITIL_Service_Catalogue_service.ttl"]

    for inputfile in listOfFiles:

        dataExtracted = "\n"

        dataExtracted += 'Input file is: ' + inputfile
        dataExtracted += "\n"

        ss = ServiceSystem("file:" + inputfile)
        results = ss.getServiceInformation()
        dataExtracted += "Service System name: " + results[0].rsplit("#", 2)[1]
        dataExtracted += "Service System desc: " + results[1]
        dataExtracted += "\n"

        print "Getting information..."

        """results = ss.getInteractions()
        for interation in results:
            dataExtracted += "Interaction: " + interation
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getConnectors()
        for result in results:
            dataExtracted += 'getConnectors: (' + result[0] + ' -> ' + result[1] + ') with condition "' + result[2] + '"'''
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getRoles()
        for role in results:
            dataExtracted += "getRoles: " + role
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getInterationsByRole()
        for result in results:
            dataExtracted += 'getInterationsByRole: ' + result[0] + ' with role ' + result[1]
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getInteractionResources()
        for result in results:
            dataExtracted += 'getInteractionResources: ' + result[0] + ' with resource ' + result[1]
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getInteractionResourcesReceived()
        for result in results:
            dataExtracted += 'getInteractionResourcesReceived: ' + result[0] + ' with resource ' + result[1]
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getFirstInteraction()
        if results:
            dataExtracted += 'getFirstInteraction: ' + results
            dataExtracted += "\n"
            dataExtracted += "\n"

        results = ss.getLastInteraction()
        if results:
            dataExtracted += 'getLastInteraction: ' + results
            dataExtracted += "\n"
            dataExtracted += "\n"

        results = ss.getDBPediaResources()
        for result in results:
            dataExtracted += 'getDBPediaResources: ' + result[0] + ' with resource ' + result[1] + ' -> ' + result[2]
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getDBPediaResources()
        for result in results:
            dbpediaAbstracts = ss.getDBPediaAbstract(result[2])
            for dbpediaAbstract in dbpediaAbstracts:
                dataExtracted += 'getDBPediaAbstract: ' + result[2] + ': ' +  dbpediaAbstract
                dataExtracted += "\n"
                dataExtracted += "\n"
        dataExtracted += "\n" """

        results = ss.getLocationsArray()
        dataExtracted += "\n==================\ngetLocationsArray:\n"
        for location in results:
            dataExtracted += "location: " + location[0] + "\n\t --> label: " + location[1]
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getGoalsArray()
        dataExtracted += "\n==================\ngetGoalsArray:\n"
        for goal in results:
            dataExtracted += "goal: " + goal[0] + "\n\t --> label: " + goal[1] + "\n\t ; comment: " + goal[
                2] + "\n\t ; interaction that has this goal: " + goal[3]
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getRolesArray()
        dataExtracted += "\n==================\ngetRolesArray:\n"
        for role in results:
            dataExtracted += "role: " + role[0] + "\n\t --> label: " + role[1] + "\n\t ; comment: " + role[
                2] + "\n\t ; business entity: " + role[3] + "\n\t ; role type: " + role[4]
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getResourcesArray()
        dataExtracted += "\n==================\ngetResourcesArray:\n"
        for resource in results:
            dataExtracted += "resource: " + resource[0] + "\n\t --> label: " + unicode(resource[
                1]) + "\n\t ; comment: " + unicode(resource[2]) + "\n\t ; asset type: " + unicode(resource[3])
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getTimesArray()
        dataExtracted += "\n==================\ngetTimesArray:\n"
        for time in results:
            dataExtracted += "time: " + time[0] + "\n\t --> label: " + unicode(time[
                1]) + "\n\t ; comment: " + unicode(time[2]) + "\n\t ; interval after: " + unicode(
                time[3]) + "\n\t ; interval before: " + unicode(time[4]) + "\n\t ; interval equals: " + unicode(
                time[5])
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getProcessesArray()
        dataExtracted += "\n==================\ngetProcessesArray:\n"
        for process in results:
            dataExtracted += "process: " + process[0] + "\n\t --> label: " + process[1] + "\n\t ; comment: " + process[
                2] + "\n\t ; type of process: " + process[3]
            dataExtracted += "\n"
        dataExtracted += "\n"

        results = ss.getInteractionsArray()
        dataExtracted += "\n==================\ngetProcessesArray:\n"
        for interaction in results:
            dataExtracted += "interaction: " + interaction[0] + "\n\t --> label: " + interaction[
                1] + "\n\t ; comment: " + interaction[2] + "\n\t ; type of interaction: " + interaction[3]
            dataExtracted += "\n"
        dataExtracted += "\n"

        print dataExtracted

        fileName = inputfile + "_Results.txt"
        textFile = open(fileName, "w")

        dataExtracted = dataExtracted.encode('utf-8')
        textFile.write(dataExtracted)
        textFile.close()

        print ("Data extracted saved to file " + fileName + "\n")

