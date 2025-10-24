A physics simulation that demonstrates gravitational time dilation effects near black holes using Python, implementing the Schwarzschild metric from General Relativity.

## Table of Contents

- [Overview](#overview)
- [Physical Theory](#physical-theory)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Examples](#examples)

## Overview

This project provides a comprehensive simulation of relativistic effects near non-rotating black holes, including accurate calculations of time dilation, orbital mechanics, and visual representations of spacetime curvature effects.

## Physical Theory

### Schwarzschild Metric

The spacetime geometry around a non-rotating, spherically symmetric mass is described by the Schwarzschild metric:

```
ds² = -(1 - rs/r)c²dt² + (1 - rs/r)⁻¹dr² + r²(dθ² + sin²θdφ²)
```

### Key Equations Implemented

#### Schwarzschild Radius
The event horizon radius for a non-rotating black hole:
```
rs = 2GM/c²
```
Where:
- `G` = 6.67430 × 10⁻¹¹ m³/kg·s² (gravitational constant)
- `M` = black hole mass (kg)
- `c` = 299,792,458 m/s (speed of light)

#### Gravitational Time Dilation
The time dilation factor between observers:
```
Δt₀/Δt = √(1 - rs/r)
```
Where:
- `Δt₀` = proper time interval for distant observer
- `Δt` = proper time interval at distance r
- `rs` = Schwarzschild radius
- `r` = radial distance from black hole center

#### Photon Sphere
The radius where photons can orbit:
```
r_photon = 3GM/c² = 1.5rs
```

#### Innermost Stable Circular Orbit (ISCO)
For a Schwarzschild black hole:
```
r_ISCO = 6GM/c² = 3rs
```

#### Gravitational Redshift
The frequency shift of light escaping the gravitational field:
```
z = (1/√(1 - rs/r)) - 1
```

#### Tidal Force
The differential gravitational acceleration across an object:
```
F_tidal ≈ 2GMh/r³
```
Where `h` is the object size.

### Module Descriptions

#### physics.py
Core physics engine implementing relativistic calculations:

```python
def schwarzschild_radius(mass_solar: float) -> float:
    G = 6.67430e-11
    c = 299_792_458
    M_sol = 1.98847e30
    
    mass_kg = mass_solar * M_sol
    rs_m = 2 * G * mass_kg / (c ** 2)
    return rs_m / 1000
```

#### visualization.py
Rendering engine for 2D plots and 3D simulations:

```python
def create_orbital_object(radius: float, time_factor: float) -> sphere:
    color_hue = 0.7 * time_factor  # Red (slow) to blue (normal)
    return sphere(
        pos=vector(radius * scale_factor, 0, 0),
        color=color.hsv_to_rgb(vector(color_hue, 1, 1)),
        make_trail=True
    )
```

## API Reference

### Physics Module

#### Core Functions

```python
schwarzschild_radius(mass_solar: float) -> float
time_dilation(r_km: float, rs_km: float) -> float
escape_velocity(r_km: float, mass_solar: float) -> float
orbital_period(r_km: float, mass_solar: float) -> float
gravitational_redshift(r_km: float, rs_km: float) -> float
tidal_force(r_km: float, mass_solar: float, object_size_m: float) -> float
photon_sphere_radius(mass_solar: float) -> float
innermost_stable_orbit(mass_solar: float) -> float
```

### Visualization Module

#### Plotting Functions

```python
plot_dilation(mass_solar: float) -> None
plot_multiple_masses() -> None
visualize_orbits(mass_solar: float, num_orbits: int) -> None
create_interactive_simulation(mass_solar: float) -> None
```

### Utils Module

#### Helper Functions

```python
format_time(seconds: float) -> str
format_distance(km: float) -> str
calculate_safe_distance(mass_solar: float, safety_factor: float) -> float
compare_time_passages(r_km: float, rs_km: float, observer_time_hours: float) -> Dict
generate_orbit_data(mass_solar: float, num_orbits: int) -> List[Dict]
interpolate_color(factor: float) -> Tuple[float, float, float]
```

### Benchmarks

| Configuration | Orbits | Trail Points | FPS | Memory Usage |
|--------------|--------|--------------|-----|--------------|
| Minimal      | 1      | 50           | 60  | ~50 MB       |
| Standard     | 4      | 150          | 60  | ~100 MB      |
| Maximum      | 10     | 150          | 60  | ~200 MB      |

## Examples

### Calculate Time Dilation

```python
from physics import schwarzschild_radius, time_dilation

M = 10
rs = schwarzschild_radius(M)

r = 2 * rs
factor = time_dilation(r, rs)

print(f"Time dilation factor: {factor:.4f}")
# Output: Time dilation factor: 0.7071
```

### Generate Orbital Data

```python
from utils import generate_orbit_data

orbits = generate_orbit_data(mass_solar=10, num_orbits=5)
for orbit in orbits:
    print(f"r={orbit['radius_rs']:.1f}Rs: "
          f"Period={orbit['orbital_period_formatted']}, "
          f"Dilation={orbit['time_dilation']:.3f}")
```

### Create Custom Visualization

```python
from vpython import sphere, vector, color
from physics import schwarzschild_radius, time_dilation

def create_custom_simulation(mass):
    rs = schwarzschild_radius(mass)

    blackhole = sphere(
        pos=vector(0, 0, 0),
        radius=rs * scale_factor,
        color=color.black
    )

    r = 3 * rs
    factor = time_dilation(r, rs)
    
    orbiter = sphere(
        pos=vector(r * scale_factor, 0, 0),
        radius=0.5,
        color=color.hsv_to_rgb(vector(0.7 * factor, 1, 1))
    )
    
    while True:
        rate(60)
        angle = factor * time.time()
        orbiter.pos = vector(
            r * cos(angle),
            0,
            r * sin(angle)
        )
```

<img width="1916" height="1001" alt="image" src="https://github.com/user-attachments/assets/101badcb-64f5-4009-8548-c5c45590d1b8" />

## Installation

### Requirements

- Python 3.8 or higher
- pip package manager

### Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `vpython>=7.6.4` - 3D visualization engine
- `numpy>=1.24.0` - Numerical computations
- `matplotlib>=3.6.0` - 2D plotting

### Quick Install

```bash
git clone https://github.com/orafaelmiguel/black-hole-time-dilation.git
cd black-hole-time-dilation
pip install -r requirements.txt
```

## Usage

### Basic Simulation

```bash
python src/main.py
```

### Interactive 3D Visualization

```bash
python src/interactive_ui.py
```

### Demo with Examples

```bash
python src/demo.py
```

### Command Line Options

```bash
python src/demo.py --help
python src/demo.py --basic    
python src/demo.py --plot     
python src/demo.py --3d       
```

## Architecture

### Project Structure

```
black-hole-time-dilation/
├── src/
│   ├── physics.py          # Core physics calculations
│   ├── visualization.py    # 2D and 3D rendering
│   ├── interactive_ui.py   # Interactive GUI controls
│   ├── utils.py           # Helper functions
│   ├── main.py            # Entry point
│   └── demo.py            # Demonstration suite
├── requirements.txt
└── README.md
```

## Visualization Features

### 2D Graph
- X-axis: Distance from black hole (km)
- Y-axis: Time dilation factor (t₀/tf)
- Red dashed line: Schwarzschild radius (event horizon)
- Orange dashed line: Photon sphere
- Green dashed line: ISCO

### 3D Simulation
- Central black sphere: Black hole
- Colored orbiting spheres: Test particles
- Color gradient: Red (slow time) to Blue (normal time)
- Trail effects: Orbital paths
- Differential rotation speeds based on time dilation

### Interactive Controls
- **Mass Slider**: Adjust black hole mass (1-100 solar masses)
- **Orbit Slider**: Number of orbiting objects (1-10)
- **Speed Slider**: Animation speed multiplier (0.1x-5x)
- **Pause/Resume**: Control animation state
- **Reset**: Return to initial configuration
- **Presets**: Load known black hole configurations

## References

- Schwarzschild, K. (1916). "Über das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie"
- Misner, C. W., Thorne, K. S., & Wheeler, J. A. (1973). "Gravitation"
- Carroll, S. (2004). "Spacetime and Geometry: An Introduction to General Relativity"
- VPython Documentation: https://vpython.org
- NumPy Documentation: https://numpy.org
- Matplotlib Documentation: https://matplotlib.org
