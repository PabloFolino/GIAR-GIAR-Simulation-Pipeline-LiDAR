# GSPL-SPEC-002

# Engineering Assembly Specification

**GIAR Simulation Pipeline for LiDAR (GSPL)**

---

| Item | Value |
|------|-------|
| Document | GSPL-SPEC-002 |
| Title | Engineering Assembly Specification |
| Version | 3.0 |
| Status | Released |
| Author | GIAR – Grupo de Inteligencia Artificial y Robótica |
| Related Programs | GSPL-01, GSPL-02 |
| Related Files | `1_assembly.json`, `1_assembly_table.xlsx` |

---

# 1. Introduction

## 1.1 Purpose

This document defines the engineering interface used by the **GIAR Simulation Pipeline for LiDAR (GSPL)** to transform a CAD model created in Rhino into a complete simulation model for CoppeliaSim.

The specification describes two complementary engineering artifacts:

- `1_assembly.json`
- `1_assembly_table.xlsx`

Although both files describe the same assembly, they have different purposes within the pipeline.

---

## 1.2 Scope

This document specifies:

- the structure of `1_assembly.json`;
- the structure of `1_assembly_table.xlsx`;
- the engineering workflow between GSPL-01 and GSPL-02;
- the responsibilities of the simulation engineer;
- the validation rules applied by the pipeline;
- the engineering best practices for preparing simulation models.

This specification applies to every project developed using the GSPL architecture.

---

## 1.3 Intended Audience

This document is intended for:

- Mechanical Engineers
- Robotics Engineers
- Mechatronics Engineers
- Simulation Engineers
- Researchers
- Developers extending the GSPL

No previous knowledge of the internal implementation of the GSPL software is required.

---

## 1.4 Engineering Philosophy

The GSPL separates the complete simulation process into independent stages.

Each program performs one specific task and generates well-defined intermediate files.

This philosophy provides:

- modularity;
- traceability;
- reproducibility;
- maintainability;
- scalability.

The engineer interacts only with the engineering interface.

The remaining files are considered internal pipeline files.

---

## 1.5 Internal Pipeline vs Engineering Interface

One of the main design principles of the GSPL is the separation between **engineering data** and **pipeline data**.

The simulation engineer should work only with the engineering interface.

The internal JSON files are generated, updated and consumed automatically by the GSPL programs.

The following table summarizes the role of each file.

| File | Purpose | Edited by Engineer |
|------|---------|:------------------:|
| `1_model_database.json` | CAD database extracted from Rhino | ❌ |
| `1_assembly.json` | Internal pipeline representation of the assembly | ⚠ Normally No |
| `1_assembly_table.xlsx` | Engineering editing interface | ✔ |
| `2_assembly_database.json` | Validated assembly database | ❌ |

Except for debugging or advanced development, the engineer should never edit `1_assembly.json` directly.

Instead, all engineering information shall be entered into `1_assembly_table.xlsx`.

GSPL-02 automatically converts the spreadsheet into the corresponding JSON representation.

---

## 1.6 Document Organization

This specification is divided into the following chapters.

| Chapter | Description |
|----------|-------------|
| 2 | GSPL Architecture |
| 3 | Internal Pipeline Files |
| 4 | Specification of `1_assembly.json` |
| 5 | Engineering Interface (`1_assembly_table.xlsx`) |
| 6 | Engineering Workflow |
| 7 | Practical Examples |
| 8 | Validation Rules |
| 9 | Best Practices |
| 10 | Design Philosophy |

The chapters should be read sequentially.

# 2. GSPL Architecture

## 2.1 Overview

The **GIAR Simulation Pipeline for LiDAR (GSPL)** is organized as a sequence of independent programs.

Each program performs a single well-defined task and generates one or more intermediate files that become the input of the following stage.

This modular architecture simplifies development, testing, debugging and maintenance while providing complete traceability throughout the conversion process.

The pipeline transforms a Rhino CAD model into a fully configured CoppeliaSim model.

---

## 2.2 Pipeline Overview

```text
                    Rhino CAD Model
                          (.3dm)
                             │
                             ▼
          GSPL-01_Rhino_Extractor.py
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
1_model_database.json   1_assembly.json   1_assembly_table.xlsx
                             │                   │
                             │                   │
                             │        Simulation Engineer
                             │                   │
                             └───────────┬───────┘
                                         ▼
                  GSPL-02_Assembly_Builder.py
                                         │
                                         ▼
                         2_assembly_database.json
                                         │
                                         ▼
                  GSPL-03_Transform_Builder.py
                                         │
                                         ▼
                        3_transform_database.json
                                         │
                                         ▼
                     GSPL-04_STL_Exporter.py
                                         │
                                         ▼
                           STL Mesh Collection
                                         │
                                         ▼
                  GSPL-05_Coppelia_Builder.py
                                         │
                                         ▼
                    GIAR_Low_Cost_3D_LiDAR.ttm
```

---

## 2.3 Pipeline Philosophy

Each GSPL program has a single responsibility.

Programs never modify information that belongs to previous stages unless explicitly specified by the pipeline.

This approach guarantees:

- predictable behaviour;
- independent testing;
- reproducibility;
- easy maintenance;
- scalability.

Each output file becomes the official input of the next stage.

---

## 2.4 Program Responsibilities

### GSPL-01 — Rhino Extractor

Purpose

Extract all engineering information available from the Rhino model.

Responsibilities

- Read the `.3dm` file.
- Audit the CAD model.
- Verify supported geometry.
- Generate the CAD database.
- Generate the initial assembly template.
- Generate the engineering spreadsheet.

Outputs

- `1_model_database.json`
- `1_assembly.json`
- `1_assembly_table.xlsx`

---

### GSPL-02 — Assembly Builder

Purpose

Transform the engineering description into a complete assembly definition.

Responsibilities

- Read `1_assembly_table.xlsx`.
- Validate engineering data.
- Complete Parent IDs.
- Validate hierarchy.
- Validate simulation objects.
- Update `1_assembly.json`.
- Generate `2_assembly_database.json`.

Outputs

- Updated `1_assembly.json`
- `2_assembly_database.json`

---

### GSPL-03 — Transform Builder

Purpose

Calculate all geometric transformations required by the simulation.

Responsibilities

- Build transformation matrices.
- Calculate local reference systems.
- Compute component positions.
- Compute object transformations.
- Validate transformations.

Output

- `3_transform_database.json`

---

### GSPL-04 — STL Exporter

Purpose

Generate the geometric meshes used by CoppeliaSim.

Responsibilities

- Export STL meshes.
- Organize exported geometry.
- Update mesh information.

Outputs

- STL files
- Updated database information

---

### GSPL-05 — Coppelia Builder

Purpose

Generate the final simulation model.

Responsibilities

- Create the CoppeliaSim scene.
- Create Shapes.
- Create Joints.
- Create Dummies.
- Create Sensors.
- Create Cameras.
- Create Lights.
- Configure dynamics.
- Configure hierarchy.
- Save the `.ttm` model.

Output

- `GIAR_Low_Cost_3D_LiDAR.ttm`

---

## 2.5 Engineering Intervention

Only one stage of the pipeline requires manual engineering input.

```text
GSPL-01
     │
     ▼

1_assembly_table.xlsx

     ▲

     │
Simulation Engineer

     │

     ▼

GSPL-02
```

All remaining stages operate automatically.

This design minimizes manual intervention while preserving complete engineering control over the simulation model.

---

## 2.6 Internal Files

The pipeline generates several intermediate files.

These files are considered **internal data structures**.

They are intended for communication between GSPL programs rather than for manual editing.

Examples include:

- `1_model_database.json`
- `1_assembly.json`
- `2_assembly_database.json`
- `3_transform_database.json`

Although they use the JSON format, they should be regarded as implementation artifacts of the pipeline.

---

## 2.7 Engineering Files

Engineering files are specifically designed to be edited by users.

Current engineering files include:

| File | Purpose |
|------|---------|
| `1_assembly_table.xlsx` | Complete definition of the simulation assembly. |

Future versions of the GSPL may introduce additional engineering spreadsheets for other stages of the pipeline.

---

## 2.8 Why an Engineering Spreadsheet?

Although JSON provides an excellent machine-readable format, it is not the most convenient format for daily engineering work.

Large robotic systems may contain hundreds of components and thousands of simulation objects.

Spreadsheet-based editing provides several advantages:

- familiar engineering workflow;
- filtering and sorting;
- drop-down lists;
- validation rules;
- color coding;
- progress tracking;
- easier review by multidisciplinary teams.

For these reasons, the GSPL adopts `1_assembly_table.xlsx` as the official engineering editing interface.

---

## 2.9 Data Flow

The following diagram summarizes the complete data flow.

```text
 Rhino CAD
     │
     ▼
1_model_database.json
     │
     ▼
1_assembly.json
     │
     ▼
1_assembly_table.xlsx
     │
Engineer
     │
     ▼
GSPL-02 Validation
     │
     ▼
Updated 1_assembly.json
     │
     ▼
2_assembly_database.json
     │
     ▼
3_transform_database.json
     │
     ▼
STL Meshes
     │
     ▼
CoppeliaSim Model
```

---

## 2.10 Design Principles

The GSPL architecture follows the following principles.

### DP-001

One program, one responsibility.

---

### DP-002

One file, one purpose.

---

### DP-003

Engineering data shall be separated from internal pipeline data.

---

### DP-004

The simulation engineer interacts with spreadsheets rather than internal JSON files.

---

### DP-005

Every stage shall produce deterministic outputs from deterministic inputs.

---

### DP-006

All intermediate files shall remain human-readable whenever possible.

---

### DP-007

The pipeline shall be modular and extensible.

---

### DP-008

Every generated file shall be traceable to its originating stage.


# 3. Internal Pipeline Files

## 3.1 Overview

The GSPL generates a sequence of intermediate files during the conversion process.

These files are collectively referred to as the **Pipeline Layer**.

They represent the internal data exchanged between the different GSPL programs.

Although most of these files are stored using the JSON format, they are **not intended to be edited manually**.

Instead, they provide a structured, deterministic and machine-readable representation of the complete engineering process.

---

## 3.2 Pipeline Files

The current version of the GSPL generates the following internal files.

| Stage | File | Description |
|--------|------|-------------|
| GSPL-01 | `1_model_database.json` | CAD database extracted from Rhino. |
| GSPL-01 | `1_assembly.json` | Internal assembly representation. |
| GSPL-02 | `2_assembly_database.json` | Validated assembly database. |
| GSPL-03 | `3_transform_database.json` | Global and local transformations. |
| GSPL-04 | STL Meshes | Geometry exported for CoppeliaSim. |
| GSPL-05 | `.ttm` | Final CoppeliaSim model. |

---

## 3.3 Engineering Files

Unlike the internal pipeline files, engineering files are intended to be edited by the simulation engineer.

Current engineering files are:

| File | Purpose |
|------|---------|
| `1_assembly_table.xlsx` | Definition of the complete simulation assembly. |

Future versions of the GSPL may introduce additional engineering spreadsheets.

---

# 3.4 Internal vs Engineering Files

The following table summarizes the intended use of every file.

| File | Generated By | Edited By Engineer | Used By |
|------|--------------|:------------------:|--------|
| `1_model_database.json` | GSPL-01 | ❌ | GSPL-02 |
| `1_assembly.json` | GSPL-01 / GSPL-02 | ⚠ Normally No | GSPL-02, GSPL-03 |
| `1_assembly_table.xlsx` | GSPL-01 | ✔ | GSPL-02 |
| `2_assembly_database.json` | GSPL-02 | ❌ | GSPL-03 |
| `3_transform_database.json` | GSPL-03 | ❌ | GSPL-04 |
| STL Meshes | GSPL-04 | ❌ | GSPL-05 |
| `.ttm` | GSPL-05 | ❌ | CoppeliaSim |

---

# 3.5 The Role of `1_assembly.json`

`1_assembly.json` is the internal representation of the complete simulation assembly.

It is the common language spoken by all GSPL programs after the engineering phase has finished.

The file contains:

- assembly hierarchy;
- reference frames;
- simulation models;
- CoppeliaSim objects;
- object properties;
- engineering metadata.

Although it is stored in JSON format and therefore can be opened with any text editor, it should normally **not** be edited manually.

Instead, it is generated and updated automatically by the GSPL.

---

# 3.6 The Role of `1_assembly_table.xlsx`

The spreadsheet is the official engineering editing interface.

It allows the simulation engineer to define:

- assembly hierarchy;
- simulation models;
- simulation objects;
- joints;
- sensors;
- engineering notes;
- validation status.

The spreadsheet intentionally hides all implementation details of the pipeline.

This makes the engineering workflow independent from the internal JSON representation.

---

# 3.7 Why Two Representations?

One of the main design decisions of the GSPL is maintaining two different representations of the same assembly.

## Engineering Representation

```
1_assembly_table.xlsx
```

Designed for people.

Characteristics:

- easy to edit;
- tabular format;
- filtering;
- sorting;
- drop-down lists;
- engineering workflow.

---

## Internal Representation

```
1_assembly.json
```

Designed for software.

Characteristics:

- hierarchical;
- machine-readable;
- deterministic;
- extensible;
- optimized for processing.

---

Keeping both representations separated provides significant advantages.

---

# 3.8 Automatic Synchronization

The synchronization between both representations is performed by GSPL-02.

```
Engineer

        │

        ▼

1_assembly_table.xlsx

        │

        ▼

GSPL-02

        │

        ▼

Updated

1_assembly.json
```

The engineer never needs to manually synchronize both files.

---

# 3.9 Parent Resolution

One example of this synchronization is the assembly hierarchy.

Inside the spreadsheet the engineer selects the parent using the component name.

Example

| Parent Name |
|-------------|
| Base |
| Rotating_Head |
| LIDAR_Frame |

During execution GSPL-02 automatically resolves these names into component identifiers.

The resulting JSON contains

```json
"parent":15
```

or

```json
"parent":null
```

for the root component.

The engineer shall never manually edit the Parent ID.

---

# 3.10 Pipeline Independence

One important objective of the GSPL architecture is keeping the engineering interface independent from the internal implementation.

Future versions of the pipeline may:

- change JSON structures;
- introduce additional metadata;
- optimize databases;
- split files;
- merge files.

None of these changes should require modifications to the engineering spreadsheet.

This separation guarantees long-term compatibility of engineering projects.

---

# 3.11 Engineering Responsibility

The simulation engineer is responsible only for engineering decisions.

Examples include:

- selecting the parent component;
- deciding whether a component belongs to the visual model;
- deciding whether a component belongs to the simulation model;
- adding joints;
- adding sensors;
- configuring simulation objects;
- documenting engineering decisions.

The engineer is not responsible for maintaining internal pipeline structures.

Those tasks belong to the GSPL software.

---

# 3.12 Summary

The GSPL intentionally separates the engineering workflow from the software implementation.

This separation is achieved by maintaining two complementary representations of the same assembly.

| Engineering Layer | Pipeline Layer |
|-------------------|----------------|
| `1_assembly_table.xlsx` | `1_assembly.json` |

The spreadsheet is optimized for engineering.

The JSON is optimized for software.

Both files describe exactly the same assembly, but from different perspectives.

# 4. Specification of `1_assembly.json`

## 4.1 Overview

`1_assembly.json` is the internal representation of the engineering assembly used by the GSPL.

It is automatically generated during the execution of **GSPL-01_Rhino_Extractor.py** and later updated by **GSPL-02_Assembly_Builder.py** after processing the information contained in the **Engineering Assembly Table** (`1_assembly_table.xlsx`).

Although the file uses the JSON format and can be opened with any text editor, it is considered an **internal pipeline file**.

Under normal circumstances it shall **not** be edited manually.

Instead, the simulation engineer shall complete the Engineering Assembly Table and allow GSPL-02 to generate the corresponding JSON representation.

---

## 4.2 Purpose

The purpose of `1_assembly.json` is to provide a hierarchical, deterministic and machine-readable description of the complete simulation assembly.

The file combines:

- component hierarchy;
- engineering metadata;
- simulation models;
- reference frames;
- bounding boxes;
- CoppeliaSim object definitions.

It represents the official assembly definition exchanged between GSPL programs.

---

## 4.3 General Structure

The file is divided into two major sections.

1. Metadata
2. Component Definitions

General structure

```json
{
    "format_version":"1.0",

    "generated_by":"GSPL-01_Rhino_Extractor",

    "generator_version":"1.0.0",

    "project":"GIAR Low Cost 3D LiDAR",

    "root":null,

    "components":[]
}
```

---

# 4.4 Metadata

The metadata section identifies the generated file.

| Field | Description |
|--------|-------------|
| format_version | File format version. |
| generated_by | Program that generated the file. |
| generator_version | Generator version. |
| project | Project name. |
| root | Identifier of the root component. |

Example

```json
{

    "format_version":"1.0",

    "generated_by":"GSPL-01_Rhino_Extractor",

    "generator_version":"1.0.0",

    "project":"GIAR Low Cost 3D LiDAR",

    "root":1

}
```

The value of **root** corresponds to the component whose **parent** is `null`.

---

# 4.5 Components

The **components** array contains every engineering component extracted from the CAD model.

Each Rhino component shall appear exactly once.

Example

```json
{

    "id":18,

    "name":"NEMA17",

    "description":"Stepper Motor",

    "notes":"",

    "enabled":true,

    "parent":4,

    "frame":{

        "position":[0,0,0],

        "orientation":[0,0,0]

    },

    "bounding_box":{

        "min":[...],

        "max":[...],

        "center":[...],

        "size":[...]

    },

    "models":[

        "visual"

    ],

    "objects":[

    ]

}
```

---

# 4.6 Component Fields

Every component contains the following fields.

| Field | Required | Description |
|--------|:-------:|-------------|
| id | ✔ | Unique identifier generated by GSPL-01. |
| name | ✔ | Component name extracted from Rhino. |
| description | | Engineering description. |
| notes | | Engineering notes. |
| enabled | ✔ | Enables or disables the component. |
| parent | ✔ | Parent component ID. |
| frame | ✔ | Local component reference frame. |
| bounding_box | ✔ | Bounding Box automatically calculated by GSPL-01. |
| models | ✔ | Simulation models where the component participates. |
| objects | ✔ | List of generated CoppeliaSim objects. |

---

# 4.7 Component Identification

Every component receives a unique identifier.

Example

```json
"id":27
```

The identifier is generated automatically by GSPL-01.

It shall never be modified manually.

The ID is used internally by the GSPL to:

- define parent relationships;
- reference components;
- build the assembly tree;
- create deterministic transformations.

---

# 4.8 Parent Relationship

The field

```json
"parent"
```

defines the assembly hierarchy.

Example

```json
"parent":8
```

The parent always references another component by its identifier.

The root component is represented by

```json
"parent":null
```

Only one component in the assembly shall have a null parent.

---

# 4.9 Reference Frame

Every component contains its own local reference frame.

```json
"frame":{

    "position":[...],

    "orientation":[...]

}
```

Initially GSPL-01 estimates the frame automatically using the Rhino geometry.

During the engineering stage the reference frame may later be adjusted through the Engineering Assembly Table.

GSPL-02 updates the JSON accordingly.

---

# 4.10 Bounding Box

Every component stores its Bounding Box.

```json
"bounding_box":{

    "min":[...],

    "max":[...],

    "center":[...],

    "size":[...]

}
```

The Bounding Box is generated automatically.

It shall never be modified manually.

Later stages use it for:

- transformation calculations;
- collision estimation;
- STL generation;
- engineering validation.

---

# 4.11 Models

The field

```json
"models"
```

defines where the component participates.

Supported values are

| Value | Description |
|--------|-------------|
| visual | Visual model. |
| simulation | Simulation model. |

Examples

Visual only

```json
"models":[

    "visual"

]
```

Simulation only

```json
"models":[

    "simulation"

]
```

Both

```json
"models":[

    "visual",

    "simulation"

]
```

---

# 4.12 Objects

Every component owns a list of CoppeliaSim objects.

Initially GSPL-01 generates a minimal definition.

GSPL-02 later expands this list according to the Engineering Assembly Table.

Example

```json
"objects":[

    {

        "type":"shape",

        "name":"NEMA17_Shape",

        "position":[0,0,0],

        "orientation":[0,0,0],

        "properties":{

        }

    }

]
```

---

# 4.13 Synchronization with the Engineering Assembly Table

One of the most important characteristics of the GSPL is that `1_assembly.json` is synchronized automatically from the Engineering Assembly Table.

The following information is transferred by GSPL-02:

- Parent hierarchy;
- Enabled state;
- Simulation models;
- Component descriptions;
- Engineering notes;
- CoppeliaSim objects;
- Joint definitions;
- Sensor definitions;
- Cameras;
- Lights;
- Additional engineering properties.

This synchronization guarantees that the JSON representation always reflects the engineer's decisions.

---

# 4.14 Editing Policy

The following table summarizes which fields are edited manually.

| Field | GSPL | Engineer |
|--------|:----:|:--------:|
| Metadata | ✔ | |
| ID | ✔ | |
| Name | ✔ | |
| Parent | ✔ *(from Parent Name)* | |
| Description | | ✔ |
| Notes | | ✔ |
| Models | | ✔ |
| Objects | | ✔ |
| Bounding Box | ✔ | |
| Frame | ✔ / GSPL-02 | ✔ |

---

# 4.15 Summary

`1_assembly.json` is not intended to be an engineering document.

Instead, it is the **internal representation** used by the GSPL programs.

The simulation engineer should work with the **Engineering Assembly Table**.

GSPL-02 automatically converts the engineering information into the corresponding JSON structure, ensuring consistency, traceability and deterministic execution throughout the pipeline.

***

# 5. Engineering Assembly Table (`1_assembly_table.xlsx`)

## 5.1 Overview

The **Engineering Assembly Table** (`1_assembly_table.xlsx`) is the official engineering interface of the GSPL.

It provides a user-friendly environment where the simulation engineer defines all simulation-specific information that cannot be automatically extracted from the Rhino CAD model.

Unlike the internal JSON files, the Engineering Assembly Table is specifically designed for human interaction.

It supports:

- filtering;
- sorting;
- engineering review;
- data validation;
- drop-down lists;
- progress tracking.

The spreadsheet is automatically generated by **GSPL-01_Rhino_Extractor.py** and later processed by **GSPL-02_Assembly_Builder.py**.

The engineer should complete this spreadsheet before continuing with the pipeline.

---

# 5.2 Workbook Structure

The workbook currently contains three worksheets.

| Worksheet | Purpose | Editable |
|------------|---------|:--------:|
| Components | Defines the engineering assembly | ✔ |
| Objects | Defines all CoppeliaSim objects | ✔ |
| Lists | Internal validation lists | ❌ |

The **Lists** worksheet is automatically generated by GSPL-01 and is hidden from normal users.

It shall never be modified manually.

---

# 5.3 Engineering Workflow

The normal engineering workflow is illustrated below.

```text
Rhino CAD

     │

     ▼

GSPL-01

     │

     ▼

1_assembly_table.xlsx

     │

Engineer completes

     │

     ▼

GSPL-02

     │

     ▼

Updated 1_assembly.json

     │

     ▼

2_assembly_database.json
```

The engineer never edits the JSON files directly.

---

# 5.4 Components Worksheet

The **Components** worksheet defines the logical assembly hierarchy.

Each row represents exactly one CAD component extracted from Rhino.

Example

| ID | Name | Parent Name | Visual | Simulation |
|---:|------|-------------|:------:|:----------:|
| 1 | Base | | ✔ | ✔ |
| 2 | Motor | Base | ✔ | ✔ |
| 3 | Cover | Base | ✔ | ✖ |

---

# 5.5 Components Columns

## ID

Generated by

GSPL-01

Editable

No

Description

Unique component identifier.

Example

```text
15
```

The ID shall never be modified manually.

---

## Name

Generated by

GSPL-01

Editable

No

Description

Component name extracted from Rhino.

Example

```text
Motor_Bracket
```

If the component name changes, regenerate the project using GSPL-01.

Never edit this field manually.

---

## Type

Generated by

Engineer

Editable

Yes

Purpose

Engineering classification.

Examples

```text
Mechanical

Electrical

Electronic

Sensor

Structure

Actuator
```

---

## Description

Free engineering description.

Example

```text
Main rotating platform.
```

---

## Enabled

Determines whether the component participates in the project.

Values

```text
TRUE

FALSE
```

Normally every component should remain enabled.

---

## Parent Name

One of the most important fields.

The engineer selects the parent component using the drop-down list.

Example

| Component | Parent Name |
|-----------|-------------|
| Motor | Base |
| Encoder | Motor |
| Cover | Base |

The engineer always works with names.

Never with IDs.

---

## Parent ID

Generated by

GSPL-02

Editable

No

This column is automatically completed when GSPL-02 processes the Engineering Assembly Table.

The engineer shall never modify this field.

If Parent Name is empty, Parent ID remains empty and the generated JSON will contain

```json
"parent": null
```

Otherwise GSPL-02 automatically resolves

```text
Base
```

into

```json
"parent":1
```

---

## Visual

Indicates whether the component belongs to the visual model.

Values

```text
TRUE

FALSE
```

Decorative parts are usually visual only.

---

## Simulation

Indicates whether the component belongs to the simulation model.

Values

```text
TRUE

FALSE
```

Mechanical parts generally belong to both models.

---

## Reviewed

Engineering review flag.

Values

```text
TRUE

FALSE
```

Initially

```text
FALSE
```

After verification

```text
TRUE
```

---

## Status

Engineering workflow state.

Current values

```text
NEW

IN_PROGRESS

REVIEWED

VERIFIED

DONE
```

---

## Notes

Free engineering comments.

Example

```text
Pending mechanical verification.
```

---

# 5.6 Objects Worksheet

The **Objects** worksheet defines every CoppeliaSim object created from each Rhino component.

Unlike the Components worksheet, a single component may generate multiple CoppeliaSim objects.

Example

| Component | Object |
|-----------|--------|
| Motor | Shape |
| Motor | Joint |
| Motor | Dummy |

Therefore multiple rows may reference the same component.

---

# 5.7 Typical Objects

Common object types include

- Shape
- Joint
- Dummy
- Vision Sensor
- Proximity Sensor
- Force Sensor
- Camera
- Light

Future versions of the GSPL may support additional CoppeliaSim object types.

---

# 5.8 Lists Worksheet

The Lists worksheet contains every drop-down list used by the Engineering Assembly Table.

Examples include:

- Component names
- Object types
- Joint types
- Status values
- Component types
- Boolean values

This worksheet is generated automatically.

It is marked as **VeryHidden** and should never be modified manually.

---

# 5.9 Data Validation

The Engineering Assembly Table contains built-in validation rules.

Examples include:

- Parent selection
- Object type selection
- Joint type selection
- Boolean fields
- Engineering status

These validations reduce typing errors before GSPL-02 validates the assembly.

---

# 5.10 Automatic Processing

When GSPL-02 reads the Engineering Assembly Table it automatically performs several operations.

Examples include:

- resolving Parent IDs;
- updating the internal JSON;
- validating hierarchy;
- validating object definitions;
- generating engineering reports.

Therefore the spreadsheet always remains the primary engineering interface.

---

# 5.11 Engineering Responsibility

The simulation engineer is responsible for:

- defining the assembly hierarchy;
- selecting simulation models;
- creating CoppeliaSim objects;
- configuring joints;
- documenting engineering decisions.

The engineer is **not** responsible for maintaining internal JSON structures.

---

# 5.12 Summary

The Engineering Assembly Table is the central engineering document of the GSPL.

It provides a simple, familiar and robust environment for preparing simulation models while hiding the complexity of the internal pipeline representation.

Every engineering modification should be performed in this workbook.

The GSPL software is responsible for translating those modifications into the corresponding internal JSON structures.

***
# 6. Engineering Workflow

## 6.1 Overview

The GSPL has been designed to separate engineering decisions from software implementation.

The engineer focuses exclusively on the mechanical and simulation aspects of the project, while the GSPL automatically generates the internal data structures required to build the final CoppeliaSim model.

The complete workflow consists of six stages.

```text
Rhino CAD
    │
    ▼
GSPL-01
    │
    ▼
Engineering Assembly Table
    │
    ▼
GSPL-02
    │
    ▼
GSPL-03
    │
    ▼
GSPL-04
    │
    ▼
GSPL-05
    │
    ▼
CoppeliaSim (.ttm)
```

---

# 6.2 Stage 1 — CAD Modeling

The engineering process begins with the mechanical model created in Rhino.

At this stage, the CAD model should contain only geometric information.

The Rhino model should define:

- all mechanical components;
- component names;
- component geometry;
- layers;
- colors (optional);
- materials (optional).

The CAD model should **not** contain simulation-specific information such as:

- joints;
- sensors;
- cameras;
- lights;
- dynamics;
- collision parameters.

Those elements are defined later during the engineering stage.

---

# 6.3 Stage 2 — GSPL-01

Execute

```text
GSPL-01_Rhino_Extractor.py
```

This program performs the following tasks automatically.

• Audits the Rhino model.

• Verifies supported geometry.

• Generates

```text
1_model_database.json
```

• Generates

```text
1_assembly.json
```

• Generates

```text
1_assembly_table.xlsx
```

At this point the engineering interface is ready.

---

# 6.4 Stage 3 — Engineering Assembly Table

The simulation engineer opens

```text
1_assembly_table.xlsx
```

and completes all engineering information.

Typical tasks include:

• defining the assembly hierarchy;

• selecting parent components;

• deciding whether components belong to the visual model;

• deciding whether components belong to the simulation model;

• adding simulation objects;

• defining joints;

• defining sensors;

• adding engineering notes.

This stage represents the only manual intervention required by the GSPL.

---

# 6.5 Stage 4 — GSPL-02

Execute

```text
GSPL-02_Assembly_Builder.py
```

GSPL-02 performs several automatic operations.

Examples include:

• reads the Engineering Assembly Table;

• validates every worksheet;

• resolves Parent IDs;

• builds the assembly tree;

• validates hierarchy consistency;

• validates simulation objects;

• updates

```text
1_assembly.json
```

• generates

```text
2_assembly_database.json
```

If errors are detected, GSPL-02 reports them together with the worksheet name, row number and a description of the problem.

The engineer corrects the spreadsheet and executes GSPL-02 again.

---

# 6.6 Stage 5 — GSPL-03

Execute

```text
GSPL-03_Transform_Builder.py
```

This stage computes every geometric transformation required by the simulation.

Typical calculations include:

- local reference frames;
- global transformations;
- component positions;
- object positions;
- transformation matrices.

The resulting information is stored in

```text
3_transform_database.json
```

---

# 6.7 Stage 6 — GSPL-04

Execute

```text
GSPL-04_STL_Exporter.py
```

This program exports the meshes required by CoppeliaSim.

Each enabled visual component generates an STL mesh.

The exported meshes preserve:

- geometry;
- orientation;
- scale.

The STL collection becomes the geometric input for the final builder.

---

# 6.8 Stage 7 — GSPL-05

Execute

```text
GSPL-05_Coppelia_Builder.py
```

The builder creates the complete simulation model.

Typical operations include:

- creating Shapes;
- creating Joints;
- creating Dummies;
- creating Sensors;
- creating Cameras;
- creating Lights;
- configuring dynamics;
- creating the assembly hierarchy;
- configuring simulation properties.

Finally the program saves

```text
GIAR_Low_Cost_3D_LiDAR.ttm
```

---

# 6.9 Iterative Development

Engineering projects are rarely completed in a single iteration.

The recommended workflow is iterative.

```text
Rhino
   │
   ▼
GSPL-01
   │
   ▼
Engineering Table
   │
   ▼
GSPL-02
   │
   ▼
Validation

Errors?

YES ─────────────┐
                 │
                 ▼
Engineer updates
Engineering Table
                 │
                 ▼
GSPL-02 again

NO
 │
 ▼
Continue with GSPL-03
```

The engineer may execute GSPL-02 as many times as necessary until the assembly is completely validated.

---

# 6.10 Typical Engineering Session

A typical engineering session may follow the sequence below.

1. Modify the Rhino CAD model.

2. Execute GSPL-01.

3. Open the Engineering Assembly Table.

4. Complete the Components worksheet.

5. Complete the Objects worksheet.

6. Save the workbook.

7. Execute GSPL-02.

8. Correct reported errors.

9. Repeat until validation succeeds.

10. Continue with GSPL-03.

11. Execute GSPL-04.

12. Execute GSPL-05.

13. Open the generated model in CoppeliaSim.

---

# 6.11 Engineering Responsibilities

The engineer is responsible for making engineering decisions.

Examples include:

- assembly hierarchy;
- simulation models;
- object definitions;
- sensor placement;
- joint configuration;
- engineering documentation.

The engineer is not responsible for maintaining the internal JSON databases.

These databases are automatically maintained by the GSPL.

---

# 6.12 Error Handling

Whenever possible, GSPL programs should never terminate with generic Python exceptions.

Instead they should generate engineering-oriented diagnostic messages.

A validation message should always include:

- program name;
- worksheet;
- row number;
- component name;
- error description;
- suggested correction.

Example

```text
GSPL-02

Worksheet : Components

Row : 18

Component : Motor

ERROR

Parent component "Motor_Base" does not exist.

Suggested Action

Select a valid Parent Name from the drop-down list.
```

This philosophy allows engineers to correct the model without inspecting the source code.

---

# 6.13 Workflow Summary

The GSPL workflow intentionally separates engineering activities from software implementation.

The engineer works exclusively with Rhino and the Engineering Assembly Table.

The GSPL software is responsible for:

- data extraction;
- validation;
- synchronization;
- transformation;
- mesh generation;
- CoppeliaSim model generation.

This separation provides a robust, traceable and scalable methodology suitable for both research and industrial engineering projects.

***
# 7. Practical Examples

## 7.1 Overview

This chapter presents practical engineering examples illustrating how the **Engineering Assembly Table** is completed and how GSPL-02 converts the engineering information into the internal assembly representation.

The examples are intentionally simple and progressively introduce more advanced concepts.

Although the examples refer to a LiDAR project, the same engineering methodology can be applied to any robotic or mechatronic system.

---

# 7.2 Example 1 — Decorative Component

This example shows a component that only belongs to the visual model.

Typical examples include:

- Covers
- Labels
- Decorative plates
- Logos

Since the component has no influence on the simulation, it is excluded from the simulation model.

## Components Worksheet

| Field | Value |
|--------|-------|
| Name | Front_Cover |
| Parent Name | Base |
| Visual | TRUE |
| Simulation | FALSE |

## Objects Worksheet

| Component | Object Name | Object Type |
|-----------|-------------|-------------|
| Front_Cover | Front_Cover_Shape | Shape |

Result

• Visible in CoppeliaSim.

• No dynamics.

• No joints.

• No sensors.

---

# 7.3 Example 2 — Structural Component

The component belongs to both generated models.

Typical examples include:

- Base
- Frame
- Mechanical Supports

## Components Worksheet

| Field | Value |
|--------|-------|
| Name | Base |
| Parent Name | *(empty)* |
| Visual | TRUE |
| Simulation | TRUE |

## Objects Worksheet

| Component | Object Name | Object Type |
|-----------|-------------|-------------|
| Base | Base_Shape | Shape |

Result

The component appears in both models and participates in the simulation.

---

# 7.4 Example 3 — Revolute Joint

This example illustrates the creation of a rotating component.

Typical examples include:

- Servo Motors
- Rotary Platforms
- Wheels

## Components Worksheet

| Field | Value |
|--------|-------|
| Name | Rotating_Head |
| Parent Name | Base |
| Visual | TRUE |
| Simulation | TRUE |

## Objects Worksheet

| Component | Object Name | Object Type | Joint Type | Motor |
|-----------|-------------|-------------|------------|-------|
| Rotating_Head | Rotating_Head_Shape | Shape | | |
| Rotating_Head | Joint_Z | Joint | Revolute | TRUE |

Result

The component generates:

- one Shape;
- one Revolute Joint.

GSPL-05 later creates the corresponding CoppeliaSim joint.

---

# 7.5 Example 4 — Camera

The CAD model contains the physical camera housing.

The engineer additionally creates the simulation camera.

## Components Worksheet

| Field | Value |
|--------|-------|
| Name | Camera |
| Parent Name | Rotating_Head |
| Visual | TRUE |
| Simulation | TRUE |

## Objects Worksheet

| Component | Object Name | Object Type |
|-----------|-------------|-------------|
| Camera | Camera_Shape | Shape |
| Camera | Camera | Camera |

Result

Two independent CoppeliaSim objects are created.

- Shape
- Camera

The Shape represents the physical housing.

The Camera provides the simulated image.

---

# 7.6 Example 5 — Hall Sensor

Hall sensors usually have no visible geometry inside the simulation.

Only their position is relevant.

## Components Worksheet

| Field | Value |
|--------|-------|
| Name | Hall_Sensor |
| Parent Name | Base |
| Visual | FALSE |
| Simulation | TRUE |

## Objects Worksheet

| Component | Object Name | Object Type |
|-----------|-------------|-------------|
| Hall_Sensor | Hall_Frame | Dummy |
| Hall_Sensor | Hall | Proximity Sensor |

Result

Only simulation objects are generated.

No visual mesh is required.

---

# 7.7 Example 6 — LiDAR

The LiDAR contains mechanical geometry together with a simulated sensor.

## Components Worksheet

| Field | Value |
|--------|-------|
| Name | TFMini |
| Parent Name | Rotating_Head |
| Visual | TRUE |
| Simulation | TRUE |

## Objects Worksheet

| Component | Object Name | Object Type |
|-----------|-------------|-------------|
| TFMini | TFMini_Shape | Shape |
| TFMini | TFMini_Frame | Dummy |
| TFMini | TFMini | Vision Sensor |

Result

The generated model contains:

- one Shape;
- one Dummy;
- one Vision Sensor.

---

# 7.8 Example 7 — IMU

An IMU normally has no visible representation.

Only its reference frame is required.

## Components Worksheet

| Field | Value |
|--------|-------|
| Name | IMU |
| Parent Name | Base |
| Visual | FALSE |
| Simulation | TRUE |

## Objects Worksheet

| Component | Object Name | Object Type |
|-----------|-------------|-------------|
| IMU | IMU_Frame | Dummy |
| IMU | IMU | Force Sensor |

Result

The Dummy defines the IMU reference frame.

The Force Sensor is later configured by GSPL-05.

---

# 7.9 Example 8 — Multiple Objects per Component

A single Rhino component may generate several CoppeliaSim objects.

Example

Component

```
Motor
```

Objects

| Object |
|--------|
| Shape |
| Joint |
| Dummy |
| Camera |
| Vision Sensor |

This flexibility allows the engineer to build sophisticated simulation models without modifying the CAD geometry.

---

# 7.10 Example 9 — Parent Resolution

The engineer never writes component IDs.

Instead, the hierarchy is defined using component names.

Engineering Table

| Component | Parent Name |
|-----------|-------------|
| Base | |
| Motor | Base |
| Camera | Motor |

During execution GSPL-02 automatically generates

```json
Base

"parent": null

Motor

"parent": 1

Camera

"parent": 2
```

The Parent ID column is therefore considered informative and automatically maintained by the pipeline.

---

# 7.11 Example 10 — Visual vs Simulation

The following table summarizes common engineering decisions.

| Component | Visual | Simulation |
|-----------|:------:|:----------:|
| Decorative Cover | ✔ | |
| Mechanical Frame | ✔ | ✔ |
| Motor Housing | ✔ | ✔ |
| Camera Housing | ✔ | ✔ |
| Camera Sensor | | ✔ |
| Hall Sensor | | ✔ |
| IMU | | ✔ |
| LIDAR Housing | ✔ | ✔ |

---

# 7.12 Lessons Learned

The previous examples illustrate the main engineering philosophy adopted by the GSPL.

A Rhino component represents a physical element of the real system.

During the engineering stage, that component may generate one or several CoppeliaSim objects depending on the intended simulation behaviour.

The engineer therefore focuses on **engineering intent** rather than software implementation.

The GSPL automatically transforms those engineering decisions into a consistent internal representation that will later be converted into the final CoppeliaSim model.

***

# 8. Validation Rules

## 8.1 Overview

The purpose of the validation process is to guarantee that the engineering information contained in the **Engineering Assembly Table** is complete, consistent and suitable for generating a valid CoppeliaSim model.

Validation is performed automatically by **GSPL-02_Assembly_Builder.py**.

Whenever possible, validation errors should be reported using engineering terminology rather than programming exceptions.

Each validation rule defined in this chapter has a unique identifier.

---

# 8.2 Validation Categories

The validation process is divided into the following categories.

| Category | Description |
|----------|-------------|
| Components | Validation of component definitions. |
| Hierarchy | Validation of the assembly tree. |
| Objects | Validation of CoppeliaSim objects. |
| Geometry | Validation of positions and orientations. |
| Simulation | Validation of simulation-specific properties. |

---

# 8.3 Component Validation

---

## VAL-001

### Component IDs shall be unique.

Every component generated by GSPL-01 must have a unique identifier.

Correct

```text
1
2
3
4
```

Incorrect

```text
1
2
2
4
```

Error Message

```
Duplicated Component ID detected.
```

---

## VAL-002

### Component Names shall be unique.

Correct

```text
Base

Motor

Camera
```

Incorrect

```text
Motor

Motor
```

Error Message

```
Duplicated Component Name detected.
```

---

## VAL-003

### Every enabled component shall have a valid name.

Names cannot be empty.

Incorrect

```text

```

Error Message

```
Component name is missing.
```

---

# 8.4 Hierarchy Validation

---

## VAL-010

Exactly one root component shall exist.

A root component is defined as a component whose Parent Name is empty.

Correct

| Name | Parent |
|------|--------|
| Base | |

Incorrect

| Name | Parent |
|------|--------|
| Base | |
| Motor | |

Error Message

```
Multiple root components detected.
```

---

## VAL-011

Every Parent Name shall reference an existing component.

Correct

```
Motor

↓

Base
```

Incorrect

```
Motor

↓

Base123
```

Error Message

```
Parent component does not exist.
```

---

## VAL-012

The hierarchy shall not contain cycles.

Correct

```
Base

↓

Motor

↓

Camera
```

Incorrect

```
Base

↓

Motor

↓

Camera

↓

Base
```

Error Message

```
Circular hierarchy detected.
```

---

## VAL-013

A component cannot be its own parent.

Incorrect

```
Motor

↓

Motor
```

Error Message

```
Component cannot reference itself as parent.
```

---

# 8.5 Model Validation

---

## VAL-020

Every enabled component shall belong to at least one model.

Correct

```
Visual = TRUE

Simulation = FALSE
```

Correct

```
Visual = FALSE

Simulation = TRUE
```

Correct

```
Visual = TRUE

Simulation = TRUE
```

Incorrect

```
Visual = FALSE

Simulation = FALSE
```

Error Message

```
Component does not belong to any model.
```

---

# 8.6 Object Validation

---

## VAL-030

Every enabled simulation component shall contain at least one object.

Incorrect

```
Simulation = TRUE

Objects = none
```

Error Message

```
Simulation component has no objects.
```

---

## VAL-031

Object names shall be unique.

Correct

```
Motor_Shape

Motor_Joint
```

Incorrect

```
Motor

Motor
```

Error Message

```
Duplicated object name detected.
```

---

## VAL-032

Every object shall define a valid object type.

Supported values

- Shape
- Joint
- Dummy
- Camera
- Vision Sensor
- Force Sensor
- Proximity Sensor
- Light

Error Message

```
Unsupported object type.
```

---

## VAL-033

Joint objects shall define a Joint Type.

Incorrect

```
Object Type = Joint

Joint Type = empty
```

Error Message

```
Joint Type not specified.
```

---

## VAL-034

Joint Type shall be valid.

Allowed values

```
Revolute

Prismatic

Spherical
```

---

## VAL-035

Joint limits shall satisfy

```
Lower Limit < Upper Limit
```

Incorrect

```
180

-180
```

Error Message

```
Invalid joint limits.
```

---

# 8.7 Geometry Validation

---

## VAL-040

Every position shall contain numeric values.

Incorrect

```
Position X

ABC
```

---

## VAL-041

Every orientation shall contain numeric values.

Incorrect

```
Rotation Y

LEFT
```

---

## VAL-042

No coordinate shall contain NaN values.

---

## VAL-043

No coordinate shall contain infinite values.

---

# 8.8 Spreadsheet Validation

---

## VAL-050

The workbook shall contain all required worksheets.

Required worksheets

- Components
- Objects
- Lists

---

## VAL-051

Worksheet names shall not be modified.

---

## VAL-052

Required columns shall exist.

---

## VAL-053

The Lists worksheet shall remain hidden.

---

# 8.9 Engineering Validation

---

## VAL-060

Parent ID is automatically maintained by GSPL-02.

The engineer shall never modify this column.

---

## VAL-061

ID shall never be modified.

---

## VAL-062

Component Name shall never be modified manually.

Rename the Rhino component and regenerate the project instead.

---

## VAL-063

Bounding Box information shall never be modified manually.

---

## VAL-064

Reference Frames shall only be modified when justified by engineering requirements.

---

# 8.10 Validation Report

Whenever validation fails, GSPL-02 should generate engineering-oriented messages.

Every validation report should include

- Validation Rule
- Worksheet
- Row
- Component
- Error Description
- Suggested Correction

Example

```
Validation Rule

VAL-011

Worksheet

Components

Row

18

Component

Motor

Error

Parent component "Motor_Base" does not exist.

Suggested Action

Select a valid Parent Name from the drop-down list.
```

---

# 8.11 Validation Philosophy

Validation should detect engineering problems before they propagate through the pipeline.

Whenever possible, GSPL-02 should continue validating the remaining components after detecting an error.

The objective is to generate a complete engineering report instead of forcing the engineer to correct one error at a time.

This approach significantly reduces engineering time when working with large assemblies.

---

# 8.12 Summary

The validation process guarantees that every engineering decision recorded in the Engineering Assembly Table is internally consistent before the remaining stages of the GSPL are executed.

A validated assembly ensures that:

- the hierarchy is correct;
- component relationships are valid;
- simulation objects are complete;
- transformations can be computed;
- STL meshes can be generated;
- the final CoppeliaSim model can be built without ambiguity.

The validation rules defined in this chapter constitute the official validation specification for **GSPL-02_Assembly_Builder.py**.

***
# 9. Best Practices

## 9.1 Overview

The Engineering Assembly Table has been designed to provide a simple and reliable interface between the simulation engineer and the GSPL.

Following the recommendations described in this chapter will reduce engineering time, simplify validation and improve the quality of the generated simulation models.

These recommendations are not mandatory unless explicitly indicated, but they are strongly encouraged for every GSPL project.

---

# 9.2 Component Identification

## BP-001

Never modify the **ID** column.

Component identifiers are automatically generated by GSPL-01 and uniquely identify every CAD component.

Changing an ID may invalidate the assembly hierarchy.

---

## BP-002

Never modify the **Name** column.

If a component name must be changed, rename the Rhino object and regenerate the project using GSPL-01.

---

## BP-003

Use meaningful component names.

Good examples

```
Base
Rotating_Head
Motor_Support
Camera_Housing
```

Avoid names such as

```
Part01
Object5
Mesh123
```

---

# 9.3 Assembly Hierarchy

## BP-004

Keep the assembly hierarchy as simple as possible.

A shallow hierarchy is easier to understand, debug and maintain.

---

## BP-005

Always select the parent using the drop-down list.

Never type the Parent Name manually.

This prevents spelling mistakes and guarantees a valid hierarchy.

---

## BP-006

The root component should normally represent the main mechanical structure of the system.

Typical examples

- Base
- Chassis
- Robot_Base

---

# 9.4 Engineering Models

## BP-007

Decorative components should normally belong only to the Visual model.

Examples

- Covers
- Labels
- Decorative parts

---

## BP-008

Mechanical components should normally belong to both models.

Examples

- Frames
- Motors
- Supports
- Bearings

---

## BP-009

Pure simulation objects usually belong only to the Simulation model.

Examples

- IMU
- Hall Sensor
- GPS
- Virtual Camera

---

# 9.5 CoppeliaSim Objects

## BP-010

Every simulation component should normally contain at least one Shape object.

---

## BP-011

Use descriptive object names.

Good examples

```
Motor_Shape
Motor_Joint
Motor_Frame
Camera_Front
```

Avoid

```
Shape1
Joint1
Dummy3
```

---

## BP-012

Whenever possible, use one Shape object per physical component.

---

## BP-013

Create separate Dummy objects to define engineering reference frames.

---

# 9.6 Joints

## BP-014

Create joints only when relative motion exists.

Do not create unnecessary joints.

---

## BP-015

Use Revolute joints whenever possible.

Only use Prismatic or Spherical joints when required by the mechanism.

---

## BP-016

Always verify joint limits.

Incorrect limits may generate unstable simulations.

---

# 9.7 Sensors

## BP-017

Separate the sensor body from the sensing element.

Example

```
Camera Housing

↓

Shape

Camera

↓

Camera Sensor
```

---

## BP-018

Use Dummy objects to define sensor reference frames.

This simplifies future modifications.

---

# 9.8 Documentation

## BP-019

Use the Description field to describe the engineering purpose of the component.

---

## BP-020

Use the Notes field to document design decisions.

Examples

```
Pending verification.

Temporary placeholder.

To be replaced by optical encoder.
```

---

# 9.9 Engineering Review

## BP-021

Review every component before marking **Reviewed = TRUE**.

---

## BP-022

Use the Status column to monitor engineering progress.

Typical workflow

```
NEW

↓

IN_PROGRESS

↓

REVIEWED

↓

VERIFIED

↓

DONE
```

---

## BP-023

Do not execute GSPL-02 until all critical components have been reviewed.

---

# 9.10 General Recommendations

## BP-024

Save the workbook frequently.

---

## BP-025

Never modify the Lists worksheet.

---

## BP-026

Keep engineering documentation up to date.

---

## BP-027

Validate the assembly regularly during development.

Do not wait until the project is complete.

---

## BP-028

Prefer several simple components over one extremely complex component.

---

## BP-029

Maintain consistent naming conventions throughout the project.

---

## BP-030

Treat the Engineering Assembly Table as the single source of truth for all simulation-related engineering decisions.

---

# 9.11 Summary

The recommendations described in this chapter are intended to improve model quality, reduce engineering effort and simplify future maintenance.

Following these best practices will significantly reduce validation errors and improve the robustness of the generated CoppeliaSim models.

---

# 10. Frequently Asked Questions (FAQ)

## 10.1 Can one Rhino component generate multiple CoppeliaSim objects?

Yes.

A single CAD component may generate any number of CoppeliaSim objects.

Example

```
Motor

↓

Shape

↓

Joint

↓

Dummy
```

---

## 10.2 Can multiple components share one Joint?

No.

Each Joint belongs to a single engineering component.

---

## 10.3 Can a component belong only to the Visual model?

Yes.

Typical examples include decorative covers, labels and cosmetic parts.

---

## 10.4 Can a component belong only to the Simulation model?

Yes.

Typical examples include virtual sensors, IMUs, GPS receivers and reference frames.

---

## 10.5 What happens if Parent Name is empty?

The component becomes the assembly root.

GSPL-02 automatically generates

```json
"parent": null
```

Only one component should have an empty Parent Name.

---

## 10.6 Should I edit Parent ID?

No.

Parent ID is automatically calculated by GSPL-02.

The engineer should only select Parent Name.

---

## 10.7 Can I edit 1_assembly.json directly?

Normally, no.

The recommended workflow is to modify the Engineering Assembly Table and allow GSPL-02 to regenerate the JSON automatically.

Direct modification of `1_assembly.json` should be reserved for debugging or advanced development.

---

## 10.8 Can I delete the default Shape object?

Yes.

However, simulation components should normally contain at least one Shape unless the component represents a purely virtual element.

---

## 10.9 Can a component have no Shape object?

Yes.

Examples include:

- IMUs
- GPS
- Hall Sensors
- Reference Frames

---

## 10.10 Why are there two assembly representations?

The spreadsheet is optimized for engineering work.

The JSON is optimized for software processing.

Both describe exactly the same assembly but serve different purposes.

---

## 10.11 Why does GSPL use Excel instead of JSON?

Engineering work benefits from:

- filters;
- sorting;
- drop-down lists;
- validation;
- comments;
- progress tracking.

These features make spreadsheet editing significantly more efficient for large engineering projects.

---

## 10.12 What happens if validation fails?

GSPL-02 generates a validation report describing:

- the worksheet;
- the row number;
- the affected component;
- the validation rule;
- the suggested correction.

The engineer corrects the workbook and executes GSPL-02 again.

---

## 10.13 Can I execute GSPL-02 multiple times?

Yes.

The GSPL has been designed as an iterative engineering process.

Repeated validation is encouraged during development.

---

## 10.14 What is the recommended workflow?

```
Rhino

↓

GSPL-01

↓

Engineering Assembly Table

↓

GSPL-02

↓

Correct Errors

↓

GSPL-02

↓

Continue with GSPL-03
```

---

## 10.15 What is the official engineering document?

The official engineering document is

```
1_assembly_table.xlsx
```

The JSON files are internal pipeline data structures automatically generated and maintained by the GSPL.

---

## 10.16 Summary

The questions presented in this chapter summarize the most common engineering situations encountered when preparing simulation models.

Following the recommended workflow ensures that engineering information remains consistent throughout the entire GSPL pipeline while minimizing validation errors and simplifying future maintenance.

***
# 11. Future Extensions

## 11.1 Overview

The GSPL has been designed as an extensible engineering framework rather than a fixed conversion tool.

Although the current version focuses on converting Rhino CAD models into CoppeliaSim simulation models, the architecture intentionally leaves room for future capabilities without requiring significant modifications to the engineering workflow.

The Engineering Assembly Table and the internal JSON databases have been designed to accommodate additional information while preserving backward compatibility.

---

# 11.2 New CoppeliaSim Object Types

Future versions of the GSPL may support additional CoppeliaSim objects.

Possible extensions include:

- Paths
- Octrees
- Point Clouds
- Graphs
- Collections
- Scripts
- IK Groups
- Collision Objects
- Distance Objects

These objects can be incorporated by extending the **Objects** worksheet without modifying the overall pipeline architecture.

---

# 11.3 Dynamic Properties

Future versions may allow engineers to configure advanced dynamic properties directly from the Engineering Assembly Table.

Examples include:

- Mass
- Inertia Tensor
- Center of Mass
- Friction
- Restitution
- Linear Damping
- Angular Damping
- Collision Masks
- Dynamic Material Properties

These parameters are intentionally excluded from the current version to keep the engineering workflow simple.

---

# 11.4 Materials and Appearance

The current version focuses primarily on geometry and simulation.

Future releases may support:

- Colors
- Transparency
- Textures
- Material Libraries
- Surface Properties
- Rendering Options

This information could be managed through additional engineering worksheets.

---

# 11.5 Sensors

Future sensor support may include:

- RGB Cameras
- Depth Cameras
- Stereo Cameras
- Thermal Cameras
- GPS
- IMU
- Magnetometers
- Encoders
- Laser Scanners
- Custom Sensors

Each sensor type may introduce its own engineering parameters while preserving the common object structure defined in this specification.

---

# 11.6 Controllers

The GSPL architecture may later include support for controller configuration.

Possible extensions include:

- PID Controllers
- Motion Profiles
- Velocity Controllers
- Torque Controllers
- Position Controllers
- State Machines

These definitions could be exported directly to CoppeliaSim scripts.

---

# 11.7 Robot Description Formats

Although the current implementation uses Rhino as the engineering source, the pipeline architecture could be extended to support additional formats.

Possible future importers include:

- STEP
- URDF
- MuJoCo XML
- SDF
- Collada
- FBX
- glTF

Each importer would generate the same intermediate engineering databases, preserving compatibility with the remaining GSPL stages.

---

# 11.8 Additional Simulation Platforms

The GSPL architecture has been intentionally designed to minimize dependencies on a specific simulator.

Although GSPL-05 currently generates CoppeliaSim models, future builders may target:

- MuJoCo
- Gazebo
- Isaac Sim
- Webots
- Unity
- Unreal Engine

Only the final builder would need to be replaced.

The engineering workflow would remain unchanged.

---

# 11.9 Cloud Integration

Future versions may support:

- Cloud Storage
- Collaborative Engineering
- Version Control Integration
- Automatic Validation
- Continuous Integration
- Automatic Documentation Generation

These features would simplify collaborative engineering projects involving multiple contributors.

---

# 11.10 Long-Term Vision

The long-term objective of the GSPL is to become a generic engineering pipeline capable of transforming mechanical CAD models into complete robotic simulation environments.

The architecture has therefore been designed to evolve incrementally while preserving compatibility with existing engineering projects.

---

# 12. Design Philosophy

## 12.1 Overview

The GSPL was conceived as an engineering methodology rather than a simple conversion program.

Its primary objective is to separate engineering knowledge from software implementation.

This philosophy allows engineers to focus on designing robotic systems while the software automatically generates the required simulation artifacts.

---

# 12.2 Separation of Responsibilities

One of the fundamental principles of the GSPL is the clear separation between different engineering activities.

```text
Mechanical Design

↓

Engineering Definition

↓

Automatic Processing

↓

Simulation Generation
```

Each stage has a single responsibility and produces a well-defined output.

---

# 12.3 Geometry vs Simulation

Mechanical geometry and simulation behaviour represent different engineering domains.

For this reason they are intentionally stored separately.

The Rhino model defines:

- Geometry
- Dimensions
- Physical Components

The Engineering Assembly Table defines:

- Hierarchy
- Simulation Objects
- Sensors
- Joints
- Engineering Decisions

The pipeline combines both sources to generate the final simulation model.

---

# 12.4 Human-Oriented Engineering

The GSPL has been designed around the needs of engineers rather than software developers.

Instead of requiring engineers to edit JSON files, the system provides a familiar spreadsheet interface supporting:

- filtering;
- sorting;
- drop-down lists;
- engineering review;
- documentation;
- validation.

This approach significantly reduces engineering effort.

---

# 12.5 Machine-Oriented Processing

Although engineers work with spreadsheets, the software internally uses structured JSON databases.

These databases provide:

- deterministic processing;
- traceability;
- modularity;
- reproducibility;
- scalability.

The internal representation remains hidden from the engineer whenever possible.

---

# 12.6 Deterministic Pipeline

Given identical inputs, every GSPL stage produces identical outputs.

This deterministic behaviour simplifies:

- debugging;
- testing;
- validation;
- collaboration;
- version control.

Deterministic processing is considered a fundamental design requirement.

---

# 12.7 Traceability

Every engineering decision can be traced from the final CoppeliaSim model back to its origin.

Typical traceability chain:

```text
CoppeliaSim Object

↓

Engineering Assembly Table

↓

Rhino Component
```

This greatly simplifies maintenance and debugging.

---

# 12.8 Modularity

Each GSPL program performs only one specific task.

No program attempts to perform responsibilities belonging to another stage.

This modular architecture provides:

- simpler development;
- independent testing;
- easier maintenance;
- extensibility.

---

# 12.9 Extensibility

New capabilities should be added by extending existing stages rather than redesigning the pipeline.

Examples include:

- new object types;
- new engineering properties;
- new simulation platforms;
- new CAD importers.

Backward compatibility should always be preserved whenever possible.

---

# 12.10 Engineering First

One of the guiding principles of the GSPL is:

> **Engineering decisions should always take precedence over software implementation.**

The software exists to automate repetitive tasks, not to constrain engineering creativity.

The engineer defines the model.

The GSPL builds the simulation.

---

# 12.11 Final Remarks

The GSPL represents an engineering methodology that integrates CAD modeling, engineering documentation and simulation generation into a single reproducible workflow.

By separating geometry, engineering knowledge and software implementation, the GSPL provides a robust foundation for developing increasingly complex robotic systems.

The architecture has been designed to remain maintainable, extensible and simulator-independent, ensuring that future developments can build upon the same engineering principles without disrupting existing projects.

---

# 12.12 Conclusion

The GSPL demonstrates that the automatic generation of simulation environments is not merely a software problem but an engineering process.

By combining:

- structured CAD information;
- engineering knowledge;
- automated validation;
- deterministic processing;
- modular software design;

the GSPL establishes a scalable framework for transforming mechanical designs into high-quality robotic simulation models.

The philosophy presented in this document serves as the foundation for the continued evolution of the GIAR Simulation Pipeline for LiDAR and future engineering projects based on the same methodology.