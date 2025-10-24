import numpy as np
import matplotlib.pyplot as plt
import math
from vpython import sphere, vector, color, rate, scene, slider, wtext, button, box
from physics import (
    schwarzschild_radius,
    time_dilation,
    photon_sphere_radius,
    innermost_stable_orbit,
)


def plot_dilation(mass_solar: float):
    rs = schwarzschild_radius(mass_solar)
    photon_r = photon_sphere_radius(mass_solar)
    isco_r = innermost_stable_orbit(mass_solar)

    r = np.linspace(rs * 1.01, rs * 10, 1000)

    dilation = [time_dilation(x, rs) for x in r]

    plt.figure(figsize=(12, 7))

    plt.subplot(1, 2, 1)
    plt.plot(r / rs, dilation, "b-", linewidth=2, label="Dilatação temporal")
    plt.axvline(
        1, color="red", linestyle="--", linewidth=2, label="Horizonte de Eventos"
    )
    plt.axvline(
        photon_r / rs,
        color="orange",
        linestyle="--",
        alpha=0.7,
        label="Esfera de Fótons",
    )
    plt.axvline(
        isco_r / rs,
        color="green",
        linestyle="--",
        alpha=0.7,
        label="Órbita Estável Mínima",
    )

    plt.xlabel("Distância (em raios de Schwarzschild)", fontsize=12)
    plt.ylabel("Fator de Dilatação Temporal (t₀/tf)", fontsize=12)
    plt.title(f"Dilatação Temporal - Buraco Negro de {mass_solar} M☉", fontsize=14)
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.xlim(1, 10)
    plt.ylim(0, 1)

    plt.subplot(1, 2, 2)
    plt.semilogy(r / rs, 1 / np.array(dilation) - 1, "r-", linewidth=2)
    plt.axvline(
        1, color="red", linestyle="--", linewidth=2, label="Horizonte de Eventos"
    )
    plt.axvline(
        photon_r / rs,
        color="orange",
        linestyle="--",
        alpha=0.7,
        label="Esfera de Fótons",
    )
    plt.axvline(
        isco_r / rs,
        color="green",
        linestyle="--",
        alpha=0.7,
        label="Órbita Estável Mínima",
    )

    plt.xlabel("Distância (em raios de Schwarzschild)", fontsize=12)
    plt.ylabel("Fator de Desaceleração do Tempo (log)", fontsize=12)
    plt.title(f"Desaceleração Temporal (Escala Log)", fontsize=14)
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.xlim(1, 10)

    plt.tight_layout()
    
    info_text = f"""
    Informações do Buraco Negro:
    • Massa: {mass_solar} massas solares
    • Raio de Schwarzschild: {rs:.2f} km
    • Esfera de Fótons: {photon_r:.2f} km
    • Órbita Estável Mínima: {isco_r:.2f} km
    """
    plt.figtext(
        0.5,
        0.02,
        info_text,
        ha="center",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    plt.show()


def plot_multiple_masses():
    masses = [1, 5, 10, 50, 100]  
    colors_plot = ["blue", "green", "red", "purple", "orange"]

    plt.figure(figsize=(10, 6))

    for mass, color_plot in zip(masses, colors_plot):
        rs = schwarzschild_radius(mass)
        r = np.linspace(rs * 1.01, rs * 10, 500)
        dilation = [time_dilation(x, rs) for x in r]

        plt.plot(
            r / rs,
            dilation,
            color=color_plot,
            linewidth=2,
            label=f"{mass} M☉ (rs = {rs:.0f} km)",
        )

    plt.axvline(1, color="red", linestyle="--", linewidth=1.5, alpha=0.5)
    plt.text(
        1.02,
        0.5,
        "Horizonte\nde Eventos",
        rotation=90,
        verticalalignment="center",
        fontsize=9,
        alpha=0.7,
    )

    plt.xlabel("Distância (em raios de Schwarzschild)", fontsize=12)
    plt.ylabel("Fator de Dilatação Temporal (t₀/tf)", fontsize=12)
    plt.title("Comparação de Dilatação Temporal para Diferentes Massas", fontsize=14)
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.xlim(1, 10)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()


def visualize_orbits(mass_solar: float, num_orbits: int = 4):
    scene.title = f"Dilatação Temporal - Buraco Negro de {mass_solar} M☉"
    scene.width = 1000
    scene.height = 700
    scene.background = color.black
    scene.caption = """
    Simulação de Dilatação Temporal em torno de um Buraco Negro

    As cores representam a dilatação temporal:
    • Vermelho: Tempo muito lento (próximo ao horizonte de eventos)
    • Amarelo/Verde: Tempo moderadamente afetado
    • Azul: Tempo quase normal (longe do buraco negro)

    A velocidade orbital também é afetada pela dilatação temporal.
    """

    rs = schwarzschild_radius(mass_solar)
    scale_factor = 10 / rs  

    blackhole = sphere(
        pos=vector(0, 0, 0),
        radius=1 * scale_factor * rs,
        color=color.black,
        emissive=True,
    )

    accretion_disk = box(
        pos=vector(0, 0, 0),
        size=vector(6 * scale_factor * rs, 0.1, 6 * scale_factor * rs),
        color=vector(0.5, 0.2, 0.1),
        opacity=0.3,
    )

    event_horizon = sphere(
        pos=vector(0, 0, 0),
        radius=1.01 * scale_factor * rs,
        color=color.red,
        opacity=0.2,
    )

    photon_r = photon_sphere_radius(mass_solar)
    photon_sphere = sphere(
        pos=vector(0, 0, 0),
        radius=scale_factor * photon_r,
        color=color.orange,
        opacity=0.1,
    )

    orbit_radii = np.linspace(rs * 1.5, rs * 5, num_orbits)
    planets = []

    for i, r in enumerate(orbit_radii):
        factor = time_dilation(r, rs)

        if factor < 0.3:
            planet_color = color.red
        elif factor < 0.5:
            planet_color = color.orange
        elif factor < 0.7:
            planet_color = color.yellow
        else:
            planet_color = color.cyan

        planet = sphere(
            pos=vector(r * scale_factor, 0, 0),
            radius=0.3,
            color=planet_color,
            make_trail=True,
            trail_radius=0.05,
            retain=100,
        )

        planet.label = wtext(
            text=f"r={r / rs:.1f}rs\nΔt={factor:.3f}",
            pos=planet.pos,
            height=7,
            color=color.white,
            opacity=0.7,
        )

        planets.append(
            {
                "sphere": planet,
                "radius": r,
                "factor": factor,
                "angle": 0,
                "angular_velocity": math.sqrt(1 / r**3)
                * 1000, 
            }
        )

    running = True
    speed_factor = 1.0

    def toggle_pause():
        nonlocal running
        running = not running
        pause_button.text = "Play" if not running else "Pause"

    pause_button = button(text="Pause", bind=toggle_pause, pos=scene.title_anchor)

    def set_speed(s):
        nonlocal speed_factor
        speed_factor = s.value
        speed_label.text = f"Velocidade: {s.value:.1f}x"

    speed_slider = slider(
        min=0.1, max=5.0, value=1.0, bind=set_speed, pos=scene.title_anchor
    )

    speed_label = wtext(text="Velocidade: 1.0x", pos=scene.title_anchor)

    dt = 0.01
    while True:
        rate(60)

        if running:
            for planet_data in planets:
                planet_data["angle"] += (
                    planet_data["angular_velocity"]
                    * planet_data["factor"]
                    * dt
                    * speed_factor
                )

                r_scaled = planet_data["radius"] * scale_factor
                planet_data["sphere"].pos = vector(
                    r_scaled * math.cos(planet_data["angle"]),
                    0,
                    r_scaled * math.sin(planet_data["angle"]),
                )

                planet_data["sphere"].label.pos = planet_data["sphere"].pos


def create_interactive_simulation(mass_solar: float = 10):
    scene.title = "Simulação Interativa de Buraco Negro"
    scene.width = 1200
    scene.height = 800
    scene.background = color.black
    scene.range = 20

    current_mass = mass_solar
    rs = schwarzschild_radius(current_mass)
    scale_factor = 10 / rs

    blackhole = sphere(pos=vector(0, 0, 0), radius=1, color=color.black, emissive=True)

    event_horizon = sphere(
        pos=vector(0, 0, 0), radius=1.01, color=color.red, opacity=0.15
    )

    grid_size = 20
    grid_points = []

    for x in range(-grid_size // 2, grid_size // 2 + 1, 2):
        for z in range(-grid_size // 2, grid_size // 2 + 1, 2):
            if x != 0 or z != 0:  
                distance = math.sqrt(x**2 + z**2)
                if distance > 1.5:  
                    point = sphere(pos=vector(x, 0, z), radius=0.2, color=color.white)
                    grid_points.append(
                        {
                            "sphere": point,
                            "original_pos": vector(x, 0, z),
                            "distance": distance,
                        }
                    )

    def update_colors():
        nonlocal rs
        rs = schwarzschild_radius(current_mass)

        for point_data in grid_points:
            distance_km = point_data["distance"] / scale_factor
            if distance_km > rs:
                factor = time_dilation(distance_km, rs)
                hue = 0.7 * factor  
                point_data["sphere"].color = color.hsv_to_rgb(vector(hue, 1, 1))
            else:
                point_data["sphere"].color = color.black

    def set_mass(s):
        nonlocal current_mass
        current_mass = s.value
        mass_label.text = f"Massa: {s.value:.1f} M☉"
        blackhole.radius = schwarzschild_radius(current_mass) * scale_factor
        event_horizon.radius = blackhole.radius * 1.01
        update_colors()

    mass_slider = slider(
        min=1, max=100, value=mass_solar, bind=set_mass, pos=scene.title_anchor
    )

    mass_label = wtext(text=f"Massa: {mass_solar} M☉", pos=scene.title_anchor)

    update_colors()

    theta = 0
    while True:
        rate(30)
        theta += 0.01
        scene.forward = vector(
            -1 * math.sin(theta) * math.cos(0.3),
            -math.sin(0.3),
            -1 * math.cos(theta) * math.cos(0.3),
        )
