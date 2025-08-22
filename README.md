# School Survey Report Generator

An automated system for generating comprehensive school survey reports based on student responses. This tool processes Excel survey data and produces formatted Word documents with statistical analysis, visualizations, and AI-generated insights.

## Installation

You can use the PPT Report Generator directly online at [https://pptgenerator-uqzlepmjiojt6h6mowtmk7.streamlit.app/](https://pptgenerator-uqzlepmjiojt6h6mowtmk7.streamlit.app/) and skip the following steps.

If you prefer to run it locally, follow these steps:

1. Make sure you're using Python 3.10 or higher.

1. Clone the repository:
   ```bash
   git clone https://github.com/ansonk4/report_gen.git
   cd report
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```


4. Run the Streamlit web interface:
   ```bash
   streamlit run src/streamlit.py
   ```

## Usage

The School Survey Report Generator can be used either through the online hosted version or locally on your machine. The system provides a user-friendly web interface with two main sections:

### Main Interface (Report Generator)


1. **Configuration Settings (Sidebar)**
    **Basic Information**: Input the school name, select whether to generate reports for all schools or a specific one, and set the survey year.
    
    **LLM Settings**: Choose an AI provider for generating insights:
    - **Disabled (default):** No AI-generated insights will be included in the report.
    - **Gemini:** Requires a VPN connection. If you leave `GEMINI_API_KEY` blank and `Model` as default value, the system will use the default API key and model. If report generation fails after selecting Gemini, the default API key or model may have expired. See the [LLM API Key](#llm-api-key) section for setup instructions.
    - **OpenRouter:** If you leave `OPENROUTER_API_KEY` blank and `Model` as default value, the system will use the default API key and model. If report generation fails after selecting OpenRouter, the default API key or model may have expired. See the [LLM API Key](#llm-api-key) section for setup instructions.

    **File and Output Paths**: Optionally set custom locations for the template file, output report, and image directory.

2. **File Upload**
   - **Template File (Optional)**: Upload a custom Word template (.docx) if you want to use a different format than [the default template](doc/template.docx). (Not recommended)
   - **Data File (Required)**: Upload your survey data in Excel format (.xlsx).
   - **Sample Data**: Download a sample Excel file to understand the required format and columns.

3. **Data Validation**
   - Once you upload your data file, the system automatically validates it against required columns and value formats.
   - Any validation errors will be displayed with specific row and column information.
   - Invalid data values will be replaced with NA during processing.

4. **Report Generation**
   - After successful validation, click the "Generate Report" button.
   - The system will create visualizations and generate a Word document report.
   - Download your completed report using the download button.
   - View generated visualizations directly in the interface.

### Questionnaire Editor

The Questionnaire Editor allows you to customize the mappings used for majors and occupations in the survey data.

1. **Majors Tab**
   - Add new majors with codes, names, classes, and Chinese names.
   - Edit existing majors using the data editor table.
   - Update changes by clicking the "Update Majors" button.

2. **Occupations Tab**
   - Add new occupations with codes, names, classes, and Chinese names.
   - Edit existing occupations using the data editor table.
   - Update changes by clicking the "Update occupations" button.

3. **Major Influence Tab**
   - Modify the Excel columns used to generate the Major Influence Factor Graph.
   - Column names must end with '_A'.
   - Press Enter after updating each cell.

4. **Occupation Influence Tab**
   - Modify the Excel columns used to generate the Occupation Influence Factor Graph.
   - Column names must end with '_B'.
   - Press Enter after updating each cell.

### LLM setup

#### Gemini

##### API Key setup
1. Visit [Google Cloud Resource Manager](https://console.cloud.google.com/cloud-resource-manager) and create a new Google Cloud Project.
2. Enable a VPN to access services outside Hong Kong.
3. Go to [Google AI Studio API Keys](https://aistudio.google.com/apikey).
4. Click `+ Create API Key` at the top right.
5. Select your project and confirm to create the API key.
6. Copy the generated API key and paste it into the LLM Settings section of the Streamlit page.

##### Model setup
1. Visit [Google AI Studio](https://ai.google.dev/gemini-api/docs/models)
2. Copy the name of the model of your choices (e.g. `gemini-2.5-flash`) and paste it into the LLM Settings section of the Streamlit page.

#### OpenRouter

##### API Key setup
1. Sign in at [OpenRouter](https://openrouter.ai/).
2. Navigate to [API Keys Settings](https://openrouter.ai/settings/keys).
3. Click `Create API Key`.
4. Enter a name and confirm creation.
5. Copy the API key and paste it into the LLM Settings section of the Streamlit page.

##### Model setup
1. Visit [OpenRouter](https://openrouter.ai/models) and find a free model.
2. Copy its name (e.g. `openai/gpt-oss-20b:free`) and paste it into the LLM Settings section of the Streamlit page.

#### Optional:
To change the default local API keys, create a `.env` file in your project directory with the following content:

```
OPENROUTER_KEY=[Your OpenRouter API Key]
GEMINI_API_KEY=[Your Gemini API Key]
```


### Tips for Best Results

1. Always start by downloading and examining the sample data file to understand the required format.
2. Ensure all required columns are present in your data file.
3. Follow the value validation rules for each column to avoid data processing errors.
4. Use the Questionnaire Editor to customize major and occupation mappings if needed.

### Common Issues

- **Invalid Chinese Name for Major/Occupation**: Majors or occupations in your Excel file may be flagged as invalid due to subtle differences in Chinese characters (e.g., `市埸營銷/公關` vs. `市場營銷/公關`). The system treats these as distinct values.

    **Solution:** To ensure consistency, copy major or occupation names directly from the README or Questionnaire Editor. You can also use the Questionnaire Editor to update and correct mappings as needed.

- **LLM Insight Errors or Missing Output (Gemini/OpenRouter)**

    Common Causes and Solutions:

    1. **Invalid API Key**  
    *Solution:* Verify that your API key is correct in the LLM Settings section. If using a `.env` file, ensure the key matches the selected provider.

    2. **VPN Required for Gemini**  
    *Solution:* Gemini requires a VPN connection outside Hong Kong. Activate your VPN before generating the report.

    3. **Rate Limiting (Too Many Requests)**  
    *Solution:* Wait a few minutes or try again later. If the issue persists, use a different API key or provider.

    4. **Unavailable Model**  
    *Solution:* Enter a supported model name in the 'Model' field in the sidebar. Refer to Gemini/OpenRouter documentation for available models and update your selection.

## Input Data Format

The system requires an Excel file with specific columns and value formats. You can refer to the [sample.xlsx](sample_data/sample.xlsx) file for the required structure and formatting. We recommend following this sample for preparing your own survey data.

The following columns **must** be present in your Excel file and only contain values from the specified lists:

#### Basic Information
Columns: `問卷編號`
- interger

Columns: `學校編號`
- interger

Columns: `Banding`
- `Band 1`
- `Band 2`
- `Band 3`

#### Student Demographics
Columns: `性別`
- `男`
- `女`

Columns: `高中選修學科`
- `理科`
- `商科`
- `理商科`
- `文科`
- `文理科`
- `文商科`
- `文理商科`

#### Academic Performance
Columns: `中文成績`, `英文成績`, `數學成績`
- `< 25 分`
- `25-49 分`
- `50-75 分`
- `> 75 分`

Columns: `父母教育程度`
- `小學`
- `初中`
- `高中`
- `預科`
- `大專 (非學士學位)`
- `大學`
- `學士後課程或以上`

#### Post-Exam Plans
Columns: `試後計劃`
- `進修`
- `工作`
- `進修及工作`
- `其他`

Columns: `香港`, `內地`, `亞洲`, `歐美澳`
- `1` (1st ranking)
- `2` (2nd ranking)
- `3` (3nd ranking)
- `4` (4th ranking)

Columns: `工作地方`
- `香港`
- `內地`
- `國外 - 亞洲`
- `國外 - 歐美澳`

Columns: `大學`, `副學士`, `文憑`, `高級文憑`, `工作`, `工作假期`, `其他`
- `0` (not selected)
- `1` (selected)

#### University Selection Factors
Columns: `學科知識`, `院校因素`, `大學學費`, `助學金`, `主要行業`, `朋輩老師`, `家庭因素`, `預期收入`, `DSE成績`, `高中選修科目`
- `十分重要`
- `重要`
- `不太重要`
- `不重要`

#### STEM Participation
Columns: `參加STEM`
- `有`
- `沒有`

#### Skill Development
Columns: `領導能力`, `團隊合作`, `創新思維`, `科學知識`, `解難能力`
- `顯著提升`
- `部分提升`
- `較少提升`
- `沒有提升`
- `0` (not applicable)

#### Career Decision Factors
Columns: `個人能力_B`, `個人興趣性格_B`, `成就感_B`, `家庭因素_B`, `人際關係_B`, `工作性質_B`, `工作模式_B`, `工作量_B`, `工作環境_B`, `薪水及褔利_B`, `晉升機會_B`, `發展前景_B`, `社會貢獻_B`, `社會地位_B`
- `十分重要`
- `重要`
- `不太重要`
- `不重要`

#### Greater Bay Area Awareness
Columns: `大灣區了解`
- `完全不了解`
- `不太了解`
- `了解`
- `非常了解`

#### Stress Assessment
Columns: `壓力程度`
- `完全沒有`
- `較少`
- `少`
- `大`
- `較大`
- `非常大`

Columns: `壓力來源`
- `個人因素`
- `外在因素`

Columns: `承受壓力`
- `完全不能`
- `大部分不能`
- `大部分能夠`
- `完全能夠`

#### Stress Coping Strategies

Columns: `家人期望`, `朋輩比較`, `密集的時間表`, `考試成績`, `人際關係`, `個人前途`, `個人期望`, `長期獨處`, `疫情`, `上課不穩定`, `調動考試`
- `0` (not selected)
- `1` (selected)

Columns: `做運動`, `家人溝通`, `朋友溝通`, `尋求社工`, `重整時間表`, `打遊戲機`, `睡覺`, `聼音樂`, `沒有概念`
- `0` (not selected)
- `1` (selected)

#### Major Preferences
Columns: `希望修讀`, `希望修讀_A`, `希望修讀_B`, `不希望修讀`, `不希望修讀_A`, `不希望修讀_B`
- Default majors in [major_job_zh.yaml](src/major_job_zh.yaml) or the customized list 
you create in the Questionnaire Editor's Majors Tab

#### Occupation Preferences
Columns: `希望從事`, `希望從事_A`, `希望從事_B`, `不希望從事`, `不希望從事_A`, `不希望從事_B`
- Default jobs in [major_job_zh.yaml](src/major_job_zh.yaml) or the customized list 
you create in the Questionnaire Editor's Occupations Tab

### Special Values

All columns accept `999` as a special value indicating "Not Applicable" or "Skipped". This value will be converted to NaN during data processing.

## Unspecified Columns

- Columns not listed in the [Input Data Format](#Input-Data-Format) are not used or validated by the system; you may delete or modify them as needed.



## Project Structure

```
report/
├── src/                    # Source code
│   ├── auto_gen.py         # Automatic report generation script
│   ├── document_generator.py # Main report generation engine
│   ├── data_converter.py   # Data conversion and validation utilities
│   ├── read_csv.py         # Data reading and processing
│   ├── mapping.py          # Data mapping functions
│   ├── plotter.py          # Data visualization
│   ├── prompt_template.py  # AI prompt templates
│   ├── conclusion_gen.py   # LLM integration
│   ├── questionnaire.yaml  # Questionnaire mappings
│   └── major_job_zh.yaml   # Chinese major/occupation mappings
├── sample_data/            # Sample survey data
│   ├── sample_data.xlsx    # Original survey data
│   └── converted_data.xlsx # Processed data
├── doc/                    # Document templates and examples
│   ├── template.docx       # Report template
│   └── filled_report.docx  # Example generated report
├── output/                 # Generated reports
├── img/                    # Generated charts and images
├── requirements.txt        # Python dependencies
└── packages.txt            # System dependencies
```