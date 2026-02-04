# 🚀 QUICK START GUIDE

## Get the Application Running in 3 Steps!

### Step 1: Install Dependencies ⚙️

Open your terminal and run:

```bash
pip install Flask rdflib
```

Or if you're using Python 3:

```bash
pip3 install Flask rdflib
```

### Step 2: Navigate to Project Directory 📁

```bash
cd scheme_checker
```

### Step 3: Run the Application ▶️

```bash
python app.py
```

Or if using Python 3:

```bash
python3 app.py
```

### Step 4: Open in Browser 🌐

Open your web browser and go to:

```
http://localhost:5000
```

---

## What You'll See 👀

1. **Home Page** - Overview of features and statistics
2. **Search Page** - Filter schemes by your criteria
3. **Results** - Personalized scheme recommendations

---

## First Time Running? 🆕

When you first run the application, it will:
1. ✅ Read the CSV data file (20 government schemes)
2. ✅ Build the RDF knowledge graph
3. ✅ Save it as `data/schemes.ttl`
4. ✅ Start the web server

This takes about 2-3 seconds. Subsequent runs are instant!

---

## Try These Searches 🔍

### Example 1: Farmer in Maharashtra
- **State**: Maharashtra
- **Occupation**: Farmer
- **Age**: 30

**Expected**: PM-KISAN, Kisan Credit Card, Maharashtra Shetakari Sanman Yojana

### Example 2: Student seeking education schemes
- **State**: All States
- **Category**: Education
- **Age**: 18
- **Income**: 150000

**Expected**: National Scholarship schemes, State education programs

### Example 3: Woman entrepreneur
- **Gender**: Female
- **Occupation**: Entrepreneur
- **State**: All States

**Expected**: Beti Bachao Beti Padhao, State women empowerment schemes

---

## Understanding the Results 📊

Each scheme card shows:
- ✨ **Scheme Name** - Official name
- 🏷️ **Category** - Type of scheme
- 📍 **State** - Where it's applicable
- 🎁 **Benefits** - What you'll get
- 📄 **Documents** - What you need
- 📋 **Application Process** - How to apply
- 🔗 **Official Website** - Direct link

---

## Troubleshooting 🔧

### Port 5000 already in use?

Change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Module not found error?

Make sure you installed the dependencies:

```bash
pip install Flask rdflib
```

### Can't connect to localhost?

Try:
- `http://127.0.0.1:5000`
- Check if firewall is blocking port 5000
- Ensure Flask is running (check terminal output)

---

## Testing the Semantic Features 🧪

### View the Knowledge Graph

After running once, check the generated RDF file:

```bash
cat data/schemes.ttl
```

You'll see RDF triples in Turtle format!

### Run the Demo

To understand the concepts without starting the web server:

```bash
python demo.py
```

This shows:
- Ontology structure
- Sample RDF triples
- Example SPARQL queries
- System workflow

---

## Adding Your Own Schemes 📝

1. Edit `data/schemes.csv`
2. Add new rows with scheme details
3. Restart the application

The RDF graph will be automatically rebuilt!

---

## Project Statistics 📈

- **Total Files**: 13
- **Lines of Code**: ~1500+
- **Government Schemes**: 20
- **States Covered**: 6 + All States
- **Categories**: 10+
- **Technologies**: Python, Flask, RDF, SPARQL, HTML, CSS, JavaScript

---

## Next Steps 🎯

1. ✅ **Explore the UI** - Try different search combinations
2. ✅ **View Source Code** - Understand the implementation
3. ✅ **Read Documentation** - Check README.md and PROJECT_STRUCTURE.md
4. ✅ **Customize** - Add your own schemes or modify the ontology
5. ✅ **Extend** - Add new features like user accounts or mobile app

---

## Need Help? 💬

- Read `README.md` for detailed documentation
- Check `PROJECT_STRUCTURE.md` for architecture details
- Run `python demo.py` to see concepts in action
- Review code comments for implementation details

---

## Success Indicators ✅

You'll know it's working when you see:

```
Building knowledge graph from CSV...
Successfully loaded 20 schemes into knowledge graph
RDF graph saved to data/schemes.ttl
Knowledge graph initialized with 260 triples
 * Running on http://0.0.0.0:5000
```

---

**🎉 Congratulations! You're running a Semantic Web application!**

The application uses:
- RDF for knowledge representation
- SPARQL for intelligent querying
- Flask for web serving
- Modern responsive design

Enjoy exploring government schemes! 🇮🇳
