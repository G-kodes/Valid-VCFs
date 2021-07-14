import re
import os
import glob


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
        for filename in glob.glob(os.path.join(dataDir, "*"))
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
results["MV"] = {filename for filename in data["TABIX"] if filename in data["gzVCF"]}
results['ALL'].update(data['gzVCF'], data['VCF'], data['TABIX'])

return results
