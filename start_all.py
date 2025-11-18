"""
Inicia Flask (puerto 5000) y Spring Boot (puerto 8080) simultáneamente.
Uso:
    python start_all.py  (desde el entorno virtual activado)
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def main():
    # Rutas
    project_root = Path(__file__).parent
    flask_script = project_root / "run.py"
    spring_dir = project_root / "adopcion-mascotas"
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    
    # Verificar que el entorno virtual existe
    if not venv_python.exists():
        print("❌ Error: No se encuentra el entorno virtual en .venv/")
        print("   Ejecuta primero: python -m venv .venv")
        print("   Luego: .\.venv\Scripts\Activate.ps1")
        print("   Y: pip install -r requirements.txt")
        return
    
    print("🚀 Iniciando aplicaciones...")
    
    # 1. Iniciar Flask con el Python del entorno virtual
    print("\n📦 Iniciando Flask (puerto 5000)...")
    flask_process = subprocess.Popen(
        [str(venv_python), str(flask_script)],
        cwd=project_root
    )
    
    # 2. Esperar un poco antes de iniciar Spring Boot
    time.sleep(3)
    
    # 3. Verificar si Maven Wrapper existe
    mvnw_cmd = spring_dir / "mvnw.cmd"
    if mvnw_cmd.exists():
        print("☕ Usando Maven Wrapper (mvnw.cmd)...")
        spring_cmd = [str(mvnw_cmd), "spring-boot:run"]
    else:
        print("❌ Error: No se encuentra mvnw.cmd en adopcion-mascotas/")
        print("   Maven no está instalado y el wrapper no existe.")
        flask_process.terminate()
        return
    
    print("   (Esto puede tardar 10-30 segundos la primera vez)\n")
    
    # Iniciar Spring Boot
    spring_process = subprocess.Popen(
        spring_cmd,
        cwd=spring_dir,
        shell=True
    )
    
    print("\n✅ Aplicaciones iniciadas:")
    print("   🐍 Flask:       http://localhost:5000/")
    print("   ☕ Spring Boot: http://localhost:8080/evaluacion")
    print("\n⚠️  Presiona Ctrl+C para detener ambas aplicaciones\n")
    
    try:
        # Mantener el script corriendo
        spring_process.wait()
        flask_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo aplicaciones...")
        flask_process.terminate()
        spring_process.terminate()
        time.sleep(2)
        # Forzar terminación si es necesario
        try:
            flask_process.kill()
            spring_process.kill()
        except:
            pass
        print("✅ Aplicaciones detenidas")

if __name__ == "__main__":
    main()
