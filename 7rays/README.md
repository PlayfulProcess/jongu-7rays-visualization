# Seven Rays & Seven Planes Interactive Visualization

An interactive web visualization exploring the dynamic relationships between the Seven Rays (divine qualities) and Seven Planes (levels of consciousness) according to Alice Bailey's esoteric teachings.

## Overview

This project represents an experiment in visualizing complex esoteric relationships through interactive web technology. Unlike static correspondence charts, this visualization emphasizes the **dynamic, living nature** of these spiritual energies and their relationships.

## Key Features

### 🌟 Dynamic Relationship Matrix
- No static 1:1 mappings between rays and planes
- Relationships change based on evolutionary context and consciousness level
- Interactive exploration of connection strengths and types

### 🎨 Meaningful Color Visualization
- Ray colors based on traditional esoteric associations
- Plane colors representing different levels of consciousness
- Dynamic color blending showing interaction qualities

### 🔄 Fourth Emphasis
- Special highlighting of 4th Ray (Harmony through Conflict) and 4th Plane (Buddhic/Intuitional)
- Represents humanity's role as bridge between spiritual and material realms

### 📊 Multiple View Modes
- **Circular Ray Display**: Shows the seven rays as divine qualities
- **Vertical Plane Display**: Hierarchical arrangement from spirit to matter
- **Relationship Matrix**: Interactive grid showing all ray-plane connections

### 🎛️ Context Controls
- **Evolutionary Context**: Human, Spiritual, Animal kingdom perspectives
- **Cycle Phases**: Outgoing (manifestation) vs. Incoming (spiritualization)
- **Animation**: Pulse effects for strong relationships

## Technical Implementation

### Frontend Stack
- **Vanilla HTML/CSS/JavaScript** - Simple, no framework dependencies
- **D3.js** - For sophisticated data visualization
- **Responsive Design** - Works on desktop and mobile

### Data Processing
- **Python Scripts** - For extracting and analyzing esoteric relationships
- **JSON Data** - Structured storage of rays, planes, and relationships
- **Dynamic Calculations** - Real-time relationship strength computation

### Files Structure
```
7rays/
├── index.html              # Main visualization interface
├── visualization.js        # D3.js visualization logic
├── vercel.json            # Deployment configuration
├── extract_meanings.py    # Extract ray/plane definitions
├── relationship_analyzer.py # Dynamic relationship analysis
├── 7rays_data.json        # Generated: Core data definitions
└── ray_plane_relationships_*.json # Generated: Relationship matrices
```

## Local Development

1. **Generate Data**:
   ```bash
   python extract_meanings.py
   python relationship_analyzer.py
   ```

2. **View Locally**:
   Open `index.html` in a modern web browser, or use a local server:
   ```bash
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

## Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Alternative Static Hosts
- **GitHub Pages**: Push to a repository and enable Pages
- **Netlify**: Drag and drop the folder to Netlify dashboard
- **Any HTTP Server**: The project is pure static files

## Philosophical Approach

This visualization is built on several key principles:

### 1. **No Static Correspondences**
Unlike traditional esoteric charts that show fixed relationships, this system recognizes that ray-plane interactions are **contextual and evolutionary**. A 5th ray soul might express through different planes at different stages of development.

### 2. **Fourth Kingdom Emphasis**
Special attention to humanity as the "4th kingdom" - the bridge between animal instinct and spiritual intuition. The 4th ray and 4th plane receive enhanced visualization to represent this crucial mediating function.

### 3. **Dynamic Rather Than Dogmatic**
The system avoids presenting any single "correct" mapping, instead showing how relationships **shift and flow** based on consciousness level, evolutionary stage, and cosmic cycles.

### 4. **Multi-Modal Representation**
Each relationship can be expressed through:
- **Visual**: Color blending and intensity
- **Spatial**: Geometric arrangements and proximity
- **Interactive**: Hover effects and click exploration
- **Temporal**: Animation showing relationship dynamics

## Data Sources

The relationships and definitions are based on:
- Alice Bailey's "Treatise on the Seven Rays" (5 volumes)
- "Esoteric Psychology" volumes 1 & 2
- "A Treatise on Cosmic Fire"
- Traditional Theosophical teachings

However, the **interpretations and relationship calculations are experimental** - designed to stimulate insight rather than provide definitive answers.

## Future Enhancements

### Phase 2 Possibilities
- **Audio Sonification**: Each ray-plane relationship could generate harmonic frequencies
- **3D Visualization**: WebGL/Three.js for spatial relationship exploration  
- **Historical Context**: Show how relationships have shifted over different ages
- **Personal Ray Analysis**: Input personal ray structure and see emphasized relationships

### Phase 3 Advanced Features
- **Collaborative Exploration**: Multi-user synchronized exploration
- **AI-Assisted Insights**: Natural language explanations of relationship patterns
- **Integration with Astrological Data**: Planetary cycles affecting ray-plane emphasis
- **Mobile AR**: Augmented reality visualization of ray-plane interactions

## Contributing

This is an **experiment in collaborative spiritual technology**. Contributions welcome in areas of:

- **Esoteric Research**: Deeper analysis of Bailey's teachings
- **Visualization Design**: New ways to represent dynamic relationships
- **Technical Enhancement**: Performance, accessibility, new features
- **Documentation**: Better explanations of complex concepts

## License

This project is released under **Creative Commons Attribution-ShareAlike 4.0**. 

The goal is to freely share tools that help people explore their spiritual development, while ensuring derivative works remain open and accessible to all.

## Contact

Part of the **Jongu Collective** - experiments in collaborative spiritual technology.

For questions, suggestions, or collaboration: [GitHub Issues](../../issues)

---

*"The goal of all esoteric teaching is to develop intuitive perception and to train the candidate to be sensitive to those subtle influences and energy streams which emanate from the various centers of spiritual force."* - Alice Bailey