# 🧭 Fase 5 — Interface e Parâmetros Dinâmicos

## Objetivo
Adicionar controles interativos para ajustar parâmetros da simulação em tempo real, permitindo exploração dinâmica dos efeitos de dilatação temporal.

## Funcionalidades a Implementar

### 1. Controles de Interface VPython

#### Sliders Principais
```python
from vpython import slider, wtext, button, menu

# Slider para massa do buraco negro
mass_slider = slider(
    min=1,
    max=100,
    value=10,
    bind=update_mass,
    pos=scene.title_anchor,
    length=200,
    width=10
)

# Slider para número de órbitas
orbit_slider = slider(
    min=1,
    max=10,
    value=4,
    bind=update_orbits,
    pos=scene.title_anchor
)

# Slider para velocidade da animação
speed_slider = slider(
    min=0.1,
    max=5.0,
    value=1.0,
    bind=update_speed,
    pos=scene.title_anchor
)
```

### 2. Funções de Atualização Dinâmica

```python
def update_mass(slider_obj):
    """Atualiza a massa do buraco negro em tempo real."""
    global current_mass, rs, scale_factor
    
    current_mass = slider_obj.value
    rs = schwarzschild_radius(current_mass)
    scale_factor = 10 / rs
    
    # Atualizar visualização
    blackhole.radius = rs * scale_factor
    event_horizon.radius = rs * scale_factor * 1.01
    
    # Recalcular órbitas
    recalculate_orbits()
    
    # Atualizar labels
    mass_label.text = f"Massa: {current_mass:.1f} M☉"
    info_label.text = f"Rs = {rs:.2f} km"

def update_orbits(slider_obj):
    """Atualiza o número de órbitas exibidas."""
    global num_orbits
    num_orbits = int(slider_obj.value)
    recreate_orbital_objects()

def update_speed(slider_obj):
    """Ajusta a velocidade da animação."""
    global animation_speed
    animation_speed = slider_obj.value
```

### 3. Painel de Informações em Tempo Real

```python
# Criar painel de informações
info_panel = wtext(
    text="",
    pos=scene.title_anchor,
    height=10
)

def update_info_panel():
    """Atualiza o painel com informações atuais."""
    info_text = f"""
    Buraco Negro: {current_mass:.1f} M☉
    Raio de Schwarzschild: {rs:.2f} km
    Esfera de Fótons: {photon_sphere_radius(current_mass):.2f} km
    Órbita Estável Mínima: {innermost_stable_orbit(current_mass):.2f} km
    Órbitas Ativas: {num_orbits}
    """
    info_panel.text = info_text
```

### 4. Menu de Opções Avançadas

```python
# Menu dropdown para modos de visualização
def menu_handler(menu_choice):
    if menu_choice == "Órbitas Circulares":
        set_circular_orbits()
    elif menu_choice == "Órbitas Elípticas":
        set_elliptical_orbits()
    elif menu_choice == "Trajetórias de Queda":
        set_falling_trajectories()
    elif menu_choice == "Campo de Distorção":
        show_distortion_field()

visualization_menu = menu(
    choices=["Órbitas Circulares", "Órbitas Elípticas", 
             "Trajetórias de Queda", "Campo de Distorção"],
    bind=menu_handler,
    pos=scene.title_anchor
)
```

### 5. Controles de Câmera

```python
# Botões para controle de câmera
def reset_camera():
    scene.forward = vector(-1, -0.5, -1).norm()
    scene.up = vector(0, 1, 0)
    scene.range = 20

def toggle_rotation():
    global auto_rotate
    auto_rotate = not auto_rotate
    rotate_button.text = "Parar Rotação" if auto_rotate else "Iniciar Rotação"

camera_reset_button = button(
    text="Resetar Câmera",
    bind=reset_camera,
    pos=scene.title_anchor
)

rotate_button = button(
    text="Iniciar Rotação",
    bind=toggle_rotation,
    pos=scene.title_anchor
)
```

### 6. Sistema de Presets

```python
# Presets de buracos negros conhecidos
presets = {
    "Cygnus X-1": 21,
    "GW150914": 36,
    "Sagittarius A*": 4.3e6,
    "M87*": 6.5e9,
    "Personalizado": None
}

def apply_preset(preset_choice):
    if preset_choice in presets and presets[preset_choice]:
        mass_slider.value = presets[preset_choice]
        update_mass(mass_slider)

preset_menu = menu(
    choices=list(presets.keys()),
    bind=apply_preset,
    pos=scene.title_anchor
)
```

### 7. Visualização de Dados em Tempo Real

```python
# Gráfico de dilatação temporal embarcado
from vpython import graph, gcurve

time_graph = graph(
    title="Dilatação Temporal vs Distância",
    xtitle="Distância (Rs)",
    ytitle="Fator de Dilatação",
    width=400,
    height=250,
    align="right"
)

dilation_curve = gcurve(
    graph=time_graph,
    color=color.cyan
)

def update_graph():
    """Atualiza o gráfico de dilatação temporal."""
    dilation_curve.delete()
    
    rs = schwarzschild_radius(current_mass)
    for r_factor in np.linspace(1.01, 10, 100):
        r = r_factor * rs
        factor = time_dilation(r, rs)
        dilation_curve.plot(r_factor, factor)
```

### 8. Sistema de Salvamento/Carregamento

```python
import json

def save_configuration():
    """Salva a configuração atual em arquivo JSON."""
    config = {
        "mass": current_mass,
        "num_orbits": num_orbits,
        "animation_speed": animation_speed,
        "camera_position": {
            "forward": [scene.forward.x, scene.forward.y, scene.forward.z],
            "up": [scene.up.x, scene.up.y, scene.up.z],
            "range": scene.range
        }
    }
    
    with open("simulation_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("Configuração salva!")

def load_configuration():
    """Carrega configuração de arquivo JSON."""
    try:
        with open("simulation_config.json", "r") as f:
            config = json.load(f)
        
        mass_slider.value = config["mass"]
        orbit_slider.value = config["num_orbits"]
        speed_slider.value = config["animation_speed"]
        
        # Restaurar câmera
        cam = config["camera_position"]
        scene.forward = vector(*cam["forward"])
        scene.up = vector(*cam["up"])
        scene.range = cam["range"]
        
        print("Configuração carregada!")
    except FileNotFoundError:
        print("Arquivo de configuração não encontrado")
```

### 9. Modo de Comparação

```python
comparison_mode = False

def toggle_comparison():
    """Alterna entre modo normal e comparação."""
    global comparison_mode
    comparison_mode = not comparison_mode
    
    if comparison_mode:
        # Criar segundo buraco negro para comparação
        create_comparison_blackhole()
        compare_button.text = "Sair da Comparação"
    else:
        # Remover objetos de comparação
        remove_comparison_objects()
        compare_button.text = "Modo Comparação"

compare_button = button(
    text="Modo Comparação",
    bind=toggle_comparison,
    pos=scene.title_anchor
)
```

### 10. Implementação Completa - Arquivo `interactive_ui.py`

```python
from vpython import *
import numpy as np
from physics import *
from utils import *

class InteractiveBlackHoleSimulation:
    def __init__(self, initial_mass=10):
        self.mass = initial_mass
        self.num_orbits = 4
        self.animation_speed = 1.0
        self.auto_rotate = False
        self.running = True
        self.comparison_mode = False
        
        self.setup_scene()
        self.create_controls()
        self.create_objects()
        self.run()
    
    def setup_scene(self):
        """Configura a cena VPython."""
        scene.title = "Simulação Interativa de Buraco Negro"
        scene.width = 1400
        scene.height = 900
        scene.background = color.black
        scene.range = 20
        
        # Adicionar iluminação
        scene.lights = []
        scene.ambient = color.gray(0.2)
        distant_light(direction=vector(1, 1, 1), color=color.white)
    
    def create_controls(self):
        """Cria todos os controles interativos."""
        # Slider de massa
        self.mass_slider = slider(
            min=1, max=100, value=self.mass,
            bind=self.update_mass,
            pos=scene.title_anchor,
            length=250, width=15
        )
        
        # Labels
        self.mass_label = wtext(
            text=f"Massa: {self.mass:.1f} M☉",
            pos=scene.title_anchor
        )
        
        # Botões
        self.pause_button = button(
            text="Pausar",
            bind=self.toggle_pause,
            pos=scene.title_anchor
        )
        
        self.reset_button = button(
            text="Resetar",
            bind=self.reset_simulation,
            pos=scene.title_anchor
        )
        
        # Menu de presets
        self.preset_menu = menu(
            choices=["Personalizado", "Cygnus X-1", "Sagittarius A*"],
            bind=self.apply_preset,
            pos=scene.title_anchor
        )
    
    def create_objects(self):
        """Cria os objetos da simulação."""
        self.rs = schwarzschild_radius(self.mass)
        self.scale_factor = 10 / self.rs
        
        # Buraco negro
        self.blackhole = sphere(
            pos=vector(0, 0, 0),
            radius=self.rs * self.scale_factor,
            color=color.black,
            emissive=True
        )
        
        # Horizonte de eventos
        self.event_horizon = sphere(
            pos=vector(0, 0, 0),
            radius=self.rs * self.scale_factor * 1.01,
            color=color.red,
            opacity=0.15
        )
        
        # Criar órbitas
        self.create_orbits()
    
    def create_orbits(self):
        """Cria objetos orbitantes."""
        self.orbits = []
        radii = np.linspace(self.rs * 1.5, self.rs * 5, self.num_orbits)
        
        for r in radii:
            factor = time_dilation(r, self.rs)
            
            # Cor baseada na dilatação
            if factor < 0.3:
                obj_color = color.red
            elif factor < 0.6:
                obj_color = color.yellow
            else:
                obj_color = color.cyan
            
            orbit_obj = sphere(
                pos=vector(r * self.scale_factor, 0, 0),
                radius=0.3,
                color=obj_color,
                make_trail=True,
                trail_radius=0.05
            )
            
            self.orbits.append({
                'object': orbit_obj,
                'radius': r,
                'angle': 0,
                'factor': factor
            })
    
    def update_mass(self, slider_obj):
        """Atualiza a massa do buraco negro."""
        self.mass = slider_obj.value
        self.rs = schwarzschild_radius(self.mass)
        self.scale_factor = 10 / self.rs
        
        # Atualizar objetos
        self.blackhole.radius = self.rs * self.scale_factor
        self.event_horizon.radius = self.rs * self.scale_factor * 1.01
        
        # Recalcular órbitas
        self.update_orbit_properties()
        
        # Atualizar label
        self.mass_label.text = f"Massa: {self.mass:.1f} M☉"
    
    def update_orbit_properties(self):
        """Recalcula propriedades das órbitas."""
        for orbit in self.orbits:
            orbit['factor'] = time_dilation(orbit['radius'], self.rs)
            
            # Atualizar cor
            factor = orbit['factor']
            if factor < 0.3:
                orbit['object'].color = color.red
            elif factor < 0.6:
                orbit['object'].color = color.yellow
            else:
                orbit['object'].color = color.cyan
    
    def toggle_pause(self):
        """Pausa/retoma a simulação."""
        self.running = not self.running
        self.pause_button.text = "Retomar" if not self.running else "Pausar"
    
    def reset_simulation(self):
        """Reseta a simulação."""
        # Limpar trilhas
        for orbit in self.orbits:
            orbit['object'].clear_trail()
            orbit['angle'] = 0
        
        # Resetar câmera
        scene.forward = vector(-1, -0.5, -1).norm()
        scene.up = vector(0, 1, 0)
        scene.range = 20
    
    def apply_preset(self, choice):
        """Aplica um preset de buraco negro."""
        presets = {
            "Cygnus X-1": 21,
            "Sagittarius A*": 4.3e6
        }
        
        if choice in presets:
            self.mass_slider.value = presets[choice]
            self.update_mass(self.mass_slider)
    
    def run(self):
        """Loop principal da simulação."""
        dt = 0.01
        
        while True:
            rate(60)
            
            if self.running:
                for orbit in self.orbits:
                    # Velocidade angular proporcional à dilatação
                    omega = (1 / orbit['radius']**1.5) * 100
                    orbit['angle'] += omega * orbit['factor'] * dt * self.animation_speed
                    
                    # Atualizar posição
                    r_scaled = orbit['radius'] * self.scale_factor
                    orbit['object'].pos = vector(
                        r_scaled * cos(orbit['angle']),
                        0,
                        r_scaled * sin(orbit['angle'])
                    )
            
            # Rotação automática da câmera
            if self.auto_rotate:
                scene.forward = scene.forward.rotate(angle=0.01, axis=vector(0, 1, 0))

# Iniciar simulação
if __name__ == "__main__":
    simulation = InteractiveBlackHoleSimulation(initial_mass=10)
```

## Como Usar a Fase 5

1. **Instalação de Dependências Adicionais**
   ```bash
   pip install vpython numpy matplotlib
   ```

2. **Executar a Simulação Interativa**
   ```bash
   python src/interactive_ui.py
   ```

3. **Controles Disponíveis**
   - **Slider de Massa**: Ajusta a massa do buraco negro (1-100 M☉)
   - **Botão Pausar/Retomar**: Controla a animação
   - **Botão Resetar**: Reinicia a simulação
   - **Menu de Presets**: Seleciona buracos negros conhecidos
   - **Mouse**: Rotaciona e zoom na visualização

## Próximas Melhorias Possíveis

1. **Exportação de Dados**: Salvar dados da simulação em CSV/Excel
2. **Modo Educacional**: Adicionar tooltips e explicações interativas
3. **Simulação de Partículas**: Adicionar sistema de partículas para disco de acreção
4. **Efeitos Visuais**: Implementar lente gravitacional visual
5. **Modo VR**: Suporte para visualização em realidade virtual