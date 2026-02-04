"""
Ontology Builder Module
Converts government schemes CSV data into RDF knowledge graph
"""

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import csv
import os


class SchemeOntologyBuilder:
    def __init__(self):
        self.graph = Graph()
        
        # Define custom namespace for our ontology
        self.SCHEME = Namespace("http://schemes.gov.in/ontology#")
        self.graph.bind("scheme", self.SCHEME)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        
        # Build ontology classes and properties
        self._build_ontology_structure()
    
    def _build_ontology_structure(self):
        """Define the ontology classes and properties"""
        
        # Define Classes
        self.graph.add((self.SCHEME.Scheme, RDF.type, RDFS.Class))
        self.graph.add((self.SCHEME.Category, RDF.type, RDFS.Class))
        self.graph.add((self.SCHEME.State, RDF.type, RDFS.Class))
        self.graph.add((self.SCHEME.Occupation, RDF.type, RDFS.Class))
        
        # Define Object Properties
        properties = [
            'hasCategory', 'applicableInState', 'requiresOccupation',
            'requiresGender', 'hasDocument', 'hasBenefit'
        ]
        
        for prop in properties:
            self.graph.add((self.SCHEME[prop], RDF.type, RDF.Property))
        
        # Define Data Properties
        data_properties = [
            'schemeName', 'schemeId', 'minAge', 'maxAge', 'incomeLimit',
            'benefits', 'documentsRequired', 'applicationProcess', 'officialWebsite'
        ]
        
        for prop in data_properties:
            self.graph.add((self.SCHEME[prop], RDF.type, RDF.Property))
    
    def load_schemes_from_csv(self, csv_file):
        """Load schemes from CSV and convert to RDF triples"""
        
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                self._add_scheme_to_graph(row)
        
        print(f"Successfully loaded {len(list(self.graph.subjects(RDF.type, self.SCHEME.Scheme)))} schemes into knowledge graph")
    
    def _add_scheme_to_graph(self, scheme_data):
        """Add a single scheme as RDF triples"""
        
        scheme_id = scheme_data['scheme_id']
        scheme_uri = self.SCHEME[f"scheme_{scheme_id}"]
        
        # Add scheme as instance of Scheme class
        self.graph.add((scheme_uri, RDF.type, self.SCHEME.Scheme))
        
        # Add basic properties
        self.graph.add((scheme_uri, self.SCHEME.schemeId, Literal(scheme_id, datatype=XSD.integer)))
        self.graph.add((scheme_uri, self.SCHEME.schemeName, Literal(scheme_data['scheme_name'])))
        
        # Add category
        category_uri = self.SCHEME[f"category_{scheme_data['category'].replace(' ', '_')}"]
        self.graph.add((category_uri, RDF.type, self.SCHEME.Category))
        self.graph.add((category_uri, RDFS.label, Literal(scheme_data['category'])))
        self.graph.add((scheme_uri, self.SCHEME.hasCategory, category_uri))
        
        # Add state
        state_uri = self.SCHEME[f"state_{scheme_data['state'].replace(' ', '_')}"]
        self.graph.add((state_uri, RDF.type, self.SCHEME.State))
        self.graph.add((state_uri, RDFS.label, Literal(scheme_data['state'])))
        self.graph.add((scheme_uri, self.SCHEME.applicableInState, state_uri))
        
        # Add age criteria
        self.graph.add((scheme_uri, self.SCHEME.minAge, Literal(int(scheme_data['min_age']), datatype=XSD.integer)))
        self.graph.add((scheme_uri, self.SCHEME.maxAge, Literal(int(scheme_data['max_age']), datatype=XSD.integer)))
        
        # Add occupation
        if scheme_data['occupation'] and scheme_data['occupation'] != 'All':
            occupation_uri = self.SCHEME[f"occupation_{scheme_data['occupation'].replace(' ', '_')}"]
            self.graph.add((occupation_uri, RDF.type, self.SCHEME.Occupation))
            self.graph.add((occupation_uri, RDFS.label, Literal(scheme_data['occupation'])))
            self.graph.add((scheme_uri, self.SCHEME.requiresOccupation, occupation_uri))
        
        # Add gender
        self.graph.add((scheme_uri, self.SCHEME.requiresGender, Literal(scheme_data['gender'])))
        
        # Add income limit
        self.graph.add((scheme_uri, self.SCHEME.incomeLimit, Literal(int(scheme_data['income_limit']), datatype=XSD.integer)))
        
        # Add benefits
        self.graph.add((scheme_uri, self.SCHEME.benefits, Literal(scheme_data['benefits'])))
        
        # Add documents
        self.graph.add((scheme_uri, self.SCHEME.documentsRequired, Literal(scheme_data['documents_required'])))
        
        # Add application process
        self.graph.add((scheme_uri, self.SCHEME.applicationProcess, Literal(scheme_data['application_process'])))
        
        # Add official website
        self.graph.add((scheme_uri, self.SCHEME.officialWebsite, Literal(scheme_data['official_website'])))
    
    def save_graph(self, output_file, format='turtle'):
        """Save the RDF graph to a file"""
        self.graph.serialize(destination=output_file, format=format)
        print(f"RDF graph saved to {output_file}")
    
    def get_graph(self):
        """Return the RDF graph"""
        return self.graph


if __name__ == "__main__":
    # Test the ontology builder
    builder = SchemeOntologyBuilder()
    builder.load_schemes_from_csv('data/schemes.csv')
    builder.save_graph('data/schemes.ttl', format='turtle')
    print(f"Total triples in graph: {len(builder.get_graph())}")
