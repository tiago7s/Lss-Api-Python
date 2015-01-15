__author__ = 'tiagosalvador'

from rdflib import Graph, RDF, URIRef, RDFS  # , Literal, BNode
from SPARQLWrapper import SPARQLWrapper, JSON


class ServiceSystem:
    'A API to a Service Systems'
    filename = ''
    g = Graph()

    def __init__(self, filename):
        ServiceSystem.filename = filename
        ServiceSystem.g.parse(filename, format='n3')

    # ------------------------------------------------------------------
    # ---------- Show information about the Service System -------------
    # ------------------------------------------------------------------
    def getServiceInformation(self):

        URIServiceSystem = URIRef("http://w3id.org/lss-usdl/v2#ServiceSystem")
        if ( None, RDF.type, URIServiceSystem ) in ServiceSystem.g:
            lss = ServiceSystem.g.value(predicate=RDF.type, object=URIServiceSystem, any=False)
            # print "Service System found! " + lss
        else:
            raise Exception("Cannot find Service System!!")

        if ( None, RDF.type, URIServiceSystem ) in ServiceSystem.g:
            lss_description = ServiceSystem.g.value(predicate=RDFS.comment, subject=lss, any=False)
            # print "Service System description found! " + lss_description
        else:
            raise Exception("Cannot find Service System description!!")

        # Can also be done this way
        # for lss in ServiceSystem.g.subjects(RDF.type, URIRef("http://w3id.org/lss-usdl/v2#ServiceSystem")):
        # print "Service System Name: ", lss.rsplit("#", 2)[1]
        # for lss_description in ServiceSystem.g.objects(lss, RDFS.comment):
        # print "Description:", lss_description

        information = []
        information.append(lss)
        information.append(lss_description)

        return information


    # ------------------------------------------------------------------
    # -------------- Get Interactions   --------------------------------
    # ------------------------------------------------------------------
    def getInteractions(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?a ?b
                WHERE {
                  ?a lss-usdl:hasInteraction ?b .
                }""")

        results = []
        for row in qres:
            s, r = row
            sl = s.rsplit("#", 2)[1]
            rl = r.rsplit("#", 2)[1]
            results.append(rl)
            # print sl, "hasInteraction", rl

        return results

    # Can also be done this way
    # print("")
    # print "--- Interaction Points: ---"
    # for sub, obj in ServiceSystem.g.subject_objects(URIRef("http://w3id.org/lss-usdl/v2#hasInteraction")):
    # interaction = obj.rsplit("#", 2)[1]
    # print interaction


    # ------------------------------------------------------------------
    # -------------- Connectors ----------------------------------------
    # ------------------------------------------------------------------
    def getConnectors(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?src ?tgt ?cond
                WHERE {
                  ?ss lss-usdl:hasControlFlow ?cf.
                  ?cf lss-usdl:hasSource ?src  .
                  ?cf lss-usdl:hasTarget ?tgt .
                  ?cf lss-usdl:hasCondition ?cond .
                }""")

        results = []
        for row in qres:
            src, tgt, cond = row
            source = src.rsplit("#", 2)[1]
            target = tgt.rsplit("#", 2)[1]
            condition = cond
            results.append([source, target, condition])
            # str = 'ControlFlow (' + source + ' -> ' + target + ') with condition "' + condition + '"'''
            # print str

        return results


    # ------------------------------------------------------------------
    # -------------- Get Service Roles ---------------------------------
    #------------------------------------------------------------------
    def getRoles(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?role
                WHERE {
                  ?s ?prop ?o .
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:performedBy ?role .
                }""")

        results = []
        for row in qres:
            r = getattr(row, "role")
            role = r.rsplit("#", 2)[1]
            results.append(role)

        return results


    #------------------------------------------------------------------
    #-------------- Interactions done by Role -------------------------
    #------------------------------------------------------------------
    def getInterationsByRole(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?lss ?int ?role
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:performedBy ?role .
                }""")

        results = []
        for row in qres:
            s, i, r = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]
            role = r.rsplit("#", 2)[1]
            results.append([interaction, role])

        return results


    #------------------------------------------------------------------
    #-------------- Interactions that receive and returns Resources ---
    #------------------------------------------------------------------
    def getInteractionResources(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?lss ?int ?resource
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:receivesResource ?resource .
                  ?int lss-usdl:returnsResource ?resource .
                }""")

        results = []
        for row in qres:
            s, i, r = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource])

        return results

    #------------------------------------------------------------------
    #-------------- Interactions that only receive Resources: ---------
    #------------------------------------------------------------------
    def getInteractionResourcesReceived(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?lss ?int ?role
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:receivesResource ?role .
                }""")

        results = []
        for row in qres:
            s, i, r = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource])

        return results


    #------------------------------------------------------------------
    #-------------- Print first interaction: --------------------------
    #------------------------------------------------------------------
    # Look for an interaction which is a source but not the target of any connector
    #
    def getFirstInteraction(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl: <http://w3id.org/lss-usdl/v2#>
               PREFIX time: <http://www.w3.org/2006/time/>
                SELECT DISTINCT ?lss ?tgt
                WHERE {
                  ?lss lss-usdl:hasControlFlow ?cf.
                  ?cf lss-usdl:hasSource ?src  .
                  ?cf lss-usdl:hasTarget ?tgt .
                  MINUS {?temp lss-usdl:hasTarget ?src .}
                }""")

        interaction = ''
        for row in qres:
            s, i = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]

        return interaction


    #------------------------------------------------------------------
    #-------------- get last interaction(s) -------------------------
    #------------------------------------------------------------------
    # Look for an interaction which is a target but not the source of any connector
    #
    def getLastInteraction(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl: <http://w3id.org/lss-usdl/v2#>
               PREFIX time: <http://www.w3.org/2006/time/>
                SELECT DISTINCT ?lss ?tgt
                WHERE {
                  ?lss lss-usdl:hasControlFlow ?cf.
                  ?cf lss-usdl:hasSource ?src  .
                  ?cf lss-usdl:hasTarget ?tgt .
                  MINUS {?temp lss-usdl:hasSource ?tgt .}
                }""")

        interaction = ''
        for row in qres:
            s, i = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]

        return interaction


    #------------------------------------------------------------------
    #-------------- get DBpedia Resources -----------------------------
    #------------------------------------------------------------------
    def getDBPediaResources(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl: <http://w3id.org/lss-usdl/v2#>
               PREFIX dbpedia: <http://dbpedia.org/>
                SELECT DISTINCT ?int ?res ?dbres
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:createsResource ?res .
                  ?res a ?dbres .
                }""")

        results = []
        for row in qres:
            i, r, dbr = row
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource, dbr])

        return results

    #------------------------------------------------------------------
    #-------------- get Abstract for DBpedia Resource -----------------
    #------------------------------------------------------------------
    def getDBPediaAbstract(self, resource):

        #              ?dbres <http://dbpedia.org/ontology/abstract> ?abs .
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        qs = """SELECT DISTINCT ?abs
             WHERE {
             <"""
        qe = """> dbpedia-owl:abstract ?abs .
              FILTER(langMatches(lang(?abs), "EN"))
             }"""

        q = qs + resource + qe
        sparql.setQuery(q)
        sparql.setReturnFormat(JSON)
        sparqlresults = sparql.query().convert()

        results = []
        for sparqlresult in sparqlresults["results"]["bindings"]:
            str = sparqlresult["abs"]["value"] + ''
            results.append(str)

        return results


    def getLocationsArray(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?location ?label
                WHERE {
                  ?location a lss-usdl:Location .
                  ?location rdfs:label ?label .
                }""")

        results = []
        for row in qres:
            r, label = row
            location = r.rsplit("#", 2)[1]
            results.append([location, label])

        return results

    def getGoalsArray(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?goal ?label ?comment ?int
                WHERE {
                  ?goal a lss-usdl:Goal .
                  ?goal rdfs:label ?label .
                  ?goal rdfs:comment ?comment .
                  ?service lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:hasGoal ?goal
                }""")

        results = []
        for row in qres:
            r, label, comment, inte = row
            goal = r.rsplit("#", 2)[1]
            interaction = inte.rsplit("#", 2)[1]
            results.append([goal, label, comment, interaction])

        return results

    def getRolesArray(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?role ?label ?comment ?bi ?type
                WHERE {
                  ?service lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:performedBy ?role .
                  ?role rdfs:label ?label .
                  ?role rdfs:comment ?comment .
                  ?role lss-usdl:belongsToBusinessEntity ?bi .
                  ?role a ?type
                }""")

        results = []
        for row in qres:
            r, label, comment, bi, tp = row
            role = r.rsplit("#", 2)[1]
            businessEntity = bi.rsplit("#", 2)[1]
            type = tp.rsplit("#", 2)[1]
            results.append([role, label, comment, businessEntity, type])

        return results

    def getResourcesArray(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?resource ?label ?comment ?type
                WHERE {
                  ?service lss-usdl:hasInteraction ?int .
                  {?int lss-usdl:receivesResource ?resource} UNION
                  {?int lss-usdl:consumesResource ?resource} UNION
                  {?int lss-usdl:createsResource ?resource} UNION
                  {?int lss-usdl:returnsResource ?resource} .
                  OPTIONAL {?resource rdfs:label ?label} .
                  OPTIONAL {?resource rdfs:comment ?comment} .
                  OPTIONAL {?resource a ?type }.
                }""")

        results = []
        for row in qres:
            r, label, comment, type = row
            resource = r.rsplit("#", 2)[1]
            results.append([resource, label, comment, type])

        return results

    def getTimesArray(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX time: <http://www.w3.org/2006/time#>
                SELECT DISTINCT ?time ?label ?comment ?intAfter ?intBefore ?intEquals
                WHERE {
                  {?time a time:TemporalEntity} UNION
                  {?time a time:ProperInterval .
                  {?time time:intervalAfter ?intAfter} UNION
                  {?time time:intervalBefore ?intBefore} UNION
                  {?time time:intervalEquals ?intEquals} . } .
                  OPTIONAL {?time rdfs:label ?label} .
                  OPTIONAL {?time rdfs:comment ?comment} .
                }""")

        results = []
        for row in qres:
            t, label, comment, intAfter, intBefore, intEquals = row
            time = t.rsplit("#", 2)[1]
            intervalAfter = "none"
            if intAfter is not None:
                intervalAfter = intAfter.rsplit("#", 2)[1]

            intervalBefore = "none"
            if intBefore is not None:
                intervalBefore = intBefore.rsplit("#", 2)[1]

            intervalEquals = "none"
            if intEquals is not None:
                intervalEquals = intEquals.rsplit("#", 2)[1]
            results.append([time, label, comment, intervalAfter, intervalBefore, intervalEquals])

        return results

    def getProcessesArray(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?process ?label ?comment ?type
                WHERE {
                  ?service lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:belongsToProcess ?process .
                  ?process rdfs:label ?label .
                  ?process rdfs:comment ?comment .
                  ?process a ?type .
                }""")

        results = []
        for row in qres:
            p, label, comment, type = row
            process = p.rsplit("#", 2)[1]
            results.append([process, label, comment, type])

        return results

    def getInteractionsArray(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?int ?label ?comment ?type
                WHERE {
                  ?service lss-usdl:hasInteraction ?int .
                  ?int rdfs:label ?label .
                  ?int rdfs:comment ?comment .
                  ?int a ?type .
                }""")

        results = []
        for row in qres:
            i, label, comment, type = row
            interaction = i.rsplit("#", 2)[1]
            results.append([interaction, label, comment, type])

        return results

# ------------------------------------------------------------------
# -------------- parse command line  -------------------------------
# ------------------------------------------------------------------

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

