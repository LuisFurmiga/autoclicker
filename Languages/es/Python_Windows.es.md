# Guía de Instalación de Python para Windows

Esta guía le mostrará cómo instalar Python en un sistema Windows. Siga los pasos a continuación para configurar correctamente el entorno Python.

### Paso 1: Descargar el instalador de Python

1. Vaya a la página oficial de descargas de Python:  
   [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Haga clic en el botón de descarga para la última versión de Python para Windows (generalmente será la versión más estable). La página reconocerá automáticamente su sistema operativo y ofrecerá el instalador correcto.

### Paso 2: Iniciar la instalación

1. Ejecute el archivo `.exe` descargado.
2. **Importante**: En la primera pantalla del instalador, marque la opción **"Add Python to PATH"**. Esto asegura que puede usar Python desde el terminal en cualquier directorio.
3. Haga clic en **"Install Now"** para comenzar la instalación.

### Paso 3: Verificar la instalación

Una vez que la instalación haya finalizado, es hora de verificar si Python se instaló correctamente:

1. Abra el **Símbolo del sistema** (presione `Win + R`, escriba `cmd` y presione Enter).
2. Escriba el siguiente comando para verificar la versión de Python:
   ```sh
   python --version
   ```
   o, dependiendo de la configuración:
   ```sh
   python3 --version
   ```

   Si la instalación fue exitosa, verá la versión de Python instalada, como por ejemplo:
   ```
   Python 3.x.x
   ```

### Paso 4: Instalar `pip` (gestor de paquetes de Python)

`pip` generalmente se instala automáticamente con Python. Para verificar si `pip` está instalado, ejecute el siguiente comando en el Símbolo del sistema:

```sh
pip --version
```

Si `pip` no está instalado, puede descargarlo e instalarlo manualmente siguiendo las instrucciones en [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/).

### Paso 5: Instalar paquetes de Python

Con `pip` instalado, puede comenzar a instalar paquetes y bibliotecas. Por ejemplo, para instalar la biblioteca `requests`, use el siguiente comando:

```sh
pip install requests
```

### Paso 6: Configurar un entorno virtual (opcional pero recomendado)

Para administrar las dependencias de los proyectos de manera aislada, se recomienda utilizar entornos virtuales. Para crear un entorno virtual, siga estos pasos:

1. En el terminal, navegue hasta el directorio donde desea crear el entorno virtual.
2. Ejecute el comando:
   ```sh
   python -m venv nombre_del_entorno
   ```
   Esto creará una carpeta llamada `nombre_del_entorno` con Python aislado.

3. Para activar el entorno virtual, use el comando:
   ```sh
   nombre_del_entorno\Scripts\activate
   ```

4. Ahora, cualquier paquete instalado con `pip` estará restringido a este entorno virtual.

5. Para desactivar el entorno virtual, escriba:
   ```sh
   deactivate
   ```

---

Con esto, Python estará instalado y listo para usar en su sistema Windows. Si tiene algún problema, consulte la [documentación oficial](https://docs.python.org/3/) para más información.
