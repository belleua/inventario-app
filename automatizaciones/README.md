#  Pruebas Automatizadas – Inventario App

Proyecto de pruebas Selenium para la aplicación **inventario-app** (React + Bootstrap).

---

##  Estructura del proyecto

```
selenium-inventario/
├── tests/
│   └── test_inventario.py     ← Casos de prueba (7 HU, 21 pruebas)
├── screenshots/               ← Capturas automáticas (se genera al ejecutar)
├── reports/                   ← Reportes HTML (se genera al ejecutar)
├── run_report.py              ← Script principal: ejecuta y genera reporte
├── requirements.txt
└── README.md
```

---

##  Requisitos previos

| Herramienta | Versión mínima |
|-------------|---------------|
| Python      | 3.9+          |
| Google Chrome | Cualquier versión reciente |
| Node.js     | 18+ (para correr la app React) |

---

##  Instalación paso a paso

### 1. Clona este repositorio de pruebas (o copia los archivos)

```bash
git clone <URL-DE-TU-REPO-DE-PRUEBAS>
cd selenium-inventario
```

### 2. Crea un entorno virtual (recomendado)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

> **Nota:** `webdriver-manager` descarga automáticamente el ChromeDriver correcto.
> No necesitas instalarlo manualmente.

### 4. Levanta la aplicación React

En **otra terminal**:

```bash
cd inventario-app       # tu carpeta del proyecto React
npm install
npm start
```

Asegúrate de que esté corriendo en `http://localhost:3000`.

---

##  Ejecutar las pruebas

```bash
python -m pytest tests/test_inventario.py -v
# o sin pytest:
python tests/test_inventario.py
```

---

## Historias de Usuario cubiertas

| ID   | Historia                            | Pruebas |
|------|-------------------------------------|---------|
| HU-01 | Acceso a la aplicación             | Camino feliz · Negativo · Límite |
| HU-02 | Agregar producto (CREATE)          | Camino feliz · Negativo · 2 Límites |
| HU-03 | Ver lista de productos (READ)      | Camino feliz · Negativo · Límite |
| HU-04 | Editar producto (UPDATE)           | Camino feliz · Negativo · Límite |
| HU-05 | Eliminar producto (DELETE)         | Camino feliz · Negativo · Límite |
| HU-06 | Clasificación por estado           | Camino feliz · Negativo · Límite |
| HU-07 | Panel de estadísticas              | Camino feliz · Negativo · Límite |

**Total: 21 casos de prueba**

---

##  Modo headless (sin abrir navegador)

Edita `tests/test_inventario.py` y descomenta esta línea en `get_driver()`:

```python
# options.add_argument("--headless=new")
```

Cambia a:

```python
options.add_argument("--headless=new")
```

---
##  Capturas automáticas

Todas las capturas se guardan en `screenshots/` con formato:

```
YYYYMMDD_HHMMSS_HUxx_nombre_escenario.png
```

El reporte HTML las incrusta directamente en formato base64.

---

##  Accesos requeridos

- Repositorio GitHub: público
- Jira/Azure DevOps: acceso a `ktejada@itla.edu.do` y `20186927@itla.edu.do`
- Video YouTube: público

---

##  Tecnologías utilizadas

- **Lenguaje:** Python 3
- **Framework de pruebas:** `unittest` (estándar de Python)
- **Automatización:** Selenium 4 + WebDriver Manager
- **Reporte:** HTML generado dinámicamente con capturas incrustadas
