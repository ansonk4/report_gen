# job_mapping.py
import numpy as np
import yaml
import streamlit as st

with open("src/questionnaire.yaml", "r") as file:
    data = yaml.safe_load(file)

def get_job_name(code):
    job_names = st.session_state.get("occupation", data["19.occupation"])
    return job_names.get(code, np.nan)

def get_job_class(code):
    job_class_map= st.session_state.get("occupation_class", data["occupation_class"])
    return job_class_map.get(code, np.nan)

def get_major_name(code):
    """Returns the job name for a given code."""
    major_name_map = st.session_state.get("major", data["11.major"])
    return major_name_map.get(code, np.nan)

def get_major_class(code):
    """Returns the job class for a given code."""
    major_class_map = st.session_state.get("major_class", data["major_class"])
    return major_class_map.get(code, np.nan)

