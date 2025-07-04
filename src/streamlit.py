"""
Streamlit web application for School Survey Report Generator
"""

import streamlit as st
import pandas as pd
import os
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime
import shutil
import logging
from typing import Optional, Dict, Any
import traceback

# Import the refactored document generator
from tmp import DocumentGenerator, Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="School Survey Report Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitReportGenerator:
    """Streamlit interface for the document generator."""
    
    def __init__(self):
        self.temp_dir = None
        self.config = None
        self.setup_session_state()
    
    def setup_session_state(self):
        """Initialize session state variables."""
        if 'generation_complete' not in st.session_state:
            st.session_state.generation_complete = False
        if 'report_path' not in st.session_state:
            st.session_state.report_path = None
        if 'config' not in st.session_state:
            st.session_state.config = None
    
    def create_temp_directory(self) -> str:
        """Create a temporary directory for file operations."""
        if self.temp_dir is None:
            self.temp_dir = tempfile.mkdtemp()
            # Create subdirectories
            os.makedirs(os.path.join(self.temp_dir, "data"), exist_ok=True)
            os.makedirs(os.path.join(self.temp_dir, "doc"), exist_ok=True)
            os.makedirs(os.path.join(self.temp_dir, "img"), exist_ok=True)
        return self.temp_dir
    
    def render_header(self):
        """Render the main header."""
        st.markdown('<div class="main-header">📊 School Survey Report Generator</div>', 
                   unsafe_allow_html=True)
        st.markdown("""
        Generate comprehensive school survey reports with automated analysis of:
        - **Major & Occupation Preferences** 
        - **STEM Participation Analysis**
        - **Stress & Mental Health Assessment**
        - **Comparative Analysis** with general population data
        """)
    
    def render_sidebar_config(self) -> Optional[Config]:
        """Render the configuration sidebar."""
        st.sidebar.markdown('<div class="section-header">⚙️ Configuration</div>', 
                           unsafe_allow_html=True)
        
        # Basic settings
        school_name = st.sidebar.text_input("School Name", value="High School")
        year = st.sidebar.number_input("Report Year", min_value=2020, max_value=2030, value=2025)
        
        # File uploads
        st.sidebar.markdown("### 📁 File Uploads")
        
        template_file = st.sidebar.file_uploader(
            "Upload Document Template (.docx)", 
            type=['docx'],
            help="Upload the Word document template for the report"
        )
        
        school_data_file = st.sidebar.file_uploader(
            "Upload School Data (.xlsx)", 
            type=['xlsx'],
            help="Upload the Excel file containing school survey data"
        )
        
        general_data_file = st.sidebar.file_uploader(
            "Upload General Data (.xlsx)", 
            type=['xlsx'],
            help="Upload the Excel file containing general population data for comparison"
        )
        
        # Validate required files
        if not all([template_file, school_data_file, general_data_file]):
            st.sidebar.warning("⚠️ Please upload all required files to proceed.")
            return None
        
        # Save uploaded files
        temp_dir = self.create_temp_directory()
        
        try:
            # Save template
            template_path = os.path.join(temp_dir, "doc", "template.docx")
            with open(template_path, "wb") as f:
                f.write(template_file.read())
            
            # Save school data
            school_data_path = os.path.join(temp_dir, "data", "school_data.xlsx")
            with open(school_data_path, "wb") as f:
                f.write(school_data_file.read())
            
            # Save general data
            general_data_path = os.path.join(temp_dir, "data", "general_data.xlsx")
            with open(general_data_path, "wb") as f:
                f.write(general_data_file.read())
            
            # Create config
            config = Config(
                template_path=template_path,
                output_path=os.path.join(temp_dir, "doc", "filled_report.docx"),
                school_data_path=school_data_path,
                general_data_path=general_data_path,
                image_dir=os.path.join(temp_dir, "img"),
                year=year,
                school_name=school_name,
            )
            
            st.sidebar.success("✅ All files uploaded successfully!")
            return config
            
        except Exception as e:
            st.sidebar.error(f"❌ Error saving files: {str(e)}")
            return None
    
    def render_data_preview(self, config: Config):
        """Render data preview section."""
        st.markdown('<div class="section-header">📋 Data Preview</div>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("School Data")
            try:
                school_df = pd.read_excel(config.school_data_path)
                st.dataframe(school_df.head(10), use_container_width=True)
                st.info(f"📊 Shape: {school_df.shape[0]} rows × {school_df.shape[1]} columns")
            except Exception as e:
                st.error(f"Error loading school data: {str(e)}")
        
        with col2:
            st.subheader("General Data")
            try:
                general_df = pd.read_excel(config.general_data_path)
                st.dataframe(general_df.head(10), use_container_width=True)
                st.info(f"📊 Shape: {general_df.shape[0]} rows × {general_df.shape[1]} columns")
            except Exception as e:
                st.error(f"Error loading general data: {str(e)}")
    
    def render_generation_section(self, config: Config):
        """Render the report generation section."""
        st.markdown('<div class="section-header">🚀 Generate Report</div>', 
                   unsafe_allow_html=True)
        
        # Configuration summary
        with st.expander("📋 Configuration Summary", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**School Name:** {config.school_name}")
                st.write(f"**Year:** {config.year}")
            with col2:
                st.write(f"**Template:** {os.path.basename(config.template_path)}")
                st.write(f"**School Data:** {os.path.basename(config.school_data_path)}")
                st.write(f"**General Data:** {os.path.basename(config.general_data_path)}")
        
        # Generation button
        if st.button("🎯 Generate Report", type="primary", use_container_width=True):
            self.generate_report(config)
    
    def generate_report(self, config: Config):
        """Generate the report with progress tracking."""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize generator
            status_text.text("🔧 Initializing report generator...")
            progress_bar.progress(10)
            
            # Change working directory to temp directory
            original_cwd = os.getcwd()
            os.chdir(self.temp_dir)
            
            try:
                generator = DocumentGenerator(config)
                progress_bar.progress(20)
                
                # Process different sections
                sections = [
                    ("📚 Processing major preferences...", 30),
                    ("💼 Processing occupation preferences...", 45),
                    ("🔬 Processing STEM analysis...", 60),
                    ("🌐 Processing GBA analysis...", 75),
                    ("😰 Processing stress analysis...", 90),
                    ("📄 Finalizing report...", 95)
                ]
                
                for status, progress in sections:
                    status_text.text(status)
                    progress_bar.progress(progress)
                
                # Generate the report
                generator.generate_report()
                
                # Final update
                status_text.text("✅ Report generated successfully!")
                progress_bar.progress(100)
                
                # Store results in session state
                st.session_state.generation_complete = True
                st.session_state.report_path = config.output_path
                st.session_state.config = config
                
                # Show success message
                st.success("🎉 Report generated successfully!")
                
            finally:
                # Restore original working directory
                os.chdir(original_cwd)
                
        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())
    
    def render_download_section(self):
        """Render the download section."""
        if not st.session_state.generation_complete:
            return
        
        st.markdown('<div class="section-header">⬇️ Download Report</div>', 
                   unsafe_allow_html=True)
        
        config = st.session_state.config
        report_path = st.session_state.report_path
        
        if os.path.exists(report_path):
            # Create download package
            package_path = self.create_download_package(config, report_path)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download report only
                with open(report_path, "rb") as file:
                    st.download_button(
                        label="📄 Download Report (.docx)",
                        data=file.read(),
                        file_name=f"{config.school_name}_Report_{config.year}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            
            with col2:
                # Download complete package
                if package_path and os.path.exists(package_path):
                    with open(package_path, "rb") as file:
                        st.download_button(
                            label="📦 Download Complete Package (.zip)",
                            data=file.read(),
                            file_name=f"{config.school_name}_Complete_Package_{config.year}.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
            
            # Report info
            st.info(f"📋 Report generated for **{config.school_name}** ({config.year})")
            
        else:
            st.error("❌ Report file not found. Please regenerate the report.")
    
    def create_download_package(self, config: Config, report_path: str) -> Optional[str]:
        """Create a zip package with report and generated images."""
        try:
            package_path = os.path.join(self.temp_dir, f"{config.school_name}_package.zip")
            
            with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add the report
                zipf.write(report_path, f"{config.school_name}_Report_{config.year}.docx")
                
                # Add generated images
                img_dir = config.image_dir
                if os.path.exists(img_dir):
                    for img_file in os.listdir(img_dir):
                        if img_file.endswith(('.png', '.jpg', '.jpeg')):
                            img_path = os.path.join(img_dir, img_file)
                            zipf.write(img_path, f"images/{img_file}")
                
                # Add a readme
                readme_content = f"""
School Survey Report Package
===========================

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
School: {config.school_name}
Year: {config.year}

Contents:
- {config.school_name}_Report_{config.year}.docx: Main report document
- images/: Generated charts and visualizations

This package was generated using the School Survey Report Generator.
                """.strip()
                
                zipf.writestr("README.txt", readme_content)
            
            return package_path
            
        except Exception as e:
            logger.error(f"Error creating download package: {e}")
            return None
    
    def render_footer(self):
        """Render the footer."""
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p>📊 School Survey Report Generator | Built with Streamlit</p>
            <p>For support or questions, please contact your system administrator.</p>
        </div>
        """, unsafe_allow_html=True)
    
    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                logger.warning(f"Could not clean up temp directory: {e}")
    
    def run(self):
        """Main application runner."""
        try:
            # Render header
            self.render_header()
            
            # Render sidebar configuration
            config = self.render_sidebar_config()
            
            if config:
                # Main content area
                tab1, tab2, tab3 = st.tabs(["📋 Data Preview", "🚀 Generate Report", "⬇️ Download"])
                
                with tab1:
                    self.render_data_preview(config)
                
                with tab2:
                    self.render_generation_section(config)
                
                with tab3:
                    self.render_download_section()
            
            else:
                # Show instructions when no files are uploaded
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("""
                ### 🚀 Getting Started
                
                1. **Upload Files** in the sidebar:
                   - Document template (.docx)
                   - School survey data (.xlsx)
                   - General population data (.xlsx)
                
                2. **Configure Settings**:
                   - Set school name and year
                
                3. **Generate Report**:
                   - Preview your data
                   - Generate comprehensive analysis
                   - Download results
                
                ### 📋 File Requirements
                
                - **Template File**: Word document with placeholders for data insertion
                - **School Data**: Excel file with survey responses from your school
                - **General Data**: Excel file with general population data for comparison
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Render footer
            self.render_footer()
            
        except Exception as e:
            st.error(f"Application error: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())
        
        finally:
            # Cleanup is handled by Streamlit's session management
            pass


def main():
    """Main function to run the Streamlit app."""
    app = StreamlitReportGenerator()
    app.run()


if __name__ == "__main__":
    main()