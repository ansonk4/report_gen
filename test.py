import pandas as pd
import random
import numpy as np
from datetime import datetime
import yaml

def generate_sample_data(num_records=100, output_file='sample_survey_data.xlsx'):
    """
    Generate sample Excel data based on the School Survey Report Generator requirements.
    
    Args:
        num_records (int): Number of sample records to generate
        output_file (str): Output Excel file name
    """
    
    # Define valid values for each column based on README specifications
    valid_values = {
        'Banding': ['Band 1', 'Band 2', 'Band 3'],
        '性別': ['男', '女'],
        '高中選修學科': ['理科', '商科', '理商科', '文科', '文理科', '文商科', '文理商科'],
        '中文成績': ['< 25 分', '25-49 分', '50-75 分', '> 75 分'],
        '英文成績': ['< 25 分', '25-49 分', '50-75 分', '> 75 分'],
        '數學成績': ['< 25 分', '25-49 分', '50-75 分', '> 75 分'],
        '父母教育程度': ['小學', '初中', '高中', '預科', '大專 (非學士學位)', '大學', '學士後課程或以上'],
        '試後計劃': ['進修', '工作', '進修及工作', '其他'],
        '工作地方': ['香港', '內地', '國外 - 亞洲', '國外 - 歐美澳'],
        '參加STEM': ['有', '沒有'],
        '大灣區了解': ['完全不了解', '不太了解', '了解', '非常了解'],
        '壓力程度': ['完全沒有', '較少', '少', '大', '較大', '非常大'],
        '壓力來源': ['個人因素', '外在因素'],
        '承受壓力': ['完全不能', '大部分不能', '大部分能夠', '完全能夠']
    }
    
    # Importance scale columns
    importance_columns = [
        '學科知識', '院校因素', '大學學費', '助學金', '主要行業', '朋輩老師', 
        '家庭因素', '預期收入', 'DSE成績', '高中選修科目'
    ]
    
    career_decision_columns = [
        '個人能力_B', '個人興趣性格_B', '成就感_B', '家庭因素_B', '人際關係_B', 
        '工作性質_B', '工作模式_B', '工作量_B', '工作環境_B', '薪水及褔利_B', 
        '晉升機會_B', '發展前景_B', '社會貢獻_B', '社會地位_B'
    ]
    
    skill_columns = ['領導能力', '團隊合作', '創新思維', '科學知識', '解難能力']
    
    importance_values = ['十分重要', '重要', '不太重要', '不重要']
    skill_values = ['顯著提升', '部分提升', '較少提升', '沒有提升', '0']
    
    # Binary columns (0 or 1)
    binary_columns = [
        '大學', '副學士', '文憑', '高級文憑', '工作', '工作假期', '其他',
        '家人期望', '朋輩比較', '密集的時間表', '考試成績', '人際關係', '個人前途', 
        '個人期望', '長期獨處', '疫情', '上課不穩定', '調動考試',
        '做運動', '家人溝通', '朋友溝通', '尋求社工', '重整時間表', '打遊戲機', 
        '睡覺', '聼音樂', '沒有概念'
    ]
    
    # Ranking columns (1-4)
    ranking_columns = ['香港', '內地', '亞洲', '歐美澳']
    
    # Sample majors and occupations (simplified list)
    # Load majors and occupations from YAML file

    with open('src/major_job_zh.yaml', 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    sample_majors = list(yaml_data.get('major', []).values())
    sample_occupations = list(yaml_data.get('job', []).values())

    print(sample_majors)

    # Generate sample data
    data = {}
    
    # Basic information
    data['問卷編號'] = range(1, num_records + 1)
    data['學校編號'] = [random.randint(1, 50) for _ in range(num_records)]
    
    # Fill in all the required columns
    for column, values in valid_values.items():
        data[column] = [random.choice(values) for _ in range(num_records)]
    
    # Add importance scale columns
    for column in importance_columns:
        data[column] = [random.choice(importance_values) for _ in range(num_records)]
    
    # Add career decision columns
    for column in career_decision_columns:
        data[column] = [random.choice(importance_values) for _ in range(num_records)]
    
    # Add skill development columns
    for column in skill_columns:
        data[column] = [random.choice(skill_values) for _ in range(num_records)]
    
    # Add binary columns
    for column in binary_columns:
        data[column] = [random.choice([0, 1]) for _ in range(num_records)]
    
    # Add ranking columns with unique rankings per row
    for i in range(num_records):
        rankings = random.sample([1, 2, 3, 4], 4)
        for j, column in enumerate(ranking_columns):
            if column not in data:
                data[column] = []
            data[column].append(rankings[j])
    
    # Add major preference columns
    major_columns = ['希望修讀', '希望修讀_A', '希望修讀_B', '不希望修讀', '不希望修讀_A', '不希望修讀_B']
    for column in major_columns:
        data[column] = [random.choice(sample_majors) for _ in range(num_records)]
    
    # Add occupation preference columns
    occupation_columns = ['希望從事', '希望從事_A', '希望從事_B', '不希望從事', '不希望從事_A', '不希望從事_B']
    for column in occupation_columns:
        data[column] = [random.choice(sample_occupations) for _ in range(num_records)]
    
    # Add some 999 values randomly to simulate "Not Applicable" responses
    for column in data:
        if column not in ['問卷編號', '學校編號']:
            # Randomly replace 5% of values with 999
            for i in range(num_records):
                if random.random() < 0.05:
                    data[column][i] = 999
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    try:
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"✅ Successfully generated {output_file} with {num_records} records")
        print(f"📊 File contains {len(df.columns)} columns")
        print(f"📁 File size: {len(df)} rows")
        
        # Display basic statistics
        print("\n📋 Sample data preview:")
        print(df.head())
        
        print(f"\n📈 Column names ({len(df.columns)} total):")
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")
            
    except Exception as e:
        print(f"❌ Error saving Excel file: {str(e)}")
        print("💡 Make sure you have openpyxl installed: pip install openpyxl")

def main():
    """Main function to run the generator"""
    print("🏫 School Survey Data Generator")
    print("=" * 50)
    
    # Get user input

    num_records = 500
    output_file = "sample_survey_data.xlsx"
    
    if not output_file.endswith('.xlsx'):
        output_file += '.xlsx'
        
    print(f"\n🔄 Generating {num_records} sample records...")
    generate_sample_data(num_records, output_file)
    
    print(f"\n✨ Generation complete!")
    print(f"📂 Output file: {output_file}")
    print(f"📅 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
 

if __name__ == "__main__":
    main()