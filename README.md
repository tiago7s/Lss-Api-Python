# Lss-Api-Python
A python api with functions for calculating the maturity and compliance of a service system based on ITIL.

This was done for a Master's Degree class and it has the objective of calculating the maturity and compliance of a service system modeled in RDF. It uses SPARQL queries along with the rdflib to get Interactions, Roles, Resources and other entities of the modeled system. With this information it is possible to calculate the maturity and compliance of the modeled service compared to already existing ITIL Processes.

Quick Testing of the Model

      Install Python and the RDF parser
      If the operating system is Linux or Mac OS X, probably it already has Python 2.6.
      If not, there are the websites for the download and installation:
      
      http://code.google.com/p/winpython/
      http://www.python.org/getit/ http://wiki.python.org/moin/BeginnersGuide/Download

Install RDF Api

      RdfLib: https://github.com/RDFLib
        1. Download https://raw.github.com/pypa/pip/master/contrib/get-pip.py
        2. run python get-pip.py
        3. run pip install rdflib
