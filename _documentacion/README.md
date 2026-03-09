# 📚 DOCUMENTACIÓN COMPLETA - SISTEMA DE VIAJES DHL

## Bienvenido a la Documentación Técnica

Esta carpeta contiene **toda la documentación** del Sistema de Viajes DHL en dos formatos:
- **📄 PDF**: Ideal para imprimir o leer sin conexión
- **📝 Markdown (.md)**: Ideal para editar o leer en navegador/VS Code

---

## 📦 CONTENIDO DISPONIBLE

### 1️⃣ ARQUITECTURA DE LA APLICACIÓN
Estructura completa del sistema, componentes y tecnologías

- 📄 [PDF - ARQUITECTURA_APLICACION.pdf](pdfs/ARQUITECTURA_APLICACION.pdf)
- 📝 [Markdown - ARQUITECTURA_APLICACION.md](ARQUITECTURA_APLICACION.md)

**Temas**: Flask, SQLite, Waitress, estructura de carpetas, módulos Python

---

### 2️⃣ SERVIDOR (WAITRESS + FLASK)
Configuración y uso del servidor web de producción

- 📄 [PDF - SERVIDOR_DOCUMENTACION.pdf](pdfs/SERVIDOR_DOCUMENTACION.pdf)
- 📝 [Markdown - SERVIDOR_DOCUMENTACION.md](SERVIDOR_DOCUMENTACION.md)

**Temas**: Instalación, puertos, IPs, comandos, troubleshooting

---

### 3️⃣ INTERFAZ DE USUARIO
Manual completo para usuarios del sistema web

- 📄 [PDF - INTERFAZ_USO.pdf](pdfs/INTERFAZ_USO.pdf)
- 📝 [Markdown - INTERFAZ_USO.md](INTERFAZ_USO.md)

**Temas**: Crear viajes, editar, generar PDFs, reportes Excel, maestras

---

### 4️⃣ DIAGRAMAS DE FLUJO
12 diagramas visuales de procesos del sistema

- 📄 [PDF - DIAGRAMAS_FLUJO.pdf](pdfs/DIAGRAMAS_FLUJO.pdf)
- 📝 [Markdown - DIAGRAMAS_FLUJO.md](DIAGRAMAS_FLUJO.md)

**Temas**: Flujos de autenticación, creación de viaje, PDFs, reportes

---

### 5️⃣ ESTRUCTURA DE BASE DE DATOS
Esquema completo de SQLite con 9 tablas

- 📄 [PDF - ESTRUCTURA_BD.pdf](pdfs/ESTRUCTURA_BD.pdf)
- 📝 [Markdown - ESTRUCTURA_BD.md](ESTRUCTURA_BD.md)

**Temas**: Tablas, relaciones, índices, queries, backup, ER diagrams

---

## 🎯 INICIO RÁPIDO

### ¿Primera vez aquí?

1. **Si eres USUARIO**: Lee [INTERFAZ_USO.pdf](pdfs/INTERFAZ_USO.pdf)
2. **Si eres DESARROLLADOR**: Lee [ARQUITECTURA_APLICACION.pdf](pdfs/ARQUITECTURA_APLICACION.pdf)
3. **Si eres ADMIN DE SISTEMA**: Lee [SERVIDOR_DOCUMENTACION.pdf](pdfs/SERVIDOR_DOCUMENTACION.pdf)

### ¿Necesitas algo específico?

| Necesitas... | Ve a este documento |
|--------------|---------------------|
| Crear un viaje nuevo | INTERFAZ_USO.md → Sección 2 |
| Iniciar el servidor | SERVIDOR_DOCUMENTACION.md → Sección 5 |
| Ver estructura de BD | ESTRUCTURA_BD.md → Sección 11 (Diagrama ER) |
| Entender el código | ARQUITECTURA_APLICACION.md → Sección 3 |
| Ver flujos visuales | DIAGRAMAS_FLUJO.md (todos los diagramas) |
| Generar reportes | INTERFAZ_USO.md → Sección 4 |
| Gestionar usuarios | INTERFAZ_USO.md → Sección 5 |
| Hacer backup de BD | ESTRUCTURA_BD.md → Sección 16 |

---

## 🔄 REGENERAR PDFs

Si actualizaste los archivos Markdown y quieres regenerar los PDFs:

```cmd
# Ejecutar desde la raíz del proyecto:
GENERAR_DOCS_PDF.bat
```

Los PDFs se generarán automáticamente en la carpeta `pdfs/`

---

## 📂 ESTRUCTURA DE ARCHIVOS

```
_documentacion/
│
├── pdfs/                                    ← PDFs GENERADOS
│   ├── ARQUITECTURA_APLICACION.pdf
│   ├── SERVIDOR_DOCUMENTACION.pdf
│   ├── INTERFAZ_USO.pdf
│   ├── DIAGRAMAS_FLUJO.pdf
│   ├── ESTRUCTURA_BD.pdf
│   └── README.md
│
├── ARQUITECTURA_APLICACION.md              ← MARKDOWN FUENTE
├── SERVIDOR_DOCUMENTACION.md
├── INTERFAZ_USO.md
├── DIAGRAMAS_FLUJO.md
├── ESTRUCTURA_BD.md
├── README.md                               ← ESTE ARCHIVO
│
├── CHANGELOG_26FEB2026.md                  ← Otros documentos
├── COMO_EJECUTAR_PORTABLE.md
├── COMO_VER_BASE_DATOS.md
└── CONFIGURACION_ENTORNOS.md
```

---

## 📊 ESTADÍSTICAS DE DOCUMENTACIÓN

| Documento | Secciones | Páginas (aprox.) | Tamaño |
|-----------|-----------|------------------|--------|
| ARQUITECTURA_APLICACION | 18 | 65 | 650 KB |
| SERVIDOR_DOCUMENTACION | 15 | 35 | 420 KB |
| INTERFAZ_USO | 22 | 80 | 890 KB |
| DIAGRAMAS_FLUJO | 12 | 25 | 380 KB |
| ESTRUCTURA_BD | 20 | 55 | 630 KB |
| **TOTAL** | **87** | **~260** | **~3 MB** |

---

## 🎨 CARACTERÍSTICAS DE LOS PDFs

✅ **Portadas Profesionales**: Con logo DHL y fecha
✅ **Diseño a Color**: Tablas naranjas, alertas rojas, código con fondo gris
✅ **Tipografía Grande**: Fuentes de 10-14pt para fácil lectura
✅ **Separación Visual**: Secciones claramente delimitadas con colores
✅ **Tablas Coloreadas**: Headers destacados, filas alternadas
✅ **Códigos Resaltados**: Fondo gris claro con bordes
✅ **Alertas Visuales**: Cajas de color (verde=éxito, rojo=error, azul=info)
✅ **Optimizado para Impresión**: Márgenes correctos, saltos de página inteligentes

---

## 🖨️ TIPS DE IMPRESIÓN

**Configuración Recomendada:**
- Orientación: Vertical
- Color: Sí (mejora mucho la legibilidad)
- Doble cara: Sí (ahorra ~130 hojas)
- Calidad: Media
- Páginas por hoja: 1

**Costo Estimado (impresión externa):**
- B&N: ~$10 USD para 260 páginas
- Color: ~$30 USD para 260 páginas

---

## 📖 FORMATO MARKDOWN

Los archivos `.md` se pueden:
- ✅ Ver en VS Code (con vista previa: `Ctrl+Shift+V`)
- ✅ Ver en GitHub/GitLab automáticamente
- ✅ Editar con cualquier editor de texto
- ✅ Convertir a HTML con herramientas como Pandoc
- ✅ Ver diagramas Mermaid en GitHub o con extensiones

---

## 💡 TIPS DE NAVEGACIÓN

### En PDFs:
- `Ctrl+F`: Buscar texto
- Panel izquierdo: Marcadores de secciones
- `Ctrl++`/`Ctrl+-`: Zoom in/out
- `Ctrl+P`: Imprimir secciones específicas

### En Markdown (VS Code):
- `Ctrl+Shift+V`: Vista previa
- `Ctrl+Click`: Seguir enlaces
- `Ctrl+F`: Buscar en documento
- Extensión Mermaid: Ver diagramas renderizados

---

## 🔗 DOCUMENTOS RELACIONADOS

Otros archivos útiles en esta carpeta:
- [CHANGELOG_26FEB2026.md](CHANGELOG_26FEB2026.md) - Cambios recientes del sistema
- [COMO_EJECUTAR_PORTABLE.md](COMO_EJECUTAR_PORTABLE.md) - Ejecutar sin instalación
- [COMO_VER_BASE_DATOS.md](COMO_VER_BASE_DATOS.md) - Abrir SQLite en DB Browser
- [CONFIGURACION_ENTORNOS.md](CONFIGURACION_ENTORNOS.md) - Setup de desarrollo

---

## ❓ SOPORTE Y CONTACTO

¿Tienes preguntas sobre la documentación?

📧 **Email IT**: [soporte-it@dhl.com]  
💬 **Teams**: Canal #sistema-viajes-soporte  
📞 **Teléfono**: Ext. 1234

---

## 📅 ÚLTIMA ACTUALIZACIÓN

**Fecha**: 27 de Febrero de 2026  
**Versión del Sistema**: 2.0  
**Documentos**: 5 principales + 4 complementarios

---

*Documentación generada automáticamente por el Sistema de Viajes DHL*  
*Para regenerar PDFs: `GENERAR_DOCS_PDF.bat`*
