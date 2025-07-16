import streamlit as st
import os
import pandas as pd
from pathlib import Path
import tempfile
import shutil
from doc import DocumentGenerator, Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
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
    
    
    # Configuration preview
    # st.header("⚙️ Configuration Preview")
    # config_data = {
    #     "School Name": school_name,
    #     "School ID": school_id,
    #     "Survey Year": year,
    # }
    
    # config_df = pd.DataFrame(list(config_data.items()), columns=['Setting', 'Value'])
    # st.dataframe(config_df, use_container_width=True)
    
    # File validation
    # st.header("📋 File Validation")
    # validation_status = {}
    
    # Check if files exist or are uploaded
    # if template_file or os.path.exists(template_path):
    #     validation_status["Template File"] = "✅ Available"
    # else:
    #     validation_status["Template File"] = "❌ Missing"
    
    # if data_file or os.path.exists(general_data_path):
    #     validation_status["General Data File"] = "✅ Available"
    # else:
    #     validation_status["General Data File"] = "❌ Missing"
    
    # # Check output directory
    # output_dir = os.path.dirname(output_path)
    # if output_dir and not os.path.exists(output_dir):
    #     validation_status["Output Directory"] = f"❌ Directory '{output_dir}' does not exist"
    # else:
    #     validation_status["Output Directory"] = "✅ Available"
    
    # # Check image directory
    # if not os.path.exists(image_dir):
    #     validation_status["Image Directory"] = f"❌ Directory '{image_dir}' does not exist"
    # else:
    #     validation_status["Image Directory"] = "✅ Available"
    
    # # Display validation results
    # for item, status in validation_status.items():
    #     if "✅" in status:
    #         st.success(f"{item}: {status}")
    #     else:
    #         st.error(f"{item}: {status}")
    
    # Generate report button
    st.header("🚀 Generate Report")
    
    # Check if all required files are available
    # all_files_available = (
    #     (template_file or os.path.exists(template_path)) and
    #     (data_file or os.path.exists(general_data_path)) and
    #     (not use_school_data or (school_file if use_school_data else None) or (school_data_path and os.path.exists(school_data_path)))
    # )
    
    # if not all_files_available:
    #     st.warning("⚠️ Please ensure all required files are available before generating the report.")
    
    if st.button("Generate Report", use_container_width=True):
        with st.spinner("Generating report... This may take a few minutes."):
            try:
                # Create temporary directory for processing
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_template_path = template_path
                    temp_data_path = general_data_path
                    
                    # Save uploaded files to temporary locations
                    if template_file:
                        temp_template_path = os.path.join(temp_dir, "template.docx")
                        with open(temp_template_path, "wb") as f:
                            f.write(template_file.getvalue())
                    
                    if data_file:
                        temp_data_path = os.path.join(temp_dir, "data.xlsx")
                        with open(temp_data_path, "wb") as f:
                            f.write(data_file.getvalue())
                    
                    # Ensure output directory exists
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    # Ensure image directory exists
                    os.makedirs(image_dir, exist_ok=True)
                    
                    # Create configuration
                    config = Config(
                        use_gemini= (llm_choice == "Gemini (Require VPN)"),
                        use_llm = (llm_choice != "Disabled"),
                        model_name = model_name,
                        template_path=temp_template_path,
                        output_path=output_path,
                        general_data_path=temp_data_path,
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

if __name__ == "__main__":
    main()