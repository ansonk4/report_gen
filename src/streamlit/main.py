import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path
import tempfile
import shutil
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from doc import DocumentGenerator, Config
from questionnaire_editor import mapping_editor_page
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def report_generator_page():
    st.title("📊 School Survey Report Generator")
    st.markdown("Generate comprehensive school survey reports with automatic analysis and visualizations.")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration Settings")
    
    # Basic settings
    st.sidebar.subheader("Basic Information")
    school_name = st.sidebar.text_input("School Name", value="High School")
    school_id = st.sidebar.number_input("School ID", value=12, min_value=1, step=1)
    year = st.sidebar.number_input("Survey Year", value=2025, min_value=2020, step=1)
    
    with st.sidebar.expander("LLM Settings", expanded=False):
        # Use radio buttons to allow only one choice
        llm_choice = st.sidebar.radio(
            "Choose LLM Provider",
            ("Gemini (Require VPN)", "OpenRouter", "Disabled")
        )

        # Show API key input depending on choice
        GEMINI_API_KEY = None
        OPENROUTER_KEY = None
        model_name = None

        if llm_choice == "Gemini (Require VPN)":
            GEMINI_API_KEY = st.sidebar.text_input("GEMINI_API_KEY")
            model_name = st.sidebar.text_input("Model", value="gemini-2.5-flash")
            if GEMINI_API_KEY:
                os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
        elif llm_choice == "OpenRouter":
            OPENROUTER_KEY = st.sidebar.text_input("OPENROUTER_API_KEY")
            model_name = st.sidebar.text_input("Model", value="mistralai/mistral-small-3.2-24b-instruct:free")
            if OPENROUTER_KEY:
                os.environ["OPENROUTER_KEY"] = OPENROUTER_KEY


    # File paths
    with st.sidebar.expander("File and Output Paths", expanded=False):
        template_path = st.text_input("Template Path", value="doc/template.docx")
        output_path = st.text_input("Output Path", value=f"output/report_{school_id}_{school_name}.docx")
        image_dir = st.text_input("Image Directory", value="img")
        general_data_path = None

    # File upload section
    st.header("📁 File Upload")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Template File")
        template_file = st.file_uploader("Upload Word Template (.docx) (Optional)", type=['docx'])
        if template_file:
            st.success("Template file uploaded successfully!")
    
    with col2:
        st.subheader("Data File")
        data_file = st.file_uploader("Upload Data File (.xlsx)", type=['xlsx'])
        if data_file:
            st.success("Data file uploaded successfully!")


# Required columns for the Excel data file
REQUIRED_EXCEL_COLUMNS = [
    "school_id", "id", "banding", "gender", "elective", "chinese_reuslt", "english_result", "math_result",
    "parent_education", "uni", "asso", "diploma", "high_dip", "work", "working_hoilday", "other", "future_plan",
    "HK", "China", "Asia", "US/EU/AUS", "working_location",
    "personal_interests_A", "institute_A", "tuition_A", "scholarship_A", "career_prospect_A",
    "peers_and_teacher_A", "family_A", "salary_A", "DSE_result_A", "high_school_electives_A",
    "target_major1", "target_major2", "target_major3", "elective_major_relation",
    "dislike_major1", "dislike_major2", "dislike_major3",
    "stem_participation", "leadership", "teamwork", "creativity", "sci_knowledge", "problem_solving",
    "personal_ability_B", "personal_interest_B", "sense_of_achievement_B", "family_B",
    "interpresonal_relationship_B", "job_nature_B", "remote_work_B", "worload_B", "working_environment_B",
    "salary_and_benefit_B", "promotion_opportunites_B", "career_prospect_B", "social_contribution_B", "social_status_B",
    "major_career_relation", "target_occupation1", "target_occupation2", "target_occupation3",
    "dislike_occupation1", "dislike_occupation2", "dislike_occupation3",
    "gba_understanding",
    "stress_lv", "stress_scource", "family_expectations", "comparison", "tight_schedule", "test_scores",
    "relationships", "prospect", "expectation", "long_term_solitude", "covid_19", "unstable_class", "transfer_exam",
    "endure_lv", "exercise", "family_communication", "friends_communication", "social_workers", "restructuring_ttb",
    "video_games", "sleep", "music", "no_idea"
]

@st.cache_data(show_spinner="Checking Excel format...")
def validate_excel_and_get_path(uploaded_file_bytes):
    """
    Validates the uploaded Excel file's columns and saves it to a temporary path.
    Returns the temporary path if valid, otherwise None.
    """
    if not uploaded_file_bytes:
        return None, False

    # Create a temporary file to hold the uploaded content
    temp_fd, temp_path = tempfile.mkstemp(suffix=".xlsx")
    with os.fdopen(temp_fd, "wb") as tmp:
        tmp.write(uploaded_file_bytes)

    try:
        df_col = set(pd.read_excel(temp_path, header=2).columns)
        missing_col = [col for col in REQUIRED_EXCEL_COLUMNS if col not in df_col]

        if missing_col:
            st.warning("The following required columns are missing:")
            st.write(missing_col)
            os.remove(temp_path) # Clean up the temp file if validation fails
            return None, False
        else:
            return temp_path, True
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None, False

def report_generator_page():
    st.title("📊 School Survey Report Generator")
    st.markdown("Generate comprehensive school survey reports with automatic analysis and visualizations.")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration Settings")
    
    # Basic settings
    st.sidebar.subheader("Basic Information")
    school_name = st.sidebar.text_input("School Name", value="High School")
    school_id = st.sidebar.number_input("School ID", value=12, min_value=1, step=1)
    current_year = datetime.datetime.now().year
    year = st.sidebar.number_input("Survey Year", value=current_year, min_value=2020, step=1)
    
    with st.sidebar.expander("LLM Settings", expanded=False):
        # Use radio buttons to allow only one choice
        llm_choice = st.sidebar.radio(
            "Choose LLM Provider",
            ("Gemini (Require VPN)", "OpenRouter", "Disabled")
        )

        # Show API key input depending on choice
        GEMINI_API_KEY = None
        OPENROUTER_KEY = None
        model_name = None

        if llm_choice == "Gemini (Require VPN)":
            GEMINI_API_KEY = st.sidebar.text_input("GEMINI_API_KEY")
            model_name = st.sidebar.text_input("Model", value="gemini-2.5-flash")
            if GEMINI_API_KEY:
                os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
        elif llm_choice == "OpenRouter":
            OPENROUTER_KEY = st.sidebar.text_input("OPENROUTER_API_KEY")
            model_name = st.sidebar.text_input("Model", value="mistralai/mistral-small-3.2-24b-instruct:free")
            if OPENROUTER_KEY:
                os.environ["OPENROUTER_KEY"] = OPENROUTER_KEY


    # File paths
    with st.sidebar.expander("File and Output Paths", expanded=False):
        template_path = st.text_input("Template Path", value="doc/template.docx")
        output_path = st.text_input("Output Path", value=f"output/report_{school_id}_{school_name}.docx")
        image_dir = st.text_input("Image Directory", value="img")
        general_data_path = None # This line can be removed as it's not used

    # File upload section
    st.header("📁 File Upload")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Template File")
        template_file = st.file_uploader("Upload Word Template (.docx) (Optional)", type=['docx'])
        if template_file:
            st.success("Template file uploaded successfully!")
    
    with col2:
        st.subheader("Data File")
        data_file = st.file_uploader("Upload Data File (.xlsx)", type=['xlsx', 'xls'], key="data_file_uploader")

    temp_data_path_for_report = None
    excel_format_ok = False

    if data_file:
        if "data_file_bytes" not in st.session_state or st.session_state.data_file_bytes != data_file.getvalue():
            st.session_state.data_file_bytes = data_file.getvalue()
            st.session_state.temp_data_path_validated, st.session_state.excel_columns_validated_ok = \
                validate_excel_and_get_path(st.session_state.data_file_bytes)
        
        temp_data_path_for_report = st.session_state.get("temp_data_path_validated")
        excel_format_ok = st.session_state.get("excel_columns_validated_ok", False)
    else:
        if "data_file_bytes" in st.session_state:
            del st.session_state.data_file_bytes
        if "temp_data_path_validated" in st.session_state and st.session_state.temp_data_path_validated:
            if os.path.exists(st.session_state.temp_data_path_validated):
                os.remove(st.session_state.temp_data_path_validated)
            del st.session_state.temp_data_path_validated
        if "excel_columns_validated_ok" in st.session_state:
            del st.session_state.excel_columns_validated_ok

    if excel_format_ok and temp_data_path_for_report and os.path.exists(temp_data_path_for_report):
        # Generate report button
        st.header("🚀 Generate Report")
        
        if st.button("Generate Report", use_container_width=True):
            with st.spinner("Generating report... This may take a few minutes."):
                try:
                    # Create temporary directory for template and final output if needed
                    # The temp_data_path_for_report is already validated and persisted by the cached function.
                    
                    # Ensure output directory exists
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    # Ensure image directory exists
                    os.makedirs(image_dir, exist_ok=True)
                    
                    # Handle template file if uploaded
                    current_template_path = template_path
                    if template_file:
                        with tempfile.TemporaryDirectory() as temp_dir_template:
                            temp_uploaded_template_path = os.path.join(temp_dir_template, "template.docx")
                            with open(temp_uploaded_template_path, "wb") as f:
                                f.write(template_file.getvalue())
                            current_template_path = temp_uploaded_template_path

                    # Create configuration
                    config = Config(
                        use_gemini= (llm_choice == "Gemini (Require VPN)"),
                        use_llm = (llm_choice != "Disabled"),
                        model_name = model_name,
                        template_path=current_template_path,
                        output_path=output_path,
                        general_data_path=temp_data_path_for_report,
                        image_dir=image_dir,
                        year=year,
                        school_name=school_name,
                        school_id=school_id
                    )
                    
                    # Generate report
                    generator = DocumentGenerator(config)
                    generator.generate_report()
                    
                    st.success("✅ Report generated successfully!")
                    
                    # Provide download link
                    if os.path.exists(output_path):
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="📥 Download Report",
                                data=file.read(),
                                file_name=f"{school_name}_Survey_Report_{year}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
                    
                    # Show generated images
                    st.subheader("📊 Generated Visualizations")
                    image_files = [
                        "major_factors.png",
                        "occpuation_factors.png",
                        "stem_major.png",
                        "stem_job.png",
                        "stress_sources.png",
                        "stress_level_distribution.png",
                        "endure_level_distribution.png",
                        "stress_method.png"
                    ]
                    
                    cols = st.columns(2)
                    for i, img_file in enumerate(image_files):
                        img_path = os.path.join(image_dir, img_file)
                        if os.path.exists(img_path):
                            with cols[i % 2]:
                                st.image(img_path, caption=img_file.replace("_", " ").title(), use_container_width=True)
                
                except Exception as e:
                    st.error(f"❌ Error generating report: {str(e)}")
                    logger.error(f"Report generation failed: {e}")
                    
                    # Show detailed error in expander
                    with st.expander("Show Error Details"):
                        st.code(str(e))
    elif data_file: # Only show this warning if a file was uploaded but not valid
        st.warning("Please correct the Excel file format before generating the report.")
    
    # Help section
    st.header("❓ Help & Information")
    
    with st.expander("How to Use This App"):
        st.markdown("""
        1. **Configure Settings**: Enter your school information and file paths in the sidebar
        2. **Upload Files**: Upload your Word template and Excel data files
        3. **Validate**: Check that all required files are available
        4. **Generate**: Click the "Generate Report" button to create your report
        5. **Download**: Download the generated report and view the visualizations
        """)
    
    with st.expander("File Requirements"):
        st.markdown("""
        - **Template File**: Word document (.docx) with placeholders for data
        - **Data File**: Excel file (.xlsx) containing survey data
        - **School Data File**: Optional Excel file with school-specific data
        """)
    
    with st.expander("Troubleshooting"):
        st.markdown("""
        - Ensure all file paths are correct and files exist
        - Check that the image directory exists and is writable
        - Verify that the output directory exists or can be created
        - Make sure data files contain the expected columns and format
        """)

def main():
    """Main function with page navigation."""
    st.set_page_config(
        page_title="School Survey Report System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["📊 Report Generator", "🗂️ Questionnaire Editor"]
    )
    
    # Route to appropriate page
    if page == "📊 Report Generator":
        report_generator_page()
    elif page == "🗂️ Questionnaire Editor":
        mapping_editor_page()

if __name__ == "__main__":
    main()

