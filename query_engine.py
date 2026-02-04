"""
SPARQL Query Module
Handles intelligent querying of the RDF knowledge graph
"""

from rdflib import Namespace
from rdflib.plugins.sparql import prepareQuery


class SchemeQueryEngine:
    def __init__(self, graph):
        self.graph = graph
        self.SCHEME = Namespace("http://schemes.gov.in/ontology#")
    
    def search_schemes(self, state=None, occupation=None, category=None, age=None, gender=None, income=None):
        """
        Search for schemes based on user criteria
        Returns list of matching schemes with details
        """
        
        # Build dynamic SPARQL query based on provided filters
        query_parts = []
        filters = []
        
        # Base query structure
        query_parts.append("""
            PREFIX scheme: <http://schemes.gov.in/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            SELECT DISTINCT ?scheme ?name ?category ?state ?minAge ?maxAge ?gender ?income 
                            ?benefits ?documents ?process ?website
            WHERE {
                ?scheme a scheme:Scheme ;
                        scheme:schemeName ?name ;
                        scheme:hasCategory ?cat ;
                        scheme:applicableInState ?st ;
                        scheme:minAge ?minAge ;
                        scheme:maxAge ?maxAge ;
                        scheme:requiresGender ?gender ;
                        scheme:incomeLimit ?income ;
                        scheme:benefits ?benefits ;
                        scheme:documentsRequired ?documents ;
                        scheme:applicationProcess ?process ;
                        scheme:officialWebsite ?website .
                
                ?cat rdfs:label ?category .
                ?st rdfs:label ?state .
        """)
        
        # Add state filter
        if state and state != "All States":
            filters.append(f'?state = "{state}"')
        
        # Add category filter
        if category and category != "All":
            filters.append(f'?category = "{category}"')
        
        # Add occupation filter
        if occupation and occupation != "All":
            query_parts.append("""
                OPTIONAL {
                    ?scheme scheme:requiresOccupation ?occ .
                    ?occ rdfs:label ?occupation .
                }
            """)
            filters.append(f'(!BOUND(?occupation) || ?occupation = "{occupation}")')
        
        # Add age filter
        if age:
            try:
                age_int = int(age)
                filters.append(f'?minAge <= {age_int}')
                filters.append(f'?maxAge >= {age_int}')
            except ValueError:
                pass
        
        # Add gender filter
        if gender and gender != "All":
            filters.append(f'(?gender = "{gender}" || ?gender = "All")')
        
        # Add income filter
        if income:
            try:
                income_int = int(income)
                filters.append(f'(?income = 0 || ?income >= {income_int})')
            except ValueError:
                pass
        
        # Add filters to query
        if filters:
            query_parts.append("FILTER (" + " && ".join(filters) + ")")
        
        query_parts.append("} ORDER BY ?name")
        
        sparql_query = "\n".join(query_parts)
        
        # Execute query
        results = self.graph.query(sparql_query)
        
        # Format results
        schemes = []
        for row in results:
            scheme = {
                'uri': str(row.scheme),
                'name': str(row.name),
                'category': str(row.category),
                'state': str(row.state),
                'min_age': int(row.minAge),
                'max_age': int(row.maxAge),
                'gender': str(row.gender),
                'income_limit': int(row.income),
                'benefits': str(row.benefits),
                'documents': str(row.documents),
                'application_process': str(row.process),
                'website': str(row.website)
            }
            schemes.append(scheme)
        
        return schemes
    
    def get_all_categories(self):
        """Get list of all scheme categories"""
        query = """
            PREFIX scheme: <http://schemes.gov.in/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?category
            WHERE {
                ?cat a scheme:Category ;
                     rdfs:label ?category .
            }
            ORDER BY ?category
        """
        
        results = self.graph.query(query)
        return [str(row.category) for row in results]
    
    def get_all_states(self):
        """Get list of all states"""
        query = """
            PREFIX scheme: <http://schemes.gov.in/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?state
            WHERE {
                ?st a scheme:State ;
                    rdfs:label ?state .
            }
            ORDER BY ?state
        """
        
        results = self.graph.query(query)
        return [str(row.state) for row in results]
    
    def get_all_occupations(self):
        """Get list of all occupations"""
        query = """
            PREFIX scheme: <http://schemes.gov.in/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?occupation
            WHERE {
                ?occ a scheme:Occupation ;
                     rdfs:label ?occupation .
            }
            ORDER BY ?occupation
        """
        
        results = self.graph.query(query)
        occupations = [str(row.occupation) for row in results]
        return ['All'] + occupations
    
    def get_scheme_statistics(self):
        """Get statistics about schemes in the knowledge graph"""
        stats = {
            'total_schemes': 0,
            'categories': 0,
            'states': 0,
            'occupations': 0
        }
        
        # Total schemes
        query = """
            PREFIX scheme: <http://schemes.gov.in/ontology#>
            SELECT (COUNT(?scheme) as ?count)
            WHERE { ?scheme a scheme:Scheme . }
        """
        result = list(self.graph.query(query))
        if result:
            stats['total_schemes'] = int(result[0][0])
        
        stats['categories'] = len(self.get_all_categories())
        stats['states'] = len(self.get_all_states())
        stats['occupations'] = len(self.get_all_occupations()) - 1  # Exclude 'All'
        
        return stats
