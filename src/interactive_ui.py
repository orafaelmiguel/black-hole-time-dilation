#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vpython import *
import numpy as np
import math
from physics import (
    schwarzschild_radius,
    time_dilation,
    photon_sphere_radius,
    innermost_stable_orbit,
    orbital_period,
    escape_velocity,
)
from utils import format_time, format_distance, interpolate_color, generate_orbit_data


class InteractiveBlackHoleSimulation:
    def __init__(self, initial_mass=10):
        self.mass = initial_mass
        self.num_orbits = 4
        self.animation_speed = 1.0
        self.auto_rotate = False
        self.running = True
        self.comparison_mode = False
        self.show_trails = True
        self.show_labels = True

        self.orbits = []
        self.labels = []
        self.comparison_objects = []

        self.setup_scene()
        self.create_ui_controls()
        self.create_objects()
        self.create_info_display()
        self.run()

    def setup_scene(self):
        scene.title = "Simulação buraco negro"
        scene.width = 1400
        scene.height = 900
        scene.background = color.black
        scene.range = 25
        scene.forward = vector(-1, -0.3, -1).norm()
        scene.up = vector(0, 1, 0)

        scene.lights = []
        scene.ambient = color.gray(0.1)
        distant_light(direction=vector(1, 1, 1), color=color.gray(0.8))
        distant_light(direction=vector(-1, -0.5, -1), color=color.gray(0.3))

    def create_ui_controls(self):
        scene.append_to_title(
            '<div style="background: linear-gradient(45deg, #1a1a2e, #16213e); padding: 10px; border-radius: 5px;">'
        )
        scene.append_to_title(
            '<h3 style="color: #fff; margin: 5px;">Controles da Simulação</h3>'
        )

        scene.append_to_title('<div style="margin: 10px 0;">')
        scene.append_to_title(
            '<span style="color: #fff;">Massa do Buraco Negro: </span>'
        )
        self.mass_label = wtext(text=f"{self.mass:.1f} M☉", pos=scene.title_anchor)
        scene.append_to_title("</div>")

        self.mass_slider = slider(
            min=1,
            max=100,
            value=self.mass,
            bind=self.update_mass,
            pos=scene.title_anchor,
            length=300,
            width=15,
            left=10,
            right=10,
        )

        scene.append_to_title('<div style="margin: 10px 0;">')
        scene.append_to_title('<span style="color: #fff;">Número de Órbitas: </span>')
        self.orbit_label = wtext(text=f"{self.num_orbits}", pos=scene.title_anchor)
        scene.append_to_title("</div>")

        self.orbit_slider = slider(
            min=1,
            max=10,
            value=self.num_orbits,
            bind=self.update_num_orbits,
            pos=scene.title_anchor,
            length=300,
            width=15,
        )

        scene.append_to_title('<div style="margin: 10px 0;">')
        scene.append_to_title(
            '<span style="color: #fff;">Velocidade da Animação: </span>'
        )
        self.speed_label = wtext(
            text=f"{self.animation_speed:.1f}x", pos=scene.title_anchor
        )
        scene.append_to_title("</div>")

        self.speed_slider = slider(
            min=0.1,
            max=5.0,
            value=self.animation_speed,
            bind=self.update_speed,
            pos=scene.title_anchor,
            length=300,
            width=15,
        )
        scene.append_to_title('<div style="margin: 15px 0;">')

        self.pause_button = button(
            text="⏸ Pausar", bind=self.toggle_pause, pos=scene.title_anchor
        )

        scene.append_to_title(" ")

        self.reset_button = button(
            text="🔄 Resetar", bind=self.reset_simulation, pos=scene.title_anchor
        )

        scene.append_to_title(" ")

        self.rotate_button = button(
            text="🔄 Auto-Rotação", bind=self.toggle_rotation, pos=scene.title_anchor
        )

        scene.append_to_title("</div>")

        scene.append_to_title('<div style="margin: 10px 0;">')
        scene.append_to_title(
            '<span style="color: #fff;">Presets de Buracos Negros: </span>'
        )

        self.preset_menu = menu(
            choices=[
                "Personalizado",
                "Buraco Negro Estelar Mínimo (3 M☉)",
                "Cygnus X-1 (21 M☉)",
                "GW150914 (36 M☉)",
                "Buraco Negro Intermediário (100 M☉)",
            ],
            bind=self.apply_preset,
            pos=scene.title_anchor,
        )

        scene.append_to_title("</div>")

        scene.append_to_title('<div style="margin: 10px 0;">')

        self.trail_checkbox = checkbox(
            bind=self.toggle_trails,
            text="Mostrar Trilhas",
            checked=self.show_trails,
            pos=scene.title_anchor,
        )

        scene.append_to_title(" ")

        self.label_checkbox = checkbox(
            bind=self.toggle_labels,
            text="Mostrar Rótulos",
            checked=self.show_labels,
            pos=scene.title_anchor,
        )

        scene.append_to_title("</div>")

        scene.append_to_title('<div style="margin: 10px 0;">')
        scene.append_to_title(
            '<span style="color: #fff;">Modo de Visualização: </span>'
        )

        self.viz_menu = menu(
            choices=["Órbitas Circulares", "Órbitas Elípticas", "Grade de Distorção"],
            bind=self.change_visualization,
            pos=scene.title_anchor,
        )

        scene.append_to_title("</div>")
        scene.append_to_title("</div>")

    def create_objects(self):
        self.rs = schwarzschild_radius(self.mass)
        self.scale_factor = 15 / self.rs if self.rs > 0 else 1

        self.blackhole = sphere(
            pos=vector(0, 0, 0),
            radius=self.rs * self.scale_factor,
            color=color.black,
            emissive=False,
        )

        self.event_horizon = sphere(
            pos=vector(0, 0, 0),
            radius=self.rs * self.scale_factor * 1.01,
            color=color.red,
            opacity=0.2,
        )

        photon_r = photon_sphere_radius(self.mass)
        self.photon_sphere = sphere(
            pos=vector(0, 0, 0),
            radius=photon_r * self.scale_factor,
            color=color.orange,
            opacity=0.1,
        )

        self.accretion_disk = cylinder(
            pos=vector(0, 0, 0),
            axis=vector(0, 0.05, 0),
            radius=self.rs * self.scale_factor * 4,
            color=vector(0.8, 0.4, 0.1),
            opacity=0.3,
        )

        self.create_orbits()

    def create_orbits(self):
        for orbit in self.orbits:
            orbit["object"].visible = False
            if orbit.get("label"):
                orbit["label"].visible = False
            del orbit["object"]
        self.orbits.clear()

        radii = np.linspace(self.rs * 1.5, self.rs * 6, self.num_orbits)

        for i, r in enumerate(radii):
            factor = time_dilation(r, self.rs)

            orbit_color = color.hsv_to_rgb(vector(0.7 * factor, 1, 1))

            orbit_obj = sphere(
                pos=vector(r * self.scale_factor, 0, 0),
                radius=0.4,
                color=orbit_color,
                make_trail=self.show_trails,
                trail_radius=0.05,
                retain=150,
                emissive=True,
            )

            if self.show_labels:
                label_text = f"r={r / self.rs:.1f}Rs\nΔt={factor:.3f}"
                orbit_label = label(
                    pos=orbit_obj.pos,
                    text=label_text,
                    height=10,
                    color=color.white,
                    opacity=0.8,
                    box=False,
                    line=False,
                )
            else:
                orbit_label = None

            v_orbital = math.sqrt(1 / r**1.5) * 500 if r > 0 else 0

            self.orbits.append(
                {
                    "object": orbit_obj,
                    "radius": r,
                    "angle": np.random.uniform(
                        0, 2 * np.pi
                    ),  
                    "factor": factor,
                    "angular_velocity": v_orbital,
                    "label": orbit_label,
                }
            )

    def create_info_display(self):
        self.info_panel = wtext(text="", pos=scene.caption_anchor)

        scene.caption = '<div style="background: rgba(0,0,0,0.8); color: #fff; padding: 10px; border-radius: 5px; font-family: monospace;">'
        scene.caption += "<h4>📊 Informações do Sistema</h4>"
        scene.caption += "</div>"

        self.update_info_display()

    def update_info_display(self):
        rs_km = self.rs
        photon_r = photon_sphere_radius(self.mass)
        isco_r = innermost_stable_orbit(self.mass)

        info_text = f"""
        <div style="background: rgba(0,0,0,0.8); color: #fff; padding: 10px; border-radius: 5px; font-family: monospace;">
        <b>Propriedades do Buraco Negro:</b><br>
        • Massa: {self.mass:.1f} M☉<br>
        • Raio de Schwarzschild: {format_distance(rs_km)}<br>
        • Esfera de Fótons: {format_distance(photon_r)} ({photon_r / rs_km:.1f}Rs)<br>
        • Órbita Estável Mínima: {format_distance(isco_r)} ({isco_r / rs_km:.1f}Rs)<br>
        <br>
        <b>Controles do Mouse:</b><br>
        • Arrastar: Rotacionar câmera<br>
        • Scroll: Zoom in/out<br>
        • Botão direito: Pan<br>
        <br>
        <b>Legenda de Cores:</b><br>
        🔴 Vermelho: Tempo muito lento (próximo ao horizonte)<br>
        🟡 Amarelo: Tempo moderadamente afetado<br>
        🔵 Azul/Ciano: Tempo quase normal<br>
        </div>
        """

        self.info_panel.text = info_text

    def update_mass(self, slider_obj):
        self.mass = slider_obj.value
        self.mass_label.text = f"{self.mass:.1f} M☉"

        self.rs = schwarzschild_radius(self.mass)
        self.scale_factor = 15 / self.rs if self.rs > 0 else 1

        self.blackhole.radius = self.rs * self.scale_factor
        self.event_horizon.radius = self.rs * self.scale_factor * 1.01
        self.photon_sphere.radius = photon_sphere_radius(self.mass) * self.scale_factor
        self.accretion_disk.radius = self.rs * self.scale_factor * 4

        self.update_orbit_properties()

        self.update_info_display()

    def update_num_orbits(self, slider_obj):
        self.num_orbits = int(slider_obj.value)
        self.orbit_label.text = f"{self.num_orbits}"
        self.create_orbits()

    def update_speed(self, slider_obj):
        self.animation_speed = slider_obj.value
        self.speed_label.text = f"{self.animation_speed:.1f}x"

    def update_orbit_properties(self):
        for orbit in self.orbits:
            orbit["factor"] = time_dilation(orbit["radius"], self.rs)

            orbit["object"].color = color.hsv_to_rgb(
                vector(0.7 * orbit["factor"], 1, 1)
            )

            if orbit.get("label"):
                label_text = (
                    f"r={orbit['radius'] / self.rs:.1f}Rs\nΔt={orbit['factor']:.3f}"
                )
                orbit["label"].text = label_text

    def toggle_pause(self):
        self.running = not self.running
        self.pause_button.text = "▶ Retomar" if not self.running else "⏸ Pausar"

    def toggle_rotation(self):
        self.auto_rotate = not self.auto_rotate
        self.rotate_button.text = (
            "⏹ Parar Rotação" if self.auto_rotate else "🔄 Auto-Rotação"
        )

    def toggle_trails(self, checkbox_obj):
        self.show_trails = checkbox_obj.checked
        for orbit in self.orbits:
            orbit["object"].make_trail = self.show_trails
            if not self.show_trails:
                orbit["object"].clear_trail()

    def toggle_labels(self, checkbox_obj):
        self.show_labels = checkbox_obj.checked
        for orbit in self.orbits:
            if orbit.get("label"):
                orbit["label"].visible = self.show_labels

    def reset_simulation(self):
        for orbit in self.orbits:
            orbit["object"].clear_trail()
            orbit["angle"] = np.random.uniform(0, 2 * np.pi)

        scene.forward = vector(-1, -0.3, -1).norm()
        scene.up = vector(0, 1, 0)
        scene.range = 25

        self.animation_speed = 1.0
        self.speed_slider.value = 1.0
        self.speed_label.text = "1.0x"

    def apply_preset(self, choice):
        presets = {
            "Buraco Negro Estelar Mínimo (3 M☉)": 3,
            "Cygnus X-1 (21 M☉)": 21,
            "GW150914 (36 M☉)": 36,
            "Buraco Negro Intermediário (100 M☉)": 100,
        }

        if choice in presets:
            self.mass_slider.value = presets[choice]
            self.update_mass(self.mass_slider)

    def change_visualization(self, choice):
        if choice == "Órbitas Circulares":
            self.create_orbits()
        elif choice == "Órbitas Elípticas":
            self.create_elliptical_orbits()
        elif choice == "Grade de Distorção":
            self.create_distortion_grid()

    def create_elliptical_orbits(self):
        self.create_orbits()
        print("Órbitas elípticas serão implementadas em uma versão futura")

    def create_distortion_grid(self):
        self.create_orbits()
        print("Grade de distorção será implementada em uma versão futura")

    def run(self):
        dt = 0.01
        camera_angle = 0

        while True:
            rate(60)  
            if self.running:
                for orbit in self.orbits:
                    omega = orbit["angular_velocity"] * orbit["factor"]
                    orbit["angle"] += omega * dt * self.animation_speed

                    r_scaled = orbit["radius"] * self.scale_factor
                    x = r_scaled * math.cos(orbit["angle"])
                    z = r_scaled * math.sin(orbit["angle"])
                    orbit["object"].pos = vector(x, 0, z)

                    if orbit.get("label") and self.show_labels:
                        orbit["label"].pos = orbit["object"].pos

            if self.auto_rotate:
                camera_angle += 0.005
                scene.forward = vector(
                    math.sin(camera_angle), -0.3, math.cos(camera_angle)
                ).norm()


def main():
    print("=" * 60)
    print("SIMULAÇÃO INTERATIVA DE BURACO NEGRO - FASE 5")
    print("=" * 60)
    print("\nIniciando simulação interativa...")
    print("Use os controles na janela para ajustar os parâmetros.")
    print("Feche a janela para encerrar a simulação.\n")

    simulation = InteractiveBlackHoleSimulation(initial_mass=10)


if __name__ == "__main__":
    main()
