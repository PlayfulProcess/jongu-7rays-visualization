#!/usr/bin/env python3
"""
Minimal test version of the Gradio app to verify everything works
"""

import gradio as gr
import pandas as pd
import numpy as np
import pickle
from pathlib import Path

def test_data_loading():
    """Test if all required files are available"""
    try:
        # Test entities
        entities_df = pd.read_csv('data/nodes.csv')
        print(f"Loaded {len(entities_df)} entities")
        
        # Test embeddings
        embeddings = np.load('kg_embeddings.npy')
        print(f"Loaded embeddings: {embeddings.shape}")
        
        # Test mappings
        with open('entity_mapping.pkl', 'rb') as f:
            mapping = pickle.load(f)
        print(f"Loaded entity mappings: {len(mapping['entity_to_id'])} entities")
        
        return True, entities_df, embeddings, mapping
    except Exception as e:
        print(f"Error loading data: {e}")
        return False, None, None, None

def create_simple_interface():
    """Create a simple test interface"""
    
    success, entities_df, embeddings, mapping = test_data_loading()
    
    if not success:
        return gr.Interface(
            fn=lambda x: "Data loading failed - check console for errors",
            inputs="text",
            outputs="text",
            title="Seven Rays - Data Loading Error"
        )
    
    def show_entities():
        return entities_df.head(10)
    
    def find_entity(query):
        if not query.strip():
            return "Enter a search term"
        
        # Simple search in entity labels
        matches = entities_df[entities_df['label'].str.contains(query, case=False, na=False)]
        if len(matches) == 0:
            return f"No entities found matching '{query}'"
        
        return matches[['label', 'kind', 'description']].head(5)
    
    with gr.Blocks(title="Seven Rays Vector Space - Test") as app:
        gr.Markdown("# Seven Rays Vector Space - Test Interface")
        gr.Markdown(f"Successfully loaded {len(entities_df)} entities with {embeddings.shape[1]}D embeddings")
        
        with gr.Tab("Data Overview"):
            gr.Markdown("### Sample Entities")
            entity_display = gr.Dataframe(
                value=entities_df.head(10),
                headers=["ID", "Label", "Kind", "Color", "Description"],
                label="First 10 Entities"
            )
        
        with gr.Tab("Entity Search"):
            search_input = gr.Textbox(label="Search entities", placeholder="e.g., Ray 4, harmony, buddhic")
            search_btn = gr.Button("Search")
            search_output = gr.Dataframe(label="Search Results")
            
            search_btn.click(
                fn=find_entity,
                inputs=[search_input],
                outputs=[search_output]
            )
        
        with gr.Tab("Embeddings Info"):
            gr.Markdown(f"""
            ### Embedding Details
            - **Entities**: {len(entities_df)}
            - **Embedding Dimensions**: {embeddings.shape[1]}
            - **Entity Types**: {', '.join(entities_df['kind'].unique())}
            
            ### Sample Entity Mappings:
            """)
            
            # Show some mappings
            sample_mappings = list(mapping['entity_to_id'].items())[:10]
            mapping_df = pd.DataFrame(sample_mappings, columns=['Entity', 'ID'])
            gr.Dataframe(value=mapping_df, label="Entity to ID Mapping (first 10)")
    
    return app

if __name__ == "__main__":
    app = create_simple_interface()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False
    )