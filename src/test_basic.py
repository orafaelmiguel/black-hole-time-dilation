#!/usr/bin/env python
# -*- coding: utf-8 -*-

from physics import schwarzschild_radius, time_dilation


def test_basic():
    print("=" * 50)
    print("TESTE BÁSICO DO SIMULADOR")
    print("=" * 50)

    M = 10 
    r = 30_000  

    rs = schwarzschild_radius(M)

    dilation = time_dilation(r, rs)

    print(f"\nParâmetros:")
    print(f"  Massa do buraco negro: {M} massas solares")
    print(f"  Distância de teste: {r:,} km")

    print(f"\nResultados:")
    print(f"  Raio de Schwarzschild: {rs:.2f} km")
    print(f"  Dilatação temporal (t0/tf): {dilation:.6f}")

    if dilation > 0:
        time_factor = 1 / dilation
        print(f"  Tempo relativo: {time_factor:.2f}x mais lento")
    else:
        print(f"  Tempo relativo: infinitamente lento (no horizonte)")

    expected_rs = 29530  
    if abs(rs - expected_rs) < 100:
        print("\n✓ Raio de Schwarzschild calculado corretamente!")
    else:
        print(f"\n✗ Erro no cálculo do raio de Schwarzschild")
        print(f"  Esperado: ~{expected_rs} km")
        print(f"  Obtido: {rs:.2f} km")

    if 0 < dilation < 1:
        print("✓ Dilatação temporal está no intervalo correto (0 < t < 1)")
    else:
        print("✗ Dilatação temporal fora do intervalo esperado")

    print("\n" + "=" * 50)
    print("TESTE CONCLUÍDO")
    print("=" * 50)


if __name__ == "__main__":
    test_basic()
