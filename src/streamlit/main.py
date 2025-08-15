import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path
import tempfile
import shutil
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from document_generator import DocumentGenerator, Config
from questionnaire_editor import mapping_editor_page
from data_converter import DataConverter
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_data(show_spinner="Checking Excel format...")
def validate_excel_and_get_path(uploaded_file_bytes) -> tuple[str | None, bool]:
    """
    Validates the uploaded Excel file's columns and converts it using DataConverter.
    Returns the temporary path if valid, otherwise None.
    """
    if not uploaded_file_bytes:
        return None, False

    # Create a temporary file to hold the uploaded content
    temp_fd, temp_path = tempfile.mkstemp(suffix=".xlsx")
    with os.fdopen(temp_fd, "wb") as tmp:
        tmp.write(uploaded_file_bytes)

    try:
        # Use DataConverter to check if all required columns exist
        converter = DataConverter(temp_path)
        missing_col = converter.check_all_columns_exist()
        
        if missing_col:
            st.warning("The following required columns are missing:")
            st.write(missing_col)
            os.remove(temp_path) # Clean up the temp file if validation fails
            return None, False
        else:
            # Convert column names and values
            converter.convert_all()
            converter.convert_columns_name()
            
            # Save the converted data to a new temporary file
            converted_fd, converted_path = tempfile.mkstemp(suffix=".xlsx")
            os.close(converted_fd)  # Close the file descriptor as pandas will handle the file
            converter.df.to_excel(converted_path, index=False)
            
            # Clean up the original temp file
            os.remove(temp_path)
            
            return converted_path, True

    except Exception as e:
        st.error(f"Error processing Excel file: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None, False


def report_generator_page():
    st.title("📊 School Survey Report Generator")
    st.markdown("Generate comprehensive school survey reports with automatic analysis and visualizations.")
    
    # st.write(st.session_state.get("major_zh", "Major data not loaded. Please edit the questionnaire first."))
    st.write(st.session_state.get("major", "Major data not loaded. Please edit the questionnaire first."))
    st.write(st.session_state.get("major_zh", "Major data not loaded. Please edit the questionnaire first."))
    
    # Sidebar for configuration
    st.sidebar.header("Configuration Settings")
    
    # Basic settings
    st.sidebar.subheader("Basic Information")
    school_name = st.sidebar.text_input("School Name", value="High School")
    school_id = st.sidebar.number_input("School ID", value=12, min_value=1, step=1)
    # Allow user to select all schools or a specific school
    all_schools_option = st.sidebar.checkbox("All Schools", value=False)
    if all_schools_option:
        school_name = "All Schools"
        school_id = 0
    current_year = datetime.datetime.now().year
    year = st.sidebar.number_input("Survey Year", value=current_year, min_value=2020, step=1)
    
    with st.sidebar.expander("LLM Settings", expanded=False):
        # Use radio buttons to allow only one choice
        llm_choice = st.sidebar.radio(
            "Choose LLM Provider",
            ("Disabled", "Gemini (Require VPN)", "OpenRouter")
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


    # File upload section
    st.header("📁 File Upload")
    
    # Sample data download section
    with st.expander("📥 Download Sample Data", expanded=False):
        col_sample1, col_sample2 = st.columns([1, 3])
        
        with col_sample1:
            sample_data_path = "sample_data/sample_data.xlsx"
            if os.path.exists(sample_data_path):
                with open(sample_data_path, "rb") as sample_file:
                    st.download_button(
                        label="📥 Download Sample Excel",
                        data=sample_file.read(),
                        file_name="sample_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="Download a sample Excel file with the correct format and required columns"
                    )
        
        with col_sample2:
            st.info("💡 **Tip:** Download the sample Excel file to see the expected format and required columns for your data file.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Template File")
        template_file = st.file_uploader("Upload Word Template (.docx) **(Optional)**", type=['docx'])
        if template_file:
            st.success("Template file uploaded successfully!")
    
    with col2:
        st.subheader("Data File")
        data_file = st.file_uploader("Upload Data File (.xlsx)", type=['xlsx', 'xls'], key="data_file_uploader")

    temp_data_path_for_report = None
    excel_format_ok = False
    if data_file:
        temp_data_path_for_report, excel_format_ok = validate_excel_and_get_path(data_file.getvalue())

    if excel_format_ok and temp_data_path_for_report and os.path.exists(temp_data_path_for_report):
        # Display first 5 rows of the converted data
        with st.expander("📊 Data Preview (First 5 Rows)", expanded=False):
            try:
                df_preview = pd.read_excel(temp_data_path_for_report)
            except Exception as e:
                st.warning(f"Could not display data preview: {e}")
        
        # Generate report button
        st.header("🚀 Generate Report")
        
        if st.button("Generate Report", use_container_width=True):
            with st.spinner("Generating report... This may take a few minutes."):
                try:                    
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
        1. **Download Sample**: Download the sample Excel file to understand the required format
        2. **Configure Settings**: Enter your school information and file paths in the sidebar
        3. **Upload Files**: Upload your Word template and Excel data files
        4. **Validate**: Check that all required files are available
        5. **Generate**: Click the "Generate Report" button to create your report
        6. **Download**: Download the generated report and view the visualizations
        """)
    
    with st.expander("File Requirements"):
        st.markdown("""
        - **Sample Data**: Use the sample Excel file as a reference for the correct format
        - **Template File**: Word document (.docx) with placeholders for data
        - **Data File**: Excel file (.xlsx) containing survey data with all required columns
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

