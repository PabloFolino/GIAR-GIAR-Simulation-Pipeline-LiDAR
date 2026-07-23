# Table of Contents

## Part I — Introduction

1. Introduction
   - 1.1 Purpose
   - 1.2 Scope
   - 1.3 Objectives
   - 1.4 Target Audience
   - 1.5 Terminology
   - 1.6 Document Organization

---

## Part II — GSPL Architecture

2. GSPL Architecture
   - 2.1 Overview
   - 2.2 Layered Architecture
   - 2.3 Layer Responsibilities
   - 2.4 Pipeline Overview
   - 2.5 Program Responsibilities
   - 2.6 Engineering Intervention
   - 2.7 Data Flow
   - 2.8 Design Principles

3. Pipeline Databases
   - 3.1 Overview
   - 3.2 Pipeline Databases
   - 3.3 Engineering Files
   - 3.4 Database Ownership
   - 3.5 Model Database
   - 3.6 Engineering Assembly Database
   - 3.7 Engineering Assembly Table
   - 3.8 Simulation Database
   - 3.9 Transform Database
   - 3.10 Database Evolution
   - 3.11 Engineering Responsibility
   - 3.12 Summary

---

## Part III — Engineering Layer

4. Engineering Assembly Database (`1_assembly.json`)
   - 4.1 Overview
   - 4.2 Purpose
   - 4.3 Generation
   - 4.4 General Structure
   - 4.5 Metadata
   - 4.6 Components
   - 4.7 Component Structure
   - 4.8 Automatically Generated Information
   - 4.9 Engineering Control Database
   - 4.10 Relationship with the Engineering Assembly Table
   - 4.11 Relationship with the Simulation Database
   - 4.12 Editing Policy
   - 4.13 Summary

5. Engineering Assembly Table (`1_assembly_table.xlsx`)
   - 5.1 Overview
   - 5.2 Purpose
   - 5.3 Engineering Philosophy
   - 5.4 Workbook Structure
   - 5.5 Components Worksheet
   - 5.6 Components Fields
   - 5.7 Objects Worksheet
   - 5.8 Object Definition
   - 5.9 Lists Worksheet
   - 5.10 Validation
   - 5.11 Engineering Workflow
   - 5.12 Compilation
   - 5.13 Engineering Responsibility
   - 5.14 Single Source of Truth
   - 5.15 Summary

6. Engineering Workflow
   - 6.1 Overview
   - 6.2 Workflow Overview
   - 6.3 Mechanical Design
   - 6.4 Engineering Extraction
   - 6.5 Engineering Definition
   - 6.6 Simulation Compilation
   - 6.7 Transformation Generation
   - 6.8 Geometry Export
   - 6.9 Simulation Construction
   - 6.10 Iterative Engineering
   - 6.11 Engineering Traceability
   - 6.12 Workflow Principles
   - 6.13 Summary

---

## Part IV — Simulation Layer

7. Simulation Database (`2_simulation_database.json`)
   - 7.1 Overview
   - 7.2 Purpose
   - 7.3 Generation
   - 7.4 Inputs
   - 7.5 General Structure
   - 7.6 Metadata
   - 7.7 Components
   - 7.8 Simulation Objects
   - 7.9 Component Compilation
   - 7.10 Validation
   - 7.11 Traceability
   - 7.12 Downstream Consumers
   - 7.13 Engineering Independence
   - 7.14 Design Principles
   - 7.15 Summary

8.8. Reference Frame Database (3_reference_frame_database.json)

9. Simulation Objects

10. Validation Rules

11. Reports

---

## Part V — Runtime Layer

12. STL Export

13. CoppeliaSim Builder

14. Runtime Assets

---

## Part VI — Configuration

15. Configuration File (`config.json`)

16. Directory Structure

17. Naming Conventions

18. Logging

---

## Part VII — Appendices

A. JSON Schemas

B. Excel Workbook Specification

C. Validation Rules

D. Object Types

E. Joint Types

F. Reference Frames

G. Glossary

H. Revision History

***

# 1. Introduction

## 1.1 Purpose

This document defines the architecture, engineering principles and operational workflow of the **GIAR Simulation Pipeline (GSPL)**.

The GSPL is an automated software pipeline designed to transform three-dimensional Computer-Aided Design (CAD) models into complete robotic simulation models.

The specification establishes a standardized methodology for converting engineering information into simulator-ready assets while maintaining traceability, reproducibility and modularity throughout the entire process.

This document serves as the authoritative technical reference for the development, maintenance and future evolution of the GSPL.

---

## 1.2 Scope

The GSPL covers the complete transformation process from a mechanical CAD model to a fully operational simulation model.

The current implementation targets:

- Rhino as the CAD authoring environment.
- STL as the geometry exchange format.
- CoppeliaSim as the simulation platform.

The pipeline architecture has been intentionally designed to remain simulator-independent, allowing future support for additional simulation environments without modifying the engineering workflow.

This specification describes the overall architecture of the GSPL rather than the implementation details of individual programs.

---

## 1.3 Objectives

The primary objectives of the GSPL are:

- automate the conversion of CAD models into simulation models;
- separate engineering decisions from software implementation;
- provide deterministic execution throughout the pipeline;
- preserve engineering traceability;
- minimize manual intervention;
- simplify maintenance and future extensions;
- establish a standardized engineering workflow.

Together, these objectives enable the creation of complex robotic simulation models using a repeatable and scalable methodology.

---

## 1.4 Target Audience

This document is intended for:

- simulation engineers;
- robotics researchers;
- software developers;
- CAD designers;
- system integrators;
- future contributors to the GSPL project.

A general understanding of CAD systems and robotic simulation is assumed.

---

## 1.5 Terminology

Throughout this specification, the following terminology is used.

| Term | Description |
|------|-------------|
| CAD | Computer-Aided Design model created in Rhino. |
| Component | Logical engineering element extracted from the CAD model. |
| Simulation Object | Entity created inside the simulation environment. |
| Pipeline Database | JSON database generated by a GSPL stage. |
| Engineering Database | Database describing the engineering model. |
| Engineering Assembly Table | Excel workbook used to define engineering decisions. |
| Simulation Database | Fully compiled engineering description of the simulation model. |
| Transform Database | Database containing calculated reference frames and transformations. |
| Runtime Assets | Files consumed directly by the simulation environment. |

---

## 1.6 Document Organization

This specification is organized into seven major parts.

### Part I — Introduction

Introduces the GSPL, its objectives and the overall scope of the specification.

### Part II — GSPL Architecture

Describes the layered architecture, the pipeline organization and the engineering databases that support the GSPL.

### Part III — Engineering Layer

Defines the engineering artifacts used to configure and validate the simulation model.

### Part IV — Simulation Layer

Describes the Simulation Database and the information required to construct the simulation model.

### Part V — Runtime Layer

Defines the generation of runtime assets including STL geometry and the CoppeliaSim model.

### Part VI — Configuration

Describes configuration files, directory organization, naming conventions and logging.

### Part VII — Appendices

Contains reference material, schemas, validation rules and supporting documentation.

---

## 1.7 GSPL Overview

The GSPL is organized as a strictly sequential processing pipeline.

Each stage performs a single engineering responsibility and produces the complete set of outputs required by the next stage.

```text
Rhino CAD (.3dm)
        │
        ▼
GSPL-01 Rhino Extractor
        │
        ▼
GSPL-02 Simulation Compiler
        │
        ▼
GSPL-03 Transform Builder
        │
        ▼
GSPL-04 STL Exporter
        │
        ▼
GSPL-05 Coppelia Builder
        │
        ▼
Simulation Model (.ttm)
```

This architecture ensures modularity, deterministic execution and complete traceability across the entire engineering workflow.

---

## 1.8 Design Philosophy

The GSPL is based on four fundamental principles.

- **Separation of Responsibilities**  
  Each program performs a single, well-defined task.

- **Deterministic Processing**  
  Identical inputs always produce identical outputs.

- **Engineering Traceability**  
  Every simulation entity can be traced back to its engineering origin.

- **Pipeline Modularity**  
  Each stage depends only on the outputs of the immediately preceding stage, allowing independent development, testing and maintenance.

These principles define the foundation upon which the entire GSPL architecture is built.

***
# 2. GSPL Architecture

## 2.1 Overview

The **GIAR Simulation Pipeline for LiDAR (GSPL)** is organized as a sequence of independent programs, where each stage performs a single engineering responsibility and produces deterministic outputs for the following stage.

Rather than being viewed simply as a chain of programs, the GSPL is organized as a set of conceptual layers that progressively transform a mechanical CAD model into a complete robotic simulation.

Each layer increases the amount of engineering knowledge contained in the project while preserving complete traceability between the original CAD model and the final simulation.

This layered architecture provides:

- modularity;
- reproducibility;
- deterministic processing;
- traceability;
- maintainability;
- extensibility.

---

## 2.2 Layered Architecture

The GSPL is divided into four conceptual layers.

Each layer represents a different abstraction level of the engineering process.

```text
┌──────────────────────────────────────────────────────────────┐
│                         CAD Layer                            │
│                                                              │
│ Rhino (.3dm)                                                 │
│ 1_model_database.json                                        │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                     Engineering Layer                        │
│                                                              │
│ 1_assembly.json                                              │
│ 1_assembly_table.xlsx                                        │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                     Simulation Layer                         │
│                                                              │
│ 2_simulation_database.json                                   │
│ 3_reference_frame_database.json                                    │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      Runtime Layer                           │
│                                                              │
│ STL Meshes                                                   │
│ GIAR_Low_Cost_3D_LiDAR.ttm                                   │
└──────────────────────────────────────────────────────────────┘
```

Each layer has a clearly defined purpose and is generated by a specific GSPL program.

---

## 2.3 Layer Responsibilities

### CAD Layer

The CAD Layer contains the mechanical description extracted directly from Rhino.

It represents the physical product and contains only geometric information.

Typical information includes:

- components;
- geometry;
- bounding boxes;
- materials;
- layers;
- colors.

This layer contains no simulation knowledge.

---

### Engineering Layer

The Engineering Layer contains the engineering decisions introduced by the simulation engineer.

At this stage the engineer defines:

- assembly hierarchy;
- simulation models;
- simulation objects;
- joints;
- sensors;
- cameras;
- lights;
- engineering documentation.

The Engineering Layer describes the intended simulation but does not yet represent a complete simulation model.

---

### Simulation Layer

The Simulation Layer represents the compiled simulation model.

It combines:

- CAD information;
- engineering decisions;
- validated hierarchy;
- simulation objects;
- simulation metadata.

This layer is automatically generated by the **GSPL-02 Simulation Compiler**.

The Simulation Layer becomes the official input for all remaining stages of the pipeline.

---

### Runtime Layer

The Runtime Layer contains every resource required to execute the simulation.

This includes:

- STL meshes;
- CoppeliaSim model;
- runtime resources.

The Runtime Layer is generated automatically without additional engineering intervention.

---

## 2.4 Pipeline Overview

```text
                    Rhino CAD Model (.3dm)
                              │
                              ▼
                 GSPL-01 Rhino Extractor
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
1_model_database.json   1_assembly.json   1_assembly_table.xlsx
                                                  │
                                                  ▼
                                      Simulation Engineer
                                                  │
                                                  ▼
                               GSPL-02 Simulation Compiler
                                   │                 │
                                   ▼                 ▼
                  2_simulation_database.json   2_assembly_table.xlsx
                                   │
                                   ▼
                         GSPL-03 Transform Builder
                                   │
                                   ▼
                        3_reference_frame_database.json
                                   │
                                   ▼
                           GSPL-04 STL Exporter
                                   │
                                   ▼
                               STL Meshes
                                   │
                                   ▼
                         GSPL-05 Coppelia Builder
                                   │
                                   ▼
                     GIAR_Low_Cost_3D_LiDAR.ttm
```

---

## 2.5 Program Responsibilities

### GSPL-01 — Rhino Extractor

**Purpose**

Extract all engineering information available from the Rhino CAD model.

**Responsibilities**

- Read the Rhino project.
- Audit the CAD model.
- Generate the CAD database.
- Generate the initial Engineering Assembly.
- Generate the Engineering Assembly Table.

**Outputs**

- 1_model_database.json
- 1_assembly.json
- 1_assembly_table.xlsx

---

### GSPL-02 — Simulation Compiler

**Purpose**

Compile the engineering description into a validated Simulation Database.

**Mission**

The GSPL-02 Simulation Compiler transforms the engineering decisions recorded in the Engineering Assembly Table into a validated Simulation Database consumed by the remaining stages of the GSPL pipeline.

**Inputs**

- config.json
- 1_model_database.json
- 1_assembly.json
- 1_assembly_table.xlsx

**Internal Stages**

1. Load
2. Validate
3. Compile
4. Generate Reports

**Outputs**

- 2_simulation_database.json
- 2_assembly_table.xlsx
- 2_simulation_report.md

---

### GSPL-03 — Transform Builder

**Purpose**

Calculate every local and global transformation required by the simulation. Builds the **Reference Frame Tree (RFT)** and computes all local and global transformations.

**Outputs**

- 3_reference_frame_database.json

---

### GSPL-04 — STL Exporter

**Purpose**

Generate every STL mesh required by the simulation.

**Outputs**

- STL Meshes

---

### GSPL-05 — Coppelia Builder

**Purpose**

Generate the final CoppeliaSim model from the Simulation Database.

**Outputs**

- GIAR_Low_Cost_3D_LiDAR.ttm

---

## 2.6 Engineering Intervention

Only one stage of the pipeline requires manual engineering input.

```text
GSPL-01
     │
     ▼

Engineering Assembly Table

     ▲

     │
Simulation Engineer

     │

     ▼

GSPL-02 Simulation Compiler
```

All remaining stages execute automatically.

This design minimizes manual intervention while preserving complete engineering control over the generated simulation.

---

## 2.7 Data Flow

The complete engineering process can be summarized by the following transformation.

```text
CAD Assembly

        +

Engineering Decisions

        │

        ▼

Simulation Assembly

        │

        ▼

Simulation Database

        │

        ▼

Transform Database

        │

        ▼

Runtime Assets

        │

        ▼

CoppeliaSim Model
```

The GSPL-02 Simulation Compiler is responsible for transforming the Engineering Assembly into the Simulation Database.

---

## 2.8 Design Principles

The GSPL architecture follows the following principles.

### DP-001

One program, one responsibility.

---

### DP-002

One file, one purpose.

---

### DP-003

Engineering data shall remain separated from internal pipeline data.

---

### DP-004

The simulation engineer interacts exclusively with the Engineering Assembly Table.

---

### DP-005

GSPL-02 compiles engineering information instead of modifying previous pipeline stages.

---

### DP-006

Every stage shall produce deterministic outputs from deterministic inputs.

---

### DP-007

Every generated file shall be traceable to its originating engineering decision.

---

### DP-008

The pipeline shall remain modular, extensible and simulator independent.

---

# 3. Pipeline Databases

## 3.1 Overview

The GSPL is based on a sequence of engineering databases generated throughout the pipeline.

Each database represents a specific abstraction level of the engineering process and serves as the official interface between consecutive GSPL programs.

Rather than exchanging temporary data structures, each program produces a complete, deterministic and self-consistent database that becomes the official input for the next stage.

This approach provides:

- deterministic execution;
- reproducibility;
- traceability;
- independent program development;
- simplified debugging;
- long-term maintainability.

Although the databases are stored using the JSON format, they should be regarded as engineering artifacts rather than implementation details.

---

## 3.2 Pipeline Databases

The current GSPL architecture generates the following databases.

| Stage | Database | Layer | Purpose |
|--------|----------|-------|---------|
| GSPL-01 | `1_model_database.json` | CAD | CAD information extracted from Rhino. |
| GSPL-01 | `1_assembly.json` | Engineering | Initial Engineering Assembly generated from the CAD model. |
| GSPL-02 | `2_simulation_database.json` | Simulation | Validated simulation database. |
| GSPL-03 | `3_reference_frame_database.json` | Reference Frame and Transform Database |Stores the complete Reference Frame Tree (RFT) together with all local and global reference frames and the transformations derived from them. |
| GSPL-04 | STL Meshes | Runtime | Geometry exported for simulation. |
| GSPL-05 | `.ttm` | Runtime | Final CoppeliaSim model. |

Each database has exactly one producer and one primary consumer.

No program modifies databases generated by previous stages.

---

## 3.3 Engineering Files

Unlike the internal databases, engineering files are intended to be edited by the simulation engineer.

The current engineering files are:

| File | Purpose |
|------|---------|
| `1_assembly_table.xlsx` | Engineering Assembly definition. |

The Engineering Assembly Table is the only document that should normally be modified manually.

Future versions of the GSPL may introduce additional engineering workbooks while preserving the same overall architecture.

---

## 3.4 Database Ownership

One of the fundamental architectural principles of the GSPL is database ownership.

Every database belongs to exactly one program.

Once generated, a database becomes immutable.

Subsequent programs may read the database but shall never modify it.

This guarantees deterministic execution and complete traceability.

| Database | Generated By | Modified By |
|-----------|--------------|-------------|
| `1_model_database.json` | GSPL-01 | None |
| `1_assembly.json` | GSPL-01 | None |
| `2_simulation_database.json` | GSPL-02 | None |
| `3_reference_frame_database.json` | GSPL-03 | None |

Whenever additional information is required, a new database shall be generated instead of modifying an existing one.

---

## 3.5 The Role of 3_reference_frame_database.json

The Model Database represents the CAD Layer.

Its purpose is to describe every component extracted from Rhino without introducing any simulation knowledge.

Typical information includes:

- component identifiers;
- names;
- geometry;
- bounding boxes;
- materials;
- Rhino attributes.

This database is generated exclusively by GSPL-01.

---

## 3.6 The Role of `1_assembly.json`

The Engineering Assembly represents the Engineering Layer.

It is generated automatically by GSPL-01 as an initial engineering template.

Its purpose is to preserve the engineering structure extracted from the CAD model before any manual intervention.

The simulation engineer normally interacts with the Engineering Assembly Table instead of editing this file directly.

The Engineering Assembly therefore acts as an intermediate engineering reference rather than as the primary simulation database.

---

## 3.7 The Role of `1_assembly_table.xlsx`

The Engineering Assembly Table is the official engineering interface of the GSPL.

It records every engineering decision introduced by the simulation engineer.

Examples include:

- assembly hierarchy;
- simulation models;
- simulation objects;
- joints;
- sensors;
- engineering notes.

This workbook is the single source of truth for every engineering decision made during the project.

---

## 3.8 The Role of `2_simulation_database.json`

The Simulation Database is the most important database generated by the GSPL.

It is produced by the **GSPL-02 Simulation Compiler**.

Unlike the Engineering Assembly, the Simulation Database represents a complete, validated and deterministic description of the simulation model.

It combines:

- CAD information;
- engineering decisions;
- validated hierarchy;
- simulation objects;
- simulation metadata.

Every remaining GSPL program operates exclusively on this database.

The Simulation Database therefore becomes the official interface between the engineering stage and the automatic simulation pipeline.

---

## 3.9 The Role of `3_reference_frame_database.json`

The Transform Database extends the Simulation Database by adding every geometric transformation required by the simulation.

Typical information includes:

- local reference frames;
- global reference frames;
- transformation matrices;
- object positions;
- object orientations.

This database is consumed by the STL Exporter and the Coppelia Builder.

---

## 3.10 Database Evolution

The GSPL progressively enriches the project information throughout the pipeline.

```text
Rhino CAD
      │
      ▼
Model Database
      │
      ▼
Engineering Assembly
      │
      ▼
Engineering Decisions
      │
      ▼
Simulation Database
      │
      ▼
Transform Database
      │
      ▼
Runtime Assets
      │
      ▼
CoppeliaSim Model
```

Each stage adds engineering knowledge while preserving all information generated by previous stages.

---

## 3.11 Engineering Responsibility

The simulation engineer is responsible only for engineering decisions.

Examples include:

- defining assembly hierarchy;
- selecting simulation models;
- creating simulation objects;
- configuring joints;
- documenting engineering decisions.

The engineer is not responsible for maintaining any pipeline database.

Those databases are generated automatically by the GSPL.

---

## 3.12 Summary

The GSPL architecture intentionally separates engineering information from pipeline processing.

Engineering decisions are recorded in the Engineering Assembly Table.

The GSPL-02 Simulation Compiler transforms those decisions into the Simulation Database, which becomes the official representation used by all remaining stages.

This architecture guarantees deterministic execution, modularity, traceability and long-term maintainability while preserving a clear separation between engineering activities and software implementation.


***
# 4. Engineering Assembly Database (`1_assembly.json`)

## 4.1 Overview

The **Engineering Assembly Database** (`1_assembly.json`) is the internal engineering database generated automatically by **GSPL-01 Rhino Extractor**.

It represents the initial engineering interpretation of the CAD model before any manual engineering decisions are introduced.

Unlike the Engineering Assembly Table, this database is not intended to be edited manually.

Its primary purpose is to provide a deterministic engineering baseline that can later be compared with the compiled simulation model generated by **GSPL-02 Simulation Compiler**.

The Engineering Assembly Database therefore acts as an engineering control document throughout the pipeline.

---

## 4.2 Purpose

The Engineering Assembly Database has four main objectives.

- Preserve the engineering structure extracted from the CAD model.
- Provide an immutable engineering reference.
- Allow auditing of engineering modifications.
- Serve as the initial input for the Simulation Compiler.

Unlike the Simulation Database, this file contains only information that can be inferred directly from the CAD model.

Engineering decisions introduced later by the simulation engineer are intentionally excluded.

---

## 4.3 Generation

The database is generated exclusively by

```text
GSPL-01_Rhino_Extractor.py
```

No subsequent GSPL program modifies this file.

Once created, it remains unchanged during the remainder of the pipeline.

This guarantees complete traceability between the original CAD model and the generated simulation.

---

## 4.4 General Structure

The Engineering Assembly Database is divided into two major sections.

1. Metadata
2. Components

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

## 4.5 Metadata

The metadata section identifies the origin of the database.

| Field | Description |
|--------|-------------|
| format_version | Database format version. |
| generated_by | Program that generated the database. |
| generator_version | Software version. |
| project | Project name. |
| root | Root component identifier. |

The metadata guarantees that every database can be traced to the software version that generated it.

---

## 4.6 Components

Each Rhino component appears exactly once in the Engineering Assembly Database.

Every component contains only information automatically extracted from the CAD model.

Typical information includes:

- identifier;
- name;
- bounding box;
- reference frame;
- geometric models;
- initial object list.

Engineering properties are intentionally omitted.

---

## 4.7 Component Structure

Example

```json
{
    "id":18,

    "name":"NEMA17",

    "enabled":true,

    "parent":null,

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

    "objects":[ ]
}
```

---

## 4.8 Automatically Generated Information

The following information is generated automatically by GSPL-01.

| Property | Source |
|----------|--------|
| Component ID | Rhino |
| Component Name | Rhino |
| Bounding Box | Rhino Geometry |
| Local Reference Frame | Rhino Geometry |
| Initial Parent | Rhino Assembly |
| Default Models | GSPL Rules |
| Initial Objects | GSPL Rules |

No engineering interpretation is required to generate these values.

---

## 4.9 Engineering Control Database

The Engineering Assembly Database serves as an engineering control document.

Its contents remain unchanged during the entire simulation pipeline.

This allows engineers to compare:

- the original engineering structure;
- the engineering decisions;
- the compiled simulation database.

Consequently, every engineering modification remains fully traceable.

---

## 4.10 Relationship with the Engineering Assembly Table

The Engineering Assembly Database and the Engineering Assembly Table complement each other.

| Engineering Assembly Database | Engineering Assembly Table |
|------------------------------|----------------------------|
| Automatically generated | Edited by the engineer |
| JSON | Excel |
| Read-only | Editable |
| Engineering baseline | Engineering decisions |

Both describe the same mechanical system from different perspectives.

---

## 4.11 Relationship with the Simulation Database

The Engineering Assembly Database should not be confused with the Simulation Database.

The Engineering Assembly Database represents the mechanical assembly extracted from the CAD model.

The Simulation Database represents the final engineering interpretation of that assembly after all engineering decisions have been compiled.

The transformation between both representations is performed exclusively by the **GSPL-02 Simulation Compiler**.

---

## 4.12 Editing Policy

The Engineering Assembly Database should normally never be edited manually.

Any engineering modification shall be performed using the Engineering Assembly Table.

Direct modifications are recommended only for:

- software debugging;
- database inspection;
- pipeline development.

Engineering projects should never depend on manual modifications of this database.

---

## 4.13 Summary

The Engineering Assembly Database represents the immutable engineering baseline of the project.

It preserves the original engineering structure extracted from Rhino while remaining independent from subsequent engineering decisions.

Together with the Engineering Assembly Table, it provides the information required by the GSPL-02 Simulation Compiler to generate the validated Simulation Database used by the remaining stages of the GSPL pipeline.

***

# 5. Engineering Assembly Table (`1_assembly_table.xlsx`)

## 5.1 Overview

The **Engineering Assembly Table** (`1_assembly_table.xlsx`) is the official engineering interface of the GSPL.

It provides a structured environment where the simulation engineer defines every engineering decision required to transform a mechanical CAD model into a complete simulation model.

Unlike the internal pipeline databases, the Engineering Assembly Table is specifically designed for human interaction.

It is generated automatically by **GSPL-01 Rhino Extractor** and later processed by the **GSPL-02 Simulation Compiler**.

Throughout the pipeline, this workbook represents the single source of truth for all engineering decisions.

---

## 5.2 Purpose

The Engineering Assembly Table has four primary objectives.

- Describe the engineering assembly.
- Record engineering decisions.
- Configure simulation objects.
- Provide a human-friendly interface independent of the internal pipeline implementation.

The workbook intentionally hides every internal database structure used by the GSPL.

This allows the engineering workflow to remain stable even if future versions modify the internal databases.

---

## 5.3 Engineering Philosophy

The GSPL intentionally separates engineering from software implementation.

The simulation engineer works exclusively with the Engineering Assembly Table.

The GSPL software is responsible for:

- validating engineering information;
- compiling simulation databases;
- generating transformation databases;
- exporting STL meshes;
- building the CoppeliaSim model.

This separation minimizes engineering effort while preserving complete traceability.

---

## 5.4 Workbook Structure

The workbook currently contains three worksheets.

| Worksheet | Purpose | Editable |
|------------|---------|:--------:|
| Components | Engineering assembly definition | ✔ |
| Objects | Simulation object definitions | ✔ |
| Lists | Validation lists | ❌ |

The Lists worksheet is automatically generated and remains hidden.

It shall never be modified manually.

---

## 5.5 Components Worksheet

Each row represents exactly one engineering component.

The worksheet defines the logical organization of the mechanical assembly.

Typical information includes:

- component hierarchy;
- engineering descriptions;
- simulation models;
- engineering status;
- documentation.

The Components worksheet intentionally contains no implementation-specific information.

---

## 5.6 Components Fields

The Components worksheet contains the following information.

| Field | Generated By | Editable | Description |
|--------|--------------|:--------:|-------------|
| ID | GSPL-01 | ❌ | Unique component identifier. |
| Name | GSPL-01 | ❌ | Component name extracted from Rhino. |
| Type | Engineer | ✔ | Engineering classification. |
| Description | Engineer | ✔ | Engineering description. |
| Enabled | Engineer | ✔ | Enables or disables the component. |
| Parent Name | Engineer | ✔ | Parent component selected by name. |
| Parent ID | GSPL-02 | ❌ | Automatically resolved identifier. |
| Visual | Engineer | ✔ | Belongs to the visual model. |
| Simulation | Engineer | ✔ | Belongs to the simulation model. |
| Reviewed | Engineer | ✔ | Engineering review flag. |
| Status | Engineer | ✔ | Engineering workflow state. |
| Notes | Engineer | ✔ | Engineering documentation. |

---

## 5.7 Objects Worksheet

The Objects worksheet defines every simulation object associated with each engineering component.

Unlike the Components worksheet, a component may generate any number of simulation objects.

Typical object types include:

- Shape
- Joint
- Dummy
- Vision Sensor
- Proximity Sensor
- Force Sensor
- Camera
- Light

Future versions of the GSPL may extend this list without modifying the overall engineering workflow.

---

## 5.8 Object Definition

Every row describes one simulation object.

Typical information includes:

- Component
- Object Name
- Object Type
- Joint Type
- Position
- Orientation
- Dynamic Properties
- Additional Parameters

The Objects worksheet represents the engineering specification that will later be compiled into the Simulation Database.

---

## 5.9 Lists Worksheet

The Lists worksheet contains every validation list required by the workbook.

Examples include:

- component names;
- object types;
- joint types;
- engineering status;
- component types;
- Boolean values.

This worksheet is generated automatically by GSPL-01.

It is marked as **VeryHidden** and should never be modified manually.

---

## 5.10 Validation

The Engineering Assembly Table incorporates multiple validation mechanisms before the Simulation Compiler performs its own validation.

Examples include:

- drop-down lists;
- mandatory fields;
- Boolean validation;
- engineering status;
- object type validation;
- parent selection.

These mechanisms reduce engineering errors before compilation.

---

## 5.11 Engineering Workflow

The Engineering Assembly Table is completed after executing GSPL-01.

The normal engineering workflow is:

```text
Rhino CAD

      │

      ▼

GSPL-01 Rhino Extractor

      │

      ▼

Engineering Assembly Table

      │

Simulation Engineer

      │

      ▼

GSPL-02 Simulation Compiler
```

The simulation engineer never edits the pipeline databases directly.

---

## 5.12 Compilation

When GSPL-02 executes, the Engineering Assembly Table becomes the primary engineering input.

The Simulation Compiler performs four major operations.

### 1. Load

Reads every worksheet.

### 2. Validate

Verifies engineering consistency.

### 3. Compile

Generates the Simulation Database.

### 4. Report

Produces engineering reports and validation messages.

No engineering information is lost during compilation.

Instead, the engineering decisions become part of the Simulation Database.

---

## 5.13 Engineering Responsibility

The simulation engineer is responsible for defining:

- assembly hierarchy;
- simulation models;
- simulation objects;
- joints;
- sensors;
- engineering documentation.

The engineer is not responsible for maintaining any internal database generated by the GSPL.

---

## 5.14 Single Source of Truth

Within the Engineering Layer, the Engineering Assembly Table is considered the official source of engineering information.

Whenever discrepancies exist between:

- Engineering Assembly Database;
- Engineering Assembly Table;

the information contained in the Engineering Assembly Table always takes precedence during compilation.

This design ensures that every engineering decision explicitly recorded by the engineer becomes part of the final simulation model.

---

## 5.15 Summary

The Engineering Assembly Table is the central engineering document of the GSPL.

It provides a stable, intuitive and simulator-independent interface between engineering activities and the automatic simulation pipeline.

By separating engineering decisions from software implementation, the GSPL allows increasingly complex simulation models to be developed while preserving modularity, traceability and deterministic execution.

***

# 6. Engineering Workflow

## 6.1 Overview

The GSPL implements a deterministic engineering workflow that transforms a mechanical CAD model into a complete simulation model.

The workflow separates engineering activities from software implementation, allowing engineers to focus exclusively on simulation design while the GSPL automates every computational task.

Each stage receives well-defined inputs, performs a single responsibility and generates deterministic outputs for the following stage.

---

## 6.2 Workflow Overview

The complete engineering workflow is illustrated below.

```text
                Rhino CAD Model
                     (.3dm)
                        │
                        ▼
          GSPL-01 Rhino Extractor
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
1_model_database   1_assembly.json   1_assembly_table.xlsx
                        │                ▲
                        │                │
                        │         Simulation Engineer
                        │                │
                        └────────┬───────┘
                                 ▼
                  GSPL-02 Simulation Compiler
                                 │
        ┌────────────────────────┼─────────────────────┐
        ▼                        ▼                     ▼
2_simulation_database     2_assembly_table     2_simulation_report
                                 │
                                 ▼
                  GSPL-03 Transform Builder
                                 │
                                 ▼
                  3_reference_frame_database.json
                                 │
                                 ▼
                     GSPL-04 STL Exporter
                                 │
                                 ▼
                           STL Meshes
                                 │
                                 ▼
                   GSPL-05 Coppelia Builder
                                 │
                                 ▼
                 GIAR_Low_Cost_3D_LiDAR.ttm
```

Every stage produces deterministic outputs that become the official inputs for the following stage.

---

## 6.3 Stage 1 — Mechanical Design

The workflow begins with the creation of the mechanical model in Rhino.

At this stage the model contains only CAD information.

Typical information includes:

- component geometry;
- component names;
- assembly hierarchy;
- materials;
- colors;
- layers.

No simulation information is introduced during this stage.

---

## 6.4 Stage 2 — Engineering Extraction

The Rhino model is processed by **GSPL-01 Rhino Extractor**.

This program automatically extracts every engineering element that can be inferred from the CAD model.

Generated outputs include:

- Model Database;
- Engineering Assembly Database;
- Engineering Assembly Table.

These files establish the engineering baseline for the project.

---

## 6.5 Stage 3 — Engineering Definition

The simulation engineer completes the Engineering Assembly Table.

Typical engineering tasks include:

- defining simulation hierarchy;
- selecting simulation models;
- creating simulation objects;
- defining joints;
- configuring sensors;
- documenting engineering decisions.

This is the only manual stage of the entire GSPL pipeline.

---

## 6.6 Stage 4 — Simulation Compilation

The Engineering Assembly Table is processed by the **GSPL-02 Simulation Compiler**.

The compiler transforms engineering information into a validated Simulation Database.

Internally, GSPL-02 executes four sequential phases.

### Phase 1 — Load

All engineering databases and workbooks are loaded into memory.

### Phase 2 — Validation

The engineering information is validated.

Examples include:

- hierarchy consistency;
- duplicate names;
- missing objects;
- invalid joint definitions;
- spreadsheet integrity.

### Phase 3 — Compilation

The validated engineering information is transformed into the Simulation Database.

Engineering decisions are merged with the Engineering Assembly Database while preserving complete traceability.

### Phase 4 — Reporting

Compilation results are documented.

Typical outputs include:

- validation report;
- engineering warnings;
- compilation statistics;
- updated engineering workbook.

---

## 6.7 Stage 5 — Reference Frame Generation

GSPL-03 builds the Reference Frame Tree (RFT) from the validated Simulation Database. Once the tree has been constructed, all local and global transformations are calculated automatically.

This stage calculates:

- local reference frames;
- global reference frames;
- transformation matrices;
- object positions;
- object orientations.

The resulting Transform Database becomes the geometric reference for the remainder of the pipeline.

---

## 6.8 Stage 6 — Geometry Export

The Transform Database is processed by **GSPL-04 STL Exporter**.

The exporter generates every STL mesh required by the simulation.

Generated meshes preserve:

- geometry;
- scale;
- orientation;
- engineering hierarchy.

These meshes become runtime resources.

---

## 6.9 Stage 7 — Simulation Construction

The final stage is executed by **GSPL-05 Coppelia Builder**.

Using the Simulation Database, the Transform Database and the exported meshes, the builder creates the complete CoppeliaSim model.

Typical operations include:

- creating Shapes;
- creating Joints;
- creating Dummies;
- creating Sensors;
- configuring dynamics;
- building hierarchy;
- assigning properties.

Finally, the complete simulation model is saved as a `.ttm` file.

---

## 6.10 Iterative Engineering

Engineering is naturally an iterative process.

Whenever validation errors are detected, the engineer updates the Engineering Assembly Table and executes the Simulation Compiler again.

```text
Engineering Assembly Table
            │
            ▼
GSPL-02 Simulation Compiler
            │
            ▼
Validation Report
            │
     Errors Found?
       │        │
      Yes       No
       │         │
       ▼         ▼
Update Table   Continue
       │
       └──────────────►
```

This cycle may be repeated as many times as necessary until the engineering model is fully validated.

---

## 6.11 Engineering Traceability

Every engineering decision remains traceable throughout the pipeline.

Typical traceability chain:

```text
Rhino Component
        │
        ▼
Engineering Assembly Database
        │
        ▼
Engineering Assembly Table
        │
        ▼
Simulation Database
        │
        ▼
Transform Database
        │
        ▼
CoppeliaSim Object
```

This traceability greatly simplifies debugging, maintenance and future project evolution.

---

## 6.12 Workflow Principles

The GSPL workflow follows the following principles.

### WF-001

One engineering responsibility per stage.

---

### WF-002

One official output database per stage.

---

### WF-003

Engineering decisions are introduced only through the Engineering Assembly Table.

---

### WF-004

Pipeline databases are generated automatically.

---

### WF-005

Compilation shall always be deterministic.

---

### WF-006

Every engineering decision shall remain traceable.

---

### WF-007

The workflow shall support unlimited engineering iterations.

---

## 6.13 Summary

The GSPL Engineering Workflow provides a structured methodology for transforming CAD models into robotic simulation models.

By separating mechanical design, engineering definition, simulation compilation and runtime generation into independent stages, the GSPL achieves a highly modular, deterministic and maintainable engineering process.

This workflow forms the operational backbone of the entire GSPL architecture.

***

# 7. Simulation Database (`2_simulation_database.json`)

## 7.1 Overview

The **Simulation Database** (`2_simulation_database.json`) is the primary output generated by the **GSPL-02 Simulation Compiler**.

It represents the complete engineering description of the simulation model after all engineering decisions have been validated and compiled.

Unlike the Engineering Assembly Database, which represents the original mechanical assembly extracted from the CAD model, the Simulation Database represents the finalized simulation model consumed by the remaining stages of the GSPL pipeline.

From this stage onward, every GSPL program operates exclusively on the Simulation Database.

---

## 7.2 Purpose

The Simulation Database has the following objectives.

- Consolidate CAD information and engineering decisions.
- Represent the complete simulation model.
- Provide a deterministic interface for subsequent pipeline stages.
- Preserve complete engineering traceability.
- Eliminate the need for additional engineering interpretation.

The Simulation Database is considered the authoritative representation of the simulation model.

---

## 7.3 Generation

The Simulation Database is generated exclusively by

```text
GSPL-02_Simulation_Compiler.py
```

Its generation consists of four sequential phases.

1. Load
2. Validate
3. Compile
4. Report

Once generated, the database becomes read-only.

No subsequent GSPL program modifies its contents.

---

## 7.4 Inputs

The Simulation Compiler combines information from the following sources.

| Source | Purpose |
|----------|---------|
| `1_model_database.json` | CAD information |
| `1_assembly.json` | Engineering control database |
| `1_assembly_table.xlsx` | Engineering decisions |
| `config.json` | Pipeline configuration |

Each input contributes a specific category of information.

---

## 7.5 General Structure

The Simulation Database is organized into four major sections.

```json
{
    "metadata": { },

    "statistics": { },

    "components": [ ],

    "simulation_objects": [ ]
}
```

This organization separates project metadata from simulation entities.

---

## 7.6 Metadata

The metadata section identifies the generated database.

Typical information includes:

- format version;
- generator;
- software version;
- project name;
- generation date;
- source databases.

This information guarantees complete traceability.

---

## 7.7 Components

The Components section describes every engineering component participating in the simulation.

Each component contains validated information such as:

- identifier;
- name;
- parent;
- hierarchy;
- enabled state;
- simulation models;
- engineering attributes.

Unlike the Engineering Assembly Database, every relationship has already been validated.

---

## 7.8 Simulation Objects

The Simulation Objects section contains every object that will later be created inside CoppeliaSim.

Typical object types include:

- Shape
- Joint
- Dummy
- Vision Sensor
- Force Sensor
- Proximity Sensor
- Camera
- Light

Each object is completely defined and no further engineering interpretation is required.

---

## 7.9 Component Compilation

During compilation, the Simulation Compiler performs the following operations.

- Resolves parent identifiers.
- Validates hierarchy.
- Expands engineering models.
- Creates simulation objects.
- Resolves object references.
- Assigns unique identifiers.
- Validates dependencies.

The resulting database is internally consistent.

---

## 7.10 Validation

Compilation succeeds only if every engineering rule is satisfied.

Typical validation rules include:

- unique identifiers;
- unique names;
- valid hierarchy;
- valid parent references;
- valid object definitions;
- valid joint configuration;
- mandatory fields;
- engineering consistency.

Compilation stops if critical validation errors are detected.

---

## 7.11 Traceability

Every simulation object can be traced back to its engineering origin.

```text
Rhino Component
        │
        ▼
Model Database
        │
        ▼
Engineering Assembly Database
        │
        ▼
Engineering Assembly Table
        │
        ▼
Simulation Database
        │
        ▼
Simulation Object
```

This traceability is preserved throughout the remaining stages of the pipeline.

---

## 7.12 Downstream Consumers

The Simulation Database becomes the official input for all remaining GSPL programs.

| Program | Usage |
|----------|-------|
| GSPL-03 | Calculate reference frames and transformations. |
| GSPL-04 | Export STL geometry. |
| GSPL-05 | Build the CoppeliaSim model. |

No engineering workbook is required after this stage.

---

## 7.13 Engineering Independence

Once the Simulation Database has been generated, the remaining pipeline executes automatically.

No manual engineering intervention is required.

This guarantees deterministic execution and reproducibility.

---

## 7.14 Design Principles

The Simulation Database follows the following principles.

### SD-001

Every component shall have a unique identifier.

---

### SD-002

Every simulation object shall have a unique identifier.

---

### SD-003

Every engineering decision shall remain traceable.

---

### SD-004

The database shall contain no unresolved references.

---

### SD-005

Every parent-child relationship shall be validated.

---

### SD-006

The database shall be deterministic.

---

### SD-007

The database shall remain simulator independent.


## SD-008 — Engineering Information Preservation

**Engineering information shall never be lost during compilation.**

Every piece of information entered by the simulation engineer in `1_assembly_table.xlsx` shall be preserved in `2_simulation_database.json`.

The GSPL-02 Simulation Compiler may reorganize, normalize or group engineering data into a more coherent internal structure, but it shall never discard engineering information.

This guarantees:

- complete engineering traceability;
- lossless compilation;
- future extensibility;
- independence of downstream pipeline stages from the engineering workbook.



---

## 7.15 Summary

The Simulation Database represents the complete compiled description of the simulation model.

It separates engineering definition from simulation execution and provides the deterministic foundation required by all subsequent stages of the GSPL pipeline.

As the central artifact produced by the GSPL-02 Simulation Compiler, it defines every component, every simulation object and every validated engineering relationship required to build the final simulation model.


***

# 8. Reference Frame Tree (RFT)

## 8.1 Overview

The **Reference Frame Tree (RFT)** is the geometric representation of the simulation model generated by **GSPL-03 Transform Builder**.

The RFT defines the spatial organization of every simulation component by assigning a unique reference frame to each component and organizing those frames into a hierarchical tree.

Unlike the Simulation Database, which describes engineering entities and their logical relationships, the Reference Frame Tree describes the complete geometric structure of the simulation.

Once the RFT has been constructed, every local and global transformation required by the simulation can be derived automatically.

The RFT therefore becomes the geometric backbone of the GSPL.

---

## 8.2 Purpose

The purpose of the Reference Frame Tree is to transform the logical engineering hierarchy into a deterministic geometric model.

Its objectives are:

- define one reference frame for every simulation component;
- preserve the engineering hierarchy as a geometric hierarchy;
- establish the spatial relationship between components;
- calculate local transformations;
- calculate global transformations;
- provide a simulator-independent geometric representation.

No engineering decisions are introduced during this stage.

---

## 8.3 Engineering Philosophy

The GSPL intentionally separates engineering information from geometric information.

The **Simulation Database** answers the question:

> **What is the simulation model?**

The **Reference Frame Tree** answers the complementary question:

> **Where does every element exist in space?**

This separation greatly simplifies maintenance, validation and future extensions of the pipeline.

---

## 8.4 Inputs

The Reference Frame Tree is generated exclusively from the validated Simulation Database.

| Source | Purpose |
|---------|---------|
| `2_simulation_database.json` | Simulation hierarchy and component information |
| `config.json` | Pipeline configuration |

No manual intervention is required.

---

## 8.5 Outputs

GSPL-03 generates the following database.

| Output | Description |
|---------|-------------|
| `3_reference_frame_database.json` | Complete geometric representation of the simulation model. |

This database becomes the official geometric reference for the remainder of the GSPL pipeline.

---

## 8.6 General Structure

The Transform Database is organized into several logical sections.

```json
{
    "metadata": { },

    "statistics": { },

    "reference_frames": [ ],

    "kinematic_tree": { },

    "local_transforms": [ ],

    "global_transforms": [ ]
}
```

This organization separates the geometric topology of the model from the transformations derived from it.

---

## 8.7 The Reference Frame Tree

The Reference Frame Tree is a rooted hierarchical structure.

Every simulation component owns exactly one reference frame.

Every reference frame has exactly one parent, except the root frame.

```text
World
 │
 └── Base
      │
      ├── Motor
      │      │
      │      └── Encoder
      │
      ├── LiDAR
      │
      └── Camera
```

The hierarchy of the RFT is inherited directly from the validated Simulation Database.

---

## 8.8 Reference Frames

Each reference frame defines the local coordinate system of one simulation component.

Typical information includes:

- unique identifier;
- associated component;
- parent frame;
- local origin;
- local orientation;
- reference frame type.

Reference frames describe only geometry.

Simulation behaviour remains stored in the Simulation Database.

---

## 8.9 Local and Global Frames

Two coordinate systems are maintained throughout the pipeline.

### Local Reference Frame

Describes the position and orientation of a component relative to its parent.

### Global Reference Frame

Describes the position and orientation of a component relative to the root reference frame.

Global frames are never entered manually.

They are calculated recursively from the local hierarchy.

---

## 8.10 Transformation Computation

After constructing the Reference Frame Tree, GSPL-03 computes every transformation required by the simulation.

For every component, the following information is generated.

- Local position
- Local orientation
- Global position
- Global orientation
- Local transformation matrix
- Global transformation matrix

Every transformation is derived from the Reference Frame Tree.

---

## 8.11 Recursive Evaluation

The Reference Frame Tree is evaluated from the root toward the leaves.

For each node the algorithm performs the following operations.

1. Read the local reference frame.
2. Read the parent global frame.
3. Compute the global frame.
4. Store the resulting transformation.

Since every component depends exclusively on its parent, the resulting geometry is deterministic and reproducible.

---

## 8.12 Validation

Before computing transformations, GSPL-03 validates the integrity of the Reference Frame Tree.

Typical validation rules include:

- unique reference frames;
- unique root;
- valid parent references;
- disconnected branches;
- cyclic dependencies;
- duplicated identifiers.

Compilation stops if the Reference Frame Tree is invalid.

---

## 8.13 Traceability

Every geometric entity remains traceable to its engineering origin.

```text
Rhino Component
        │
        ▼
Engineering Assembly
        │
        ▼
Simulation Component
        │
        ▼
Reference Frame
        │
        ▼
Transform
        │
        ▼
Simulation Object
```

This guarantees complete geometric traceability throughout the pipeline.

---

## 8.14 Downstream Consumers

The Reference Frame Tree becomes the geometric foundation for the remaining stages.

| Program | Purpose |
|----------|---------|
| GSPL-04 STL Exporter | Position every exported mesh. |
| GSPL-05 Coppelia Builder | Construct the simulation hierarchy and place every object. |

No additional geometric calculations are required after GSPL-03.

---

## 8.15 Design Principles

### RFT-001

Every simulation component shall own exactly one reference frame.

---

### RFT-002

Reference frames shall form a rooted tree.

---

### RFT-003

Every non-root reference frame shall have exactly one parent.

---

### RFT-004

Every transformation shall be derived exclusively from the Reference Frame Tree.

---

### RFT-005

Reference frame evaluation shall be deterministic.

---

### RFT-006

The geometric representation shall remain simulator independent.

---

## 8.16 Summary

The Reference Frame Tree transforms the logical engineering model into a complete geometric representation of the simulation.

It provides a deterministic spatial description of every simulation component while preserving complete traceability with the engineering information generated during previous stages.

By separating engineering knowledge from geometric representation, the GSPL establishes a clear distinction between the definition of the simulation model and its spatial realization.

The Reference Frame Tree therefore constitutes the geometric foundation upon which all subsequent stages of the GSPL pipeline are built.

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