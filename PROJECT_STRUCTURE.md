# Project Structure

```
scheme_checker/
│
├── 📄 app.py                          # Main Flask application (Entry Point)
│   ├── Initializes RDF knowledge graph
│   ├── Defines web routes
│   ├── Handles API endpoints
│   └── Runs Flask server on port 5000
│
├── 📄 ontology_builder.py             # RDF Knowledge Graph Builder
│   ├── Defines ontology structure (classes & properties)
│   ├── Converts CSV data to RDF triples
│   ├── Creates semantic relationships
│   └── Saves graph in Turtle format
│
├── 📄 query_engine.py                 # SPARQL Query Engine
│   ├── Builds dynamic SPARQL queries
│   ├── Executes queries on RDF graph
│   ├── Filters schemes by criteria
│   └── Returns formatted results
│
├── 📄 demo.py                         # Demonstration Script
│   ├── Shows ontology structure
│   ├── Displays sample RDF triples
│   ├── Example SPARQL queries
│   └── Explains workflow
│
├── 📄 requirements.txt                # Python Dependencies
│   ├── Flask==3.0.0
│   └── rdflib==7.0.0
│
├── 📄 README.md                       # Complete Documentation
│
├── 📁 data/                           # Data Directory
│   ├── schemes.csv                    # Source data (20 government schemes)
│   └── schemes.ttl                    # Generated RDF graph (auto-created)
│
├── 📁 templates/                      # HTML Templates
│   ├── base.html                      # Base template with navbar & footer
│   ├── index.html                     # Home page with features
│   ├── search.html                    # Search interface with filters
│   └── about.html                     # About page with tech details
│
└── 📁 static/                         # Static Assets
    └── css/
        └── style.css                  # Complete styling (responsive)
```

## Component Descriptions

### Core Application (app.py)
- **Purpose**: Main Flask application entry point
- **Key Functions**:
  - `initialize_knowledge_graph()`: Loads or builds RDF graph
  - `index()`: Renders home page with statistics
  - `search()`: Renders search interface
  - `api_search()`: API endpoint for scheme search
  - `rebuild_graph()`: Rebuild RDF graph from CSV

### Ontology Builder (ontology_builder.py)
- **Purpose**: Converts structured data to semantic representation
- **Key Components**:
  - `SchemeOntologyBuilder` class
  - Ontology structure definition
  - CSV to RDF conversion
  - Triple generation for schemes

### Query Engine (query_engine.py)
- **Purpose**: Intelligent scheme retrieval using SPARQL
- **Key Components**:
  - `SchemeQueryEngine` class
  - Dynamic SPARQL query construction
  - Filter application (state, occupation, age, etc.)
  - Result formatting

### Templates
1. **base.html**: Navigation, footer, common layout
2. **index.html**: Landing page, features, statistics
3. **search.html**: Interactive search form, results display
4. **about.html**: Project documentation, workflow

### Styling (style.css)
- Modern, responsive design
- CSS Grid and Flexbox layouts
- Color scheme with CSS variables
- Mobile-first responsive design
- Interactive elements with transitions

## Data Flow

```
CSV Data (schemes.csv)
    ↓
Ontology Builder (ontology_builder.py)
    ↓
RDF Knowledge Graph (schemes.ttl)
    ↓
Query Engine (query_engine.py) ← User Input (Flask routes)
    ↓
SPARQL Query Execution
    ↓
Filtered Results
    ↓
JSON Response → Web Interface (templates)
```

## Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | Python 3.x | Core programming language |
| Web Framework | Flask | HTTP server & routing |
| Semantic Web | RDFLib | RDF graph management |
| Query Language | SPARQL | Semantic data querying |
| Frontend | HTML5/CSS3 | User interface |
| Interactivity | JavaScript | Dynamic behavior |
| Icons | Font Awesome | UI icons |

## Installation Steps

1. **Install Python 3.8+**
2. **Install dependencies**:
   ```bash
   pip install Flask==3.0.0 rdflib==7.0.0
   ```
3. **Navigate to project**:
   ```bash
   cd scheme_checker
   ```
4. **Run application**:
   ```bash
   python app.py
   ```
5. **Access in browser**:
   ```
   http://localhost:5000
   ```

## Features Implemented

✅ **Semantic Knowledge Graph**: RDF-based data representation
✅ **SPARQL Querying**: Intelligent scheme retrieval
✅ **Multi-criteria Filtering**: State, occupation, age, gender, income
✅ **Responsive UI**: Works on desktop, tablet, mobile
✅ **Complete Information**: Benefits, documents, application process
✅ **Statistics Dashboard**: Real-time scheme statistics
✅ **Extensible Design**: Easy to add new schemes and criteria

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/search` | GET | Search interface |
| `/about` | GET | About page |
| `/api/search` | POST | Search schemes (JSON) |
| `/api/stats` | GET | Get statistics (JSON) |
| `/rebuild-graph` | POST | Rebuild RDF graph |

## Database Schema (RDF Ontology)

### Classes
- `scheme:Scheme` - Government scheme entity
- `scheme:Category` - Scheme classification
- `scheme:State` - Geographic region
- `scheme:Occupation` - Target profession

### Properties
- Object Properties: `hasCategory`, `applicableInState`, `requiresOccupation`
- Data Properties: `schemeName`, `minAge`, `maxAge`, `benefits`, etc.

## Sample SPARQL Query

```sparql
PREFIX scheme: <http://schemes.gov.in/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?benefits ?state
WHERE {
    ?scheme a scheme:Scheme ;
            scheme:schemeName ?name ;
            scheme:benefits ?benefits ;
            scheme:applicableInState ?st ;
            scheme:minAge ?minAge ;
            scheme:maxAge ?maxAge .
    
    ?st rdfs:label ?state .
    
    FILTER (?state = "Maharashtra" && 
            ?minAge <= 25 && 
            ?maxAge >= 25)
}
```

This query finds all schemes in Maharashtra for someone aged 25.
