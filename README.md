# Semantic Web-Based Smart Government Scheme Checker

A web-based application that uses Semantic Web technologies (RDF, SPARQL) to help citizens find government welfare schemes relevant to them.

## 🎯 Project Overview

This project addresses the challenge of discovering government schemes scattered across different websites. It uses:
- **RDF (Resource Description Framework)** for semantic data representation
- **SPARQL** for intelligent querying
- **Flask** for the web application framework
- **Python-RDFLib** for RDF graph management

## 📋 Features

- ✅ Semantic knowledge graph of government schemes
- ✅ Intelligent SPARQL-based search
- ✅ Personalized scheme recommendations
- ✅ Filter by state, occupation, age, gender, income
- ✅ Detailed scheme information with application process
- ✅ Modern, responsive web interface
- ✅ Extensible ontology structure

## 🏗️ Architecture

```
scheme_checker/
├── app.py                  # Flask application (main entry point)
├── ontology_builder.py     # Converts CSV to RDF knowledge graph
├── query_engine.py         # SPARQL query execution engine
├── requirements.txt        # Python dependencies
├── data/
│   ├── schemes.csv        # Government schemes dataset
│   └── schemes.ttl        # Generated RDF graph (auto-created)
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── search.html        # Search interface
│   └── about.html         # About page
└── static/
    └── css/
        └── style.css      # Styling
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install Flask==3.0.0 rdflib==7.0.0
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Navigate to Project Directory

```bash
cd scheme_checker
```

### Step 3: Run the Application

```bash
python app.py
```

The application will:
1. Build the RDF knowledge graph from CSV data (first run)
2. Start the Flask server on `http://localhost:5000`

### Step 4: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 🔍 How It Works

### 1. Data to RDF Conversion
The `ontology_builder.py` module converts CSV scheme data into RDF triples:

```python
# Example RDF triple structure
<scheme:scheme_1> rdf:type scheme:Scheme
<scheme:scheme_1> scheme:schemeName "Pradhan Mantri Kisan Samman Nidhi"
<scheme:scheme_1> scheme:hasCategory <scheme:category_Agriculture>
<scheme:scheme_1> scheme:applicableInState <scheme:state_All_States>
```

### 2. Ontology Classes

- `scheme:Scheme` - Government scheme entity
- `scheme:Category` - Scheme category (Agriculture, Education, etc.)
- `scheme:State` - Geographic applicability
- `scheme:Occupation` - Target occupation groups

### 3. SPARQL Querying

The `query_engine.py` module builds dynamic SPARQL queries based on user input:

```sparql
SELECT DISTINCT ?scheme ?name ?category ?state ?benefits
WHERE {
    ?scheme a scheme:Scheme ;
            scheme:schemeName ?name ;
            scheme:hasCategory ?cat ;
            scheme:applicableInState ?st .
    
    ?cat rdfs:label ?category .
    ?st rdfs:label ?state .
    
    FILTER (?state = "Maharashtra" && ?minAge <= 25 && ?maxAge >= 25)
}
```

## 📊 Sample Dataset

The application comes with 20 sample government schemes including:
- PM-KISAN (Agriculture)
- Ayushman Bharat (Healthcare)
- MGNREGA (Employment)
- Startup India (Entrepreneurship)
- State-specific schemes (Maharashtra, Kerala, Gujarat, etc.)

## 🎨 User Interface

### Home Page
- Platform statistics
- Feature highlights
- How it works section

### Search Page
- Interactive filters (State, Occupation, Category, Age, Gender, Income)
- Real-time SPARQL query execution
- Scheme cards with complete information

### About Page
- Project overview
- Technology stack explanation
- Ontology structure
- Future enhancements

## 🔧 Customization

### Adding New Schemes

1. Edit `data/schemes.csv`
2. Add new rows with scheme details
3. Restart the application or call rebuild endpoint:

```bash
curl -X POST http://localhost:5000/rebuild-graph
```

### Extending the Ontology

Modify `ontology_builder.py` to add new classes or properties:

```python
# Add new class
self.graph.add((self.SCHEME.Document, RDF.type, RDFS.Class))

# Add new property
self.graph.add((self.SCHEME.hasDocument, RDF.type, RDF.Property))
```

## 📈 Future Enhancements

- [ ] Natural language query interface
- [ ] Multi-language support (Hindi, regional languages)
- [ ] Integration with government APIs
- [ ] OWL reasoning for automatic eligibility inference
- [ ] User authentication and saved schemes
- [ ] Mobile application
- [ ] Advanced filtering with boolean logic
- [ ] Scheme comparison feature
- [ ] Application tracking

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Backend programming language |
| Flask | Web application framework |
| RDFLib | RDF graph creation and querying |
| SPARQL | Query language for RDF data |
| HTML5/CSS3 | Frontend interface |
| JavaScript | Dynamic interactions |

## 🧪 Testing the Semantic Features

### Test Knowledge Graph Creation
```bash
python ontology_builder.py
```

This will create `data/schemes.ttl` file.

### Test SPARQL Queries
```python
from rdflib import Graph
from query_engine import SchemeQueryEngine

graph = Graph()
graph.parse('data/schemes.ttl', format='turtle')

engine = SchemeQueryEngine(graph)
results = engine.search_schemes(state="Maharashtra", occupation="Farmer")
print(f"Found {len(results)} schemes")
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/search` | GET | Search interface |
| `/about` | GET | About page |
| `/api/search` | POST | Search schemes (JSON) |
| `/api/stats` | GET | Get statistics (JSON) |
| `/rebuild-graph` | POST | Rebuild RDF graph |

## 🤝 Contributing

This is an educational project demonstrating Semantic Web concepts. Feel free to:
- Add more government schemes
- Improve the ontology structure
- Enhance the UI/UX
- Add new features

## 📄 License

This project is created for educational purposes.

## 👥 Authors

Semantic Web & Knowledge Graph Project

## 🙏 Acknowledgments

- Government of India for scheme information
- W3C for Semantic Web standards
- RDFLib community
- Flask framework developers

---

**Note**: This is a demonstration project. For production use, integrate with official government APIs and databases for real-time scheme information.
