import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path
import tempfile
import shutil
import logging
import yaml
from typing import Dict, Any


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mapping import get_job_name

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_questionnaire_yaml(file_path: str = "src/questionnaire.yaml") -> Dict[str, Any]:
    """Load the questionnaire YAML file."""
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.error(f"Questionnaire file not found: {file_path}")
        return {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing YAML file: {e}")
        return {}

def save_questionnaire_yaml(data: Dict[str, Any], file_path: str = "src/questionnaire.yaml") -> bool:
    """Save the questionnaire YAML file."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        st.error(f"Error saving YAML file: {e}")
        return False

def insert_and_shift_keys(dictionary, new_key, new_value):
    keys_to_shift = [k for k in dictionary.keys() if k >= new_key]
    keys_to_shift.sort(reverse=True)
    for key in keys_to_shift:
        dictionary[key + 1] = dictionary.pop(key)
    dictionary[new_key] = new_value

    # Recreate dictionary with sorted keys to maintain order
    sorted_items = sorted(dictionary.items())
    dictionary.clear()
    dictionary.update(sorted_items)
    return dictionary

def mapping_editor_page():
    """Page for editing the questionnaire mappings."""
    st.title("🗂️ Questionnaire Mapping Editor")
    st.markdown("Edit the mappings used for majors, occupations, and their classifications.")
    
    # Load current data
    yaml_data = load_questionnaire_yaml()

    if not yaml_data:
        st.warning("Could not load questionnaire data. Please check if the file exists.")
        return
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["📚 Majors", "💼 Occupations"])
    
    with tab1:
        major_data = st.session_state["major"] if "major" in st.session_state else yaml_data.get("11.major", {})
        major_class = st.session_state["major_class"] if "major_class" in st.session_state else yaml_data.get("major_class", {})

        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.write("**Insert New Major**")
            new_major_code = st.number_input("Code", min_value=1, step=1, key="new_major_code")
            new_major_name = st.text_input("Name", key="new_major_name")
            new_major_class = st.text_input("Class", key="new_major_class")
            if st.button("Insert Major", key="add_major"):
                st.session_state["major"] = insert_and_shift_keys(major_data, new_major_code, new_major_name)
                st.session_state["major_class"] = insert_and_shift_keys(major_class, new_major_code, new_major_class)
                st.rerun()
        
        with col2:
            st.write("**Edit Existing Majors**")
            if major_data:
                # Create a dataframe for editing
                df_majors = pd.DataFrame({
                    'Code': list(major_data.keys()), 
                    'Major': list(major_data.values()),
                    'Class': list(major_class.values())
                })
                
                # Use data editor for bulk editing
                edited_majors = st.data_editor(
                    df_majors,
                    num_rows="dynamic",
                    use_container_width=True,
                    key="majors_editor"
                )
                
                if st.button("Update Majors", key="update_majors"):
                    # Convert back to dictionary
                    new_major_data = {}
                    new_major_class = {}
                    for _, row in edited_majors.iterrows():
                        if pd.notna(row['Code']) and pd.notna(row['Major']) and pd.notna(row['Class']):
                            new_major_data[int(row['Code'])] = str(row['Major'])
                            new_major_class[int(row['Code'])] = str(row['Class'])

                    st.session_state["major"] = new_major_data
                    st.session_state["major_class"] = new_major_class
                    st.rerun() 
  
    with tab2:
        occupation_data = yaml_data.get("19.occupation", {})
        occupation_data = st.session_state["occupation"] if "occupation" in st.session_state else yaml_data.get("19.occupation", {})
        occupation_class = st.session_state["occupation_class"] if "occupation_class" in st.session_state else yaml_data.get("occupation_class", {})

        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.write("**Add New Occupation**")
            new_occ_code = st.number_input("Code", min_value=1, step=1, key="new_occ_code")
            new_occ_name = st.text_input("Name", key="new_occ_name")
            new_occ_class = st.text_input("Class", key="new_occ_class")
            if st.button("Insert Occupation", key="add_occ"):
                st.session_state["occupation"] = insert_and_shift_keys(occupation_data, new_occ_code, new_occ_name)
                st.session_state["occupation_class"] = insert_and_shift_keys(occupation_class, new_occ_code, new_occ_class)
                st.rerun()

        with col2:
            st.write("**Edit Existing Occupations**")
            if occupation_data:
                # Create a dataframe for editing
                df_occupations = pd.DataFrame({
                    'Code': list(occupation_data.keys()), 
                    'occupation': list(occupation_data.values()),
                    'Class': list(occupation_class.values())
                })
                
                # Use data editor for bulk editing
                edited_occupations = st.data_editor(
                    df_occupations,
                    num_rows="dynamic",
                    use_container_width=True,
                    key="occupations_editor"
                )
                
                if st.button("Update occupations", key="update_occupations"):
                    # Convert back to dictionary
                    new_occ_data = {}
                    new_occ_class = {}
                    for _, row in edited_occupations.iterrows():
                        if pd.notna(row['Code']) and pd.notna(row['occupation']) and pd.notna(row['Class']):
                            new_occ_data[int(row['Code'])] = str(row['occupation'])
                            new_occ_class[int(row['Code'])] = str(row['Class'])

                    st.session_state["occupation"] = new_occ_data
                    st.session_state["occupation_class"] = new_occ_class
                    st.rerun() 
    
   