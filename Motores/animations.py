import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
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

def animate_phase_space():
    """Animación del espacio de fase"""
    print("🎬 Preparando animación del espacio de fase...")
    
    # Cargar datos
    data_file = find_data_file()
    if not data_file:
        return
    
    data = np.loadtxt(data_file)
    t, x, v, s, E_total = data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4]
    
    # Configurar la figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Configurar límites
    x_min, x_max = np.min(x), np.max(x)
    v_min, v_max = np.min(v), np.max(v)
    
    # Espacio de fase (ax1)
    ax1.set_xlim(x_min - 0.1, x_max + 0.1)
    ax1.set_ylim(v_min - 0.1, v_max + 0.1)
    ax1.set_xlabel('Posición $x$', fontsize=12)
    ax1.set_ylabel('Velocidad $v$', fontsize=12)
    ax1.set_title('Espacio de Fase - Animación', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Trayectoria vs tiempo (ax2)
    ax2.set_xlim(np.min(t), np.max(t))
    ax2.set_ylim(x_min - 0.1, x_max + 0.1)
    ax2.set_xlabel('Tiempo $t$', fontsize=12)
    ax2.set_ylabel('Posición $x$', fontsize=12)
    ax2.set_title('Posición vs Tiempo - Animación', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Elementos de la animación
    # Espacio de fase
    phase_line, = ax1.plot([], [], 'b-', linewidth=1, alpha=0.7, label='Trayectoria')
    phase_point, = ax1.plot([], [], 'ro', markersize=8, label='Posición actual')
    phase_trail, = ax1.plot([], [], 'g-', linewidth=0.5, alpha=0.5, label='Últimos puntos')
    
    # Posición vs tiempo
    time_line, = ax2.plot([], [], 'b-', linewidth=1, alpha=0.7, label='Posición')
    time_point, = ax2.plot([], [], 'ro', markersize=6, label='Posición actual')
    time_vertical, = ax2.plot([], [], 'r--', alpha=0.5, label='Tiempo actual')
    
    # Leyendas
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')
    
    # Texto informativo
    info_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, fontsize=10,
                        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Función de inicialización
    def init():
        phase_line.set_data([], [])
        phase_point.set_data([], [])
        phase_trail.set_data([], [])
        time_line.set_data([], [])
        time_point.set_data([], [])
        time_vertical.set_data([], [])
        info_text.set_text('')
        return phase_line, phase_point, phase_trail, time_line, time_point, time_vertical, info_text
    
    # Función de animación
    def animate(i):
        # Usar cada n puntos para hacer la animación más rápida
        n = max(1, len(x) // 500)  # Mostrar ~500 frames
        idx = i * n
        
        if idx >= len(x):
            idx = len(x) - 1
        
        # Espacio de fase
        phase_line.set_data(x[:idx], v[:idx])
        phase_point.set_data([x[idx]], [v[idx]])
        
        # Trail de los últimos 50 puntos
        trail_start = max(0, idx - 50)
        phase_trail.set_data(x[trail_start:idx], v[trail_start:idx])
        
        # Posición vs tiempo
        time_line.set_data(t[:idx], x[:idx])
        time_point.set_data([t[idx]], [x[idx]])
        time_vertical.set_data([t[idx], t[idx]], [x_min, x[idx]])
        
        # Texto informativo
        info_text.set_text(f'Tiempo: {t[idx]:.2f}\nPosición: {x[idx]:.3f}\nVelocidad: {v[idx]:.3f}\nEstado: {int(s[idx])}')
        
        return phase_line, phase_point, phase_trail, time_line, time_point, time_vertical, info_text
    
    # Crear animación
    frames = min(500, len(x))  # Máximo 500 frames
    
    anim = FuncAnimation(fig, animate, init_func=init,
                        frames=frames, interval=50, blit=True)
    
    # Guardar animación
    os.makedirs("results/animations", exist_ok=True)
    output_file = "results/animations/animacion_espacio_fase.mp4"
    
    print("📹 Guardando animación... (esto puede tomar unos segundos)")
    
    # Guardar como MP4
    try:
        anim.save(output_file, writer='ffmpeg', fps=20, dpi=100)
        print(f"✅ Animación guardada: {output_file}")
    except Exception as e:
        print(f"❌ Error guardando MP4: {e}")
        print("💡 Intentando guardar como GIF...")
        
        # Intentar guardar como GIF
        try:
            output_file_gif = "results/animations/animacion_espacio_fase.gif"
            anim.save(output_file_gif, writer='pillow', fps=20)
            print(f"✅ Animación guardada como GIF: {output_file_gif}")
        except Exception as e2:
            print(f"❌ Error guardando GIF: {e2}")
            print("💡 Mostrando animación en pantalla...")
            plt.show()
    
    plt.close()

def animate_position_only():
    """Animación solo de posición vs tiempo con el potencial"""
    print("🎬 Preparando animación de posición con potencial...")
    
    # Cargar datos
    data_file = find_data_file()
    if not data_file:
        return
    
    data = np.loadtxt(data_file)
    t, x, v, s, E_total = data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4]
    
    # Parámetros del potencial
    k0, k1 = 0.1, 10.0
    l = 0.5
    
    # Configurar la figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Gráfica 1: Posición vs tiempo con potencial
    x_range = np.linspace(np.min(x) - 0.5, np.max(x) + 0.5, 1000)
    U0 = 0.5 * k0 * (x_range - 0.0)**2
    U1 = 0.5 * k1 * (x_range - l)**2
    
    ax1.plot(x_range, U0, 'b-', alpha=0.3, label='$U_0(x)$')
    ax1.plot(x_range, U1, 'r-', alpha=0.3, label='$U_1(x)$')
    ax1.set_xlabel('Posición $x$')
    ax1.set_ylabel('Energía Potencial $U(x)$')
    ax1.set_title('Potencial y Posición de la Partícula', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gráfica 2: Posición vs tiempo
    ax2.set_xlim(np.min(t), np.max(t))
    ax2.set_ylim(np.min(x) - 0.1, np.max(x) + 0.1)
    ax2.set_xlabel('Tiempo $t$')
    ax2.set_ylabel('Posición $x$')
    ax2.set_title('Evolución Temporal', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Elementos de la animación
    # Potencial y partícula
    part_point, = ax1.plot([], [], 'ko', markersize=10, label='Partícula')
    state_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, fontsize=12,
                         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Línea de tiempo
    time_line, = ax2.plot([], [], 'b-', linewidth=1, alpha=0.7)
    time_point, = ax2.plot([], [], 'ro', markersize=6)
    time_vertical, = ax2.plot([], [], 'r--', alpha=0.5)
    
    # Función de inicialización
    def init():
        part_point.set_data([], [])
        state_text.set_text('')
        time_line.set_data([], [])
        time_point.set_data([], [])
        time_vertical.set_data([], [])
        return part_point, state_text, time_line, time_point, time_vertical
    
    # Función de animación
    def animate(i):
        n = max(1, len(x) // 300)  # Mostrar ~300 frames
        idx = i * n
        
        if idx >= len(x):
            idx = len(x) - 1
        
        # Actualizar posición de la partícula en el potencial
        current_U = 0.5 * k0 * x[idx]**2 if s[idx] == 0 else 0.5 * k1 * (x[idx] - l)**2
        part_point.set_data([x[idx]], [current_U])
        
        # Actualizar texto del estado
        state_color = 'blue' if s[idx] == 0 else 'red'
        state_name = 'DÉBIL (U₀)' if s[idx] == 0 else 'FUERTE (U₁)'
        state_text.set_text(f'Estado: {state_name}\nPosición: {x[idx]:.3f}\nEnergía: {current_U:.3f}')
        state_text.set_color(state_color)
        
        # Resaltar el potencial activo
        if s[idx] == 0:
            ax1.lines[0].set_alpha(1.0)  # U0 visible
            ax1.lines[1].set_alpha(0.3)  # U1 tenue
        else:
            ax1.lines[0].set_alpha(0.3)  # U0 tenue
            ax1.lines[1].set_alpha(1.0)  # U1 visible
        
        # Actualizar gráfica de tiempo
        time_line.set_data(t[:idx], x[:idx])
        time_point.set_data([t[idx]], [x[idx]])
        time_vertical.set_data([t[idx], t[idx]], [np.min(x), x[idx]])
        
        return part_point, state_text, time_line, time_point, time_vertical
    
    # Crear animación
    frames = min(300, len(x))
    
    anim = FuncAnimation(fig, animate, init_func=init,
                        frames=frames, interval=50, blit=True)
    
    # Guardar animación
    os.makedirs("results/animations", exist_ok=True)
    output_file = "results/animations/animacion_posicion_potencial.mp4"
    
    print("📹 Guardando animación...")
    
    try:
        anim.save(output_file, writer='ffmpeg', fps=20, dpi=100)
        print(f"✅ Animación guardada: {output_file}")
    except Exception as e:
        print(f"❌ Error guardando MP4: {e}")
        try:
            output_file_gif = "results/animations/animacion_posicion_potencial.gif"
            anim.save(output_file_gif, writer='pillow', fps=15)
            print(f"✅ Animación guardada como GIF: {output_file_gif}")
        except Exception as e2:
            print(f"❌ Error guardando GIF: {e2}")
            print("💡 Mostrando animación en pantalla...")
            plt.show()
    
    plt.close()

def main():
    print("=== ANIMACIONES DEL MOTOR MOLECULAR ===")
    print()
    
    # Verificar dependencias
    try:
        import matplotlib.animation as animation
    except ImportError:
        print("❌ matplotlib no está instalado o no tiene soporte para animaciones")
        print("💡 Instala con: pip install matplotlib")
        return
    
    # Crear directorio de animaciones
    os.makedirs("results/animations", exist_ok=True)
    
    while True:
        print("\n🎬 ¿Qué animación quieres generar?")
        print("1. Espacio de fase + Posición vs tiempo")
        print("2. Posición con potencial + Evolución temporal") 
        print("3. Ambas animaciones")
        print("4. Salir")
        
        choice = input("\nSelecciona una opción (1-4): ").strip()
        
        if choice == '1':
            animate_phase_space()
        elif choice == '2':
            animate_position_only()
        elif choice == '3':
            animate_phase_space()
            animate_position_only()
        elif choice == '4':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")
        
        continuar = input("\n¿Generar otra animación? (s/n): ").strip().lower()
        if continuar != 's':
            print("👋 ¡Animaciones completadas!")
            break

if __name__ == "__main__":
    main()