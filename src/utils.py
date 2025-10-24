import math
import numpy as np
from typing import Tuple, List, Dict, Any
from physics import schwarzschild_radius, time_dilation


def format_time(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f} segundos"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minutos"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} horas"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} dias"
    else:
        return f"{seconds / 31536000:.2f} anos"


def format_distance(km: float) -> str:
    if km < 1:
        return f"{km * 1000:.2f} m"
    elif km < 1000:
        return f"{km:.2f} km"
    elif km < 149597870.7: 
        return f"{km / 1000:.2f} mil km"
    else:
        au = km / 149597870.7
        if au < 1000:
            return f"{au:.2f} AU"
        else:
            ly = km / 9.461e12  
            return f"{ly:.2f} anos-luz"


def calculate_safe_distance(mass_solar: float, safety_factor: float = 10.0) -> float:
    rs = schwarzschild_radius(mass_solar)
    return rs * safety_factor


def time_to_cross_horizon(r_km: float, rs_km: float) -> float:
    if r_km <= rs_km:
        return 0.0

    c = 299_792_458  # m/s
    return (math.pi / 2) * (r_km * 1000 / c) * math.sqrt(r_km / rs_km)


def compare_time_passages(
    r_km: float, rs_km: float, observer_time_hours: float
) -> Dict[str, Any]:
    factor = time_dilation(r_km, rs_km)

    if factor == 0:
        local_time = 0
        time_ratio = float("inf")
    else:
        local_time = observer_time_hours * factor
        time_ratio = 1 / factor

    return {
        "distance_km": r_km,
        "distance_rs": r_km / rs_km if rs_km > 0 else float("inf"),
        "time_dilation_factor": factor,
        "observer_time_hours": observer_time_hours,
        "local_time_hours": local_time,
        "time_ratio": time_ratio,
        "observer_time_formatted": format_time(observer_time_hours * 3600),
        "local_time_formatted": format_time(local_time * 3600)
        if local_time > 0
        else "Tempo parado",
    }


def generate_orbit_data(
    mass_solar: float, num_orbits: int = 5
) -> List[Dict[str, float]]:
    rs = schwarzschild_radius(mass_solar)

    orbits = []
    radii = np.linspace(rs * 1.5, rs * 10, num_orbits)

    for r in radii:
        factor = time_dilation(r, rs)

        G = 6.67430e-11
        M = mass_solar * 1.98847e30
        v_orbital = math.sqrt(G * M / (r * 1000))  # m/s

        period = 2 * math.pi * r * 1000 / v_orbital  

        orbits.append(
            {
                "radius_km": r,
                "radius_rs": r / rs,
                "time_dilation": factor,
                "orbital_velocity_ms": v_orbital,
                "orbital_velocity_c": v_orbital / 299_792_458,
                "orbital_period_s": period,
                "orbital_period_formatted": format_time(period),
                "perceived_period_s": period / factor if factor > 0 else float("inf"),
                "perceived_period_formatted": format_time(period / factor)
                if factor > 0
                else "Infinito",
            }
        )

    return orbits


def calculate_event_horizon_properties(mass_solar: float) -> Dict[str, Any]:
    rs_km = schwarzschild_radius(mass_solar)
    rs_m = rs_km * 1000

    area = 4 * math.pi * rs_m**2

    G = 6.67430e-11
    M = mass_solar * 1.98847e30
    c = 299_792_458
    surface_gravity = c**4 / (4 * G * M)

    h_bar = 1.054571817e-34 
    k_b = 1.380649e-23  
    temperature = (h_bar * c**3) / (8 * math.pi * G * M * k_b)

    return {
        "schwarzschild_radius_km": rs_km,
        "schwarzschild_radius_formatted": format_distance(rs_km),
        "horizon_area_km2": area / 1e6,
        "horizon_circumference_km": 2 * math.pi * rs_km,
        "surface_gravity_ms2": surface_gravity,
        "surface_gravity_g": surface_gravity / 9.81,
        "hawking_temperature_k": temperature,
        "hawking_temperature_formatted": f"{temperature:.2e} K",
    }


def interpolate_color(factor: float) -> Tuple[float, float, float]:
    if factor < 0.2:
        return (1.0, 0.0, 0.0)
    elif factor < 0.4:
        t = (factor - 0.2) / 0.2
        return (1.0, t * 0.5, 0.0)
    elif factor < 0.6:
        t = (factor - 0.4) / 0.2
        return (1.0, 0.5 + t * 0.5, 0.0)
    elif factor < 0.8:
        t = (factor - 0.6) / 0.2
        return (1.0 - t * 0.5, 1.0, 0.0)
    else:
        t = (factor - 0.8) / 0.2
        return (0.0, 1.0 - t * 0.5, t)


def create_data_table(mass_solar: float, distances_rs: List[float]) -> str:
    rs = schwarzschild_radius(mass_solar)

    table = f"Buraco Negro de {mass_solar} M☉ (Rs = {rs:.2f} km)\n"
    table += "=" * 70 + "\n"
    table += f"{'Distância':<15} {'Distância':<15} {'Dilatação':<15} {'Tempo':<15}\n"
    table += f"{'(Rs)':<15} {'(km)':<15} {'Temporal':<15} {'Relativo':<15}\n"
    table += "-" * 70 + "\n"

    for d_rs in distances_rs:
        d_km = d_rs * rs
        factor = time_dilation(d_km, rs)

        if factor > 0:
            relative_time = 1 / factor
            time_str = f"{relative_time:.2f}x mais lento"
        else:
            time_str = "Infinito"

        table += f"{d_rs:<15.2f} {d_km:<15.0f} {factor:<15.6f} {time_str:<15}\n"

    return table


def estimate_spaghettification_distance(
    mass_solar: float, object_height_m: float = 2.0
) -> float:
    G = 6.67430e-11
    M = mass_solar * 1.98847e30

    lethal_tidal = 10 * 9.81  # m/s²

    # tidal_force = 2GMh/r³ = lethal_tidal
    r_m = (2 * G * M * object_height_m / lethal_tidal) ** (1 / 3)

    return r_m / 1000  


def generate_falling_trajectory(
    initial_r_km: float, rs_km: float, num_points: int = 100
) -> List[Dict[str, float]]:
    if initial_r_km <= rs_km:
        return []

    trajectory = []
    radii = np.linspace(initial_r_km, rs_km * 1.01, num_points)

    for i, r in enumerate(radii):
        factor = time_dilation(r, rs_km)

        if r > rs_km:
            v_fall = math.sqrt(
                2 * 6.67430e-11 * 1.98847e30 * (1 / rs_km - 1 / r) / 1000
            )
        else:
            v_fall = 299_792_458 

        trajectory.append(
            {
                "step": i,
                "radius_km": r,
                "radius_rs": r / rs_km,
                "time_dilation": factor,
                "fall_velocity_ms": v_fall,
                "fall_velocity_c": v_fall / 299_792_458,
            }
        )

    return trajectory
