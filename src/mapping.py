# job_mapping.py
import numpy as np
import yaml

with open("src/questionnaire.yaml", "r") as file:
    data = yaml.safe_load(file)

major_name_map = data["11.major"]
major_class_map = data["major_class"]
job_names = data["19.occupation"]
job_class_map = data["occupation_class"]

# === Functions ===

def get_job_name(code):
    name = job_names.get(code, np.nan)
    return name

def get_job_class(code):
    return job_class_map.get(code, np.nan)

def get_major_name(code):
    """Returns the job name for a given code."""
    return major_name_map.get(code, np.nan)

def get_major_class(code):
    """Returns the job class for a given code."""
    return major_class_map.get(code, np.nan)

