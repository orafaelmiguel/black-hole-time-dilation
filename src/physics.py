import math

G = 6.67430e-11  
C = 299_792_458  
M_SOL = 1.98847e30 


def schwarzschild_radius(mass_solar: float) -> float:
    mass_kg = mass_solar * M_SOL

    # rs = 2GM/c²
    rs_m = 2 * G * mass_kg / (C**2)

    return rs_m / 1000


def time_dilation(r_km: float, rs_km: float) -> float:
    if r_km <= rs_km:
        return 0.0  

    return math.sqrt(1 - rs_km / r_km)


def escape_velocity(r_km: float, mass_solar: float) -> float:
    mass_kg = mass_solar * M_SOL
    r_m = r_km * 1000

    # v_escape = √(2GM/r)
    return math.sqrt(2 * G * mass_kg / r_m)


def orbital_period(r_km: float, mass_solar: float) -> float:
    mass_kg = mass_solar * M_SOL
    r_m = r_km * 1000

    # T = 2π√(r³/GM)
    return 2 * math.pi * math.sqrt(r_m**3 / (G * mass_kg))


def gravitational_redshift(r_km: float, rs_km: float) -> float:
    if r_km <= rs_km:
        return float("inf")

    # z = (1/√(1 - rs/r)) - 1
    return (1 / math.sqrt(1 - rs_km / r_km)) - 1


def tidal_force(r_km: float, mass_solar: float, object_size_m: float = 2.0) -> float:
    mass_kg = mass_solar * M_SOL
    r_m = r_km * 1000

    # maréF ≈ 2GMh/r³ (onde h é o tamanho do objeto)
    return 2 * G * mass_kg * object_size_m / (r_m**3)


def photon_sphere_radius(mass_solar: float) -> float:
    # r_photon = 1.5 * rs
    rs = schwarzschild_radius(mass_solar)
    return 1.5 * rs


def innermost_stable_orbit(mass_solar: float) -> float:
    # r_ISCO = 3 * rs
    rs = schwarzschild_radius(mass_solar)
    return 3 * rs
