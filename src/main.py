from physics import schwarzschild_radius, time_dilation
from visualization import plot_dilation


def main():
    M = 10  
    r = 30_000  

    rs = schwarzschild_radius(M)

    dilation = time_dilation(r, rs)

    print("=" * 50)
    print("SIMULAÇÃO DE DILATAÇÃO TEMPORAL - BURACO NEGRO")
    print("=" * 50)
    print(f"Massa do buraco negro: {M} massas solares")
    print(f"Raio de Schwarzschild: {rs:.2f} km")
    print(f"Distância de teste: {r:,} km")
    print(f"Fator de dilatação temporal (t0/tf): {dilation:.6f}")
    print(
        f"Tempo relativo: {(1 / dilation if dilation > 0 else 'infinito'):.2f}x mais lento"
    )
    print("=" * 50)

    print("\nGerando gráfico de dilatação temporal...")
    plot_dilation(M)


if __name__ == "__main__":
    main()
