## Design Document: Sevenfold Universe Interactive Visualization Platform

### Project Overview
A web-based platform for exploring and analyzing the relationships between the seven rays and seven planes in Alice Bailey's esoteric philosophy, with emphasis on their dynamic interweaving rather than static mapping.

### Technical Architecture

#### Frontend Stack (Vercel Deployment)
```
- Framework: Next.js 14 with App Router
- Language: TypeScript
- Visualization: D3.js + Three.js (for 3D views)
- State Management: Zustand
- Styling: Tailwind CSS + CSS Modules
- Data Fetching: SWR for caching
- Audio: Tone.js for sonification
```

#### Backend Stack (Supabase)
```
- Database: PostgreSQL with pgvector extension
- Storage: Supabase Storage for text corpus
- Edge Functions: Deno for API endpoints
- Real-time: Supabase Realtime for collaborative features
- Authentication: Supabase Auth (optional)
```

#### Data Processing Pipeline (Python)
```
- Text Processing: spaCy + NLTK
- Embeddings: Sentence-BERT or OpenAI Ada
- Vector Storage: pgvector in Supabase
- Analysis: NetworkX for relationship graphs
- ML: scikit-learn for clustering/classification
```

### Database Schema

```sql
-- Main entities
CREATE TABLE planes (
  id SERIAL PRIMARY KEY,
  number INT NOT NULL (1-7),
  name VARCHAR(100),
  alternate_names TEXT[],
  color_hex VARCHAR(7),
  frequency_hz FLOAT,
  geometric_form VARCHAR(50),
  consciousness_state TEXT,
  element VARCHAR(50)
);

CREATE TABLE rays (
  id SERIAL PRIMARY KEY,
  number INT NOT NULL (1-7),
  name VARCHAR(100),
  quality VARCHAR(200),
  will_aspect TEXT,
  color_hex VARCHAR(7),
  sound_note VARCHAR(10),
  planetary_ruler VARCHAR(50)
);

-- Extracted references with embeddings
CREATE TABLE bailey_references (
  id SERIAL PRIMARY KEY,
  book_title VARCHAR(200),
  chapter INT,
  page INT,
  quote TEXT,
  context TEXT,
  embedding vector(1536),
  entity_type VARCHAR(20), -- 'ray', 'plane', 'both'
  entity_numbers INT[],
  keywords TEXT[]
);

-- Dynamic relationships
CREATE TABLE ray_plane_interactions (
  id SERIAL PRIMARY KEY,
  ray_id INT REFERENCES rays(id),
  plane_id INT REFERENCES planes(id),
  interaction_type VARCHAR(50), -- 'influences', 'governs', 'manifests_through'
  strength FLOAT (0-1),
  context VARCHAR(500),
  source_reference_id INT REFERENCES bailey_references(id)
);

-- Create indexes for vector similarity search
CREATE INDEX ON bailey_references USING ivfflat (embedding vector_cosine_ops);
```

### Core Features

#### 1. Dynamic Visualization Engine
```typescript
interface VisualizationMode {
  'hierarchical': ShowsDescentFromSpiritToMatter;
  'relational': NetworkGraphOfInterconnections;
  'temporal': AnimatedEvolutionaryFlow;
  'harmonic': MusicalRelationships;
  'geometric': SacredGeometryPatterns;
}

class DynamicMapper {
  // No static 1:1 mapping per the document's insight
  calculateRelationship(
    ray: Ray, 
    plane: Plane, 
    context: EvolutionaryContext
  ): RelationshipStrength {
    // Factors: kingdom, initiation level, time cycle
    // Returns dynamic weighting based on context
  }
}
```

#### 2. Semantic Search Interface
```typescript
interface SemanticSearch {
  findSimilar(query: string): Promise<Reference[]>;
  exploreRelationship(
    entity1: Entity,
    entity2: Entity
  ): Promise<ConnectionPath[]>;
  generateInsight(
    references: Reference[]
  ): Promise<SynthesizedUnderstanding>;
}
```

#### 3. Fourth Emphasis Analyzer
Special module highlighting the significance of "fourth" relationships:
```typescript
class FourthAnalyzer {
  identifyBridgingFunctions(): BridgePoint[];
  mapHumanityRole(): EvolutionaryPosition;
  trackHarmonyThroughConflict(): DynamicProcess;
}
```

### Python Extraction Pipeline

```python
# extraction_pipeline.py
import spacy
from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector
import re
from typing import List, Dict, Tuple

class BaileyTextProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
    def extract_references(self, text: str) -> List[Dict]:
        """Extract mentions of rays and planes with context"""
        doc = self.nlp(text)
        references = []
        
        # Patterns for rays and planes
        ray_patterns = [
            r"(?:first|second|third|fourth|fifth|sixth|seventh|\d+)(?:st|nd|rd|th)?\s+ray",
            r"ray\s+(?:one|two|three|four|five|six|seven|\d+)",
            r"ray\s+of\s+[\w\s-]+"
        ]
        
        plane_patterns = [
            r"(?:physical|astral|mental|buddhic|atmic|monadic|logoic)\s+plane",
            r"(?:first|second|third|fourth|fifth|sixth|seventh|\d+)(?:st|nd|rd|th)?\s+plane"
        ]
        
        for sent in doc.sents:
            sent_text = sent.text
            
            # Check for ray mentions
            for pattern in ray_patterns:
                if re.search(pattern, sent_text, re.IGNORECASE):
                    context = self._get_context(doc, sent)
                    embedding = self.encoder.encode(sent_text)
                    references.append({
                        'text': sent_text,
                        'context': context,
                        'type': 'ray',
                        'embedding': embedding,
                        'entities': self._extract_numbers(sent_text)
                    })
                    
        return references
    
    def _extract_numbers(self, text: str) -> List[int]:
        """Extract ray/plane numbers from text"""
        number_map = {
            'first': 1, 'second': 2, 'third': 3, 'fourth': 4,
            'fifth': 5, 'sixth': 6, 'seventh': 7
        }
        numbers = []
        
        for word, num in number_map.items():
            if word in text.lower():
                numbers.append(num)
                
        # Also check for digits
        for match in re.finditer(r'\b[1-7]\b', text):
            numbers.append(int(match.group()))
            
        return numbers
    
    def analyze_relationships(self, references: List[Dict]) -> Dict:
        """Analyze co-occurrences and relationships"""
        from sklearn.metrics.pairwise import cosine_similarity
        import networkx as nx
        
        # Build co-occurrence matrix
        G = nx.Graph()
        
        for ref in references:
            entities = ref['entities']
            ref_type = ref['type']
            
            for entity in entities:
                node_id = f"{ref_type}_{entity}"
                G.add_node(node_id, type=ref_type, number=entity)
                
        # Add edges based on semantic similarity
        embeddings = [ref['embedding'] for ref in references]
        similarities = cosine_similarity(embeddings)
        
        threshold = 0.7
        for i, ref1 in enumerate(references):
            for j, ref2 in enumerate(references):
                if i < j and similarities[i][j] > threshold:
                    # Connect entities that appear in similar contexts
                    for e1 in ref1['entities']:
                        for e2 in ref2['entities']:
                            node1 = f"{ref1['type']}_{e1}"
                            node2 = f"{ref2['type']}_{e2}"
                            G.add_edge(node1, node2, weight=similarities[i][j])
                            
        return {
            'graph': G,
            'centrality': nx.betweenness_centrality(G),
            'communities': list(nx.community.greedy_modularity_communities(G))
        }

# Sonification module
class HarmonicMapper:
    def __init__(self):
        self.base_frequency = 432  # Hz
        self.intervals = {
            1: 1.0,      # Unison
            2: 9/8,      # Major second
            3: 5/4,      # Major third
            4: 4/3,      # Perfect fourth
            5: 3/2,      # Perfect fifth
            6: 5/3,      # Major sixth
            7: 15/8      # Major seventh
        }
        
    def ray_to_frequency(self, ray_number: int) -> float:
        """Convert ray number to frequency based on harmonic intervals"""
        return self.base_frequency * self.intervals[ray_number]
    
    def plane_to_rhythm(self, plane_number: int) -> Dict:
        """Map plane to rhythmic pattern"""
        patterns = {
            1: {'beats': 1, 'subdivision': 1},  # Whole note
            2: {'beats': 2, 'subdivision': 1},  # Half notes
            3: {'beats': 3, 'subdivision': 1},  # Triplet
            4: {'beats': 4, 'subdivision': 1},  # Quarter notes
            5: {'beats': 5, 'subdivision': 1},  # Quintuplet
            6: {'beats': 6, 'subdivision': 2},  # Compound
            7: {'beats': 7, 'subdivision': 1},  # Septuplet
        }
        return patterns[plane_number]
```

### API Endpoints (Supabase Edge Functions)

```typescript
// supabase/functions/search-references/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from '@supabase/supabase-js'

serve(async (req) => {
  const { query, mode } = await req.json()
  
  // Semantic search using pgvector
  const { data, error } = await supabase.rpc('search_similar_references', {
    query_embedding: await getEmbedding(query),
    match_threshold: 0.7,
    match_count: 20
  })
  
  // Apply fourth-emphasis weighting
  if (mode === 'fourth_emphasis') {
    data = data.map(ref => ({
      ...ref,
      relevance: ref.entity_numbers.includes(4) 
        ? ref.relevance * 1.5 
        : ref.relevance
    }))
  }
  
  return new Response(JSON.stringify(data))
})
```

### Frontend Components Structure

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── api/
├── components/
│   ├── visualization/
│   │   ├── DynamicGraph.tsx
│   │   ├── GeometricPattern.tsx
│   │   ├── HarmonicVisualizer.tsx
│   │   └── FourthEmphasis.tsx
│   ├── search/
│   │   ├── SemanticSearch.tsx
│   │   └── ReferenceExplorer.tsx
│   └── analysis/
│       ├── RelationshipMatrix.tsx
│       └── EvolutionaryContext.tsx
├── lib/
│   ├── supabase.ts
│   ├── three-setup.ts
│   └── tone-setup.ts
└── stores/
    ├── visualization.ts
    └── search.ts
```

### Deployment Configuration

```yaml
# vercel.json
{
  "buildCommand": "next build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_SUPABASE_URL": "@supabase_url",
    "NEXT_PUBLIC_SUPABASE_ANON_KEY": "@supabase_anon_key"
  }
}
```

### Key Implementation Notes

1. **No Static Mapping**: The system explicitly avoids creating fixed one-to-one correspondences between rays and planes, instead showing dynamic relationships based on context.

2. **Fourth Emphasis**: Special visualization modes and analysis tools highlight the significance of fourth-related concepts (4th ray, 4th plane, humanity as 4th kingdom).

3. **Multi-Modal Representation**: Each relationship can be expressed through:
   - Color gradients (visual)
   - Geometric transformations (spatial)
   - Harmonic intervals (auditory)
   - Network density (relational)

4. **Evolutionary Context**: All relationships are shown as dynamic, changing based on:
   - Evolutionary stage
   - Initiation level
   - Time cycles
   - Kingdom context

This architecture provides a foundation for exploring the complex, non-linear relationships described in the Bailey texts while respecting the teaching that these energies are in constant dynamic interplay rather than static correspondence.


Yes — you can get **almost the whole stack running from the terminal**, without needing heavy GUIs. Here’s what that looks like in practice:

---

## 🔹 1. Database (Neo4j AuraDB or Local)

* **Neo4j AuraDB (cloud free tier)**

  * Create a free instance → it gives you a connection string + credentials.
  * From terminal, you use the **Cypher Shell** (`bin/cypher-shell`) to run queries and load data.
  * Example:

    ```bash
    cypher-shell -u neo4j -p mypassword -a neo4j+s://12345.databases.neo4j.io
    ```
* **Local Neo4j (Docker)**

  ```bash
  docker run \
    --name neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -e NEO4J_AUTH=neo4j/mypassword \
    neo4j:5.20
  ```

  Then `cypher-shell` connects to it.

---

## 🔹 2. Data Ingestion (Python CLI)

* You can script your **reference extraction + graph building** as a Python CLI:

  ```bash
  poetry run python run_etl.py ingest ./texts/
  poetry run python run_etl.py detect
  poetry run python run_etl.py publish --db neo4j
  ```
* Using the `neo4j` Python driver, your script just pushes nodes/edges directly:

  ```python
  from neo4j import GraphDatabase
  driver = GraphDatabase.driver("neo4j+s://...", auth=("neo4j","pass"))

  with driver.session() as session:
      session.run("MERGE (r:Ray {code:'R4', name:'Harmony through Conflict'})")
  ```

---

## 🔹 3. Visualization (Terminal-Friendly Options)

* **Quick checks**: run Cypher queries in `cypher-shell`, e.g.:

  ```cypher
  MATCH (r:Ray)-[rel]->(p:Plane) RETURN r,rel,p LIMIT 25;
  ```
* **Web UI auto-exposed**: even local Neo4j will expose `http://localhost:7474` → minimal GUI if you want to peek.
* **Export to JSON/CSV**: from terminal you can dump subgraphs and then render them later with D3.js or Cytoscape.js in your web front end.

---

## 🔹 4. Web Frontend (Optional Terminal Build)

* With **Next.js** (deployed on Vercel), you can fully develop from terminal:

  ```bash
  npx create-next-app@latest interwoven-rays
  cd interwoven-rays
  npm install d3 cytoscape zustand tailwindcss
  npm run dev
  ```
* No GUI required; you just code and preview in browser.
* Deploy to Vercel from terminal:

  ```bash
  vercel
  ```

---

## 🔹 5. Sonification (Sound Layer)

* You can map graph queries → MIDI or synth output (Python `mingus`, or JS `Tone.js`).
* All definable via CLI → just run:

  ```bash
  node scripts/playRay.js R4
  ```

---

✅ **So yes:** everything — DB setup, ingestion, querying, even deployment — can be done from the terminal. The only GUI bits are optional (Neo4j Bloom, Vercel dashboard), but you don’t *need* them to develop or run the system.

---

Would you like me to sketch a **starter Cypher script** that sets up the **7 Rays** and **7 Planes as nodes** with their first connections, so you can load it from terminal and immediately see a graph?

