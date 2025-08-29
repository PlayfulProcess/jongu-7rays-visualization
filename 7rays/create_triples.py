#!/usr/bin/env python3
"""
Convert existing 7rays data into knowledge graph triples for PyKEEN training
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

def load_existing_data():
    """Load the existing 7rays JSON data"""
    with open('7rays_data.json', 'r') as f:
        return json.load(f)

def create_entities_and_triples():
    """Create comprehensive entity and triple datasets"""
    
    data = load_existing_data()
    
    entities = []
    triples = []
    descriptions = []
    
    # Add Rays as entities
    for ray_id, ray_data in data['rays'].items():
        entity_id = f"Ray{ray_id}"
        entities.append({
            'id': entity_id,
            'label': f"Ray {ray_id}: {ray_data['name']}",
            'kind': 'Ray',
            'color': ray_data['color'],
            'description': f"Ray {ray_id} - {ray_data['name']}: {ray_data['quality']}. Keywords: {', '.join(ray_data['keywords'])}"
        })
        
        # Ray properties as triples
        triples.extend([
            (entity_id, 'hasName', ray_data['name']),
            (entity_id, 'hasQuality', ray_data['quality']),
            (entity_id, 'hasColor', ray_data['color']),
            (entity_id, 'hasPurpose', ray_data['purpose']),
            (entity_id, 'ruledBy', ray_data['planetary_ruler']),
            (entity_id, 'hasNote', ray_data['note']),
            (entity_id, 'hasElement', ray_data['element'])
        ])
        
        # Keywords as entities and relationships
        for keyword in ray_data['keywords']:
            keyword_id = f"Quality_{keyword.replace(' ', '_')}"
            if keyword_id not in [e['id'] for e in entities]:
                entities.append({
                    'id': keyword_id,
                    'label': keyword,
                    'kind': 'Quality',
                    'color': '#888888',
                    'description': f"Spiritual quality: {keyword}"
                })
            triples.append((entity_id, 'embodies', keyword_id))
    
    # Add Planes as entities
    for plane_id, plane_data in data['planes'].items():
        entity_id = f"Plane{plane_id}"
        entities.append({
            'id': entity_id,
            'label': f"Plane {plane_id}: {plane_data['name']}",
            'kind': 'Plane',
            'color': plane_data['color'],
            'description': f"Plane {plane_id} - {plane_data['name']}: {plane_data['consciousness_state']}. {plane_data['description']}"
        })
        
        # Plane properties as triples
        triples.extend([
            (entity_id, 'hasName', plane_data['name']),
            (entity_id, 'hasConsciousness', plane_data['consciousness_state']),
            (entity_id, 'hasElement', plane_data['element']),
            (entity_id, 'hasColor', plane_data['color']),
            (entity_id, 'hasGeometry', plane_data['geometric_form']),
            (entity_id, 'hasFrequency', str(plane_data['frequency']))
        ])
        
        # Alternate names
        for alt_name in plane_data['alternate_names']:
            alt_id = f"Name_{alt_name.replace(' ', '_')}"
            if alt_id not in [e['id'] for e in entities]:
                entities.append({
                    'id': alt_id,
                    'label': alt_name,
                    'kind': 'AlternateName',
                    'color': '#666666',
                    'description': f"Alternate name for plane: {alt_name}"
                })
            triples.append((entity_id, 'alsoKnownAs', alt_id))
    
    # Add relationship data from existing analysis
    relationships_data = data['relationships']
    
    # Primary rulerships
    for ray_num, plane_nums in relationships_data['primary_rulerships'].items():
        ray_id = f"Ray{ray_num}"
        for plane_num in plane_nums:
            plane_id = f"Plane{plane_num}"
            triples.append((ray_id, 'primarily_governs', plane_id))
            triples.append((plane_id, 'primarily_ruled_by', ray_id))
    
    # Fourth emphasis relationships
    fourth_data = relationships_data['fourth_emphasis']
    
    # Add special fourth ray/plane entities
    entities.extend([
        {
            'id': 'Fourth_Bridge_Function',
            'label': 'Fourth Bridge Function',
            'kind': 'Function',
            'color': '#00FF00',
            'description': 'The bridge function between higher spiritual triad and lower quaternary'
        },
        {
            'id': 'Humanity',
            'label': 'Humanity (Fourth Kingdom)',
            'kind': 'Kingdom',
            'color': '#FFD700',
            'description': 'Humanity as the fourth kingdom, mediator between animal and spiritual realms'
        },
        {
            'id': 'Christ_Consciousness',
            'label': 'Christ Consciousness',
            'kind': 'Consciousness',
            'color': '#00BFFF',
            'description': 'Unity awareness and Christ consciousness on the buddhic plane'
        }
    ])
    
    # Fourth emphasis triples
    triples.extend([
        ('Ray4', 'embodies', 'Fourth_Bridge_Function'),
        ('Plane4', 'embodies', 'Fourth_Bridge_Function'),
        ('Ray4', 'mediates_for', 'Humanity'),
        ('Plane4', 'enables', 'Christ_Consciousness'),
        ('Humanity', 'evolves_through', 'Ray4'),
        ('Fourth_Bridge_Function', 'harmonizes', 'Conflict')
    ])
    
    # Add color relationships
    color_data = data['color_mappings']
    for color_name, ray_num in color_data['primary_triad'].items():
        color_id = f"Color_{color_name.capitalize()}"
        if color_id not in [e['id'] for e in entities]:
            entities.append({
                'id': color_id,
                'label': color_name.capitalize(),
                'kind': 'Color',
                'color': data['rays'][str(ray_num)]['color'],
                'description': f"Primary color {color_name} associated with divine expression"
            })
        triples.append((f"Ray{ray_num}", 'manifests_as', color_id))
    
    # Load relationship matrices to add dynamic relationships
    try:
        with open('ray_plane_relationships_human.json', 'r') as f:
            human_rels = json.load(f)
        
        for rel in human_rels['relationships']:
            if rel['strength'] > 0.6:  # Only strong relationships
                ray_id = f"Ray{rel['ray']}"
                plane_id = f"Plane{rel['plane']}"
                
                # Map interaction types to relations
                relation_map = {
                    'primary_channel': 'flows_through',
                    'strong_influence': 'strongly_influences',
                    'moderate_interaction': 'interacts_with',
                    'subtle_resonance': 'resonates_with'
                }
                
                relation = relation_map.get(rel['interaction_type'], 'relates_to')
                triples.append((ray_id, relation, plane_id))
                
    except FileNotFoundError:
        print("Relationship matrices not found, using basic relationships only")
    
    # Add Bailey quote entities (sample)
    bailey_quotes = [
        "Enlightenment is humanity's emergence from self-incurred immaturity",
        "The fourth ray is the ray of harmony through conflict",
        "The buddhic plane is the plane of pure reason and intuition",
        "Humanity serves as the bridge between the animal and spiritual kingdoms",
        "The goal of evolution is the development of consciousness",
        "Each ray represents a different aspect of divine will-to-good"
    ]
    
    for i, quote in enumerate(bailey_quotes):
        quote_id = f"Quote_{i+1}"
        entities.append({
            'id': quote_id,
            'label': f"Bailey Quote {i+1}",
            'kind': 'Teaching',
            'color': '#E6E6FA',
            'description': quote
        })
        
        # Link quotes to relevant entities
        if 'fourth ray' in quote.lower():
            triples.append(('Ray4', 'described_by', quote_id))
        if 'buddhic' in quote.lower():
            triples.append(('Plane4', 'described_by', quote_id))
        if 'humanity' in quote.lower():
            triples.append(('Humanity', 'described_by', quote_id))
    
    return entities, triples

def create_data_files():
    """Create the CSV files needed for PyKEEN training"""
    
    entities, triples = create_entities_and_triples()
    
    # Create entities DataFrame
    entities_df = pd.DataFrame(entities)
    
    # Create triples DataFrame for PyKEEN
    triples_df = pd.DataFrame(triples, columns=['head', 'relation', 'tail'])
    
    # Add weights (can be refined later)
    np.random.seed(42)
    triples_df['weight'] = np.random.uniform(0.7, 1.0, len(triples_df))
    
    # Save files
    entities_df.to_csv('data/nodes.csv', index=False)
    triples_df.to_csv('data/edges.csv', index=False)
    
    print(f"Created {len(entities)} entities and {len(triples)} triples")
    print(f"Entity types: {entities_df['kind'].value_counts().to_dict()}")
    print(f"Top relations: {triples_df['relation'].value_counts().head(10).to_dict()}")
    
    return entities_df, triples_df

if __name__ == "__main__":
    # Create data directory
    Path('data').mkdir(exist_ok=True)
    
    # Generate the datasets
    entities_df, triples_df = create_data_files()
    
    # Display summary
    print("\n📊 Dataset Summary:")
    print(f"- Entities: {len(entities_df)}")
    print(f"- Triples: {len(triples_df)}")
    print(f"- Relations: {triples_df['relation'].nunique()}")
    print(f"- Entity kinds: {list(entities_df['kind'].unique())}")
    
    print("\n✅ Ready for PyKEEN training!")