<div align="center">

![Banner](banner.png)

# 🖼️ Descargador de Imágenes de Unsplash

### Descarga imágenes gratuitas de alta calidad desde Unsplash con facilidad

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.16%2B-green.svg)](https://www.selenium.dev/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow.svg)](LICENSE)
[![Estilo de Código](https://img.shields.io/badge/estilo%20de%20código-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

[English](README.md) • [Español](#español)

</div>

---

## Español

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Configuración](#-configuración)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Ejemplos](#-ejemplos)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Agradecimientos](#-agradecimientos)

## ✨ Características

- 🔍 **Búsqueda Inteligente** - Busca cualquier tema y descarga imágenes relacionadas
- 🚀 **Desplazamiento Automático** - Carga automáticamente más imágenes para cumplir tus requisitos
- 📦 **Descarga por Lotes** - Descarga múltiples imágenes de una vez
- ⚙️ **Configurable** - Fácil de personalizar configuraciones y parámetros
- 🎯 **Soporte CLI** - Modos de línea de comandos e interactivo
- 📝 **Registro Completo** - Rastrea el proceso de scraping con registros detallados
- 🧹 **Código Limpio** - Bien estructurado, documentado y siguiendo los estándares PEP 8
- 🔒 **Manejo de Errores** - Manejo robusto de errores para problemas de red y tiempos de espera
- 🎨 **Solo Licencia Gratuita** - Solo descarga imágenes con licencias gratuitas de Unsplash

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.8 o superior** ([Descargar Python](https://www.python.org/downloads/))
- **Navegador Google Chrome** (se recomienda la última versión)
- **ChromeDriver** - Será administrado automáticamente por Selenium

> **Nota:** Este scraper usa Selenium WebDriver que descargará y administrará ChromeDriver automáticamente para ti.

## 📥 Instalación

1. **Clona el repositorio**

```bash
git clone https://github.com/p0sadas/unsplash-image-scraper.git
cd unsplash-image-scraper
```

2. **Crea un entorno virtual** (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las dependencias**

```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Modo Interactivo

Simplemente ejecuta el script principal sin argumentos:

```bash
python main.py
```

Se te pedirá que ingreses:

- Consulta de búsqueda (por ejemplo, "montañas", "tecnología", "animales")
- Número de imágenes a descargar

### Modo Línea de Comandos

```bash
# Uso básico (se ejecuta en modo sin interfaz por defecto)
python main.py -q "gatos" -n 10

# Con directorio de salida personalizado
python main.py -q "naturaleza" -n 25 -o "mis_imagenes"

# Mostrar ventana del navegador (deshabilitar modo sin interfaz)
python main.py -q "tecnología" -n 15 --no-headless
```

### Argumentos Disponibles

| Argumento       | Abreviado | Descripción                                              | Requerido |
| --------------- | --------- | -------------------------------------------------------- | --------- |
| `--query`       | `-q`      | Consulta de búsqueda (ej. 'gato', 'naturaleza')          | No\*      |
| `--num-images`  | `-n`      | Número de imágenes a descargar                           | No\*      |
| `--output`      | `-o`      | Directorio de salida (predeterminado: downloads)         | No        |
| `--no-headless` | -         | Mostrar ventana del navegador (sin interfaz por defecto) | No        |
| `--help`        | `-h`      | Mostrar mensaje de ayuda                                 | No        |

\*Si no se proporcionan, se usará el modo interactivo.

## ⚙️ Configuración

Puedes personalizar el comportamiento del scraper modificando `src/config.py`:

```python
# Tiempos de espera
WEBDRIVER_TIMEOUT = 20  # segundos
SCROLL_PAUSE_TIME = 0.3  # segundos entre desplazamientos

# Salida
DOWNLOAD_DIR = BASE_DIR / "downloads"
IMAGE_FORMAT = "jpg"

# Registro
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
```

## 📁 Estructura del Proyecto

```
unsplash-image-scraper/
├── src/
│   ├── __init__.py           # Inicialización del paquete
│   ├── config.py             # Configuraciones
│   └── unsplash_scraper.py   # Clase principal del scraper
├── downloads/                # Imágenes descargadas (se crea automáticamente)
├── main.py                   # Script de punto de entrada
├── requirements.txt          # Dependencias de Python
├── .gitignore               # Reglas de ignorar de Git
├── LICENSE                  # Licencia MIT
└── README.md               # Este archivo
```

## 💡 Ejemplos

### Ejemplo 1: Descargar Imágenes de Gatos

```bash
python main.py -q "gatos" -n 20
```

Salida:

```
🔍 Buscando 'gatos'...
📊 Objetivo: 20 imágenes
📁 Salida: C:\ruta\a\downloads

✅ Se encontraron 20 imágenes
📥 Descargando imágenes...

✨ ¡Se descargaron 20 imágenes exitosamente!
📂 Imágenes guardadas en: C:\ruta\a\downloads
```

### Ejemplo 2: Usar como Módulo de Python

```python
from src.unsplash_scraper import UnsplashScraper
from pathlib import Path

# Crear instancia del scraper
with UnsplashScraper(headless=True) as scraper:
    # Extraer URLs de imágenes
    urls = scraper.scrape_images("montañas", num_images=10)

    # Descargar imágenes
    output = Path("mis_montañas")
    scraper.download_images(urls, output_dir=output)

print(f"¡Se descargaron {len(urls)} imágenes!")
```

### Ejemplo 3: Ejecutar con Navegador Visible

```bash
# Mostrar la ventana del navegador (útil para depuración)
python main.py -q "arte abstracto" -n 30 --no-headless
```

## 🔍 Solución de Problemas

### Problema: "ChromeDriver no encontrado"

**Solución:** Selenium 4.16+ administra ChromeDriver automáticamente. Asegúrate de tener la última versión:

```bash
pip install --upgrade selenium
```

### Problema: "TimeoutException"

**Solución:** Esto generalmente significa que la página tardó demasiado en cargar. Intenta:

- Aumentar `WEBDRIVER_TIMEOUT` en `src/config.py`
- Verificar tu conexión a internet
- Asegurar que Unsplash sea accesible en tu región

### Problema: "No se encontraron imágenes"

**Solución:**

- Intenta una consulta de búsqueda diferente
- Asegúrate de buscar temas que existan en Unsplash
- Verifica si Unsplash ha cambiado la estructura de su página (los selectores XPath pueden necesitar actualización)

### Problema: "La descarga falla para algunas imágenes"

**Solución:** Esto es normal - algunas imágenes pueden no estar disponibles temporalmente. El scraper registrará los errores y continuará con otras imágenes.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Aquí está cómo puedes ayudar:

1. Haz un fork del repositorio
2. Crea una rama de característica (`git checkout -b feature/CaracteristicaIncreible`)
3. Confirma tus cambios (`git commit -m 'Agregar alguna CaracteristicaIncreible'`)
4. Empuja a la rama (`git push origin feature/CaracteristicaIncreible`)
5. Abre un Pull Request

Por favor asegúrate de que tu código siga las pautas de estilo PEP 8 e incluya la documentación apropiada.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Descargo de Responsabilidad

Esta herramienta es solo para fines educativos. Por favor respeta los [Términos de Servicio](https://unsplash.com/terms) de Unsplash y las [Directrices de API](https://unsplash.com/api-terms). Siempre da crédito a los fotógrafos cuando uses sus imágenes.

## 🙏 Agradecimientos

- [Unsplash](https://unsplash.com/) por proporcionar imágenes gratuitas de alta calidad
- [Selenium](https://www.selenium.dev/) por las capacidades de automatización web
- La comunidad de código abierto por la inspiración y el apoyo

---

<div align="center">

Hecho con ❤️ por Angel Posadas

⭐ ¡Dale una estrella a este repositorio si te resultó útil!

</div>
