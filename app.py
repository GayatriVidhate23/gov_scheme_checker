"""
Flask Application for Smart Government Scheme Checker
Main application file
"""

from flask import Flask, render_template, request, jsonify
from rdflib import Graph
import os
from ontology_builder import SchemeOntologyBuilder
from query_engine import SchemeQueryEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smart-scheme-checker-2025'

# Global variables for graph and query engine
graph = None
query_engine = None


def initialize_knowledge_graph():
    """Initialize the RDF knowledge graph"""
    global graph, query_engine
    
    csv_file = 'data/schemes.csv'
    ttl_file = 'data/schemes.ttl'
    
    # Check if RDF file exists, otherwise build it from CSV
    if not os.path.exists(ttl_file):
        print("Building knowledge graph from CSV...")
        builder = SchemeOntologyBuilder()
        builder.load_schemes_from_csv(csv_file)
        builder.save_graph(ttl_file)
        graph = builder.get_graph()
    else:
        print("Loading existing knowledge graph...")
        graph = Graph()
        graph.parse(ttl_file, format='turtle')
    
    # Initialize query engine
    query_engine = SchemeQueryEngine(graph)
    print(f"Knowledge graph initialized with {len(graph)} triples")


@app.route('/')
def index():
    """Home page"""
    if query_engine:
        stats = query_engine.get_scheme_statistics()
    else:
        stats = {'total_schemes': 0, 'categories': 0, 'states': 0, 'occupations': 0}
    
    return render_template('index.html', stats=stats)


@app.route('/search')
def search():
    """Search page"""
    if not query_engine:
        return "Error: Knowledge graph not initialized", 500
    
    # Get filter options
    states = query_engine.get_all_states()
    categories = ['All'] + query_engine.get_all_categories()
    occupations = query_engine.get_all_occupations()
    
    return render_template('search.html', 
                         states=states,
                         categories=categories,
                         occupations=occupations)


@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for scheme search"""
    if not query_engine:
        return jsonify({'error': 'Knowledge graph not initialized'}), 500
    
    # Get search parameters
    data = request.get_json()
    state = data.get('state')
    occupation = data.get('occupation')
    category = data.get('category')
    age = data.get('age')
    gender = data.get('gender')
    income = data.get('income')
    
    # Execute search
    results = query_engine.search_schemes(
        state=state,
        occupation=occupation,
        category=category,
        age=age,
        gender=gender,
        income=income
    )
    
    return jsonify({
        'success': True,
        'count': len(results),
        'schemes': results
    })


@app.route('/scheme/<scheme_id>')
def scheme_detail(scheme_id):
    """Scheme detail page"""
    return render_template('scheme_detail.html', scheme_id=scheme_id)


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    if not query_engine:
        return jsonify({'error': 'Knowledge graph not initialized'}), 500
    
    stats = query_engine.get_scheme_statistics()
    return jsonify(stats)


@app.route('/rebuild-graph', methods=['POST'])
def rebuild_graph():
    """Rebuild the knowledge graph from CSV (admin function)"""
    try:
        csv_file = 'data/schemes.csv'
        ttl_file = 'data/schemes.ttl'
        
        builder = SchemeOntologyBuilder()
        builder.load_schemes_from_csv(csv_file)
        builder.save_graph(ttl_file)
        
        # Reinitialize
        initialize_knowledge_graph()
        
        return jsonify({'success': True, 'message': 'Knowledge graph rebuilt successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    # Initialize knowledge graph on startup
    initialize_knowledge_graph()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
