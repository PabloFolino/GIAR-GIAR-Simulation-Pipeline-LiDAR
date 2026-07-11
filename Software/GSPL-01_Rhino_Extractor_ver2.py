#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
------------------------------------------------------------
GSPL-01_Rhino_Extractor.py

GIAR Simulation Pipeline for LiDAR

Version : 0.2

Author:
    Ing. Pablo Daniel Folino

Description:
    Opens a Rhino (.3dm) model and inspects its contents.

------------------------------------------------------------
"""

from pathlib import Path
import json
import logging
import sys
import rhino3dm
import uuid


CONFIG_FILE = "config.json"


# ==========================================================
# Rhino Extractor
# ==========================================================

class RhinoExtractor:

    def __init__(self):

        self.cfg = None
        self.logger = None
        self.model = None


    # ------------------------------------------------------
    # Configuration
    # ------------------------------------------------------
    def load_config(self):

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)


    # ------------------------------------------------------
    # Logger
    # ------------------------------------------------------
    def configure_logger(self):

        log_dir = Path(self.cfg["paths"]["log_directory"])

        log_dir.mkdir(parents=True, exist_ok=True)

        logfile = log_dir / "GSPL-01.log"

        logging.basicConfig(

            level=logging.INFO,

            format="%(asctime)s | %(levelname)-8s | %(message)s",

            handlers=[
                logging.FileHandler(logfile, mode="w"),
                logging.StreamHandler(sys.stdout)
            ]
        )

        self.logger = logging.getLogger("GSPL")


    # ------------------------------------------------------
    # Banner
    # ------------------------------------------------------
    def print_banner(self):

        self.logger.info("")
        self.logger.info("====================================================")
        self.logger.info(" GSPL-01 Rhino Extractor")
        self.logger.info(" Version : 0.2")
        self.logger.info("====================================================")
        self.logger.info("")

        self.logger.info("Project : %s",
                         self.cfg["project"]["name"])

        self.logger.info("Version : %s",
                         self.cfg["project"]["version"])

        self.logger.info("")


    # ------------------------------------------------------
    # Verify project
    # ------------------------------------------------------
    def verify_project(self):

        for directory in [

            self.cfg["paths"]["input_directory"],
            self.cfg["paths"]["stl_directory"],
            self.cfg["paths"]["database_directory"],
            self.cfg["paths"]["output_directory"]

        ]:

            if Path(directory).exists():

                self.logger.info("[ OK ] %s", directory)

            else:

                self.logger.error("[ERROR] %s", directory)


    # ------------------------------------------------------
    # Open Rhino Model
    # ------------------------------------------------------
    def open_model(self):

        filename = (

            Path(self.cfg["paths"]["input_directory"])

            /

            self.cfg["files"]["input_file_3dm"]

        )

        self.logger.info("")
        self.logger.info("Opening Rhino model...")
        self.logger.info("%s", filename)

        self.model = rhino3dm.File3dm.Read(str(filename))

        if self.model is None:

            raise RuntimeError("Unable to open Rhino file.")

        self.logger.info("[ OK ] Rhino model loaded.")


    # ------------------------------------------------------
    # Model information
    # ------------------------------------------------------

    def print_model_information(self):

        self.logger.info("")
        self.logger.info("----------------------------------------")
        self.logger.info("Model Information")
        self.logger.info("----------------------------------------")

        self.logger.info("File Version : %s",
                         self.model.Settings.ModelUnitSystem)

        self.logger.info("Layers       : %d",
                         len(self.model.Layers))

        self.logger.info("Objects      : %d",
                         len(self.model.Objects))

        self.logger.info("Groups       : %d",
                         len(self.model.Groups))


    # ------------------------------------------------------
    # Inspect Objects
    # ------------------------------------------------------
    def inspect_objects(self):

        self.logger.info("")
        self.logger.info("----------------------------------------")
        self.logger.info("Objects")
        self.logger.info("----------------------------------------")

        for i, obj in enumerate(self.model.Objects, start=1):

            att = obj.Attributes

            geo = obj.Geometry

            self.logger.info("")
            self.logger.info("[%04d]", i)

            self.logger.info("Name     : %s", att.Name)

            self.logger.info("GUID     : %s", att.Id)

            self.logger.info("Layer Id : %d", att.LayerIndex)

            self.logger.info("Geometry : %s",
                             geo.ObjectType)

    # ------------------------------------------------------
    # Geometry Audit
    # ------------------------------------------------------
    def audit_geometry(self):

        self.logger.info("")
        self.logger.info("========================================================")
        self.logger.info(" GEOMETRY AUDIT")
        self.logger.info("========================================================")

        errors = 0

        for obj in self.model.Objects:

            att = obj.Attributes
            geo = obj.Geometry

            name = att.Name if att.Name else "<UNNAMED>"

            # Obtener nombre de la Layer
            try:
                layer = self.model.Layers[att.LayerIndex].Name
            except:
                layer = "<UNKNOWN>"

            guid = att.Id

            # --------------------------------------------------
            # BREP
            # --------------------------------------------------

            if isinstance(geo, rhino3dm.Brep):

                if geo.IsSolid:

                    continue

                errors += 1

                self.logger.error("")
                self.logger.error("ERROR %03d", errors)
                self.logger.error("--------------------------------------------")
                self.logger.error("Component : %s", name)
                self.logger.error("Layer     : %s", layer)
                self.logger.error("GUID      : %s", guid)
                self.logger.error("Geometry  : Open Brep")
                self.logger.error("")
                self.logger.error("Action:")
                self.logger.error("    Convert this Brep into a CLOSED solid.")
                self.logger.error("--------------------------------------------")

                continue

            # --------------------------------------------------
            # EXTRUSION
            # --------------------------------------------------

            if isinstance(geo, rhino3dm.Extrusion):

                if geo.IsSolid:

                    continue

                errors += 1

                self.logger.error("")
                self.logger.error("ERROR %03d", errors)
                self.logger.error("--------------------------------------------")
                self.logger.error("Component : %s", name)
                self.logger.error("Layer     : %s", layer)
                self.logger.error("GUID      : %s", guid)
                self.logger.error("Geometry  : Open Extrusion")
                self.logger.error("")
                self.logger.error("Action:")
                self.logger.error("    Close the extrusion.")
                self.logger.error("--------------------------------------------")

                continue

            # --------------------------------------------------
            # INVALID GEOMETRY
            # --------------------------------------------------

            errors += 1

            self.logger.error("")
            self.logger.error("ERROR %03d", errors)
            self.logger.error("--------------------------------------------")
            self.logger.error("Component : %s", name)
            self.logger.error("Layer     : %s", layer)
            self.logger.error("GUID      : %s", guid)
            self.logger.error("Geometry  : %s", geo.ObjectType)
            self.logger.error("")
            self.logger.error("Action:")
            self.logger.error("    Delete or convert this object into a closed solid.")
            self.logger.error("--------------------------------------------")

        self.logger.info("")
        self.logger.info("========================================================")

        if errors == 0:

            self.logger.info("Geometry Audit : PASSED")

        else:

            self.logger.error("Geometry Audit : FAILED")
            self.logger.error("Total Errors   : %d", errors)

            raise RuntimeError(
                f"Geometry Audit FAILED ({errors} errors)"
            )

        self.logger.info("========================================================")

    # ------------------------------------------------------
    # Initialize Database
    # ------------------------------------------------------
    def initialize_database(self):

        self.database = {

            "project": {

                "name": self.cfg["project"]["name"],
                "version": self.cfg["project"]["version"]

            },

            "statistics": {

                "components": 0,
                "entities": 0

            },

            "components": []

        }
    
    # ------------------------------------------------------
    # Build Component Database
    # ------------------------------------------------------
    def build_database(self):

        self.logger.info("")
        self.logger.info("========================================================")
        self.logger.info(" Building Component Database")
        self.logger.info("========================================================")

        self.initialize_database()

        components = {}

        for index, obj in enumerate(self.model.Objects):

            att = obj.Attributes
            geo = obj.Geometry

            # --------------------------------------------------
            # Component Name
            # --------------------------------------------------

            name = att.Name.strip() if att.Name else "<UNNAMED>"

            # --------------------------------------------------
            # Layer
            # --------------------------------------------------

            try:
                layer = self.model.Layers[att.LayerIndex].Name
            except Exception:
                layer = "<UNKNOWN>"

            # --------------------------------------------------
            # Geometry Type
            # --------------------------------------------------

            geometry = str(geo.ObjectType).replace("ObjectType.", "")

            # --------------------------------------------------
            # Create Component
            # --------------------------------------------------

            if name not in components:

                component = {

                    "id": len(components) + 1,

                    "uuid": str(uuid.uuid4()),

                    "name": name,

                    "type": "component",

                    "layer": layer,

                    "parent": None,

                    "children": [],

                    "stl": None,

                    "transform": None,

                    "bounding_box": None,

                    "center": None,

                    "mass": None,

                    "material": None,

                    "properties": {},

                    "status": {

                        "geometry_audit": "PASSED",
                        "hierarchy_audit": "PENDING",
                        "stl_export": "PENDING",
                        "simulation": "PENDING"

                    },

                    "entities": []

                }

                components[name] = component

            # --------------------------------------------------
            # Add Entity
            # --------------------------------------------------

            entity = {

                "index": index,

                "guid": str(att.Id),

                "geometry": geometry

            }

            components[name]["entities"].append(entity)

        # ------------------------------------------------------
        # Sort Components
        # ------------------------------------------------------

        component_list = sorted(
            components.values(),
            key=lambda c: c["name"].lower()
        )

        # ------------------------------------------------------
        # Reassign IDs after sorting
        # ------------------------------------------------------

        for new_id, component in enumerate(component_list, start=1):

            component["id"] = new_id

        # ------------------------------------------------------
        # Statistics
        # ------------------------------------------------------

        self.database["statistics"]["components"] = len(component_list)

        self.database["statistics"]["entities"] = len(self.model.Objects)

        self.database["components"] = component_list

        # ------------------------------------------------------
        # Log
        # ------------------------------------------------------

        self.logger.info("Components : %d", len(component_list))
        self.logger.info("Entities   : %d", len(self.model.Objects))

        self.logger.info("")
        self.logger.info("Component List")
        self.logger.info("--------------------------------------------------------")

        for component in component_list:

            self.logger.info(
                "[%03d] %-35s (%3d entities)",
                component["id"],
                component["name"],
                len(component["entities"])
            )

        self.logger.info("--------------------------------------------------------")

    # ------------------------------------------------------
    # Save Database
    # ------------------------------------------------------
    def save_database(self):

        self.logger.info("")
        self.logger.info("========================================================")
        self.logger.info(" Saving Component Database")
        self.logger.info("========================================================")

        # --------------------------------------------------
        # Output directory
        # --------------------------------------------------

        database_dir = Path(self.cfg["paths"]["database_directory"])

        database_dir.mkdir(parents=True, exist_ok=True)

        # --------------------------------------------------
        # Output file
        # --------------------------------------------------

        output_file = (
            database_dir /
            self.cfg["files"]["model_database"]
        )

        # --------------------------------------------------
        # Save JSON
        # --------------------------------------------------

        try:

            with open(output_file, "w", encoding="utf-8") as f:

                json.dump(
                    self.database,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            self.logger.info("")
            self.logger.info("[ OK ] Database successfully saved.")
            self.logger.info("File       : %s", output_file)
            self.logger.info("Components : %d",
                            self.database["statistics"]["components"])
            self.logger.info("Entities   : %d",
                            self.database["statistics"]["entities"])

        except Exception as e:

            self.logger.error("")
            self.logger.error("[ERROR] Unable to save database.")
            self.logger.error(str(e))
            raise

        self.logger.info("========================================================")

    # ------------------------------------------------------
    # Generate Assembly Template
    # ------------------------------------------------------
    def generate_assembly_template(self):

        self.logger.info("")
        self.logger.info("========================================================")
        self.logger.info(" Generating Assembly Template")
        self.logger.info("========================================================")

        # --------------------------------------------------
        # Create Assembly Structure
        # --------------------------------------------------

        assembly = {

            "format_version": "1.0",

            "generated_by": "GSPL-01_Rhino_Extractor",

            "generator_version": self.cfg["project"]["version"],

            "project": self.cfg["project"]["name"],

            # Root component (defined later by the engineer)
            "root": None,

            "components": []

        }

        # --------------------------------------------------
        # Process Components
        # --------------------------------------------------

        for component in self.database["components"]:

            xmin = ymin = zmin = float("inf")
            xmax = ymax = zmax = float("-inf")

            valid_bbox = False

            # ----------------------------------------------
            # Compute Component Bounding Box
            # ----------------------------------------------

            for entity in component["entities"]:

                obj = self.model.Objects[entity["index"]]

                bbox = obj.Geometry.GetBoundingBox()

                if not bbox.IsValid:

                    self.logger.warning(
                        "Invalid BoundingBox in component '%s'",
                        component["name"]
                    )

                    continue

                valid_bbox = True

                xmin = min(xmin, bbox.Min.X)
                ymin = min(ymin, bbox.Min.Y)
                zmin = min(zmin, bbox.Min.Z)

                xmax = max(xmax, bbox.Max.X)
                ymax = max(ymax, bbox.Max.Y)
                zmax = max(zmax, bbox.Max.Z)

            # ----------------------------------------------
            # Default values if BoundingBox failed
            # ----------------------------------------------

            if not valid_bbox:

                xmin = ymin = zmin = 0.0
                xmax = ymax = zmax = 0.0

            # ----------------------------------------------
            # Bounding Box Center
            # ----------------------------------------------

            center = [

                round((xmin + xmax) / 2.0, 6),
                round((ymin + ymax) / 2.0, 6),
                round((zmin + zmax) / 2.0, 6)

            ]

            # ----------------------------------------------
            # Bounding Box Information
            # ----------------------------------------------

            bounding_box = {

                "min": [

                    round(xmin, 6),
                    round(ymin, 6),
                    round(zmin, 6)

                ],

                "max": [

                    round(xmax, 6),
                    round(ymax, 6),
                    round(zmax, 6)

                ],

                "center": center,

                "size": [

                    round(xmax - xmin, 6),
                    round(ymax - ymin, 6),
                    round(zmax - zmin, 6)

                ]

            }

            # ----------------------------------------------
            # Default Scene Object (Shape)
            # ----------------------------------------------

            default_shape = {

                "type": "shape",

                "name": component["name"],

                "position": [

                    0.0,
                    0.0,
                    0.0

                ],

                "orientation": [

                    0.0,
                    0.0,
                    0.0

                ],

                "properties": {

                    "dynamic": False,

                    "respondable": False,

                    "visible": True

                }

            }

            # ----------------------------------------------
            # Assembly Component
            # ----------------------------------------------

            assembly["components"].append({

                "id": component["id"],

                "name": component["name"],

                "description": "",

                "notes": "",

                "enabled": True,

                "parent": None,

                "frame": {

                    "position": center,

                    "orientation": [

                        0.0,
                        0.0,
                        0.0

                    ]

                },

                "bounding_box": bounding_box,

                "models": [

                    "visual"

                ],

                "objects": [

                    default_shape

                ]

            })

        # --------------------------------------------------
        # Sort Components by ID
        # --------------------------------------------------

        assembly["components"] = sorted(

            assembly["components"],

            key=lambda c: c["id"]

        )

        # --------------------------------------------------
        # Output File
        # --------------------------------------------------

        output_file = (

            Path(self.cfg["paths"]["database_directory"])

            /

            self.cfg["files"]["assembly"]

        )

        # --------------------------------------------------
        # Save JSON
        # --------------------------------------------------

        try:

            with open(output_file, "w", encoding="utf-8") as f:

                json.dump(

                    assembly,

                    f,

                    indent=4,

                    ensure_ascii=False

                )

            self.logger.info("")
            self.logger.info("Assembly template successfully saved.")
            self.logger.info("File       : %s", output_file)
            self.logger.info("Components : %d", len(assembly["components"]))

        except Exception as e:

            self.logger.error("")
            self.logger.error("Unable to save assembly template.")
            self.logger.error(str(e))
            raise

        self.logger.info("========================================================")

    # ------------------------------------------------------
    # Run
    # ------------------------------------------------------
    def run(self):

        self.load_config()
        self.configure_logger()
        self.print_banner()
        self.verify_project()
        self.open_model()
        self.audit_geometry()
        self.print_model_information()
        self.inspect_objects()
        self.build_database()
        self.save_database()
        self.generate_assembly_template()
 
        self.logger.info("")
        self.logger.info("Finished.")



# ==========================================================
# Main
# ==========================================================

def main():

    extractor = RhinoExtractor()

    extractor.run()


if __name__ == "__main__":

    main()