from doc import Config, DocumentGenerator
import pandas as pd

id_2_school = {
    10: "Tsuen Wan Government Secondary School",
    11: "TWGHs S C Gaw Memorial College",
    12: "Buddhist Yip Kei Nam Memorial College",
    13: "Buddhist Sin Tak College",
    14: "Po Leung Kuk Lo Kit Sing (1983) College",
    15: "Kwun Tong Kung Lok Government Secondary School",
    16: "Mu Kuang English School",
    17: "Buddhist Kok Kwong Secondary School",
    18: "TWGHs Yow Kam Yuen College",
    19: "Ng Yuk Secondary School",
    20: "Ma On Shan Tsung Tsin Secondary School",
    21: "CCC Ming Yin College",
    22: "Tack Ching Girls' Secondary School",
    23: "St. Margaret's Co-educational English Secondary and Primary School",
    24: "Ying Wa College",
    25: "SKH Holy Carpenter Secondary School",
    26: "Hong Kong Taoist Association The Yuen Yuen Institute No. 2 Secondary School",
    27: "Yan Oi Tong Chan Wong Suk Fong Memorial Secondary School",
    28: "AD&FD POHL Leung Sing Tak College",
    29: "TWGHs Kap Yan Directors' College",
    30: "Carmel Secondary School",
    31: "SKH St. Mary's Church Mok Hing Yiu College",
    33: "Ju Ching Chu Secondary School (Kwai Chung)",
    34: "CCC Kwei Wah Shan College",
    35: "Kiangsu-Chekiang College",
    36: "Cognitio College (Hong Kong)",
    37: "Sing Yin Secondary School",
    38: "HKFEW Wong Cho Bau Secondary School",
    39: "Ho Yu College and Primary School (Sponsored by Sik Sik Yuen)",
    40: "Hotung Secondary School",
    41: "Tai Po Sam Yuk Secondary School",
    42: "Tsung Tsin College",
    43: "The Chinese Foundation Secondary School",
    44: "St. Stephen's College",
    45: "Ng Wah Catholic Secondary School",
    46: "Kowloon Tong School (Secondary Section)",
    47: "Rhenish Church Pang Hok Ko Memorial College",
    48: "CCC Kei To Secondary School",
    49: "Caritas Ma On Shan Secondary School",
    50: "NLSI Lui Kwok Pat Fong College",
    51: "Lok Sin Tong Leung Chik Wai Memorial College",
    52: "Shau Kei Wan East Government Secondary School",
    53: "Tung Chung Catholic School",
    54: "San Wui Commercial Society Chan Pak Sha School",
    55: "Carmel Divine Grace Foundation Secondary School",
    56: "HHCKLA Buddhist Ching Kok Secondary School",
    57: "LKWFSL Lau Wong Fat Secondary School",
    58: "Sir Ellis Kadoorie Secondary School (West Kowloon)",
    59: "SKH All Saints' Middle School",
    60: "De La Salle Secondary School, N.T.",
    61: "Fung Kai Liu Man Shek Tong Secondary School",
    62: "Baptist Wing Lung Secondary School",
    63: "Chung Sing Benevolent Society Mrs. Aw Boon Haw Secondary School",
    64: "Madam Lau Kam Lung Secondary School Of Miu Fat Buddhist Monastery",
    65: "San Wui Commercial Society Secondary School",
    66: "TWGHs Yau Tze Tin Memorial College",
    67: "CUHKFAA Thomas Cheung Secondary School",
    68: "Gertrude Simon Lutheran College",
    69: "Pui Shing Catholic Secondary School",
    70: "TWGHs C Y Ma Memorial College",
}

path = "data/school_all.xlsx"
df = pd.read_excel(path, header=2)
interviewed_school_ids = set(df['school_id'].unique())

start = 62

for key, value in id_2_school.items():
    if key not in interviewed_school_ids:
        continue
    if key < start:
        continue

    config = Config(
        school_id=None, 
        school_name="All School", 
        general_data_path=path, 
        output_path=f"output/report_{value}.docx",
        model_name=None,
        use_gemini=True,
    )
    generator = DocumentGenerator(config)
    generator.generate_report()