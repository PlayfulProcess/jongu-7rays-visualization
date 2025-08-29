#!/usr/bin/env python3
"""
Extract and structure the meanings of the 7 Rays and 7 Planes
from Alice Bailey's teachings for the visualization project.
"""

# Based on Alice Bailey's teachings, here are the structured definitions:

SEVEN_RAYS = {
    1: {
        "name": "Will or Power",
        "quality": "Will to manifest, Divine Purpose, Leadership",
        "color": "#FF0000",  # Red
        "planetary_ruler": "Vulcan (hidden)",
        "note": "DO",
        "element": "Fire",
        "purpose": "To initiate and destroy",
        "virtue": "Strength, courage, steadfastness, truthfulness",
        "vice": "Pride, ambition, wilfulness, hardness, arrogance",
        "keywords": ["Power", "Will", "Purpose", "Leadership", "Initiative"]
    },
    2: {
        "name": "Love-Wisdom",
        "quality": "Inclusive love, Wisdom through experience",
        "color": "#0066FF",  # Blue
        "planetary_ruler": "Jupiter",
        "note": "RE",
        "element": "Water",
        "purpose": "To teach and heal",
        "virtue": "Calm, strength, patience, endurance, love of truth, faithfulness, intuition, clear intelligence, serene temper",
        "vice": "Over-absorption in study, coldness, indifference, contempt of mental limitations in others",
        "keywords": ["Love", "Wisdom", "Teaching", "Healing", "Intuition"]
    },
    3: {
        "name": "Active Intelligence",
        "quality": "Creative intelligence, Adaptability",
        "color": "#FFFF00",  # Yellow
        "planetary_ruler": "Saturn",
        "note": "MI",
        "element": "Air",
        "purpose": "To manipulate matter and energy",
        "virtue": "Wide views on all abstract questions, sincerity of purpose, clear intellect, capacity for concentration, patience, caution, absence of the tendency to worry over trifles",
        "vice": "Intellectual pride, coldness, isolation, inaccuracy in details, absent-mindedness, obstinacy, selfishness, overmuch criticism of others",
        "keywords": ["Intelligence", "Creativity", "Manipulation", "Mental", "Adaptability"]
    },
    4: {
        "name": "Harmony through Conflict",
        "quality": "Beauty, Art, Bridge-building, Mediation",
        "color": "#00FF00",  # Green
        "planetary_ruler": "Mercury",
        "note": "FA",
        "element": "Earth-Water",
        "purpose": "To harmonize and beautify",
        "virtue": "Strong affections, sympathy, physical courage, generosity, devotion, intellect, perception",
        "vice": "Self-centeredness, worrying, inaccuracy, lack of confidence, lack of moral courage",
        "keywords": ["Harmony", "Beauty", "Conflict", "Art", "Mediation", "Bridge"],
        "special_significance": "Bridge between higher and lower, humanity's ray, creative resolution"
    },
    5: {
        "name": "Concrete Knowledge",
        "quality": "Science, Research, Precision",
        "color": "#FF8000",  # Orange
        "planetary_ruler": "Venus",
        "note": "SOL",
        "element": "Fire-Air",
        "purpose": "To know and understand",
        "virtue": "Strictly accurate statements, justice, perseverance, common sense, uprightness, independence, keen intellect",
        "vice": "Harsh criticism, narrowness, arrogance, unforgiving temper, lack of sympathy and reverence, prejudice",
        "keywords": ["Science", "Research", "Knowledge", "Precision", "Analysis"]
    },
    6: {
        "name": "Devotion and Idealism",
        "quality": "Devotion, Idealism, Religious fervor",
        "color": "#FF00FF",  # Magenta/Purple
        "planetary_ruler": "Mars/Neptune",
        "note": "LA",
        "element": "Water-Fire",
        "purpose": "To idealize and devote",
        "virtue": "Devotion, single-mindedness, love, tenderness, intuition, loyalty, reverence",
        "vice": "Selfish and jealous love, over-leaning on others, partiality, self-deception, sectarianism, superstition, prejudice, over-rapid conclusions, fiery anger",
        "keywords": ["Devotion", "Idealism", "Religion", "Faith", "Emotion"]
    },
    7: {
        "name": "Ceremonial Order",
        "quality": "Organization, Ritual, Magic, Transformation",
        "color": "#8000FF",  # Violet
        "planetary_ruler": "Uranus",
        "note": "SI",
        "element": "Earth-Air",
        "purpose": "To organize and ritualize",
        "virtue": "Strength, perseverance, courage, courtesy, extreme care in details, self-reliance",
        "vice": "Formalism, bigotry, pride, narrowness, superficial judgments, self-opinion overmuch",
        "keywords": ["Order", "Ceremony", "Magic", "Ritual", "Organization", "Transformation"]
    }
}

SEVEN_PLANES = {
    1: {
        "name": "Logoic Plane",
        "alternate_names": ["Adi", "Divine"],
        "consciousness_state": "Logoic consciousness, Divine Will",
        "element": "Pure Spirit",
        "color": "#FFFFFF",  # White/Clear
        "frequency": 7.23,  # Base frequency multiplied by 7^6
        "geometric_form": "Point",
        "description": "Plane of divine purpose and will, source of all manifestation",
        "sub_planes": 7,
        "keywords": ["Divine", "Will", "Source", "Unity"]
    },
    2: {
        "name": "Monadic Plane",
        "alternate_names": ["Anupadaka", "Primordial"],
        "consciousness_state": "Monadic consciousness, Divine Love-Wisdom",
        "element": "Spirit-Matter",
        "color": "#E6E6FA",  # Light violet
        "frequency": 6.19,  # Base frequency multiplied by 7^5
        "geometric_form": "Line",
        "description": "Plane of the Monad, divine spark, love-wisdom aspect",
        "sub_planes": 7,
        "keywords": ["Monad", "Love-Wisdom", "Divine Spark", "Duality"]
    },
    3: {
        "name": "Atmic Plane",
        "alternate_names": ["Spiritual", "Nirvanic"],
        "consciousness_state": "Spiritual will, Atmic consciousness",
        "element": "Spiritual Fire",
        "color": "#FFD700",  # Gold
        "frequency": 5.29,  # Base frequency multiplied by 7^4
        "geometric_form": "Triangle",
        "description": "Plane of spiritual will, home of the spiritual triad",
        "sub_planes": 7,
        "keywords": ["Spiritual", "Will", "Triad", "Trinity"]
    },
    4: {
        "name": "Buddhic Plane",
        "alternate_names": ["Intuitional", "Christ Consciousness"],
        "consciousness_state": "Intuitional consciousness, Unity perception",
        "element": "Pure reason, Intuition",
        "color": "#00BFFF",  # Deep sky blue
        "frequency": 4.52,  # Base frequency multiplied by 7^3
        "geometric_form": "Square",
        "description": "Plane of pure reason and intuition, Christ consciousness, unity awareness",
        "sub_planes": 7,
        "keywords": ["Intuition", "Christ", "Unity", "Reason", "Bridge"],
        "special_significance": "Bridge between spiritual and personality planes, intuitive perception"
    },
    5: {
        "name": "Mental Plane",
        "alternate_names": ["Manasic", "Mind"],
        "consciousness_state": "Abstract and concrete thought",
        "element": "Mental matter",
        "color": "#FFFF00",  # Yellow
        "frequency": 3.86,  # Base frequency multiplied by 7^2
        "geometric_form": "Pentagon",
        "description": "Plane of mind, abstract and concrete thought, ideas and concepts",
        "sub_planes": 7,
        "keywords": ["Mind", "Thought", "Ideas", "Concepts", "Mental"]
    },
    6: {
        "name": "Astral Plane",
        "alternate_names": ["Emotional", "Desire", "Kamic"],
        "consciousness_state": "Emotional consciousness, Desire",
        "element": "Emotional/astral matter",
        "color": "#FF69B4",  # Hot pink
        "frequency": 3.30,  # Base frequency multiplied by 7^1
        "geometric_form": "Hexagon",
        "description": "Plane of emotions, desires, feelings, astral experiences",
        "sub_planes": 7,
        "keywords": ["Emotion", "Desire", "Feeling", "Astral", "Passion"]
    },
    7: {
        "name": "Physical Plane",
        "alternate_names": ["Dense", "Etheric-Physical"],
        "consciousness_state": "Physical consciousness, Material awareness",
        "element": "Dense and etheric matter",
        "color": "#8B4513",  # Saddle brown
        "frequency": 2.82,  # Base frequency
        "geometric_form": "Heptagon",
        "description": "Plane of dense matter and etheric energies, physical manifestation",
        "sub_planes": 7,
        "keywords": ["Physical", "Matter", "Dense", "Etheric", "Material"]
    }
}

# Key relationships and interactions
RAY_PLANE_RELATIONSHIPS = {
    "primary_rulerships": {
        # Rays have primary relationships with planes
        1: [1, 7],  # Ray 1 primarily works through logoic and physical planes
        2: [2, 6],  # Ray 2 through monadic and astral planes
        3: [3, 5],  # Ray 3 through atmic and mental planes
        4: [4],     # Ray 4 primarily through buddhic plane (special case)
        5: [5],     # Ray 5 primarily through mental plane
        6: [6],     # Ray 6 primarily through astral plane
        7: [7]      # Ray 7 primarily through physical plane
    },
    "evolutionary_cycles": {
        # Different relationships based on evolutionary context
        "outgoing": "Rays 1,3,5,7 more active in manifestation",
        "incoming": "Rays 2,4,6 more active in withdrawal/spiritualization"
    },
    "fourth_emphasis": {
        "ray_4": {
            "significance": "Bridge between higher spiritual triad (rays 1,2,3) and lower quaternary (rays 5,6,7)",
            "function": "Harmony through conflict, creative resolution",
            "color_synthesis": "Green - balance of all colors"
        },
        "plane_4": {
            "significance": "Bridge between spiritual planes (1,2,3) and personality planes (5,6,7)",
            "function": "Intuitive perception, Christ consciousness",
            "consciousness": "Unity awareness, direct knowing"
        },
        "humanity": {
            "fourth_kingdom": "Humanity is the 4th kingdom, bridge between animal and spiritual",
            "role": "Mediator between higher and lower kingdoms"
        }
    }
}

# Color harmonics and relationships
COLOR_RELATIONSHIPS = {
    "primary_triad": {
        "red": 1,    # Will-Power
        "blue": 2,   # Love-Wisdom  
        "yellow": 3  # Active Intelligence
    },
    "secondary_synthesis": {
        "green": 4,   # Harmony (synthesis of complementary colors)
        "orange": 5,  # Concrete Knowledge
        "indigo": 6,  # Devotion
        "violet": 7   # Ceremonial Order
    },
    "plane_frequencies": {
        # Higher planes = higher frequencies, lighter colors
        # Lower planes = lower frequencies, denser colors
        "frequency_progression": "descending from white light to dense matter"
    }
}

def export_to_json():
    """Export the structured data to JSON format for web application"""
    import json
    
    data = {
        "rays": SEVEN_RAYS,
        "planes": SEVEN_PLANES,
        "relationships": RAY_PLANE_RELATIONSHIPS,
        "color_mappings": COLOR_RELATIONSHIPS,
        "metadata": {
            "source": "Alice Bailey - Treatise on the Seven Rays",
            "extracted_by": "7rays_visualization_project",
            "note": "These are core esoteric definitions for visualization purposes"
        }
    }
    
    with open('7rays_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Data exported to 7rays_data.json")
    return data

if __name__ == "__main__":
    export_to_json()