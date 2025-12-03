import os
import subprocess
import sys

def run_command(cmd, description):
    print(f"\n📍 {description}...")
    print(f"   Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error en {description}:")
            if result.stderr:
                print(result.stderr)
            return False
        else:
            print(f"✅ {description} completado")
            if result.stdout.strip():
                print(result.stdout)
            return True
    except Exception as e:
        print(f"❌ Excepción en {description}: {e}")
        return False

def main():
    print("=== CONSTRUCCIÓN COMPLETA DE MOTOR MOLECULAR ===")
    print("Incluye: Compilación + Simulación + Gráficas\n")
    
    # Obtener el directorio actual
    current_dir = os.getcwd()
    print(f"Directorio actual: {current_dir}")
    
    # Crear directorios necesarios
    print("\n📁 Creando directorios...")
    os.makedirs("bin", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)
    print("✅ Directorios creados")
    
    # 1. COMPILAR C++
    print("\n" + "="*50)
    print("🔧 ETAPA 1: COMPILACIÓN C++")
    print("="*50)
    
    compile_cmd = [
        "g++", "-o", "bin/motor_sim.exe", 
        "-Iinclude", "-std=c++11", "-O2",
        "src/main.cpp", "src/Potential.cpp", "src/ChemicalState.cpp",
        "src/MotorModel.cpp", "src/Integrator.cpp", "src/Simulator.cpp"
    ]
    
    if not run_command(compile_cmd, "Compilación C++"):
        print("❌ Falla en compilación - deteniendo proceso")
        return
    
    # 2. EJECUTAR SIMULACIÓN
    print("\n" + "="*50)
    print("🚀 ETAPA 2: SIMULACIÓN C++")
    print("="*50)
    
    if not run_command(["bin/motor_sim.exe"], "Simulación C++"):
        print("❌ Falla en simulación - deteniendo proceso")
        return
    
    # 3. VERIFICAR QUE SE GENERARON LOS DATOS
    print("\n" + "="*50)
    print("📊 ETAPA 3: VERIFICACIÓN DE DATOS")
    print("="*50)
    
    data_file = "results/datos_motor_dos_estados_langevin.txt"
    if not os.path.exists(data_file):
        print(f"❌ No se encontró el archivo de datos: {data_file}")
        print("Buscando archivos en results/:")
        if os.path.exists("results"):
            for item in os.listdir("results"):
                print(f"   - {item}")
        return
    
    # Verificar tamaño del archivo
    file_size = os.path.getsize(data_file)
    print(f"✅ Archivo de datos verificado: {data_file}")
    print(f"📏 Tamaño del archivo: {file_size} bytes")
    
    # 4. GENERAR GRÁFICAS CON TU SCRIPT EXISTENTE
    print("\n" + "="*50)
    print("🎨 ETAPA 4: GENERACIÓN DE GRÁFICAS")
    print("="*50)
    
    # Verificar que existe plot_results.py
    if not os.path.exists("plot_results.py"):
        print("❌ No se encuentra plot_results.py en el directorio actual")
        print("💡 Asegúrate de que plot_results.py esté en la misma carpeta que build.py")
        return
    
    print("✅ Script de gráficas encontrado: plot_results.py")
    
    # Ejecutar tu script de gráficas existente
    plot_cmd = [sys.executable, "plot_results.py"]
    
    print(f"🚀 Ejecutando tu script de gráficas...")
    success = run_command(plot_cmd, "Generación de gráficas")
    
    # 5. RESULTADO FINAL
    print("\n" + "="*50)
    print("📋 RESUMEN FINAL")
    print("="*50)
    
    if success:
        print("🎉🎉🎉 PROCESO COMPLETADO EXITOSAMENTE 🎉🎉🎉")
        print("✅ Compilación C++: ✓")
        print("✅ Simulación: ✓")
        print("✅ Gráficas: ✓")
        print(f"📊 Datos: {data_file}")
        print(f"🖼️  Figuras: results/figures/")
        
        # Mostrar gráficas generadas
        figures_dir = "results/figures"
        if os.path.exists(figures_dir):
            figures = [f for f in os.listdir(figures_dir) if f.endswith('.png')]
            if figures:
                print("\n📋 Gráficas generadas:")
                for fig in sorted(figures):
                    print(f"   - {fig}")
            else:
                print("\n⚠️  No se encontraron gráficas en results/figures/")
    else:
        print("❌ PROCESO INCOMPLETO - Falló la generación de gráficas")
        print("\n💡 SOLUCIÓN: Ejecuta manualmente:")
        print("   python plot_results.py")
        print("\n💡 VERIFICA:")
        print("   1. Que Python esté instalado")
        print("   2. Que matplotlib y numpy estén instalados")
        print("   3. Que plot_results.py esté en el mismo directorio")

if __name__ == "__main__":
    main()