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
    # ------------------------------------------------------------------
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
