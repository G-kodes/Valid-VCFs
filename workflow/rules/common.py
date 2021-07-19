__author__ = "Graeme Ford"
__copyright__ = "Copyright 2021, Graeme Ford"
__email__ = "graeme.ford@tuks.co.za"
__license__ = "GNU GPLv3"

import os
import json
import re
from glob import glob
from typing import List
from snakemake.rules import Wildcards

config = dict()

with open(os.path.join("config", "config.json"), 'r') as f:
    config = json.load(f)


def DataPrepRequirements():
    """Determine data-preperation requirements based on provided data in `../resources/data` folder of workflow.
    """

    regexes = {
        "gzVCF": r"^resources[\/]data[\/](.*)(\.vcf\.gz)$",
        "VCF": r"^resources[\/]data[\/](.*)(\.vcf)$",
        "TABIX": r"^resources[\/]data[\/](.*)(\.vcf\.gz\.tbi)$",
    }
    data = dict(regexes)
    results = dict(gzVCF=list(), TABIX=list(), MV=list(), ALL=set())
    dataDir = os.path.join("resources", "data")

    for name, inputRegex in regexes.items():
        data[name] = [
            re.search(inputRegex, filename).group(1)
            for filename in glob(os.path.join(dataDir, "*"))
            if re.search(inputRegex, filename)
        ]

    results["gzVCF"] = {
        filename for filename in data["VCF"] if filename not in data["gzVCF"]
    }
    results["TABIX"] = {
        filename
        for filename in data["gzVCF"]
        if filename not in data["TABIX"] and filename not in data["VCF"]
    }
    results["MV"] = {
        filename for filename in data["TABIX"] if filename in data["gzVCF"]
    }
    results["ALL"].update(data["gzVCF"], data["VCF"], data["TABIX"])

    return results


def getSnpRef(wildcards: Wildcards) -> str:
    return next(entry["File"] for entry in config["Reference Data"] if entry["Name"] == "Reference SNPs")


def getRef(wildcards: Wildcards) -> str:
    return next(entry["File"] for entry in config["Reference Data"] if entry["Type"] == "Reference Genome")
