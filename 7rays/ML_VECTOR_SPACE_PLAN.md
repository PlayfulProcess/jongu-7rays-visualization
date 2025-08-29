# Seven Rays Vector Space ML Plan

## Overview: From Static Visualization to Learned Vector Space

Transform the current D3.js visualization into a trained ML model that learns embeddings for rays, planes, and their relationships in vector space - allowing for much richer exploration and discovery.

## 🎯 Goal
Create a vector space where:
- Each ray, plane, kingdom, and concept has learned embeddings
- Relationships emerge naturally from vector proximity
- We can query semantically ("what's similar to Ray 4?")
- Visualize in 2D/3D with meaningful clustering
- Discover hidden patterns in the esoteric system

## 📊 Phase 1: Data Preparation & Graph Construction (1-2 hours)

### 1.1 Extract Relationship Triples
```python
# Convert current JSON data into knowledge graph triples
# Format: (subject, relation, object, strength)
triples = [
    ("Ray4", "bridges", "BuddhicPlane", 1.0),
    ("Ray2", "governs", "AstralPlane", 0.8),
    ("Ray5", "manifests_through", "MentalPlane", 0.9),
    ("Human", "mediated_by", "Ray4", 0.9),
    ("Ray1", "colors", "Red", 1.0),
    # ... hundreds more from existing analysis
]
```

### 1.2 Create Enhanced Graph Structure
```
Entities:
- 7 Rays (Ray1, Ray2, ..., Ray7)
- 7 Planes (Logoic, Monadic, ..., Physical)
- 4 Kingdoms (Mineral, Plant, Animal, Human)
- Colors (Red, Blue, Yellow, ...)
- Qualities (Will, Love, Intelligence, ...)
- Planetary Rulers (Mars, Jupiter, ...)

Relations:
- governs, influences, manifests_through
- bridges, mediates, harmonizes
- colors, sounds, vibrates_at
- rules, expresses, embodies
```

### 1.3 Add Bailey Text Corpus
```python
# Include actual quotes from Bailey texts as training data
bailey_quotes = [
    "The fourth ray is the ray of harmony through conflict...",
    "The buddhic plane is the plane of pure reason...",
    # Extract key passages about each ray/plane
]
```

## 🤖 Phase 2: ML Model Training (2-3 hours)

### 2.1 Method Selection: Node2Vec + TransE Hybrid

**Why this approach:**
- Node2Vec learns structural relationships from graph topology
- TransE learns semantic relationships from text descriptions
- Combination gives both structural + semantic understanding

### 2.2 Implementation Stack
```python
# Core libraries
import networkx as nx
from karateclub import Node2Vec
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.manifold import TSNE, UMAP
import torch
import pytorch_geometric as pyg
```

### 2.3 Training Pipeline
```python
class SevenRaysEmbedder:
    def __init__(self):
        self.graph = nx.Graph()
        self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.node2vec = Node2Vec(dimensions=128, walk_length=30, num_walks=200)
        
    def build_graph(self, triples):
        # Add nodes and edges with weights
        
    def train_structural_embeddings(self):
        # Node2Vec for graph structure
        
    def train_semantic_embeddings(self):
        # Text embeddings for descriptions
        
    def combine_embeddings(self):
        # Weighted combination of structural + semantic
```

## 🎨 Phase 3: Interactive Vector Space Visualization (2-3 hours)

### 3.1 2D/3D Projection Options
- **t-SNE**: Good for cluster discovery
- **UMAP**: Better preserves global structure
- **PCA**: Linear, interpretable dimensions
- **Interactive**: Plotly for web-based exploration

### 3.2 Visualization Features
```python
# Color coding
ray_colors = {1: 'red', 2: 'blue', 3: 'yellow', 4: 'green', ...}
plane_colors = {1: 'white', 2: 'violet', 3: 'gold', ...}

# Interactive features
- Hover: Show entity details + Bailey quotes
- Click: Highlight similar entities (cosine similarity)
- Slider: Adjust similarity threshold
- Search: Find nearest neighbors to query
- Animation: Show evolution paths through space
```

### 3.3 Web Interface Options
1. **Streamlit** (fastest): Pure Python, auto-refresh
2. **Plotly Dash**: More customizable, still Python
3. **Observable/D3.js**: Most flexible, requires JS
4. **TensorFlow Projector**: Drop-in solution, very polished

## 🔍 Phase 4: Semantic Query System (1-2 hours)

### 4.1 Vector Search Capabilities
```python
def find_similar(entity, top_k=5):
    # Cosine similarity in vector space
    
def query_relationship(entity1, entity2):
    # Vector arithmetic: Ray4 - Conflict + Harmony = ?
    
def explore_cluster(center_point, radius=0.5):
    # Find all entities within distance threshold
    
def ray_plane_arithmetic():
    # Ray2 + BuddhicPlane - AstralPlane = ?
```

### 4.2 Semantic Discovery Features
- **Ray Analogies**: "Ray 1 is to Will as Ray 2 is to ?"
- **Plane Progression**: Navigate consciousness evolution paths
- **Hidden Connections**: Discover non-obvious relationships
- **Fourth Emphasis**: Automatically highlight bridge entities

## 🚀 Phase 5: Deployment & Integration (1 hour)

### 5.1 Model Persistence
```python
# Save trained embeddings
np.save('ray_plane_embeddings.npy', embeddings)
pickle.dump(entity_to_id, open('entity_mapping.pkl', 'wb'))
```

### 5.2 Web Deployment Options
- **Streamlit Cloud**: Free hosting for Python apps
- **Hugging Face Spaces**: ML model hosting
- **Vercel + API**: Static frontend + serverless backend
- **Supabase**: Store embeddings in pgvector for real-time queries

## 📈 Expected Outcomes

### Discoveries You Might Find:
1. **Natural Clustering**: Rays 2,4,6 might cluster (love-oriented)
2. **Bridge Patterns**: Ray 4 equidistant from spiritual and material
3. **Evolution Paths**: Clear vectors from lower to higher planes
4. **Hidden Relationships**: Unexpected connections Bailey didn't explicitly state
5. **Kingdom Progression**: Vector arrows showing evolutionary direction

### Exploration Capabilities:
- **"Show me what's like Ray 4 but more spiritual"**
- **"What bridges the Mental and Buddhic planes?"**
- **"Find the harmony between Will and Love"**
- **"What qualities are emerging in human consciousness?"**

## 🛠️ Implementation Roadmap (6-8 hours total)

### Day 1: Foundation (3-4 hours)
1. **Extract triples** from existing JSON data ✓ (30 min)
2. **Add Bailey text corpus** (1 hour)
3. **Build knowledge graph** (1 hour)
4. **Train Node2Vec embeddings** (30 min)
5. **Basic t-SNE visualization** (1 hour)

### Day 2: Enhancement (3-4 hours)
1. **Add semantic embeddings** (1 hour)
2. **Combine structural + semantic** (1 hour)
3. **Interactive web interface** (1.5 hours)
4. **Query system** (30 min)

### Day 3: Polish & Deploy (1 hour)
1. **Deploy to Streamlit Cloud** (30 min)
2. **Documentation & examples** (30 min)

## 🎯 Success Metrics

### Technical:
- [ ] Vector space with 50+ entities (rays, planes, qualities, etc.)
- [ ] Interactive 2D/3D visualization
- [ ] Semantic search working
- [ ] Sub-1 second query response time

### Experiential:
- [ ] Discover at least 3 non-obvious relationships
- [ ] Fourth ray clearly shows as bridge in vector space
- [ ] Evolution paths visible from mineral → human → spiritual
- [ ] Beautiful, contemplative exploration experience

This approach transforms static correspondences into a **living, queryable wisdom system** where relationships emerge from learned patterns rather than fixed rules - much more aligned with Bailey's dynamic view of spiritual evolution.

Ready to start with Phase 1? 🚀