#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from physics import (
    schwarzschild_radius,
    time_dilation,
    escape_velocity,
    orbital_period,
    gravitational_redshift,
    tidal_force,
    photon_sphere_radius,
    innermost_stable_orbit,
)
from visualization import (
    plot_dilation,
    plot_multiple_masses,
    visualize_orbits,
    create_interactive_simulation,
)
from utils import (
    format_time,
    format_distance,
    calculate_safe_distance,
    compare_time_passages,
    generate_orbit_data,
    calculate_event_horizon_properties,
    create_data_table,
    estimate_spaghettification_distance,
)


def print_header(title):
    print("\n" + "=" * 70)
    print(f" {title.center(68)} ")
    print("=" * 70 + "\n")


def demo_basic_calculations():
    print_header("CÁLCULOS BÁSICOS DE FÍSICA")

    masses = [
        (3, "Buraco Negro Estelar Mínimo"),
        (10, "Buraco Negro Estelar Típico"),
        (50, "Buraco Negro Estelar Massivo"),
        (4.3e6, "Sagittarius A* (Centro da Via Láctea)"),
    ]

    for mass, description in masses:
        print(f"\n{description} ({mass} M☉)")
        print("-" * 50)

        rs = schwarzschild_radius(mass)
        photon_r = photon_sphere_radius(mass)
        isco_r = innermost_stable_orbit(mass)

        print(f"• Raio de Schwarzschild: {format_distance(rs)}")
        print(f"• Esfera de Fótons: {format_distance(photon_r)}")
        print(f"• Órbita Estável Mínima: {format_distance(isco_r)}")

        for factor in [1.5, 3, 10]:
            r = rs * factor
            v_esc = escape_velocity(r, mass)
            v_esc_c = v_esc / 299_792_458
            print(f"• Velocidade de escape a {factor}×Rs: {v_esc_c:.3f}c")


def demo_time_dilation_effects():
    print_header("EFEITOS DE DILATAÇÃO TEMPORAL")

    mass = 10
    rs = schwarzschild_radius(mass)

    print(f"Buraco Negro de {mass} M☉ (Rs = {format_distance(rs)})\n")

    distances_rs = [1.001, 1.1, 1.5, 2, 3, 5, 10, 100]

    print(
        f"{'Distância':<12} {'Dilatação':<15} {'1h na Terra':<20} {'1 ano na Terra':<20}"
    )
    print("-" * 70)

    for d_rs in distances_rs:
        d_km = d_rs * rs
        factor = time_dilation(d_km, rs)

        if factor > 0:
            hour_local = factor * 3600  # segundos
            year_local = factor * 365.25 * 24 * 3600  # segundos

            hour_str = format_time(hour_local)
            year_str = format_time(year_local)
        else:
            hour_str = "Tempo parado"
            year_str = "Tempo parado"

        print(f"{d_rs:<12.3f}Rs  {factor:<15.6f}  {hour_str:<20}  {year_str:<20}")


def demo_orbital_mechanics():
    print_header("MECÂNICA ORBITAL")

    mass = 10  
    orbit_data = generate_orbit_data(mass, 6)

    print(f"Órbitas ao redor de um Buraco Negro de {mass} M☉\n")
    print(f"{'Raio':<10} {'Período':<20} {'Velocidade':<15} {'Dilatação':<12}")
    print("-" * 60)

    for orbit in orbit_data:
        print(
            f"{orbit['radius_rs']:<10.1f}Rs  "
            f"{orbit['orbital_period_formatted']:<20}  "
            f"{orbit['orbital_velocity_c']:<15.3f}c  "
            f"{orbit['time_dilation']:<12.4f}"
        )


def demo_extreme_gravity_effects():
    print_header("EFEITOS DE GRAVIDADE EXTREMA")

    masses = [10, 100, 1000]

    for mass in masses:
        rs = schwarzschild_radius(mass)
        spaghetti_dist = estimate_spaghettification_distance(mass, 2.0)

        print(f"\nBuraco Negro de {mass} M☉:")
        print(f"• Raio de Schwarzschild: {format_distance(rs)}")
        print(
            f"• Distância de Espaguetificação (humano): {format_distance(spaghetti_dist)}"
        )
        print(f"• Razão Espaguetificação/Rs: {spaghetti_dist / rs:.2f}")

        for factor in [1.5, 3, 10]:
            r = rs * factor
            tidal = tidal_force(r, mass, 2.0)
            print(
                f"• Força de maré a {factor}×Rs: {tidal:.2e} m/s² ({tidal / 9.81:.1f}g)"
            )


def demo_redshift():
    print_header("DESVIO GRAVITACIONAL (REDSHIFT)")

    mass = 10  
    rs = schwarzschild_radius(mass)

    print(f"Buraco Negro de {mass} M☉\n")
    print(f"{'Distância':<15} {'Redshift (z)':<15} {'Comprimento de Onda':<20}")
    print("-" * 50)

    distances_rs = [1.1, 1.5, 2, 3, 5, 10, 100]

    for d_rs in distances_rs:
        d_km = d_rs * rs
        z = gravitational_redshift(d_km, rs)
        wavelength_factor = 1 + z

        print(f"{d_rs:<15.1f}Rs  {z:<15.3f}  λ × {wavelength_factor:.3f}")


def demo_comparison_table():
    print_header("COMPARAÇÃO DE BURACOS NEGROS")

    black_holes = [
        ("GW150914 (1º BN)", 36),
        ("Cygnus X-1", 21),
        ("Sagittarius A*", 4.3e6),
        ("M87*", 6.5e9),
    ]

    print(f"{'Nome':<20} {'Massa (M☉)':<15} {'Rs':<20} {'Esfera Fótons':<20}")
    print("-" * 75)

    for name, mass in black_holes:
        rs = schwarzschild_radius(mass)
        photon_r = photon_sphere_radius(mass)

        if mass >= 1e6:
            mass_str = f"{mass:.1e}"
        else:
            mass_str = f"{mass:.0f}"

        print(
            f"{name:<20} {mass_str:<15} "
            f"{format_distance(rs):<20} {format_distance(photon_r):<20}"
        )


def demo_falling_into_black_hole():
    print_header("SIMULAÇÃO DE QUEDA NO BURACO NEGRO")

    mass = 10  
    rs = schwarzschild_radius(mass)
    initial_distance = 10 * rs

    print(f"Queda a partir de {initial_distance / rs:.1f}Rs em um BN de {mass} M☉\n")

    checkpoints = [10, 5, 3, 2, 1.5, 1.2, 1.1, 1.01]

    print(
        f"{'Distância':<12} {'Tempo Terra':<15} {'Tempo Local':<15} {'Velocidade':<12}"
    )
    print("-" * 55)

    earth_time = 0  

    for i, checkpoint in enumerate(checkpoints):
        r = checkpoint * rs
        factor = time_dilation(r, rs)

        if i > 0:
            earth_time += 100  

        local_time = earth_time * factor if factor > 0 else 0
        v_fall = escape_velocity(r, mass) * 0.5  
        v_fall_c = v_fall / 299_792_458

        print(
            f"{checkpoint:<12.2f}Rs  "
            f"{format_time(earth_time):<15}  "
            f"{format_time(local_time) if factor > 0 else 'Tempo parado':<15}  "
            f"{v_fall_c:<12.3f}c"
        )


def demo_interactive_menu():
    while True:
        print_header("SIMULADOR DE DILATAÇÃO TEMPORAL - MENU PRINCIPAL")

        print("Escolha uma demonstração:\n")
        print("1. Cálculos Básicos de Física")
        print("2. Efeitos de Dilatação Temporal")
        print("3. Mecânica Orbital")
        print("4. Efeitos de Gravidade Extrema")
        print("5. Desvio Gravitacional (Redshift)")
        print("6. Comparação de Buracos Negros Conhecidos")
        print("7. Simulação de Queda no Buraco Negro")
        print("8. Gráfico de Dilatação Temporal (Matplotlib)")
        print("9. Comparação de Múltiplas Massas (Gráfico)")
        print("10. Simulação 3D de Órbitas (VPython)")
        print("11. Simulação Interativa (VPython)")
        print("0. Sair")

        try:
            choice = input("\nEscolha (0-11): ").strip()

            if choice == "0":
                print("\nEncerrando simulador...")
                break
            elif choice == "1":
                demo_basic_calculations()
            elif choice == "2":
                demo_time_dilation_effects()
            elif choice == "3":
                demo_orbital_mechanics()
            elif choice == "4":
                demo_extreme_gravity_effects()
            elif choice == "5":
                demo_redshift()
            elif choice == "6":
                demo_comparison_table()
            elif choice == "7":
                demo_falling_into_black_hole()
            elif choice == "8":
                mass = float(input("Massa do buraco negro (massas solares): "))
                plot_dilation(mass)
            elif choice == "9":
                plot_multiple_masses()
            elif choice == "10":
                mass = float(input("Massa do buraco negro (massas solares): "))
                num_orbits = int(input("Número de órbitas (1-10): "))
                print("\nIniciando simulação 3D...")
                print("Feche a janela da simulação para retornar ao menu.")
                visualize_orbits(mass, num_orbits)
            elif choice == "11":
                mass = float(input("Massa inicial (massas solares): "))
                print("\nIniciando simulação interativa...")
                print("Use o slider para ajustar a massa do buraco negro.")
                print("Feche a janela da simulação para retornar ao menu.")
                create_interactive_simulation(mass)
            else:
                print("\nOpção inválida. Tente novamente.")

            if choice in ["1", "2", "3", "4", "5", "6", "7"]:
                input("\nPressione Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\nInterrompido pelo usuário.")
            break
        except ValueError as e:
            print(f"\nErro de entrada: {e}")
            input("Pressione Enter para continuar...")
        except Exception as e:
            print(f"\nErro inesperado: {e}")
            input("Pressione Enter para continuar...")


def main():
    print_header("BEM-VINDO AO SIMULADOR DE DILATAÇÃO TEMPORAL")

    print(
        "Este programa demonstra os efeitos relativísticos próximos a buracos negros."
    )
    print("Baseado nas equações da Relatividade Geral de Einstein.\n")

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        if arg == "--basic":
            demo_basic_calculations()
        elif arg == "--time":
            demo_time_dilation_effects()
        elif arg == "--orbit":
            demo_orbital_mechanics()
        elif arg == "--extreme":
            demo_extreme_gravity_effects()
        elif arg == "--redshift":
            demo_redshift()
        elif arg == "--compare":
            demo_comparison_table()
        elif arg == "--fall":
            demo_falling_into_black_hole()
        elif arg == "--plot":
            mass = float(input("Massa (M☉): "))
            plot_dilation(mass)
        elif arg == "--3d":
            mass = float(input("Massa (M☉): "))
            visualize_orbits(mass)
        elif arg == "--help":
            print("Opções disponíveis:")
            print("  --basic     : Cálculos básicos")
            print("  --time      : Dilatação temporal")
            print("  --orbit     : Mecânica orbital")
            print("  --extreme   : Gravidade extrema")
            print("  --redshift  : Desvio gravitacional")
            print("  --compare   : Comparação de BNs")
            print("  --fall      : Queda no BN")
            print("  --plot      : Gráfico 2D")
            print("  --3d        : Simulação 3D")
            print("  --help      : Esta mensagem")
            print("\nSem argumentos: Menu interativo")
        else:
            print(f"Opção desconhecida: {arg}")
            print("Use --help para ver as opções disponíveis.")
    else:
        demo_interactive_menu()

    print("\nObrigado por usar o Simulador de Dilatação Temporal!")


if __name__ == "__main__":
    main()
