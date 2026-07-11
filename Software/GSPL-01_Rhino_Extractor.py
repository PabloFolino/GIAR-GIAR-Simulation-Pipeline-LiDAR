#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
------------------------------------------------------------
GSPL-01_Rhino_Extractor.py

GIAR Simulation Pipeline for LiDAR

Version : 0.1
Author  : Ing. Pablo Daniel Folino

Description:
    First stage of the GSPL pipeline.

    - Load configuration.
    - Verify project structure.
    - Verify Rhino model.
    - Initialize logging.

------------------------------------------------------------
"""

from pathlib import Path
import json
import logging
import sys
import rhino3dm

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------
CONFIG_FILE = "config.json"

# ----------------------------------------------------------
# Load configuration
# ----------------------------------------------------------
def load_config():

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------------------------------------
# Configure logger
# ----------------------------------------------------------
def configure_logger(log_directory):

    Path(log_directory).mkdir(parents=True, exist_ok=True)

    logfile = Path(log_directory) / "GSPL-01.log"

    logging.basicConfig(

        level=logging.INFO,

        format="%(asctime)s | %(levelname)-8s | %(message)s",

        handlers=[
            logging.FileHandler(logfile, mode="w"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger("GSPL")

# ----------------------------------------------------------
# Verify folders
# ----------------------------------------------------------
def verify_directory(path):

    p = Path(path)

    if p.exists():
        logger.info(f"[OK] Directory : {p}")
        return True

    logger.error(f"[ERROR] Directory not found : {p}")
    return False

# ----------------------------------------------------------
# Verify Rhino file
# ----------------------------------------------------------
def verify_input_file(cfg):

    file = (
        Path(cfg["paths"]["input_directory"]) /
        cfg["paths"]["input_file_3dm"]
    )

    if file.exists():

        logger.info(f"[OK] Rhino model : {file}")

        return True

    logger.error(f"[ERROR] Rhino model not found : {file}")

    return False

# ----------------------------------------------------------
# open_model()
#        Esta función será la responsable de abrir el .3dm.
# ----------------------------------------------------------
def open_model(self):

    model_file = (
        Path(self.cfg["paths"]["input_directory"]) /
        self.cfg["paths"]["input_file_3dm"]
    )

    logger.info("Opening Rhino model...")

    self.model = rhino3dm.File3dm.Read(str(model_file))

    if self.model is None:
        raise RuntimeError("Unable to open Rhino model.")

    logger.info("Model successfully loaded.")

# ----------------------------------------------------------
#print_model_information()
#           Obtiene información general:
#           versión Rhino
#           unidades
#           número de objetos
#           número de capas
#           grupos
#           vistas
# ----------------------------------------------------------


# ----------------------------------------------------------
# inspect_objects()
#           Recorre todos los objetos y para cada uno imprime:
#                   * Nombre
#                   * GUID
#                   * Layer
#                   * Tipo de geometría
#                   * Visible
#                   * Color (si existe)
# ----------------------------------------------------------

# ----------------------------------------------------------
# Main
# ----------------------------------------------------------
def main():

    global logger

    cfg = load_config()

    logger = configure_logger(cfg["paths"]["log_directory"])

    logger.info("")
    logger.info("===========================================")
    logger.info(" GSPL-01 Rhino Extractor")
    logger.info("===========================================")
    logger.info("")

    logger.info("Project : %s", cfg["project"]["name"])
    logger.info("Version : %s", cfg["project"]["version"])
    logger.info("")

    verify_directory(cfg["paths"]["input_directory"])
    verify_directory(cfg["paths"]["stl_directory"])
    verify_directory(cfg["paths"]["database_directory"])
    verify_directory(cfg["paths"]["output_directory"])

    verify_input_file(cfg)

    logger.info("")
    logger.info("Finished.")


# ----------------------------------------------------------

if __name__ == "__main__":

    main()