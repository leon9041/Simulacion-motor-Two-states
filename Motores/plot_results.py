import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def find_data_file():
    """Buscar el archivo de datos en diferentes ubicaciones"""
    possible_paths = [
        "results/datos_motor_dos_estados_langevin.txt",
        "../results/datos_motor_dos_estados_langevin.txt",
        "./results/datos_motor_dos_estados_langevin.txt",
        "datos_motor_dos_estados_langevin.txt"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Archivo de datos encontrado: {path}")
            return path
    
    print("❌ No se pudo encontrar el archivo de datos.")
    return None

def plot_schematic_model():
    """Crear gráfica esquemática del modelo de dos estados"""
    print("Generando gráfica esquemática del modelo...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Parámetros del modelo
    x = np.linspace(-1, 2, 1000)
    
    # Potenciales armónicos
    k0, k1 = 0.1, 10.0  # Constantes elásticas
    x0, x1 = 0.0, 0.5   # Posiciones de equilibrio
    
    U0 = 0.5 * k0 * (x - x0)**2
    U1 = 0.5 * k1 * (x - x1)**2
    
    # Alturas de las barreras (aproximadas)
    E1 = 0.5 * k0 * (x1 - x0)**2  # Barrera desde estado 1
    E2 = 0.5 * k1 * (x1 - x0)**2  # Barrera desde estado 2
    
    # Dibujar potenciales
    ax.plot(x, U0, 'b-', linewidth=3, label='Estado 0: $U_0(x)$ (Unión débil)', alpha=0.8)
    ax.plot(x, U1, 'r-', linewidth=3, label='Estado 1: $U_1(x)$ (Unión fuerte)', alpha=0.8)
    
    # Líneas verticales para posiciones de equilibrio
    ax.axvline(x=x0, color='blue', linestyle='--', alpha=0.5, label='$x_{min}^{(0)} = 0$')
    ax.axvline(x=x1, color='red', linestyle='--', alpha=0.5, label='$x_{min}^{(1)} = l$')
    
    # Anotaciones para las barreras
    barrier_x = (x0 + x1) / 2
    ax.annotate('', xy=(barrier_x, E1), xytext=(barrier_x, 0),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
    ax.text(barrier_x + 0.05, E1/2, '$E_1$', fontsize=14, color='purple', ha='left', va='center')
    
    ax.annotate('', xy=(barrier_x, E2), xytext=(barrier_x, E1),
                arrowprops=dict(arrowstyle='<->', color='orange', lw=2))
    ax.text(barrier_x + 0.05, (E1 + E2)/2, '$E_2$', fontsize=14, color='orange', ha='left', va='center')
    
    # Flechas de transición entre estados
    ax.annotate('', xy=(x1, 0.1), xytext=(x0, 0.1),
                arrowprops=dict(arrowstyle='->', color='green', lw=2, alpha=0.7))
    ax.text((x0 + x1)/2, 0.15, '$k_{12}$', fontsize=12, color='green', ha='center', va='bottom')
    
    ax.annotate('', xy=(x0, 0.05), xytext=(x1, 0.05),
                arrowprops=dict(arrowstyle='->', color='brown', lw=2, alpha=0.7))
    ax.text((x0 + x1)/2, 0.0, '$k_{21}$', fontsize=12, color='brown', ha='center', va='top')

def plot_potential_landscape():
    """NUEVA: Gráfica del paisaje de energía potencial teórico"""
    print("Generando gráfica del paisaje de energía potencial...")
    
    # Parámetros (deben coincidir con main.cpp)
    k0, k1 = 0.1, 10.0  # Constantes elásticas
    l = 0.5              # Desplazamiento
    
    # Crear un rango amplio de posiciones
    x_range = np.linspace(-1.0, 3.0, 1000)  # Desde -1 hasta 3
    
    # Calcular los potenciales teóricos
    U0_theoretical = 0.5 * k0 * (x_range - 0.0)**2    # Potencial estado 0
    U1_theoretical = 0.5 * k1 * (x_range - l)**2      # Potencial estado 1
    
    plt.figure(figsize=(12, 8))
    
    # Graficar ambos potenciales
    plt.plot(x_range, U0_theoretical, 'b-', linewidth=3, 
             label='$U_0(x) = \\frac{1}{2}k_0 x^2$ (Estado 0)', alpha=0.8)
    plt.plot(x_range, U1_theoretical, 'r-', linewidth=3, 
             label='$U_1(x) = \\frac{1}{2}k_1 (x - l)^2$ (Estado 1)', alpha=0.8)
    
    # Líneas verticales en posiciones importantes
    plt.axvline(x=0.0, color='blue', linestyle='--', alpha=0.6, label='$x_{min}^{(0)} = 0$')
    plt.axvline(x=l, color='red', linestyle='--', alpha=0.6, label='$x_{min}^{(1)} = l$')
    
    # Marcas en x=1, x=2, x=3
    for x_val in [1.0, 2.0, 3.0]:
        U0_val = 0.5 * k0 * x_val**2
        U1_val = 0.5 * k1 * (x_val - l)**2
        
        plt.axvline(x=x_val, color='gray', linestyle=':', alpha=0.4)
        plt.plot(x_val, U0_val, 'bo', markersize=8, alpha=0.7)
        plt.plot(x_val, U1_val, 'ro', markersize=8, alpha=0.7)
        
        # Anotar valores
        plt.annotate(f'U₀({x_val}) = {U0_val:.2f}', 
                    (x_val, U0_val), 
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=9, color='blue', alpha=0.8)
        plt.annotate(f'U₁({x_val}) = {U1_val:.2f}', 
                    (x_val, U1_val), 
                    xytext=(10, -20), textcoords='offset points',
                    fontsize=9, color='red', alpha=0.8)
    
    # Configuración del gráfico
    plt.xlabel('Posición $x$', fontsize=14)
    plt.ylabel('Energía Potencial $U(x)$', fontsize=14)
    plt.title('Paisaje de Energía Potencial Teórico', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xlim(-0.5, 3.2)
    
    # Texto informativo
    textstr = '\n'.join([
        'Parámetros:',
        f'$k_0$ = {k0}',
        f'$k_1$ = {k1}', 
        f'$l$ = {l}',
        '',
        'En x=1.0:',
        f'  $U_0$ = {0.5*k0*1.0**2:.3f}',
        f'  $U_1$ = {0.5*k1*(1.0-l)**2:.3f}',
        '',
        'En x=2.0:',
        f'  $U_0$ = {0.5*k0*2.0**2:.3f}',
        f'  $U_1$ = {0.5*k1*(2.0-l)**2:.3f}',
        '',
        'En x=3.0:',
        f'  $U_0$ = {0.5*k0*3.0**2:.3f}',
        f'  $U_1$ = {0.5*k1*(3.0-l)**2:.3f}'
    ])
    props = dict(boxstyle='round', facecolor='lightcyan', alpha=0.8)
    plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, '05_paisaje_potencial_teorico.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✅ Gráfica del paisaje potencial generada: 05_paisaje_potencial_teorico.png")

def plot_phase_space(data):
    """NUEVA: Gráfica SIMPLIFICADA del espacio de fase (posición vs velocidad)"""
    print("Generando gráfica del espacio de fase...")
    
    x, v = data[:, 1], data[:, 2]
    
    plt.figure(figsize=(10, 8))
    
    # LÍNEA CONTINUA simple - conecta todos los puntos en orden temporal
    plt.plot(x, v, 'b-', linewidth=0.5, alpha=0.7, label='Trayectoria en espacio de fase')
    
    # Configuración del gráfico
    plt.xlabel('Posición $x$', fontsize=14)
    plt.ylabel('Velocidad $v$', fontsize=14)
    plt.title('Espacio de Fase: Posición vs Velocidad', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Calcular algunas estadísticas básicas
    x_mean, x_std = np.mean(x), np.std(x)
    v_mean, v_std = np.mean(v), np.std(v)
    
    # Líneas en promedios
    plt.axvline(x=x_mean, color='green', linestyle='--', alpha=0.7, 
                label=f'$\\langle x \\rangle = {x_mean:.3f}$')
    plt.axhline(y=v_mean, color='orange', linestyle='--', alpha=0.7,
                label=f'$\\langle v \\rangle = {v_mean:.3f}$')
    
    # Punto inicial y final
    plt.plot(x[0], v[0], 'go', markersize=8, label='Inicio')
    plt.plot(x[-1], v[-1], 'ro', markersize=8, label='Final')
    
    # Texto informativo simple
    textstr = '\n'.join([
        f'Puntos totales: {len(x):,}',
        f'Rango x: [{np.min(x):.3f}, {np.max(x):.3f}]',
        f'Rango v: [{np.min(v):.3f}, {np.max(v):.3f}]'
    ])
    props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
    plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=props)
    
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, '06_espacio_fase.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✅ Gráfica del espacio de fase generada: 06_espacio_fase.png")

# Configuración
DATA_FILE = find_data_file()
FIGURES_DIR = "results/figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Configurar matplotlib para evitar problemas de backend
plt.switch_backend('Agg')

try:
    # 0. Primero generar la gráfica esquemática
    plot_schematic_model()
    
    # 1. Generar el paisaje potencial teórico (siempre)
    plot_potential_landscape()
    
    if DATA_FILE:
        # 2. Cargar los Datos (Columnas: t, x, v, s, E_total)
        print("Cargando datos de simulación...")
        data = np.loadtxt(DATA_FILE)
        t = data[:, 0]; x = data[:, 1]; v = data[:, 2]; s = data[:, 3]; E_total = data[:, 4]

        print(f"Datos cargados: {len(t)} puntos de tiempo")

        # --- Gráficas originales vs tiempo ---
        print("Generando gráficas originales vs tiempo...")
        
        # Gráfica 1: Trayectoria x(t) y Estado s(t)
        plt.figure(figsize=(12, 7))
        ax1 = plt.subplot(2, 1, 1)
        ax1.plot(t, x, label='Posición $x(t)$', color='#0077b6', linewidth=0.8)
        ax1.set_ylabel('Posición ($x$)')
        ax1.set_title('Movimiento del Motor Molecular (Langevin)')
        ax1.grid(True, linestyle=':', alpha=0.6)
        
        plt.setp(ax1.get_xticklabels(), visible=False)
        ax2 = plt.subplot(2, 1, 2, sharex=ax1)
        ax2.plot(t, s, drawstyle='steps-post', label='Estado Químico $s(t)$', color='#9b2226', linewidth=2)
        ax2.set_xlabel('Tiempo ($t$)'); ax2.set_ylabel('Estado ($s$)'); ax2.set_yticks([0, 1])
        ax2.grid(True, linestyle=':', alpha=0.6)
        
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, '01_trayectoria_y_estado_langevin.png'), dpi=150, bbox_inches='tight')
        plt.close()

        # Gráfica 2: Velocidad v(t) y Estado s(t)
        fig, ax_v = plt.subplots(figsize=(12, 5))
        ax_v.plot(t, v, label='Velocidad $v(t)$', color='#2a9d8f', alpha=0.8, linewidth=1)
        ax_v.set_xlabel('Tiempo ($t$)'); ax_v.set_ylabel('Velocidad ($v$)', color='#2a9d8f')
        ax_v.tick_params(axis='y', labelcolor='#2a9d8f')
        ax_v.grid(True, linestyle=':', alpha=0.5)

        ax_s = ax_v.twinx()
        ax_s.plot(t, s, label='Estado Químico $s(t)$', color='#9b2226', linestyle='-', linewidth=2)
        ax_s.set_ylabel('Estado Químico ($s$)', color='#9b2226')
        ax_s.tick_params(axis='y', labelcolor='#9b2226')
        ax_s.set_yticks([0, 1]); ax_s.set_ylim(-0.1, 1.1)

        plt.title('Velocidad y Estado Químico del Motor vs. Tiempo')
        fig.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, '02_velocidad_y_estado_langevin.png'), dpi=150, bbox_inches='tight')
        plt.close()
        
        # Gráfica 3: Energía Total E(t) vs tiempo
        plt.figure(figsize=(12, 4))
        plt.plot(t, E_total, label='Energía Total $E(t)$', color='#e76f51', linewidth=1)
        plt.xlabel('Tiempo ($t$)'); plt.ylabel('Energía Total ($E$)')
        plt.title('Energía Total vs. Tiempo (Sistema Disipativo)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, '03_energia_total_langevin.png'), dpi=150, bbox_inches='tight')
        plt.close()

        # Gráfica 4: Histograma de Posiciones
        plt.figure(figsize=(10, 6))
        plt.hist(x, bins=50, density=True, alpha=0.7, color='#0077b6', edgecolor='black')
        plt.xlabel('Posición ($x$)')
        plt.ylabel('Densidad de Probabilidad')
        plt.title('Distribución de Posiciones del Motor')
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, '04_histograma_posiciones.png'), dpi=150, bbox_inches='tight')
        plt.close()

        # --- NUEVAS GRÁFICAS ---
        # 6. Espacio de fase SIMPLIFICADO
        plot_phase_space(data)

        print(f"\n¡Todas las gráficas generadas exitosamente y guardadas en: {FIGURES_DIR}!")
        print("Gráficas creadas:")
        print("  - 00_esquema_modelo_dos_estados.png (ESQUEMA)")
        print("  - 01_trayectoria_y_estado_langevin.png")
        print("  - 02_velocidad_y_estado_langevin.png") 
        print("  - 03_energia_total_langevin.png")
        print("  - 04_histograma_posiciones.png")
        print("  - 05_paisaje_potencial_teorico.png (Potencial teórico)")
        print("  - 06_espacio_fase.png (Espacio de fase simplificado)")

    else:
        print("⚠️  No se encontraron datos de simulación, pero se generaron los esquemas.")

except Exception as e:
    print(f"\nERROR: Ocurrió un error al procesar los datos: {e}")
    print(f"Tipo de error: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)