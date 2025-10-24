# Black Hole Time Dilation Simulation 🌌

A physics simulation that demonstrates gravitational time dilation effects near black holes using Python, VPython, and matplotlib.

## 📖 Overview

This project simulates and visualizes the time dilation effects predicted by General Relativity in the vicinity of a black hole. The simulation calculates the Schwarzschild radius and shows how time slows down dramatically as objects approach the event horizon.

## 🚀 Features

- **Physics Engine**: Accurate calculations of Schwarzschild radius and time dilation factors
- **2D Visualization**: Matplotlib graphs showing time dilation vs. distance
- **3D Simulation**: VPython interactive visualization of orbiting objects with time-dependent motion
- **Color Coding**: Visual representation of time dilation through color gradients
- **Interactive Controls**: Adjustable parameters for black hole mass and orbit configurations

## 📋 Requirements

```bash
pip install vpython numpy matplotlib
```

## 📁 Project Structure

```
blackhole-sim/
├── src/
│   ├── main.py           # Main entry point
│   ├── physics.py        # Physics calculations
│   ├── visualization.py  # 2D and 3D visualizations
│   └── utils.py         # Utility functions
└── README.md
```

## 🔬 Physics Background

### Schwarzschild Radius
The event horizon radius of a non-rotating black hole:
```
rs = 2GM/c²
```

### Time Dilation Factor
The gravitational time dilation near a massive object:
```
Δt₀/Δt = √(1 - rs/r)
```

Where:
- `G` = Gravitational constant
- `M` = Mass of the black hole
- `c` = Speed of light
- `r` = Distance from the black hole center
- `rs` = Schwarzschild radius

## 🎮 Usage

### Basic Example
```python
python src/main.py
```

### Custom Black Hole Mass
```python
from physics import schwarzschild_radius, time_dilation

M = 10  # Solar masses
r = 30_000  # Distance in km
rs = schwarzschild_radius(M)
dilation = time_dilation(r, rs)
```

### Visualization
```python
from visualization import plot_dilation, visualize_orbits

# 2D Plot
plot_dilation(10)  # 10 solar masses

# 3D Simulation
visualize_orbits(10)
```

## 🎨 Visualization Features

### 2D Graph
- X-axis: Distance from black hole (km)
- Y-axis: Time dilation factor (t₀/tf)
- Red dashed line: Schwarzschild radius (event horizon)

### 3D Simulation
- Central black sphere: Black hole
- Colored orbiting spheres: Test particles
- Color gradient: Red (slow time) to Blue (normal time)
- Trail effects: Orbital paths
- Differential rotation speeds based on time dilation

## 🔄 Development Phases

### ✅ Phase 1: Setup and Configuration
- Project structure creation
- Basic main.py implementation
- Dependency management

### ✅ Phase 2: Physics Module
- Schwarzschild radius calculation
- Time dilation factor computation
- Physical constants definition

### ✅ Phase 3: Analytical Visualization
- Matplotlib integration
- 2D plotting of time dilation curves
- Event horizon marking

### ✅ Phase 4: 3D Visualization
- VPython scene setup
- Orbital simulation
- Color-coded time dilation representation

### 🚧 Phase 5: Interactive Interface
- Dynamic parameter adjustment
- Real-time simulation updates
- User controls for mass and orbits

## 📊 Expected Results

When running the simulation with a 10 solar mass black hole:
- Schwarzschild radius: ~29,530 km
- Time dilation at r=30,000 km: ~0.041 (time runs 24x slower)
- Visual representation shows dramatic effects near the event horizon

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📚 References

- Schwarzschild, K. (1916). "On the Gravitational Field of a Point Mass"
- General Relativity and Black Hole Physics
- VPython Documentation: https://vpython.org
- NumPy Documentation: https://numpy.org
- Matplotlib Documentation: https://matplotlib.org

## 📄 License

This project is open source and available under the MIT License.