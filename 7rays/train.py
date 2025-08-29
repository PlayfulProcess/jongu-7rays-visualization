#!/usr/bin/env python3
"""
Train knowledge graph embeddings using PyKEEN on the Seven Rays dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import pickle

from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from pykeen import predict

def train_kg_embeddings():
    """Train knowledge graph embeddings using PyKEEN"""
    
    # Load triples
    triples_df = pd.read_csv('data/edges.csv')
    
    # Create triples factory
    tf = TriplesFactory.from_labeled_triples(
        triples_df[['head', 'relation', 'tail']].values,
        create_inverse_triples=True  # Add inverse relations
    )
    
    print(f"Training on {tf.num_triples} triples with {tf.num_entities} entities and {tf.num_relations} relations")
    
    # Train TransE model (good balance of performance and interpretability)
    result = pipeline(
        training=tf,
        model='TransE',
        model_kwargs={
            'embedding_dim': 128,  # Dimensionality of embeddings
            'scoring_fct_norm': 2,  # L2 norm
        },
        optimizer='Adam',
        optimizer_kwargs={
            'lr': 0.01,
        },
        training_kwargs={
            'num_epochs': 500,
            'batch_size': 512,
        },
        evaluation_kwargs={
            'batch_size': 512,
        },
        random_seed=42,
        device='auto',
    )
    
    print("Training completed!")
    
    # Extract embeddings
    entity_embeddings = result.model.entity_representations[0].weight.detach().numpy()
    relation_embeddings = result.model.relation_representations[0].weight.detach().numpy()
    
    # Get entity and relation to ID mappings
    entity_to_id = tf.entity_to_id
    id_to_entity = {v: k for k, v in entity_to_id.items()}
    relation_to_id = tf.relation_to_id
    id_to_relation = {v: k for k, v in relation_to_id.items()}
    
    # Save everything
    np.save('kg_embeddings.npy', entity_embeddings)
    np.save('relation_embeddings.npy', relation_embeddings)
    
    with open('entity_mapping.pkl', 'wb') as f:
        pickle.dump({'entity_to_id': entity_to_id, 'id_to_entity': id_to_entity}, f)
    
    with open('relation_mapping.pkl', 'wb') as f:
        pickle.dump({'relation_to_id': relation_to_id, 'id_to_relation': id_to_relation}, f)
    
    # Save the trained model
    result.save_to_directory('trained_model')
    
    print(f"Saved embeddings: {entity_embeddings.shape}")
    print(f"Saved entity mappings: {len(entity_to_id)} entities")
    print(f"Saved relation mappings: {len(relation_to_id)} relations")
    
    # Test some predictions
    print("\n🔮 Sample predictions:")
    
    # Test what's similar to Ray4
    if 'Ray4' in entity_to_id:
        ray4_id = entity_to_id['Ray4']
        ray4_emb = entity_embeddings[ray4_id]
        
        # Calculate similarities
        similarities = np.dot(entity_embeddings, ray4_emb) / (
            np.linalg.norm(entity_embeddings, axis=1) * np.linalg.norm(ray4_emb)
        )
        
        # Get top similar entities
        top_indices = np.argsort(-similarities)[:10]
        print("Entities most similar to Ray4:")
        for idx in top_indices:
            entity = id_to_entity[idx]
            score = similarities[idx]
            print(f"  {entity}: {score:.3f}")
    
    return result, entity_embeddings, entity_to_id

if __name__ == "__main__":
    # Make sure data directory exists
    if not Path('data/edges.csv').exists():
        print("❌ No edges.csv found. Run create_triples.py first!")
        exit(1)
    
    # Train the model
    result, embeddings, entity_mapping = train_kg_embeddings()
    
    print("\n✅ Knowledge graph training complete!")
    print("Files created:")
    print("- kg_embeddings.npy")
    print("- relation_embeddings.npy") 
    print("- entity_mapping.pkl")
    print("- relation_mapping.pkl")
    print("- trained_model/")
    print("\nReady for app.py!")