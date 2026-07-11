#!/usr/bin/env python3
"""
GIAR Low Cost 3D LiDAR
CoppeliaSim Builder

Author:
Ing. Pablo Daniel Folino

"""

from logger import Logger
from importer import MeshImporter
from hierarchy import HierarchyBuilder
from joints import JointBuilder
from sensors import SensorBuilder
from dynamics import DynamicsBuilder

import json


def load_config(filename="config.json"):

    with open(filename, "r", encoding="utf8") as f:
        return json.load(f)


def main():

    logger = Logger()

    logger.info("")
    logger.info("===================================")
    logger.info(" GIAR Low Cost 3D LiDAR Builder")
    logger.info("===================================")

    cfg = load_config()

    importer = MeshImporter(cfg, logger)
    hierarchy = HierarchyBuilder(cfg, logger)
    joints = JointBuilder(cfg, logger)
    sensors = SensorBuilder(cfg, logger)
    dynamics = DynamicsBuilder(cfg, logger)

    logger.info("Connecting to CoppeliaSim...")

    importer.connect()

    logger.info("Creating scene...")

    importer.create_scene()

    logger.info("Importing meshes...")

    importer.import_meshes()

    logger.info("Building hierarchy...")

    hierarchy.build(importer)

    logger.info("Creating joints...")

    joints.build(importer)

    logger.info("Creating sensors...")

    sensors.build(importer)

    logger.info("Configuring dynamics...")

    dynamics.build(importer)

    logger.info("Saving model...")

    importer.save_model()

    importer.disconnect()

    logger.info("")
    logger.info("Finished successfully.")


if __name__ == "__main__":

    main()