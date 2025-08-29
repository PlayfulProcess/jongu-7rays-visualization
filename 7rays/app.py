#!/usr/bin/env python3
"""
Seven Rays Vector Space Explorer - Gradio/HuggingFace Space App
Interactive exploration of learned embeddings for esoteric relationships
"""

import gradio as gr
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from umap import UMAP
import json

# Global variables for loaded data
entities_df = None
kg_embeddings = None
text_embeddings = None
fused_embeddings = None
entity_mapping = None
umap_2d = None
umap_3d = None
st_model = None

def load_data():
    """Load all necessary data and models"""
    global entities_df, kg_embeddings, text_embeddings, fused_embeddings
    global entity_mapping, umap_2d, umap_3d, st_model
    
    # Load entity data
    entities_df = pd.read_csv('data/nodes.csv')
    
    # Load KG embeddings
    kg_embeddings = np.load('kg_embeddings.npy')
    
    # Load entity mapping
    with open('entity_mapping.pkl', 'rb') as f:
        entity_mapping = pickle.load(f)
    
    # Initialize sentence transformer
    st_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
    # Generate text embeddings
    descriptions = entities_df['description'].fillna(entities_df['label']).tolist()
    text_embeddings = st_model.encode(descriptions, normalize_embeddings=True)
    
    # Create initial fused embeddings (60% KG, 40% text)
    fused_embeddings = create_fused_embeddings(0.6)
    
    # Create UMAP projections
    umap_2d = UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=42)
    umap_3d = UMAP(n_neighbors=15, min_dist=0.1, n_components=3, random_state=42)
    
    print("Data loaded successfully!")

def create_fused_embeddings(alpha=0.6):
    """Create fused embeddings from KG and text embeddings"""
    # Normalize KG embeddings
    kg_norm = kg_embeddings / np.linalg.norm(kg_embeddings, axis=1, keepdims=True)
    
    # Align dimensions (pad or truncate if necessary)
    min_dim = min(kg_norm.shape[1], text_embeddings.shape[1])
    kg_aligned = kg_norm[:, :min_dim]
    text_aligned = text_embeddings[:, :min_dim]
    
    # Weighted fusion
    fused = alpha * kg_aligned + (1 - alpha) * text_aligned
    return fused

def create_visualization(dimension='2D', alpha=0.6, highlight_fourth=True, color_by='kind'):
    """Create the main visualization plot"""
    global fused_embeddings, umap_2d, umap_3d
    
    # Update fused embeddings if alpha changed
    if alpha != 0.6:  # Default alpha
        fused_embeddings = create_fused_embeddings(alpha)
    
    # Get UMAP projection
    if dimension == '2D':
        coords = umap_2d.fit_transform(fused_embeddings)
        x, y = coords[:, 0], coords[:, 1]
        z = None
    else:
        coords = umap_3d.fit_transform(fused_embeddings)
        x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
    
    # Create plot dataframe
    plot_df = entities_df.copy()
    plot_df['x'] = x
    plot_df['y'] = y
    if z is not None:
        plot_df['z'] = z
    
    # Add hover information
    plot_df['hover_text'] = (
        "<b>" + plot_df['label'] + "</b><br>" +
        "Type: " + plot_df['kind'] + "<br>" +
        "Description: " + plot_df['description'].str[:100] + "..."
    )
    
    # Handle fourth emphasis
    if highlight_fourth:
        plot_df['size'] = plot_df['label'].apply(
            lambda x: 12 if 'Ray 4' in x or 'Plane 4' in x or 'Fourth' in x else 8
        )
        plot_df['opacity'] = plot_df['label'].apply(
            lambda x: 1.0 if 'Ray 4' in x or 'Plane 4' in x or 'Fourth' in x else 0.7
        )
    else:
        plot_df['size'] = 8
        plot_df['opacity'] = 0.7
    
    # Create the plot
    if dimension == '2D':
        fig = px.scatter(
            plot_df, x='x', y='y',
            color=color_by,
            size='size',
            hover_name='label',
            hover_data={'description': True, 'kind': True, 'x': False, 'y': False, 'size': False},
            color_discrete_map=get_color_map(),
            title=f"Seven Rays Vector Space (2D) - Alpha: {alpha:.1f}"
        )
        fig.update_traces(opacity=plot_df['opacity'])
        fig.update_layout(height=600)
    else:
        fig = px.scatter_3d(
            plot_df, x='x', y='y', z='z',
            color=color_by,
            size='size',
            hover_name='label',
            hover_data={'description': True, 'kind': True, 'x': False, 'y': False, 'z': False, 'size': False},
            color_discrete_map=get_color_map(),
            title=f"Seven Rays Vector Space (3D) - Alpha: {alpha:.1f}"
        )
        fig.update_traces(opacity=plot_df['opacity'])
        fig.update_layout(height=700)
    
    return fig

def get_color_map():
    """Get color mapping for different entity types"""
    return {
        'Ray': '#FF6B6B',
        'Plane': '#4ECDC4', 
        'Quality': '#45B7D1',
        'Color': '#96CEB4',
        'Function': '#FECA57',
        'Kingdom': '#FF9FF3',
        'Consciousness': '#54A0FF',
        'AlternateName': '#5F27CD',
        'Teaching': '#00D2D3'
    }

def find_similar_entities(query, top_k=8):
    """Find entities most similar to the query"""
    if not query.strip():
        return "Please enter a search query."
    
    # Try to find exact entity match first
    query_lower = query.lower()
    matches = entities_df[entities_df['label'].str.lower().str.contains(query_lower, regex=False)]
    
    if len(matches) > 0:
        # Use first match
        query_idx = matches.index[0]
        query_emb = fused_embeddings[query_idx:query_idx+1]
    else:
        # Encode the query text
        query_emb = st_model.encode([query], normalize_embeddings=True)
    
    # Calculate similarities
    similarities = cosine_similarity(query_emb, fused_embeddings)[0]
    
    # Get top similar entities
    top_indices = np.argsort(-similarities)[:top_k]
    
    results = []
    for idx in top_indices:
        entity = entities_df.iloc[idx]
        score = similarities[idx]
        results.append({
            'Entity': entity['label'],
            'Type': entity['kind'],
            'Similarity': f"{score:.3f}",
            'Description': entity['description'][:150] + "..." if len(entity['description']) > 150 else entity['description']
        })
    
    return pd.DataFrame(results)

def ray_plane_arithmetic(ray_concept, operation, plane_concept):
    """Perform vector arithmetic: Ray + Plane, Ray - Plane, etc."""
    
    def find_entity_embedding(concept_name):
        matches = entities_df[entities_df['label'].str.lower().str.contains(concept_name.lower(), regex=False)]
        if len(matches) > 0:
            idx = matches.index[0]
            return fused_embeddings[idx], entities_df.iloc[idx]['label']
        return None, None
    
    ray_emb, ray_found = find_entity_embedding(ray_concept)
    plane_emb, plane_found = find_entity_embedding(plane_concept)
    
    if ray_emb is None or plane_emb is None:
        return f"Could not find entities for '{ray_concept}' or '{plane_concept}'"
    
    # Perform arithmetic
    if operation == "Add (+)":
        result_emb = ray_emb + plane_emb
        op_text = f"{ray_found} + {plane_found}"
    elif operation == "Subtract (-)":
        result_emb = ray_emb - plane_emb  
        op_text = f"{ray_found} - {plane_found}"
    else:  # Average
        result_emb = (ray_emb + plane_emb) / 2
        op_text = f"({ray_found} + {plane_found}) / 2"
    
    # Find most similar entities to result
    similarities = cosine_similarity([result_emb], fused_embeddings)[0]
    top_indices = np.argsort(-similarities)[:8]
    
    results = []
    for idx in top_indices:
        entity = entities_df.iloc[idx]
        score = similarities[idx]
        results.append({
            'Rank': len(results) + 1,
            'Entity': entity['label'],
            'Type': entity['kind'], 
            'Similarity': f"{score:.3f}",
            'Description': entity['description'][:100] + "..."
        })
    
    result_df = pd.DataFrame(results)
    return f"Vector arithmetic: {op_text}", result_df

def create_gradio_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(title="Seven Rays Vector Space Explorer", theme=gr.themes.Soft()) as app:
        
        gr.Markdown("""
        # Seven Rays Vector Space Explorer
        
        **Interactive exploration of Alice Bailey's Seven Rays and Seven Planes through learned vector embeddings**
        
        This system combines knowledge graph embeddings (structural relationships) with text embeddings (semantic meaning) 
        to create a navigable vector space of esoteric concepts. Discover hidden connections and explore the living 
        relationships between rays, planes, and consciousness levels.
        """)
        
        with gr.Tabs():
            
            with gr.Tab("Vector Space Visualization"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Visualization Controls")
                        
                        dimension = gr.Radio(
                            choices=['2D', '3D'],
                            value='2D',
                            label="Dimension"
                        )
                        
                        alpha = gr.Slider(
                            minimum=0.0,
                            maximum=1.0, 
                            value=0.6,
                            step=0.1,
                            label="Fusion Weight (0=Text only, 1=Graph only)"
                        )
                        
                        color_by = gr.Radio(
                            choices=['kind', 'color'],
                            value='kind',
                            label="Color nodes by"
                        )
                        
                        highlight_fourth = gr.Checkbox(
                            value=True,
                            label="Highlight Fourth Ray/Plane (Bridge function)"
                        )
                        
                        update_btn = gr.Button("Update Visualization", variant="primary")
                    
                    with gr.Column(scale=3):
                        plot = gr.Plot()
                
                # Update plot when controls change
                update_btn.click(
                    fn=create_visualization,
                    inputs=[dimension, alpha, highlight_fourth, color_by],
                    outputs=[plot]
                )
            
            with gr.Tab("Semantic Search"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Find Similar Entities")
                        search_query = gr.Textbox(
                            label="Search Query",
                            placeholder="e.g., 'harmony', 'Ray 4', 'buddhic', 'bridge'...",
                            value="Ray 4"
                        )
                        
                        search_btn = gr.Button("Search", variant="primary")
                        
                        similarity_results = gr.Dataframe(
                            headers=["Entity", "Type", "Similarity", "Description"],
                            label="Similar Entities"
                        )
                
                search_btn.click(
                    fn=find_similar_entities,
                    inputs=[search_query],
                    outputs=[similarity_results]
                )
            
            with gr.Tab("Vector Arithmetic"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Ray-Plane Vector Mathematics")
                        gr.Markdown("Explore conceptual relationships through vector arithmetic")
                        
                        ray_input = gr.Textbox(
                            label="Ray Concept",
                            placeholder="e.g., Ray 4, harmony, will...",
                            value="Ray 4"
                        )
                        
                        operation = gr.Radio(
                            choices=["Add (+)", "Subtract (-)", "Average"],
                            value="Add (+)",
                            label="Operation"
                        )
                        
                        plane_input = gr.Textbox(
                            label="Plane Concept", 
                            placeholder="e.g., Plane 4, buddhic, mental...",
                            value="Plane 4"
                        )
                        
                        arithmetic_btn = gr.Button("Calculate", variant="primary")
                        
                        arithmetic_result = gr.Textbox(label="Operation", interactive=False)
                        arithmetic_table = gr.Dataframe(
                            headers=["Rank", "Entity", "Type", "Similarity", "Description"],
                            label="Most Similar to Result"
                        )
                
                arithmetic_btn.click(
                    fn=ray_plane_arithmetic,
                    inputs=[ray_input, operation, plane_input],
                    outputs=[arithmetic_result, arithmetic_table]
                )
            
            with gr.Tab("About"):
                gr.Markdown("""
                ## About This Vector Space
                
                This interactive system transforms Alice Bailey's esoteric teachings into a learned vector space where:
                
                ### 🧠 **Machine Learning Approach**
                - **Knowledge Graph Embeddings** (PyKEEN/TransE): Learn structural relationships between entities
                - **Text Embeddings** (SentenceTransformers): Capture semantic meaning from descriptions
                - **Fusion**: Weighted combination of both embedding types
                - **UMAP Projection**: Dimensionality reduction for visualization
                
                ### 🎯 **Key Features**
                - **Fourth Emphasis**: Ray 4 and Plane 4 highlighted as bridge functions
                - **Semantic Search**: Find entities similar to any concept
                - **Vector Arithmetic**: Mathematical exploration of relationships
                - **Dynamic Relationships**: No fixed correspondences, contextual connections
                
                ### 🔬 **What You Can Discover**
                - Natural clustering of related concepts
                - Bridge points between spiritual and material realms
                - Hidden connections not explicitly stated in texts
                - Evolution paths through consciousness levels
                - Harmonic relationships between different rays/planes
                
                ### 📚 **Data Sources**
                Based on Alice Bailey's complete works, especially:
                - A Treatise on the Seven Rays (5 volumes)
                - Esoteric Psychology I & II
                - A Treatise on Cosmic Fire
                
                **Note**: This is an experimental tool for contemplative exploration, not definitive teaching.
                The vector space represents learned patterns from the source material.
                
                ---
                *Built with PyKEEN, SentenceTransformers, UMAP, and Gradio*
                """)
        
        # Load initial visualization
        app.load(
            fn=create_visualization,
            inputs=[],
            outputs=[plot]
        )
    
    return app

if __name__ == "__main__":
    # Load data first
    print("Loading data and models...")
    load_data()
    
    # Create and launch the app
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )