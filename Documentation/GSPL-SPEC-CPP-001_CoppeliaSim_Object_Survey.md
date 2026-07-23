# GSPL-SPEC-CPP-001

# Relevamiento de Objetos de CoppeliaSim para GSPL

**Proyecto:** GIAR Simulation Pipeline (GSPL)\
**Documento:** GSPL-SPEC-CPP-001\
**Estado:** Draft 1.0

------------------------------------------------------------------------

# 1. Objetivo

Este documento releva los tipos de objetos disponibles en CoppeliaSim
que serán soportados por el GIAR Simulation Pipeline (GSPL).

Su finalidad es definir la información que deberá preservar el archivo
`2_simulation_database.json` generado por **GSPL-02 Simulation
Compiler**.

## Principios

-   El componente es la unidad de ingeniería.
-   Cada componente puede contener cero o más objetos de CoppeliaSim.
-   Ningún dato ingresado por el ingeniero en `1_assembly_table.xlsx`
    debe perderse durante la compilación.
-   GSPL-02 puede reorganizar la información, pero nunca descartarla.

------------------------------------------------------------------------

# 2. Objetos soportados

## Nivel 1 (implementación inicial)

  Objeto             Prioridad
  ------------------ -----------
  Shape              Muy alta
  Joint              Muy alta
  Dummy              Muy alta
  Force Sensor       Alta
  Vision Sensor      Alta
  Proximity Sensor   Alta
  Camera             Alta
  Light              Alta

## Nivel 2 (futuras versiones)

-   Graph
-   Path
-   Point Cloud
-   Octree

------------------------------------------------------------------------

# 3. Shape

## Función

Representa geometría física y/o visual.

## Información relevante

-   Malla visual
-   Malla de colisión
-   Masa
-   Tensor de inercia
-   Centro de masa
-   Color
-   Transparencia
-   Dinámica
-   Colisiones

## Organización sugerida

``` text
Shape
 ├── geometry
 ├── appearance
 ├── physics
 ├── dynamics
 ├── collision
 └── rendering
```

------------------------------------------------------------------------

# Capítulo 4 — Joint

## 4.1 Introducción

Un **Joint** representa un grado de libertad mecánico dentro de un modelo de simulación.

En CoppeliaSim constituye el elemento encargado de conectar dos cuerpos rígidos permitiendo movimiento relativo entre ellos.

Los joints son los objetos responsables de definir la cinemática del robot o mecanismo y pueden actuar tanto como elementos pasivos como actuadores controlados.

En GSPL, un Joint siempre pertenece a un único componente de ingeniería y forma parte del conjunto de objetos de simulación asociados a dicho componente.

---

## 4.2 Tipos de Joint soportados

CoppeliaSim soporta tres tipos de joints.

| Tipo | Descripción |
|-------|-------------|
| Revolute | Movimiento rotacional alrededor de un eje. |
| Prismatic | Movimiento lineal sobre un eje. |
| Spherical | Rotación libre en tres grados de libertad. |

GSPL soportará los tres tipos.

---

## 4.3 Función dentro del GSPL

Los joints permiten construir la estructura cinemática del modelo.

Durante GSPL-05 cada Joint será convertido en un objeto Joint de CoppeliaSim.

GSPL-03 utilizará la información de los joints para construir el árbol cinemático y calcular los marcos de referencia.

---

## 4.4 Información común

Todo Joint posee la información común definida para cualquier objeto de simulación:

- Object ID
- Nombre
- Estado Enabled
- Parent
- Pose
- Reference Frame
- Propiedades comunes

Estas propiedades son independientes del tipo de joint.

---

## 4.5 Parámetros específicos

Además de las propiedades comunes, un Joint posee información propia.

### Tipo

Determina el comportamiento cinemático.

Valores posibles:

- Revolute
- Prismatic
- Spherical

---

### Cyclic

Indica si el movimiento posee límites.

Valores:

- TRUE
- FALSE

Cuando Cyclic es TRUE el movimiento puede girar indefinidamente.

---

### Límites

Para joints no cíclicos.

Campos:

- Lower Limit
- Upper Limit

Las unidades dependen del tipo de joint.

Revolute:
- radianes

Prismatic:
- metros

---

### Motor

Determina si el joint posee un actuador.

Valores soportados por GSPL:

- Position
- Velocity
- Torque

Estos modos corresponden a los modos de control soportados por CoppeliaSim.

---

### Target Position

Posición objetivo utilizada cuando el joint trabaja en modo Position.

---

### Target Velocity

Velocidad objetivo utilizada cuando el joint trabaja en modo Velocity.

---

### Maximum Force

Esfuerzo máximo permitido por el actuador.

Para joints rotacionales representa torque.

Para joints prismáticos representa fuerza lineal.

---

### Maximum Velocity

Velocidad máxima permitida para el actuador.

---

### PID

Los joints controlados en posición utilizan un controlador PID.

Parámetros:

- P
- I
- D

GSPL reservará espacio para estos parámetros aunque inicialmente utilice los valores por defecto de CoppeliaSim.

---

### Dependency

Un joint puede depender de otro joint.

Esta característica permite construir mecanismos sincronizados.

GSPL reservará soporte para esta característica.

---

### Screw Lead

Propiedad exclusiva de determinados joints prismáticos utilizados como tornillos.

GSPL reservará soporte para esta propiedad.

---

## 4.6 Propiedades no consideradas en GSPL 1.0

Las siguientes capacidades existen en CoppeliaSim pero no serán utilizadas inicialmente.

- Joint callback functions
- Hybrid operation modes
- User callbacks
- Custom control scripts

Estas propiedades podrán incorporarse en futuras versiones sin modificar la estructura general del Simulation Database.

---

## 4.7 Información proveniente del Excel

Actualmente la planilla de ingeniería proporciona los siguientes datos.

| Campo Excel | Destino |
|--------------|---------|
| Joint Type | joint.type |
| Cyclic | joint.cyclic |
| Lower Limit | joint.lower_limit |
| Upper Limit | joint.upper_limit |
| Motor | joint.motor |

En futuras versiones podrán agregarse nuevas columnas para completar el resto de la información.

---

## 4.8 Representación propuesta

Se recomienda almacenar la información específica del Joint en un bloque independiente.

```json
{
    "type": "Joint",

    "joint": {

        "type": "Revolute",

        "cyclic": false,

        "lower_limit": -180,

        "upper_limit": 180,

        "motor": "Position",

        "target_position": 0,

        "target_velocity": 0,

        "maximum_force": null,

        "maximum_velocity": null,

        "pid": {

            "p": null,
            "i": null,
            "d": null
        },

        "dependency": null,

        "screw_lead": null
    }
}
```

---

## 4.9 Filosofía de diseño

GSPL únicamente almacena la información necesaria para reconstruir completamente el Joint dentro de CoppeliaSim.

La estructura podrá ampliarse en versiones futuras incorporando nuevos parámetros sin modificar la organización general del Simulation Database.

------------------------------------------------------------------------

# Capítulo 5 — Dummy

## 5.1 Introducción

Un **Dummy** es un objeto de referencia tridimensional utilizado para representar una posición y orientación dentro de la escena de CoppeliaSim.

A diferencia de un Shape, un Dummy no posee geometría física ni visual destinada a representar un componente mecánico. Su función principal consiste en definir sistemas de coordenadas, puntos de referencia y relaciones espaciales entre objetos.

Los Dummies son ampliamente utilizados por CoppeliaSim para implementar algoritmos de cinemática directa e inversa (IK), definir puntos de ensamblado (Assembly Points), establecer referencias para sensores y herramientas, y construir árboles cinemáticos complejos.

Dentro del GSPL, el Dummy constituye el objeto estándar para representar **Reference Frames**.

---

## 5.2 Función dentro del GSPL

En el GIAR Simulation Pipeline un Dummy puede utilizarse para:

- Definir el sistema de coordenadas de un componente.
- Representar puntos de montaje.
- Representar herramientas (Tool Frames).
- Representar puntos de calibración.
- Representar sistemas de referencia locales.
- Representar referencias para sensores.
- Representar referencias para actuadores.
- Servir como extremo de cadenas cinemáticas.
- Servir como origen de transformaciones.

Los Dummies no representan geometría CAD.

Su función es exclusivamente geométrica y cinemática.

---

## 5.3 Propiedades generales

Como cualquier objeto de CoppeliaSim, un Dummy posee todas las propiedades comunes:

- Object ID
- Nombre
- Enabled
- Parent
- Pose
- Reference Frame
- Visibility
- Layer
- Alias

Estas propiedades son independientes de la función específica del Dummy.

---

## 5.4 Tamaño

El tamaño determina únicamente la representación gráfica del Dummy dentro de la escena.

No modifica el comportamiento de la simulación.

GSPL podrá definir un tamaño por defecto configurable.

---

## 5.5 Color

El color únicamente afecta la representación visual del Dummy.

Puede utilizarse para identificar distintos tipos de referencias.

Ejemplo:

- Azul → Reference Frame
- Verde → Sensor Frame
- Amarillo → Tool Frame
- Rojo → IK Target

La asignación de colores queda a criterio del constructor GSPL-05.

---

## 5.6 Link Type

CoppeliaSim permite vincular dos Dummies mediante distintos tipos de enlace.

Los principales son:

- IK Tip
- IK Target
- Dynamic Loop Closure
- GCS Loop Closure

Estos enlaces permiten construir mecanismos cerrados y resolver problemas de cinemática inversa.

GSPL reservará soporte para esta funcionalidad.

---

## 5.7 Assembly Match Values

Los Dummies pueden contener valores de ensamblado ("Assembly Match Values").

Estos valores permiten que CoppeliaSim conecte automáticamente dos componentes compatibles.

Esta característica resulta especialmente útil para:

- herramientas intercambiables;
- conectores;
- acoples rápidos;
- ensamblado automático.

GSPL reservará soporte para estos valores.

---

## 5.8 Parenting

Un Dummy puede pertenecer a cualquier objeto de la escena.

Por ejemplo:

- Shape
- Joint
- Dummy
- Vision Sensor
- Camera
- Force Sensor

Su transformación siempre dependerá del padre asignado.

---

## 5.9 Pose

El Dummy posee una transformación completa.

Compuesta por:

- Position (X,Y,Z)
- Orientation (Euler)
- Quaternion (internamente)

GSPL almacenará la pose utilizando la representación estándar definida para todos los objetos de simulación.

---

## 5.10 Reference Frames

Esta es probablemente la función más importante del Dummy dentro del GSPL.

Cada Dummy puede representar un sistema de coordenadas local.

Será utilizado por GSPL para:

- construir el Reference Frame Tree;
- calcular transformaciones;
- definir Tool Frames;
- definir Sensor Frames;
- definir Base Frames;
- definir World Frames.

Durante GSPL-03 estos marcos de referencia serán utilizados para resolver toda la cinemática del modelo.

---

## 5.11 Información proveniente del Excel

Actualmente la planilla de ingeniería proporciona la siguiente información.

| Campo Excel | Destino |
|--------------|---------|
| Object Type = Dummy | object.type |
| Object Name | object.name |
| Reference Frame | object.reference_frame |
| Position | pose.position |
| Rotation | pose.orientation |
| Enabled | enabled |

En futuras versiones podrán incorporarse nuevas columnas para Assembly Match Values y Link Type.

---

## 5.12 Representación propuesta

Se recomienda almacenar la información específica del Dummy dentro de un bloque especializado.

```json
{
    "type": "Dummy",

    "dummy": {

        "size": 0.02,

        "color": [0.0,0.5,1.0],

        "link_type": null,

        "assembly_match": null,

        "reference_frame": true,

        "role": "Reference Frame"
    }
}
```

---

## 5.13 Roles sugeridos

GSPL podrá clasificar los Dummies mediante un rol específico.

Ejemplos:

- Reference Frame
- Tool Frame
- Sensor Frame
- Mount Point
- Calibration Point
- IK Tip
- IK Target
- Connector
- User Defined

Esta clasificación no existe como propiedad propia de CoppeliaSim, pero constituye una extensión de ingeniería útil para el GSPL.

---

## 5.14 Filosofía de diseño

En GSPL un Dummy no representa un objeto físico.

Representa información geométrica.

Su finalidad es proporcionar una referencia espacial reutilizable durante todas las etapas del pipeline.

La incorporación de Dummies permite desacoplar completamente la geometría CAD de la estructura cinemática del modelo, facilitando la construcción del árbol de referencias y la generación automática del modelo de simulación.

------------------------------------------------------------------------

# Capítulo 6 — Force Sensor

## 6.1 Introducción

Un **Force Sensor** es un objeto de CoppeliaSim diseñado para medir las fuerzas y momentos (torques) transmitidos entre dos objetos conectados dentro de la escena.

A diferencia de un Shape o un Joint, un Force Sensor no representa una pieza física del modelo, sino un instrumento virtual de medición que permite conocer el esfuerzo mecánico existente entre dos cuerpos.

Los Force Sensors son ampliamente utilizados para:

- Medición de fuerzas.
- Medición de torques.
- Sensores de muñeca (Wrist Force/Torque Sensor).
- Sistemas de control por fuerza.
- Detección de colisiones.
- Protección contra sobrecargas.
- Retroalimentación para algoritmos de control.

Dentro del GSPL, un Force Sensor será tratado como un objeto de simulación especializado asociado a un componente de ingeniería.

---

## 6.2 Función dentro del GSPL

Los Force Sensors permiten incorporar capacidades de medición al modelo de simulación.

Su información podrá ser utilizada por:

- Controladores.
- Algoritmos de IA.
- Simulaciones físicas.
- Ensayos virtuales.
- Validaciones de diseño.

El Force Sensor no genera movimiento.

Su función consiste exclusivamente en medir esfuerzos mecánicos.

---

## 6.3 Propiedades generales

Como cualquier objeto de CoppeliaSim, un Force Sensor posee todas las propiedades comunes definidas para los objetos de simulación.

Entre ellas:

- Object ID
- Nombre
- Enabled
- Parent
- Pose
- Reference Frame
- Visibility
- Layer

Estas propiedades son independientes del funcionamiento propio del sensor.

---

## 6.4 Fuerza medida

El sensor mide una fuerza tridimensional.

Componentes:

- Fx
- Fy
- Fz

Las unidades corresponden al Sistema Internacional.

Unidad:

Newton (N)

---

## 6.5 Torque medido

Además de la fuerza, el sensor mide el momento aplicado.

Componentes:

- Tx
- Ty
- Tz

Unidad:

Newton·metro (N·m)

---

## 6.6 Umbrales de ruptura

CoppeliaSim permite configurar límites máximos para:

- Fuerza
- Torque

Cuando alguno de estos límites es superado, el sensor puede romper la conexión entre ambos cuerpos.

Esta característica resulta útil para simular:

- fusibles mecánicos;
- acoples de seguridad;
- uniones frágiles.

GSPL reservará soporte para estos parámetros.

---

## 6.7 Breaking Enabled

Indica si la ruptura automática se encuentra habilitada.

Valores:

- TRUE
- FALSE

---

## 6.8 Filtrado

Los valores medidos pueden filtrarse para reducir ruido numérico.

CoppeliaSim incorpora mecanismos internos de filtrado.

GSPL reservará soporte para esta configuración.

---

## 6.9 Explicit Handling

Como muchos sensores de CoppeliaSim, un Force Sensor puede funcionar en dos modos:

### Automático

La simulación actualiza el sensor durante cada paso de integración.

### Explícito

El usuario controla cuándo actualizar el sensor mediante la API.

GSPL reservará soporte para este modo de funcionamiento.

---

## 6.10 Información proveniente del Excel

Actualmente la planilla de ingeniería no posee columnas específicas para Force Sensors.

Inicialmente el ingeniero únicamente podrá definir:

| Campo Excel | Destino |
|--------------|---------|
| Object Type | Force Sensor |
| Object Name | object.name |
| Enabled | enabled |
| Position | pose.position |
| Rotation | pose.orientation |
| Reference Frame | reference_frame |

Los parámetros específicos del sensor utilizarán inicialmente los valores por defecto definidos por GSPL.

En futuras versiones podrán incorporarse nuevas columnas para su configuración.

---

## 6.11 Representación propuesta

```json
{
    "type": "Force Sensor",

    "force_sensor": {

        "breaking_enabled": false,

        "force_threshold": null,

        "torque_threshold": null,

        "filter": {

            "enabled": false,

            "sample_size": null
        },

        "explicit_handling": false
    }
}
```

---

## 6.12 Información generada durante la simulación

Durante la ejecución del modelo, el Force Sensor produce información dinámica.

Entre ella:

- Fuerza resultante
- Torque resultante
- Estado de ruptura
- Estado del sensor

Estos datos no forman parte del `2_simulation_database.json`, ya que corresponden al estado dinámico de la simulación y no a la configuración del modelo.

---

## 6.13 Filosofía de diseño

GSPL almacena únicamente la configuración necesaria para reconstruir completamente el Force Sensor dentro de CoppeliaSim.

Los valores medidos durante la simulación no forman parte de la base de datos de ingeniería, ya que representan información temporal generada por el motor físico.

Esta separación garantiza que `2_simulation_database.json` contenga exclusivamente información de configuración y no resultados de la simulación.

------------------------------------------------------------------------

# Capítulo 7 — Vision Sensor

## 7.1 Introducción

Un **Vision Sensor** es un sensor virtual capaz de generar imágenes de la escena tridimensional simulada.

A diferencia de una Camera, un Vision Sensor no está pensado únicamente para visualizar la escena, sino para producir información que pueda ser utilizada por algoritmos de percepción, visión artificial, inteligencia artificial y procesamiento de imágenes.

El Vision Sensor constituye el equivalente virtual de una cámara utilizada por un robot.

Puede generar:

- Imagen RGB
- Imagen en escala de grises
- Imagen de profundidad (Depth Buffer)
- Máscaras
- Información para procesamiento de visión

Dentro del GSPL, un Vision Sensor representa un sensor inteligente capaz de observar el entorno.

---

## 7.2 Función dentro del GSPL

Los Vision Sensors podrán utilizarse para:

- Simulación de cámaras RGB.
- Simulación de cámaras monocromáticas.
- Algoritmos de visión artificial.
- Reconocimiento de objetos.
- Seguimiento visual.
- Navegación.
- IA.
- Detección de obstáculos.
- Localización.

Durante GSPL-05 serán convertidos en Vision Sensors nativos de CoppeliaSim.

---

## 7.3 Propiedades generales

Como cualquier objeto de simulación, un Vision Sensor posee todas las propiedades comunes:

- Object ID
- Nombre
- Enabled
- Parent
- Pose
- Reference Frame
- Visibility
- Layer

Estas propiedades son independientes del funcionamiento propio del sensor.

---

## 7.4 Tipo de proyección

CoppeliaSim soporta dos modos de proyección.

### Perspective

La proyección simula el comportamiento de una cámara convencional.

Los objetos lejanos aparecen más pequeños.

Es el modo recomendado para la mayoría de las aplicaciones robóticas.

---

### Orthographic

Los rayos son paralelos.

No existe perspectiva.

Se utiliza principalmente para inspección y aplicaciones industriales.

---

## 7.5 Resolución

El Vision Sensor genera imágenes digitales.

Resolución típica:

- 320 × 240
- 640 × 480
- 800 × 600
- 1024 × 768
- 1280 × 720
- 1920 × 1080

GSPL deberá permitir configurar la resolución del sensor.

---

## 7.6 Field of View (FOV)

Define el ángulo de visión del sensor.

Un FOV pequeño produce un efecto de zoom.

Un FOV grande produce una visión panorámica.

Unidad:

grados.

---

## 7.7 Near Clipping Plane

Define la distancia mínima visible.

Todo objeto ubicado delante de este plano será descartado.

Unidad:

metros.

---

## 7.8 Far Clipping Plane

Define la distancia máxima visible.

Todo objeto situado más allá de este plano no será renderizado.

Unidad:

metros.

---

## 7.9 Explicit Handling

El Vision Sensor puede funcionar en dos modos.

### Automático

La imagen se actualiza durante cada ciclo de simulación.

### Explícito

La actualización debe realizarse mediante llamadas a la API.

Este modo resulta útil para optimizar el rendimiento cuando existen numerosos sensores.

---

## 7.10 Render Mode

CoppeliaSim permite utilizar distintos modos de renderizado.

Entre ellos:

- OpenGL
- OpenGL3
- Ray Tracing (según disponibilidad)

GSPL reservará soporte para seleccionar el modo de renderizado.

---

## 7.11 Color Image

El Vision Sensor puede generar una imagen RGB.

Esta imagen será utilizada por:

- algoritmos de visión;
- reconocimiento de objetos;
- aprendizaje automático;
- inspección visual.

---

## 7.12 Depth Buffer

Además de la imagen RGB, el sensor puede producir un mapa de profundidad.

Cada píxel representa la distancia desde el sensor hasta el objeto observado.

Esta funcionalidad resulta especialmente útil para:

- reconstrucción 3D;
- navegación;
- SLAM;
- percepción espacial.

---

## 7.13 Filtros

CoppeliaSim permite aplicar distintos filtros de procesamiento.

Por ejemplo:

- Edge Detection
- Blur
- Sharpen
- Threshold
- Color Extraction

GSPL reservará soporte para almacenar esta configuración.

---

## 7.14 Información proveniente del Excel

Actualmente la planilla de ingeniería únicamente proporciona:

| Campo Excel | Destino |
|--------------|---------|
| Object Type | Vision Sensor |
| Object Name | object.name |
| Enabled | enabled |
| Position | pose.position |
| Rotation | pose.orientation |
| Reference Frame | reference_frame |

Los parámetros específicos utilizarán inicialmente los valores por defecto definidos por GSPL.

En futuras versiones podrán incorporarse nuevas columnas de configuración.

---

## 7.15 Representación propuesta

```json
{
    "type": "Vision Sensor",

    "vision_sensor": {

        "projection": "Perspective",

        "resolution": {

            "width": 640,

            "height": 480
        },

        "field_of_view": 60.0,

        "near_clipping": 0.01,

        "far_clipping": 10.0,

        "explicit_handling": false,

        "render_mode": "OpenGL",

        "generate_rgb": true,

        "generate_depth": true,

        "filters": []
    }
}
```

---

## 7.16 Información generada durante la simulación

Durante la simulación el Vision Sensor produce información dinámica.

Entre ella:

- Imagen RGB.
- Imagen en escala de grises.
- Imagen de profundidad.
- Objetos detectados.
- Estadísticas del sensor.

Esta información no forma parte del `2_simulation_database.json`, ya que representa resultados producidos durante la ejecución del modelo.

---

## 7.17 Filosofía de diseño

GSPL almacena únicamente la configuración necesaria para reconstruir el Vision Sensor dentro de CoppeliaSim.

Las imágenes generadas por el sensor, los mapas de profundidad y cualquier otra información obtenida durante la simulación son datos temporales y no forman parte de la base de datos de ingeniería.

La separación entre configuración y datos de simulación garantiza que el modelo pueda reconstruirse de forma determinística e independiente del estado de ejecución.

------------------------------------------------------------------------

# Capítulo 8 — Proximity Sensor

## 8.1 Introducción

Un **Proximity Sensor** es un sensor virtual capaz de detectar la presencia de objetos dentro de un volumen determinado de la escena de simulación.

A diferencia de un Vision Sensor, un Proximity Sensor no genera imágenes. Su función consiste en determinar si un objeto es detectado y, opcionalmente, calcular la distancia y el punto de intersección entre el sensor y dicho objeto.

Los Proximity Sensors permiten simular una amplia variedad de sensores industriales y robóticos, entre ellos:

- Sensores infrarrojos.
- Sensores láser de distancia.
- Barreras fotoeléctricas.
- Sensores ultrasónicos.
- Detectores de presencia.
- Sensores inductivos.
- Sensores capacitivos.

Dentro del GSPL, un Proximity Sensor representa un dispositivo de detección espacial utilizado para percibir el entorno.

---

## 8.2 Función dentro del GSPL

Los Proximity Sensors podrán utilizarse para:

- Detectar obstáculos.
- Medir distancias.
- Implementar sistemas anticolisión.
- Simular sensores industriales.
- Activar eventos.
- Guiar robots móviles.
- Realizar inspecciones virtuales.
- Implementar sistemas de seguridad.

Durante GSPL-05 serán convertidos en Proximity Sensors nativos de CoppeliaSim.

---

## 8.3 Propiedades generales

Como cualquier objeto de simulación, un Proximity Sensor posee las propiedades comunes:

- Object ID
- Nombre
- Enabled
- Parent
- Pose
- Reference Frame
- Visibility
- Layer

Estas propiedades son independientes del funcionamiento del sensor.

---

## 8.4 Tipo de sensor

CoppeliaSim permite distintos volúmenes de detección.

Los principales son:

- Ray
- Cone
- Cylinder
- Disc
- Pyramid

Cada tipo define una geometría distinta para el volumen de detección.

GSPL soportará todos los tipos disponibles.

---

## 8.5 Rango de detección

El sensor posee una distancia máxima de detección.

Todo objeto situado más allá de este rango será ignorado.

Unidad:

metros.

---

## 8.6 Ángulo de apertura

Para sensores cónicos o piramidales puede definirse un ángulo de apertura.

Este parámetro determina el volumen de exploración del sensor.

Unidad:

grados.

---

## 8.7 Detectable Entity

El sensor puede configurarse para detectar únicamente determinados objetos de la escena.

Ejemplos:

- Todos los objetos.
- Sólo Shapes detectables.
- Un árbol específico.
- Una colección determinada.

Esta funcionalidad permite optimizar el rendimiento y controlar el comportamiento del sensor.

---

## 8.8 Front Face Detection

Puede configurarse para detectar únicamente las caras frontales de una superficie.

Esta opción resulta útil para evitar falsas detecciones sobre superficies posteriores.

---

## 8.9 Back Face Detection

Permite detectar también las caras posteriores de las superficies.

Su utilización depende del tipo de aplicación.

---

## 8.10 Closest Object Mode

Cuando existen múltiples objetos dentro del volumen de detección, el sensor puede configurarse para devolver únicamente el objeto más cercano.

Este modo resulta especialmente útil para sensores de distancia.

---

## 8.11 Explicit Handling

El sensor puede funcionar en dos modos.

### Automático

La detección se realiza durante cada ciclo de simulación.

### Explícito

La detección es iniciada mediante llamadas a la API.

Este modo permite optimizar el rendimiento cuando existen numerosos sensores.

---

## 8.12 Información proveniente del Excel

Actualmente la planilla de ingeniería únicamente proporciona:

| Campo Excel | Destino |
|--------------|---------|
| Object Type | Proximity Sensor |
| Object Name | object.name |
| Enabled | enabled |
| Position | pose.position |
| Rotation | pose.orientation |
| Reference Frame | reference_frame |

Los parámetros específicos utilizarán inicialmente los valores por defecto definidos por GSPL.

En futuras versiones podrán incorporarse nuevas columnas de configuración.

---

## 8.13 Representación propuesta

```json
{
    "type": "Proximity Sensor",

    "proximity_sensor": {

        "sensor_type": "Ray",

        "range": 5.0,

        "angle": 30.0,

        "detectable_entity": "All",

        "front_face_detection": true,

        "back_face_detection": false,

        "closest_object_only": true,

        "explicit_handling": false
    }
}
```

---

## 8.14 Información generada durante la simulación

Durante la ejecución del modelo, el Proximity Sensor genera información dinámica.

Entre ella:

- Estado de detección.
- Distancia medida.
- Punto de detección.
- Vector normal de la superficie.
- Objeto detectado.

Estos datos representan el estado instantáneo de la simulación y no forman parte del `2_simulation_database.json`.

---

## 8.15 Filosofía de diseño

GSPL almacena únicamente la configuración necesaria para reconstruir completamente el Proximity Sensor dentro de CoppeliaSim.

Los resultados obtenidos durante la simulación —como la distancia medida, el objeto detectado o el punto de impacto— constituyen información dinámica y, por lo tanto, no se almacenan en la base de datos de ingeniería.

Esta separación mantiene el `2_simulation_database.json` como una descripción determinística del modelo, independiente del estado de ejecución de la simulación.

------------------------------------------------------------------------

# Capítulo 9 — Camera

## 9.1 Introducción

Una **Camera** es un objeto de CoppeliaSim utilizado para visualizar la escena de simulación desde un punto de vista determinado.

A diferencia de un Vision Sensor, una Camera no está diseñada para realizar tareas de percepción o procesamiento de imágenes. Su finalidad principal consiste en proporcionar una vista de la escena para el usuario, para interfaces gráficas o para aplicaciones de visualización.

Las cámaras pueden utilizarse para:

- Supervisión de la simulación.
- Visualización de robots.
- Seguimiento de objetos.
- Generación de vistas personalizadas.
- Interfaces Hombre-Máquina (HMI).
- Grabación de animaciones.
- Presentaciones y demostraciones.

Dentro del GSPL, una Camera representa un punto de observación de la escena.

---

## 9.2 Función dentro del GSPL

Las cámaras podrán utilizarse para:

- Observar el funcionamiento del modelo.
- Generar vistas predefinidas.
- Supervisar procesos industriales.
- Seguir robots móviles.
- Seguir manipuladores.
- Crear cámaras de inspección.
- Generar recorridos de cámara.

Durante GSPL-05 serán convertidas en objetos Camera de CoppeliaSim.

---

## 9.3 Propiedades generales

Como cualquier objeto de simulación, una Camera posee las propiedades comunes:

- Object ID
- Nombre
- Enabled
- Parent
- Pose
- Reference Frame
- Visibility
- Layer

Estas propiedades son independientes del funcionamiento óptico de la cámara.

---

## 9.4 Tipo de proyección

La cámara puede utilizar dos modos de proyección.

### Perspective

Simula una cámara convencional.

Los objetos lejanos aparecen más pequeños.

Es el modo utilizado en la mayoría de las simulaciones.

---

### Orthographic

No existe perspectiva.

Los objetos mantienen su tamaño independientemente de la distancia.

Se utiliza principalmente para vistas técnicas.

---

## 9.5 Field of View (FOV)

Define el ángulo de apertura de la cámara.

Un FOV pequeño produce una imagen con efecto de zoom.

Un FOV grande permite observar una mayor porción de la escena.

Unidad:

grados.

---

## 9.6 Near Clipping Plane

Define la distancia mínima visible.

Los objetos situados delante de este plano no serán renderizados.

Unidad:

metros.

---

## 9.7 Far Clipping Plane

Define la distancia máxima visible.

Los objetos situados más allá de este plano no serán visibles.

Unidad:

metros.

---

## 9.8 Resolución de visualización

Aunque la Camera no genera imágenes para procesamiento, la ventana asociada puede utilizar distintas resoluciones.

GSPL reservará soporte para configurar esta propiedad cuando resulte necesario.

---

## 9.9 Tracking

Una Camera puede configurarse para seguir automáticamente un objeto de la escena.

Entre los modos habituales se encuentran:

- Cámara fija.
- Seguimiento de un objeto.
- Seguimiento de un robot.
- Cámara orbital.
- Vista en primera persona.

Esta funcionalidad resulta especialmente útil para inspección y depuración de modelos.

---

## 9.10 Navegación

Las cámaras pueden utilizar distintos modos de navegación dentro de la escena.

Por ejemplo:

- Libre.
- Orbital.
- Primera persona.
- Seguimiento automático.

Estos modos afectan únicamente a la interacción del usuario con la simulación.

---

## 9.11 Información proveniente del Excel

Actualmente la planilla de ingeniería únicamente proporciona:

| Campo Excel | Destino |
|--------------|---------|
| Object Type | Camera |
| Object Name | object.name |
| Enabled | enabled |
| Position | pose.position |
| Rotation | pose.orientation |
| Reference Frame | reference_frame |

Los parámetros específicos utilizarán inicialmente los valores por defecto definidos por GSPL.

En futuras versiones podrán incorporarse nuevas columnas para su configuración.

---

## 9.12 Representación propuesta

```json
{
    "type": "Camera",

    "camera": {

        "projection": "Perspective",

        "field_of_view": 60.0,

        "near_clipping": 0.01,

        "far_clipping": 50.0,

        "resolution": {

            "width": 1280,

            "height": 720
        },

        "tracking": {

            "enabled": false,

            "target": null
        }
    }
}
```

---

## 9.13 Información generada durante la simulación

Durante la ejecución del modelo, la Camera no produce información de ingeniería.

Su función consiste únicamente en proporcionar una vista de la escena.

La posición, orientación y seguimiento pueden modificarse dinámicamente durante la simulación, pero estos cambios corresponden al estado de ejecución y no forman parte del `2_simulation_database.json`.

---

## 9.14 Diferencias respecto al Vision Sensor

Aunque ambos objetos comparten numerosos parámetros ópticos, cumplen funciones diferentes.

| Camera | Vision Sensor |
|----------|---------------|
| Visualización de la escena | Percepción del entorno |
| Uso por el operador | Uso por algoritmos |
| No realiza procesamiento de imágenes | Produce imágenes para procesamiento |
| No genera mapas de profundidad | Puede generar mapas de profundidad |
| Pensada para supervisión | Pensada para visión artificial |

Por este motivo, GSPL los considera objetos distintos dentro del Simulation Database.

---

## 9.15 Filosofía de diseño

GSPL almacena únicamente la configuración necesaria para reconstruir completamente la Camera dentro de CoppeliaSim.

La Camera constituye un elemento de visualización del entorno de simulación y no un sensor destinado a la adquisición de información.

Separar conceptualmente Camera y Vision Sensor permite mantener una arquitectura clara, facilita la implementación del constructor GSPL-05 y evita mezclar objetos destinados a la interacción humana con aquellos utilizados por algoritmos de percepción.

------------------------------------------------------------------------

# Capítulo 10 — Light

## 10.1 Introducción

Un **Light** es un objeto de CoppeliaSim utilizado para iluminar la escena de simulación.

Su función consiste en generar una fuente de luz que permita visualizar correctamente los objetos y mejorar el realismo de la simulación.

Las luces no participan directamente de la simulación física, pero afectan el renderizado de la escena y, en algunos casos, el funcionamiento de los Vision Sensors cuando éstos utilizan renderizado realista.

Dentro del GSPL, un Light representa una fuente de iluminación virtual.

---

## 10.2 Función dentro del GSPL

Las luces podrán utilizarse para:

- Iluminación general de la escena.
- Simulación de iluminación industrial.
- Simulación de focos de trabajo.
- Simulación de iluminación ambiental.
- Simulación de faros de vehículos.
- Simulación de iluminación de robots móviles.
- Mejorar la visualización durante el desarrollo.

Durante GSPL-05 serán convertidas en objetos Light nativos de CoppeliaSim.

---

## 10.3 Propiedades generales

Como cualquier objeto de simulación, una Light posee todas las propiedades comunes.

Entre ellas:

- Object ID
- Nombre
- Enabled
- Parent
- Pose
- Reference Frame
- Visibility
- Layer

Estas propiedades son independientes del comportamiento luminoso.

---

## 10.4 Tipos de luz

CoppeliaSim soporta tres tipos principales de iluminación.

### Omni Light

Emite luz uniformemente en todas las direcciones.

Se utiliza para iluminación ambiental o fuentes puntuales.

---

### Spot Light

Emite un haz de luz con una dirección determinada.

Permite controlar:

- apertura;
- alcance;
- orientación.

Es el tipo utilizado para simular reflectores y faros.

---

### Directional Light

Genera rayos paralelos.

La posición de la luz no influye sobre la iluminación.

Se utiliza para simular fuentes muy alejadas, como el Sol.

---

## 10.5 Color

La luz posee un color configurable.

Generalmente se representa mediante componentes RGB.

Ejemplo:

```text
Rojo
Verde
Azul
```

También puede utilizarse una temperatura de color equivalente.

---

## 10.6 Intensidad

Define la potencia luminosa de la fuente.

Una mayor intensidad produce una escena más iluminada.

GSPL almacenará este valor como un parámetro configurable.

---

## 10.7 Atenuación

La intensidad luminosa disminuye con la distancia.

CoppeliaSim permite configurar distintos parámetros de atenuación.

Estos parámetros determinan cómo disminuye la iluminación respecto de la distancia al objeto iluminado.

---

## 10.8 Ángulo de apertura

Propiedad exclusiva de las Spot Lights.

Define la apertura del cono de iluminación.

Unidad:

grados.

---

## 10.9 Alcance

Puede definirse una distancia máxima de iluminación.

Más allá de este valor la intensidad se vuelve despreciable.

Unidad:

metros.

---

## 10.10 Sombras

Las luces pueden configurarse para generar sombras.

Cuando esta opción está habilitada:

- los objetos proyectan sombras;
- aumenta el realismo visual;
- aumenta el costo computacional.

GSPL reservará soporte para esta característica.

---

## 10.11 Información proveniente del Excel

Actualmente la planilla de ingeniería únicamente proporciona:

| Campo Excel | Destino |
|--------------|---------|
| Object Type | Light |
| Object Name | object.name |
| Enabled | enabled |
| Position | pose.position |
| Rotation | pose.orientation |
| Reference Frame | reference_frame |

Los parámetros específicos utilizarán inicialmente los valores por defecto definidos por GSPL.

En futuras versiones podrán incorporarse nuevas columnas para configurar la iluminación.

---

## 10.12 Representación propuesta

```json
{
    "type": "Light",

    "light": {

        "light_type": "Omni",

        "color": {

            "red": 1.0,

            "green": 1.0,

            "blue": 1.0
        },

        "intensity": 1.0,

        "attenuation": {

            "constant": 1.0,

            "linear": 0.0,

            "quadratic": 0.0
        },

        "spot_angle": 45.0,

        "range": 20.0,

        "cast_shadows": false
    }
}
```

---

## 10.13 Información generada durante la simulación

Las luces no generan información dinámica que deba almacenarse en el `2_simulation_database.json`.

Su efecto se observa únicamente durante el proceso de renderizado de la escena.

Los cambios producidos durante la simulación forman parte del estado de ejecución y no de la configuración del modelo.

---

## 10.14 Relación con otros objetos

Las luces interactúan principalmente con:

- Shapes, iluminando sus superficies.
- Vision Sensors, afectando la imagen renderizada.
- Cameras, modificando la apariencia visual de la escena.

No tienen interacción directa con:

- Joints.
- Dummies.
- Force Sensors.
- Proximity Sensors.

---

## 10.15 Filosofía de diseño

GSPL almacena únicamente la configuración necesaria para reconstruir completamente una fuente de luz dentro de CoppeliaSim.

Las propiedades almacenadas describen el comportamiento de la iluminación, mientras que los efectos visuales producidos durante la simulación pertenecen al estado dinámico del motor gráfico y no forman parte de la base de datos de ingeniería.

La incorporación de Lights dentro del Simulation Database permite generar automáticamente escenas completas y reproducibles, garantizando una configuración de iluminación consistente en todas las etapas del pipeline.

------------------------------------------------------------------------

# Capítulo 11 — Propiedades Comunes de los Objetos de Simulación

## 11.1 Introducción

Todos los objetos soportados por el GIAR Simulation Pipeline (GSPL) comparten un conjunto de propiedades básicas que describen su identidad, posición dentro de la escena, relaciones jerárquicas y comportamiento general.

Estas propiedades son independientes del tipo específico de objeto (Shape, Joint, Dummy, Sensor, Camera, etc.) y constituyen el contrato común utilizado por todas las etapas del pipeline.

Cada objeto almacenado en el `2_simulation_database.json` deberá poseer estas propiedades antes de incorporar aquellas específicas de su tipo.

---

## 11.2 Objetivos

Las propiedades comunes permiten:

- Identificar unívocamente cada objeto.
- Mantener la jerarquía de la escena.
- Definir la posición y orientación.
- Configurar propiedades generales de simulación.
- Facilitar la construcción automática del modelo.
- Mantener una estructura uniforme dentro del Simulation Database.

---

## 11.3 Identificación

Todo objeto deberá poseer un identificador único.

### Object ID

Identificador único dentro del Simulation Database.

Ejemplo:

```json
"id": "OBJ_000152"
```

El Object ID nunca cambia durante el pipeline.

---

### Name

Nombre del objeto.

Debe ser descriptivo y único dentro del componente.

Ejemplo:

```json
"name": "left_camera"
```

---

### Type

Indica el tipo de objeto de simulación.

Valores soportados:

- Shape
- Joint
- Dummy
- Force Sensor
- Vision Sensor
- Proximity Sensor
- Camera
- Light

Este campo determina el bloque específico que contiene la configuración del objeto.

---

## 11.4 Estado

### Enabled

Indica si el objeto debe ser creado durante GSPL-05.

Valores:

- true
- false

Cuando un objeto está deshabilitado permanece registrado en la base de datos de ingeniería, pero no será construido en la escena.

---

## 11.5 Jerarquía

### Parent

Referencia al objeto padre.

Permite construir el árbol jerárquico de la escena.

Ejemplo:

```json
"parent": "OBJ_000041"
```

Si el objeto pertenece directamente a la raíz del modelo, este valor será `null`.

---

## 11.6 Pose

Todo objeto posee una transformación espacial completa.

La pose está compuesta por:

- posición;
- orientación.

---

### Position

Representa la ubicación del origen local del objeto respecto de su padre.

Unidad:

metros.

Ejemplo:

```json
"position":
{
    "x":0.0,
    "y":0.0,
    "z":0.5
}
```

---

### Orientation

Representa la orientación del sistema de coordenadas local.

GSPL utilizará ángulos de Euler expresados en radianes.

Ejemplo:

```json
"orientation":
{
    "alpha":0.0,
    "beta":0.0,
    "gamma":1.570796
}
```

Internamente CoppeliaSim podrá utilizar matrices de rotación o cuaterniones.

---

## 11.7 Sistema de Referencia

### Reference Frame

Indica el sistema de coordenadas respecto del cual se expresa la pose del objeto.

Normalmente corresponderá al padre dentro del árbol jerárquico.

Esta información será utilizada principalmente por GSPL-03 durante el cálculo de transformaciones.

---

## 11.8 Visibilidad

### Visible

Determina si el objeto será visible dentro de la escena.

Valores:

- true
- false

La visibilidad afecta únicamente al renderizado y no modifica el comportamiento físico del objeto.

---

## 11.9 Seleccionable

### Selectable

Determina si el objeto puede seleccionarse desde la interfaz gráfica de CoppeliaSim.

Valores:

- true
- false

Esta propiedad facilita la edición y depuración del modelo.

---

## 11.10 Capas de Visibilidad

### Visibility Layer

CoppeliaSim organiza los objetos mediante capas de visibilidad.

Estas capas permiten:

- ocultar grupos de objetos;
- visualizar únicamente determinados elementos;
- facilitar el trabajo sobre modelos complejos.

GSPL almacenará esta configuración para reconstruir completamente la escena.

---

## 11.11 Alias

Opcionalmente un objeto podrá poseer un alias.

El alias constituye un nombre alternativo utilizado por scripts o aplicaciones externas.

Ejemplo:

```json
"alias":"camera_front"
```

---

## 11.12 Notas

Cada objeto podrá almacenar información descriptiva adicional.

Ejemplo:

```json
"notes":"Sensor utilizado para navegación."
```

Este campo no posee efecto sobre la simulación y está destinado exclusivamente a documentación de ingeniería.

---

## 11.13 Representación propuesta

Se recomienda que todas las propiedades comunes se agrupen dentro de un bloque independiente.

```json
{
    "common":{

        "id":"OBJ_000001",

        "name":"camera_front",

        "type":"Camera",

        "enabled":true,

        "parent":"OBJ_000000",

        "pose":{

            "position":{

                "x":0.0,
                "y":0.0,
                "z":0.0
            },

            "orientation":{

                "alpha":0.0,
                "beta":0.0,
                "gamma":0.0
            }
        },

        "reference_frame":"parent",

        "visible":true,

        "selectable":true,

        "visibility_layer":1,

        "alias":null,

        "notes":""
    }
}
```

---

## 11.14 Herencia conceptual

Todas las clases de objetos definidas por GSPL comparten este conjunto de propiedades.

Conceptualmente, puede interpretarse que todos los objetos derivan de una estructura común denominada **Simulation Object**, sobre la cual cada tipo incorpora únicamente las propiedades específicas que le corresponden.

Esta organización evita la duplicación de información y simplifica el procesamiento del Simulation Database.

---

## 11.15 Filosofía de diseño

La separación entre propiedades comunes y propiedades específicas constituye uno de los principios fundamentales del GSPL.

Las propiedades comunes describen la identidad, posición y organización del objeto dentro de la escena, mientras que las propiedades específicas describen exclusivamente su comportamiento particular.

Esta arquitectura facilita la evolución del pipeline, reduce la duplicación de información y garantiza una representación uniforme para todos los objetos soportados.

------------------------------------------------------------------------

# 12. Arquitectura recomendada

Cada objeto debe poseer:

-   Información común
-   Un bloque especializado según su tipo

Ejemplo:

``` json
{
  "type":"Shape",
  "shape":{}
}
```

``` json
{
  "type":"Joint",
  "joint":{}
}
```

``` json
{
  "type":"Vision Sensor",
  "vision_sensor":{}
}
```

Este enfoque evita campos nulos, simplifica el compilador GSPL-02 y
facilita la creación del modelo en GSPL-05.

------------------------------------------------------------------------

# 13. Próximos pasos

Para cada tipo de objeto se elaborará una ficha técnica con:

1.  Propiedades disponibles en CoppeliaSim.
2.  Correspondencia con columnas de `1_assembly_table.xlsx`.
3.  Representación en `2_simulation_database.json`.
4.  Valores calculados por GSPL.
5.  Valores por defecto.
6.  Funciones de creación en GSPL-05.

Este documento constituye la base para definir el contrato definitivo de
los objetos de simulación del GSPL.
