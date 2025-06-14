# Aplicación de Registro de Victimas de Delitos contra las Personas para fines estadísticos

## Objetivo del Proyecto
Desarrollar una aplicación web que permita:
- Registrar denuncias por delitos contra las personas
- Segmentar datos por:
  - Género
  - Comuna (1 a 15, CABA)
  - Tipo de delito
  - Edad del denunciante
- Incluir sistema de visualización con gráficos estadísticos dinámicos

## Tecnologías a Utilizar
- **Entorno de desarrollo**: Visual Studio Code
- **Lenguaje base**: Python
- **Framework web**: Django (backend)
- **Visualización de datos**: Chart.js
- **Base de datos**: SQLite (desarrollo inicial)

## Etapas de Desarrollo

### 1. Inicio del Proyecto
- Crear nuevo proyecto Django
- Configurar aplicación para gestión de denuncias
- Integrar modelos, formularios, vistas y plantillas

### 2. Diseño de la Base de Datos
Estructura para almacenar:
- Datos de la víctima:
  - Fecha de nacimiento
  - Género
- Comuna del delito (1-15)
- Tipo de delito
- Fecha de denuncia

### 3. Desarrollo del Formulario Web
- Implementar formulario interactivo con:
  - Campos validados
  - Listas desplegables
  - Facilidad de uso

### 4. Registro de Denuncias
- Almacenamiento seguro en base de datos
- Diseño accesible e intuitivo

### 5. Cálculo de Edad de la Víctima
- Cálculo automático desde fecha de nacimiento
- Datos clave para estadísticas demográficas

### 6. Generación de Estadísticas
Visualización de:
- Distribución por género
- Tipos de delitos
- Distribución por edad

### 7. Integración de Chart.js
- Gráficos interactivos:
  - Torta
  - Barras
  - Otros tipos según necesidad

### 8. Navegación y Estética
- Interfaz intuitiva
- Enlaces entre secciones
- Estilos básicos
- Mejorar experiencia de usuario

## Resultados Esperados
- Aplicación web para registro ordenado y seguro
- Base de datos estructurada para análisis
- Gráficos dinámicos para visualización de:
  - Distribución por género/edad
  - Tipos de delito
- Herramienta escalable para futuras mejoras:
  - Filtros por fecha
  - Autenticación
  - Exportación de reportes
