#!/usr/bin/env python3
"""
Quick training script for testing - lighter version of train.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import pickle

try:
    from pykeen.pipeline import pipeline
    from pykeen.triples import TriplesFactory
    pykeen_available = True
except ImportError:
    pykeen_available = False

def create_dummy_embeddings():
    """Create dummy embeddings for testing when PyKEEN isn't available"""
    
    # Load entities to get count
    entities_df = pd.read_csv('data/nodes.csv')
    n_entities = len(entities_df)
    
    # Create random embeddings
    np.random.seed(42)
    embeddings = np.random.randn(n_entities, 64)
    
    # Create entity mapping
    entity_to_id = {entity: idx for idx, entity in enumerate(entities_df['id'])}
    id_to_entity = {idx: entity for entity, idx in entity_to_id.items()}
    
    # Save everything
    np.save('kg_embeddings.npy', embeddings)
    
    with open('entity_mapping.pkl', 'wb') as f:
        pickle.dump({'entity_to_id': entity_to_id, 'id_to_entity': id_to_entity}, f)
    
    print(f"Created dummy embeddings: {embeddings.shape}")
    print(f"Entity mapping: {len(entity_to_id)} entities")
    
    return embeddings, entity_to_id

def train_quick_embeddings():
    """Quick training with reduced parameters"""
    
    if not pykeen_available:
        print("PyKEEN not available, creating dummy embeddings...")
        return create_dummy_embeddings()
    
    # Load triples
    triples_df = pd.read_csv('data/edges.csv')
    
    # Create triples factory
    tf = TriplesFactory.from_labeled_triples(
        triples_df[['head', 'relation', 'tail']].values,
        create_inverse_triples=True
    )
    
    print(f"Quick training on {tf.num_triples} triples with {tf.num_entities} entities")
    
    # Quick training - much lighter parameters
    result = pipeline(
        training=tf,
        model='TransE',
        model_kwargs={
            'embedding_dim': 64,  # Smaller dimension
            'scoring_fct_norm': 2,
        },
        optimizer='Adam',
        optimizer_kwargs={
            'lr': 0.01,
        },
        training_kwargs={
            'num_epochs': 50,  # Much fewer epochs
            'batch_size': 128,  # Smaller batch
        },
        random_seed=42,
        device='cpu',  # Force CPU for compatibility
    )
    
    print("Quick training completed!")
    
    # Extract and save embeddings
    entity_embeddings = result.model.entity_representations[0].weight.detach().numpy()
    
    entity_to_id = tf.entity_to_id
    id_to_entity = {v: k for k, v in entity_to_id.items()}
    
    np.save('kg_embeddings.npy', entity_embeddings)
    
    with open('entity_mapping.pkl', 'wb') as f:
        pickle.dump({'entity_to_id': entity_to_id, 'id_to_entity': id_to_entity}, f)
    
    print(f"Saved embeddings: {entity_embeddings.shape}")
    return entity_embeddings, entity_to_id

if __name__ == "__main__":
    if not Path('data/edges.csv').exists():
        print("ERROR: No edges.csv found. Run create_triples.py first!")
        exit(1)
    
    embeddings, entity_mapping = train_quick_embeddings()
    
    print("\nQuick training complete!")
    print("Files created:")
    print("- kg_embeddings.npy")
    print("- entity_mapping.pkl")
    print("\nReady for app.py!")