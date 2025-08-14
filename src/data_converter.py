import pandas as pd
import numpy as np
import yaml

class DataConverter:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.df = self.df.map(lambda x: x.strip() if isinstance(x, str) else x)
        self.df = self.df.map(lambda x: np.nan if isinstance(x, str) and x.strip() == "" else x)
        self.mapping = {'學校編號': 'school_id', '問卷編號': 'id', 'Banding': 'banding', '性別': 'gender', '高中選修學科': 'elective', '中文成績': 'chinese_reuslt', '英文成績': 'english_result', '數學成績': 'math_result', '父母教育程度': 'parent_education', '大學': 'uni', '副學士': 'asso', '文憑': 'diploma', '高級文憑': 'high_dip', '工作': 'work', '工作假期': 'working_hoilday', '其他': 'other', '試後計劃': 'future_plan', '香港': 'HK', '內地': 'China', '亞洲': 'Asia', '歐美澳': 'US/EU/AUS', '工作地方': 'working_location', '學科知識': 'personal_interests_A', '院校因素': 'institute_A', '大學學費': 'tuition_A', '助學金': 'scholarship_A', '主要行業': 'career_prospect_A', '朋輩老師': 'peers_and_teacher_A', '家庭因素': 'family_A', '預期收入': 'salary_A', 'DSE成績': 'DSE_result_A', '高中選修科目': 'high_school_electives_A', '希望修讀': 'target_major1', '希望修讀_A': 'target_major2', '希望修讀_B': 'target_major3', '主修相關科目': 'elective_major_relation', '不希望修讀': 'dislike_major1', '不希望修讀_A': 'dislike_major2', '不希望修讀_B': 'dislike_major3', '參加STEM': 'stem_participation', '領導能力': 'leadership', '團隊合作': 'teamwork', '創新思維': 'creativity', '科學知識': 'sci_knowledge', '解難能力': 'problem_solving', '個人能力_B': 'personal_ability_B', '個人興趣性格_B': 'personal_interest_B', '成就感_B': 'sense_of_achievement_B', '家庭因素_B': 'family_B', '人際關係_B': 'interpresonal_relationship_B', '工作性質_B': 'job_nature_B', '工作模式_B': 'remote_work_B', '工作量_B': 'worload_B', '工作環境_B': 'working_environment_B', '薪水及褔利_B': 'salary_and_benefit_B', '晉升機會_B': 'promotion_opportunites_B', '發展前景_B': 'career_prospect_B', '社會貢獻_B': 'social_contribution_B', '社會地位_B': 'social_status_B', '從事相關工作': 'major_career_relation', '希望從事': 'target_occupation1', '希望從事_A': 'target_occupation2', '希望從事_B': 'target_occupation3', '不希望從事': 'dislike_occupation1', '不希望從事_A': 'dislike_occupation2', '不希望從事_B': 'dislike_occupation3', '大灣區了解': 'gba_understanding', '壓力程度': 'stress_lv', '壓力來源': 'stress_scource', '家人期望': 'family_expectations', '朋輩比較': 'comparison', '密集的時間表': 'tight_schedule', '考試成績': 'test_scores', '人際關係': 'relationships', '個人前途': 'prospect', '個人期望': 'expectation', '長期獨處': 'long_term_solitude', '疫情': 'covid_19', '上課不穩定': 'unstable_class', '調動考試': 'transfer_exam', '承受壓力': 'endure_lv', '做運動': 'exercise', '家人溝通': 'family_communication', '朋友溝通': 'friends_communication', '尋求社工': 'social_workers', '重整時間表': 'restructuring_ttb', '打遊戲機': 'video_games', '睡覺': 'sleep', '聼音樂': 'music', '沒有概念': 'no_idea'}

    def read_major_yaml(self, item: str, yaml_path: str) -> dict:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        major_dict = data.get(item)
        if major_dict is not None:
            return {v: k for k, v in major_dict.items()}
        return None

    def _convert_data(self, column_name: list[str] | str, mapping: dict[str|int, str]) -> None:
        if isinstance(column_name, str):
            column_name = [column_name]

        for col in column_name:
            if col not in self.df.columns:
                raise ValueError(f"Missing columns: {col}")
            self.df[col] = self.df[col].replace(mapping)
            

    def convert_all(self):
        """
        Convert all relevant columns in the DataFrame to standardized formats.
        """
        self._convert_data('Banding', {'Band 1': 1, 'Band 2': 2, 'Band 3': 3})
        self._convert_data('性別', {'男': 1, '女': 2})
        self._convert_data("高中選修學科", {'理科': 1, '商科': 2, '理商科': 3, '文科': 4, '文理科': 5, '文商科': 6, '文理商科': 7})
        self._convert_data(["中文成績", "英文成績", "數學成績"], {"< 25 分": 1, "25-49 分": 2, "50-75 分": 3, "> 75 分": 4})
        self._convert_data('父母教育程度', {'小學': 1, '初中': 2, "高中": 3, "預科": 4, '大專 (非學士學位)': 5, '大學': 6, "學士後課程或以上": 7})
        self._convert_data("試後計劃", {"進修": 1, "工作": 2, "進修及工作": 3, "其他": 4})
        self._convert_data("工作地方", {'香港': 1, '內地': 2, '國外 - 亞洲': 3, '國外 - 歐美澳': 4})
        self._convert_data(
            ["學科知識", "院校因素", "大學學費", "助學金", "主要行業", "朋輩老師", "家庭因素", "預期收入", "DSE成績", "高中選修科目"], 
            {"十分重要": 1, "重要": 2, "不太重要": 3, "不重要": 4}
        )
        self._convert_data("參加STEM", {'有': 1, '沒有': 2})
        self._convert_data(
            ["領導能力", "團隊合作", "創新思維", "科學知識", "解難能力"], 
            {"顯著提升": 1, "部分提升": 2, "較少提升": 3, "沒有提升": 4}
        )
        self._convert_data(
            ["個人能力_B", "個人興趣性格_B", "成就感_B", "家庭因素_B", "人際關係_B", "工作性質_B",
            "工作模式_B", "工作量_B", "工作環境_B", "薪水及褔利_B", "晉升機會_B", "發展前景_B",
            "社會貢獻_B", "社會地位_B"],
            {"十分重要": 1, "重要": 2, "不太重要": 3, "不重要": 4}
        )
        self._convert_data("大灣區了解", {"完全不了解": 1, "不太了解": 2, "了解": 3, "非常了解": 4})
        self._convert_data("壓力程度", {"完全沒有": 1, "較少": 2, "少": 3, "大": 4, "較大": 5, "非常大": 6})
        self._convert_data("壓力來源", {"個人因素": 1, "外在因素": 2})
        self._convert_data("承受壓力", {"完全不能": 1, "大部分不能": 2, "大部分能夠": 3, "完全能夠": 4})

        self._convert_data(
            ["希望修讀", "希望修讀_A", "希望修讀_B",
            "不希望修讀", "不希望修讀_A", "不希望修讀_B",], 
            self.read_major_yaml("major", "src/major_job_zh.yaml")
        )
        self._convert_data(
            ["希望從事", "希望從事_A", "希望從事_B",
            "不希望從事", "不希望從事_A", "不希望從事_B"], 
            self.read_major_yaml("job", "src/major_job_zh.yaml")
        )

    def convert_columns_name(self):
        self.df.rename(columns=self.mapping, inplace=True)

    
    def check_all_columns_exist(self) -> list[str]:
        """
        Check if all required columns exist in the DataFrame.
        Returns a list of missing columns.
        """
        return [col for col in self.mapping if col not in self.df.columns]
        

if __name__ == "__main__":
    converter = DataConverter("sample_data/sample_ppt.xlsx")
    converter.convert_all()
    converter.convert_columns_name()
    converter.df.to_excel("sample_data/converted_data.xlsx", index=False)

# df = pd.read_excel("sample_data/sample_data.xlsx")
# map = {col: df.iloc[0][col] for col in df.columns if pd.notna(df.iloc[0][col]) and str(df.iloc[0][col]).strip() != ""}
# print(map)
