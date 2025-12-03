import os
import sys

def main():
    print("=== EJECUTOR RÁPIDO DE ANIMACIONES ===")
    
    # Verificar que existe el script de animaciones
    if not os.path.exists("animations.py"):
        print("❌ No se encuentra animations.py")
        print("💡 Asegúrate de que esté en el mismo directorio")
        return
    
    # Verificar que existen datos
    data_file = "results/datos_motor_dos_estados_langevin.txt"
    if not os.path.exists(data_file):
        print(f"❌ No se encuentran datos: {data_file}")
        print("💡 Primero ejecuta la simulación C++ con: python build.py")
        return
    
    print("✅ Datos encontrados")
    print("🚀 Ejecutando animaciones...")
    
    # Ejecutar el script de animaciones
    os.system(f'"{sys.executable}" animations.py')

if __name__ == "__main__":
    main()