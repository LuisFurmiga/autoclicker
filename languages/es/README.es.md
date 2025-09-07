# AutoClicker 2.0

## README Multilingüe
¿No hablas español? Accede: [![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/LuisFurmiga/Autoclicker/blob/main/languages/us/README.us.md)

Você fala português? Acesse: [![pt](https://img.shields.io/badge/lang-pt-green.svg)](https://github.com/LuisFurmiga/Autoclicker/blob/main/README.md)

---

## 🚀 Visión general
**AutoClicker 2.0** es una herramienta avanzada para automatizar clics y teclas en ventanas específicas.  
Ha sido completamente reescrito respecto a la versión 1.0, incorporando **soporte para múltiples perfiles, interfaz multilingüe y nuevas opciones de personalización**.

Perfecto para juegos, pruebas de software y cualquier tarea repetitiva que requiera interacciones rápidas y constantes con el ratón o el teclado.

---

## ✨ Novedades de la versión 2.0
- ✅ **Múltiples perfiles** almacenados en `profiles.json`
  - Crear, renombrar, eliminar, importar y exportar (uno o todos los perfiles).
  - Migración automática de `settings.json` (versión antigua) a `profiles.json`.
- ✅ **Interfaz reorganizada (Tkinter)**
  - Menú de **Idioma** (Portugués, Inglés, Español).
  - Menú de **Perfiles** (con selección por radiobutton y opciones de gestión).
- ✅ **Automatización completa**
  - Clic izquierdo y derecho independientes.
  - Envío de **teclas adicionales**, incluidas combinaciones (`ctrl+c`, `ctrl+shift+tab`, etc.).
- ✅ **Atajos globales**
  - `F1` → iniciar
  - `F2` → detener
- ✅ **Selección de ventana objetivo**
  - Lista desplegable con todas las ventanas abiertas en el sistema.
- ✅ **Mensajes y errores traducidos** en tres idiomas (i18n).

---

## 📂 Estructura del proyecto
```
autoclicker/
│── app.py                 # Punto de entrada
│── controllers/
│   └── app_controller.py  # Lógica principal
│── models/
│   ├── settings.py        # Configuración de perfiles
│   ├── auto_clicker.py    # Implementación del autoclicker
│   └── profiles.py        # Almacenamiento de múltiples perfiles
│── views/
│   └── main_window.py     # Interfaz Tkinter
│── profiles.json          # Perfiles del usuario
│── translations.json      # Traducciones (pt, en, es)
│── requirements.py        # Instalador automático de dependencias
│── README.md              # Documento principal (PT-BR)
```

---

## ⚙️ Instalación
1. Clona el repositorio:
    ```sh
    git clone https://github.com/LuisFurmiga/autoclicker.git
    ```
2. Accede al directorio:
    ```sh
    cd autoclicker
    ```
3. Si aún no tienes Python instalado, consulta la guía [Python para Windows](https://github.com/LuisFurmiga/Autoclicker/blob/main/languages/es/python_windows.es.md).
4. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```
   o usa el instalador automático:
    ```sh
    python requirements.py
    ```

---

## 🎮 Uso
1. Ejecuta el programa:
    ```sh
    python app.py
    ```
2. Selecciona la **ventana objetivo** desde la lista desplegable.
3. Ajusta los intervalos de clic, el tiempo de pulsación y las teclas adicionales.
4. Guarda tu configuración en un **perfil**.
5. Usa:
   - `F1` → **Iniciar**
   - `F2` → **Detener**

---

## 🌐 Idiomas soportados
- 🇧🇷 Portugués  
- 🇺🇸 Inglés  
- 🇪🇸 Español  

El idioma se puede cambiar directamente en el **menú de la interfaz**.

---

## 📤 Perfiles
- Crea tantos como quieras.
- Exporta/importa perfiles individuales o todos a la vez.
- Los perfiles se guardan en `profiles.json`.

---

## 🛠️ Dependencias
- [keyboard](https://pypi.org/project/keyboard/) → atajos globales  
- [pywin32](https://pypi.org/project/pywin32/) → manejo de ventanas y eventos de Windows  

---

## ⚠️ Notas importantes
- Ejecuta como **Administrador** si los atajos globales no funcionan dentro del juego.  
- El programa es **solo para Windows** debido a la dependencia de `pywin32`.  

---

## 📜 Licencia
Este proyecto es de código abierto bajo la licencia [MIT](https://opensource.org/licenses/MIT).
