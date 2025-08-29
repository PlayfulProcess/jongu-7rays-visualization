#!/usr/bin/env python3
"""
Advanced relationship analysis for the 7 Rays and 7 Planes
Based on Alice Bailey's dynamic, non-static approach to esoteric relationships
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Any

class DynamicRelationshipAnalyzer:
    """
    Analyzes dynamic relationships between rays and planes based on:
    - Evolutionary context
    - Initiation level  
    - Time cycles
    - Kingdom context
    """
    
    def __init__(self):
        with open('7rays_data.json', 'r') as f:
            self.data = json.load(f)
        
        self.rays = self.data['rays']
        self.planes = self.data['planes']
        
        # Define evolutionary contexts
        self.contexts = {
            'mineral': {'consciousness_level': 1, 'ray_emphasis': [7, 1]},
            'plant': {'consciousness_level': 2, 'ray_emphasis': [6, 2]},
            'animal': {'consciousness_level': 3, 'ray_emphasis': [3, 6]},
            'human': {'consciousness_level': 4, 'ray_emphasis': [4, 2, 5]},
            'spiritual': {'consciousness_level': 5, 'ray_emphasis': [2, 1]}
        }
    
    def calculate_dynamic_relationship(
        self, 
        ray_num: int, 
        plane_num: int, 
        context: str = 'human',
        cycle_phase: str = 'balanced'
    ) -> Dict[str, Any]:
        """
        Calculate relationship strength based on context and cycles
        No static 1:1 mapping - all relationships are dynamic
        """
        
        base_relationship = self._get_base_affinity(ray_num, plane_num)
        context_modifier = self._get_context_modifier(ray_num, plane_num, context)
        cycle_modifier = self._get_cycle_modifier(ray_num, plane_num, cycle_phase)
        fourth_emphasis = self._get_fourth_emphasis_bonus(ray_num, plane_num)
        
        # Dynamic strength calculation
        strength = (base_relationship * context_modifier * cycle_modifier) + fourth_emphasis
        strength = min(max(strength, 0), 1)  # Clamp between 0 and 1
        
        return {
            'ray': ray_num,
            'plane': plane_num,
            'strength': strength,
            'context': context,
            'cycle_phase': cycle_phase,
            'interaction_type': self._determine_interaction_type(ray_num, plane_num, strength),
            'color_blend': self._calculate_color_blend(ray_num, plane_num, strength),
            'frequency_harmony': self._calculate_frequency_harmony(ray_num, plane_num),
            'evolutionary_function': self._get_evolutionary_function(ray_num, plane_num, context)
        }
    
    def _get_base_affinity(self, ray_num: int, plane_num: int) -> float:
        """Base affinity patterns from Bailey's teachings"""
        
        # Primary correspondences (not rigid!)
        primary_pairs = {
            (1, 1): 0.9, (1, 7): 0.8,  # Ray 1: Logoic & Physical
            (2, 2): 0.9, (2, 6): 0.7,  # Ray 2: Monadic & Astral
            (3, 3): 0.9, (3, 5): 0.8,  # Ray 3: Atmic & Mental
            (4, 4): 1.0,               # Ray 4: Buddhic (special)
            (5, 5): 0.9,               # Ray 5: Mental
            (6, 6): 0.9,               # Ray 6: Astral
            (7, 7): 0.9                # Ray 7: Physical
        }
        
        # Secondary relationships
        secondary_pairs = {
            (1, 3): 0.6, (1, 5): 0.5,  # Will through intelligence
            (2, 4): 0.8, (2, 5): 0.6,  # Love-wisdom through intuition/mind
            (3, 1): 0.5, (3, 7): 0.7,  # Intelligence manifesting
            (4, 2): 0.7, (4, 6): 0.6,  # Harmony through love/emotion
            (5, 3): 0.8, (5, 7): 0.6,  # Concrete knowledge manifesting
            (6, 2): 0.6, (6, 4): 0.5,  # Devotion through love/harmony
            (7, 1): 0.8, (7, 3): 0.6   # Order through will/intelligence
        }
        
        # Check primary first, then secondary, then calculate base
        if (ray_num, plane_num) in primary_pairs:
            return primary_pairs[(ray_num, plane_num)]
        elif (ray_num, plane_num) in secondary_pairs:
            return secondary_pairs[(ray_num, plane_num)]
        else:
            # Calculate based on numerical proximity and harmonic relationships
            diff = abs(ray_num - plane_num)
            if diff == 0:
                return 0.9
            elif diff <= 2:
                return 0.4
            else:
                return 0.2
    
    def _get_context_modifier(self, ray_num: int, plane_num: int, context: str) -> float:
        """Context affects which relationships are emphasized"""
        
        if context not in self.contexts:
            return 1.0
            
        ctx = self.contexts[context]
        
        # Human context emphasizes 4th ray and 4th plane
        if context == 'human':
            if ray_num == 4 or plane_num == 4:
                return 1.3
            elif ray_num in [2, 5] or plane_num in [5, 6]:  # Mind and emotion active
                return 1.1
        
        # Spiritual context emphasizes higher rays/planes
        elif context == 'spiritual':
            if ray_num in [1, 2] or plane_num in [1, 2, 3]:
                return 1.2
            elif ray_num in [6, 7] or plane_num in [6, 7]:
                return 0.8
        
        # Animal context emphasizes instinctual rays/planes
        elif context == 'animal':
            if ray_num in [3, 6] or plane_num in [6, 7]:
                return 1.2
            elif ray_num in [1, 5] or plane_num in [1, 2]:
                return 0.7
        
        return 1.0
    
    def _get_cycle_modifier(self, ray_num: int, plane_num: int, cycle_phase: str) -> float:
        """Cycle phases affect ray-plane activity"""
        
        if cycle_phase == 'outgoing':
            # Odd numbered rays more active in manifestation
            if ray_num % 2 == 1:
                return 1.2
            else:
                return 0.9
        elif cycle_phase == 'incoming':
            # Even numbered rays more active in withdrawal
            if ray_num % 2 == 0:
                return 1.2
            else:
                return 0.9
        
        return 1.0  # balanced
    
    def _get_fourth_emphasis_bonus(self, ray_num: int, plane_num: int) -> float:
        """Special emphasis on 4th ray and 4th plane relationships"""
        
        if ray_num == 4 and plane_num == 4:
            return 0.2  # Strong bonus for 4th ray-4th plane
        elif ray_num == 4 or plane_num == 4:
            return 0.1  # Bonus for any 4th relationship
        
        return 0.0
    
    def _determine_interaction_type(self, ray_num: int, plane_num: int, strength: float) -> str:
        """Determine the type of interaction based on strength and characteristics"""
        
        if strength > 0.8:
            return 'primary_channel'
        elif strength > 0.6:
            return 'strong_influence'
        elif strength > 0.4:
            return 'moderate_interaction'
        elif strength > 0.2:
            return 'subtle_resonance'
        else:
            return 'minimal_connection'
    
    def _calculate_color_blend(self, ray_num: int, plane_num: int, strength: float) -> Dict[str, str]:
        """Calculate the color that emerges from ray-plane interaction"""
        
        ray_color = self.rays[str(ray_num)]['color']
        plane_color = self.planes[str(plane_num)]['color']
        
        # Convert hex to RGB for blending
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb
        
        ray_rgb = hex_to_rgb(ray_color)
        plane_rgb = hex_to_rgb(plane_color)
        
        # Blend based on strength
        blended_rgb = tuple(
            int(ray_rgb[i] * strength + plane_rgb[i] * (1 - strength))
            for i in range(3)
        )
        
        return {
            'ray_color': ray_color,
            'plane_color': plane_color,
            'blended_color': rgb_to_hex(blended_rgb),
            'blend_strength': strength
        }
    
    def _calculate_frequency_harmony(self, ray_num: int, plane_num: int) -> Dict[str, float]:
        """Calculate harmonic frequencies for sonification"""
        
        # Base frequency for ray (musical intervals)
        intervals = [1.0, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8]  # Major scale ratios
        base_freq = 432  # Hz
        
        ray_freq = base_freq * intervals[ray_num - 1]
        plane_freq = self.planes[str(plane_num)]['frequency'] * 100  # Scale up
        
        # Calculate harmonic ratio
        ratio = ray_freq / plane_freq if plane_freq != 0 else 1
        
        return {
            'ray_frequency': ray_freq,
            'plane_frequency': plane_freq,
            'harmonic_ratio': ratio,
            'consonance': self._calculate_consonance(ratio)
        }
    
    def _calculate_consonance(self, ratio: float) -> float:
        """Calculate how consonant (harmonious) the frequency ratio is"""
        
        # Simple ratios are more consonant
        # This is a simplified approach - could be more sophisticated
        simple_ratios = [1/1, 2/1, 3/2, 4/3, 5/4, 6/5, 8/7]
        
        min_distance = min(abs(ratio - r) for r in simple_ratios)
        consonance = 1 / (1 + min_distance * 5)  # Higher values = more consonant
        
        return consonance
    
    def _get_evolutionary_function(self, ray_num: int, plane_num: int, context: str) -> str:
        """Describe the evolutionary function of this ray-plane combination"""
        
        ray_name = self.rays[str(ray_num)]['name']
        plane_name = self.planes[str(plane_num)]['name']
        
        functions = {
            'human': {
                (4, 4): f"Bridge consciousness between spiritual and personality realms",
                (2, 4): f"Intuitive wisdom expressing through {plane_name}",
                (5, 5): f"Scientific understanding through concrete mind",
                (6, 6): f"Devotional aspiration in emotional nature"
            },
            'spiritual': {
                (1, 1): f"Divine will expressing through {plane_name}",
                (2, 2): f"Love-wisdom radiating from {plane_name}",
                (3, 3): f"Active intelligence organizing {plane_name}"
            }
        }
        
        if context in functions and (ray_num, plane_num) in functions[context]:
            return functions[context][(ray_num, plane_num)]
        else:
            return f"{ray_name} influencing {plane_name} in {context} context"
    
    def generate_full_relationship_matrix(self, context: str = 'human') -> List[Dict]:
        """Generate relationships for all ray-plane combinations"""
        
        relationships = []
        
        for ray_num in range(1, 8):
            for plane_num in range(1, 8):
                rel = self.calculate_dynamic_relationship(ray_num, plane_num, context)
                relationships.append(rel)
        
        return relationships
    
    def export_relationships(self, context: str = 'human', filename: str = None):
        """Export relationship matrix to JSON"""
        
        if filename is None:
            filename = f'ray_plane_relationships_{context}.json'
        
        relationships = self.generate_full_relationship_matrix(context)
        
        output = {
            'context': context,
            'total_relationships': len(relationships),
            'relationships': relationships,
            'metadata': {
                'note': 'Dynamic relationships - not static mappings',
                'fourth_emphasis': 'Ray 4 and Plane 4 receive special attention',
                'generated_by': '7rays_relationship_analyzer'
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Relationships exported to {filename}")
        return output

def main():
    """Generate relationship analysis for different contexts"""
    
    analyzer = DynamicRelationshipAnalyzer()
    
    # Generate for different evolutionary contexts
    contexts = ['human', 'spiritual', 'animal']
    
    for context in contexts:
        print(f"Analyzing relationships in {context} context...")
        analyzer.export_relationships(context)
    
    # Example: Show strong relationships in human context
    human_rels = analyzer.generate_full_relationship_matrix('human')
    strong_rels = [r for r in human_rels if r['strength'] > 0.7]
    
    print(f"\nStrong relationships in human context ({len(strong_rels)} found):")
    for rel in sorted(strong_rels, key=lambda x: x['strength'], reverse=True):
        print(f"Ray {rel['ray']} ↔ Plane {rel['plane']}: {rel['strength']:.2f} ({rel['interaction_type']})")

if __name__ == "__main__":
    main()