# job_mapping.py

import numpy as np

# Mapping from job code to job name
major_name_map = {
    1: "Architecture", 2: "Real Estate & Construction", 3: "Civil", 4: "Survey",
    5: "Design", 6: "Fashion & Textile", 7: "Music", 8: "Visual Art",
    9: "Accounting", 10: "Aviation Management", 11: "Economics", 12: "Finance",
    13: "Logistics", 14: "Hotel & Tourism Management", 15: "Human Resources",
    16: "Investment", 17: "Management", 18: "Marketing", 19: "Risk Management",
    20: "Property Management", 21: "General Education", 22: "Physical Education",
    23: "Pre-school Education", 24: "Special Education", 25: "Computer Engineering",
    26: "Mechanical / Electrical", 27: "Aviation Engineering", 28: "Science Engineering",
    29: "Anthropology", 30: "Cultural Studies", 31: "History", 32: "Philosophy",
    33: "Religion", 34: "Chinese (Literature)", 35: "English (Literature)",
    36: "Linguistics", 37: "Translation", 38: "Other Languages", 39: "Law",
    40: "Film and Media Arts", 41: "Journalism & Communication", 42: "Creative Media",
    43: "Medicine / Surgery", 44: "Dental", 45: "Chinese Medicine", 46: "Veterinary",
    47: "Pharmacy", 48: "Nursing", 49: "Therapy", 50: "Nutrition", 51: "Biomedical",
    52: "Public Health", 53: "Physics", 54: "Chemistry", 55: "Biology",
    56: "Biochemistry", 57: "Environmental Science", 58: "Mathematics",
    59: "Statistics", 60: "Actuarial", 61: "Computer Science",
    62: "Artificial Intelligence (AI)", 63: "Government & Administration",
    64: "Criminology", 65: "Psychology", 66: "Sociology", 67: "Social Work",
    68: "Geography", 69: "Culinary Arts and Management", 70: "Game Design",
    71: "Urban Studies", 72: "Others"
}

# Mapping from job code to job class
major_class_map = {
    **dict.fromkeys([1, 2, 3, 4], "Architecture"),
    **dict.fromkeys([5, 6, 7, 8], "Art"),
    **dict.fromkeys(range(9, 21), "Business"),
    **dict.fromkeys(range(21, 25), "Education"),
    **dict.fromkeys(range(25, 29), "Engineering"),
    **dict.fromkeys(range(29, 34), "Humanities"),
    **dict.fromkeys(range(34, 39), "Language"),
    **dict.fromkeys([39], "Law"),
    **dict.fromkeys([40, 41, 42], "Media"),
    **dict.fromkeys(range(43, 53), "Medicine"),
    **dict.fromkeys(range(53, 63), "Science"),
    **dict.fromkeys(range(63, 69), "Social Science"),
    **dict.fromkeys(range(69, 73), "Others")
}

# job_mapping.py

import pandas as pd

# Define job categories and job names
job_categories = {
    "Architecture": [1, 2, 3, 4],
    "Art": [5, 6, 7, 8],
    "Business": list(range(9, 20)),
    "Education": [20, 21, 22, 23],
    "Engineering": [24, 25, 26, 27, 28],
    "Professional": [29, 30, 31, 32],
    "Media": [33, 34, 35, 36],
    "Medicine": list(range(37, 48)),
    "Science": [48, 49, 50, 51, 52, 53],
    "Service": [54, 55, 56, 57],
    "Trading and Logistics": [58, 59, 60, 61],
    "Government": [62, 63, 64, 65, 66],
    "Others": list(range(67, 77))
}

# Flat map of job code to job name
job_names = {
    1: "Architecture",
    2: "Surveying",
    3: "Construction",
    4: "Civil",
    5: "Design",
    6: "Entertainment / Music",
    7: "Fashion Design",
    8: "Photography",
    9: "Advertising",
    10: "Administration / Management",
    11: "Asset Management / Stock",
    12: "Banking / Finance",
    13: "Hospitality / Tourism",
    14: "Human Resources",
    15: "Marketing / Public Relations",
    16: "Insurance",
    17: "Property / Real Estate",
    18: "Risk Management",
    19: "Start-up Business",
    20: "General Education",
    21: "Physical Education",
    22: "Pre-School Education",
    23: "Special Education",
    24: "Computer Engineering",
    25: "Mechanical Engineering",
    26: "Aviation Engineering",
    27: "Science Engineering",
    28: "Manufacturing",
    29: "Legal",
    30: "Accounting / Audit",
    31: "Actuary",
    32: "Translation",
    33: "Media / Journalism",
    34: "Digital Marketing",
    35: "Film / Television Production",
    36: "Youtuber",
    37: "Medical Service",
    38: "Specialist",
    39: "General Practitioner",
    40: "Veterinary",
    41: "Pharmacy",
    42: "Psychologist",
    43: "Nutritionist",
    44: "Therapist",
    45: "Chinese Medicine Practitioner",
    46: "Biomedical",
    47: "Nursing",
    48: "Information Technology (IT)",
    49: "Data Science",
    50: "Artificial Intelligence (AI)",
    51: "Biochemistry",
    52: "Laboratory",
    53: "Environmental Science",
    54: "Aviation",
    55: "Social Service",
    56: "Social Work",
    57: "Retail & Food & Beverage",
    58: "Import / Export / Wholesale",
    59: "Logistics",
    60: "Trading",
    61: "Transportation",
    62: "Civil Servant (Clerical)",
    63: "Fireman",
    64: "Paramedic",
    65: "Customs Officer",
    66: "Immigration Officer",
    67: "Chef",
    68: "Pastry Chef",
    69: "Pet Groomer",
    70: "Beautician",
    71: "Makeup Artist",
    72: "Archaeologist",
    73: "Game Designer",
    74: "Librarian",
    75: "Cartoonist",
    76: "Others"
}

# Inverse map for job code to category
job_code_to_category = {}
for category, codes in job_categories.items():
    for code in codes:
        job_code_to_category[code] = category

# === Functions ===

def get_job_name(code):
    name = job_names.get(code, np.nan)
    return name

def get_job_class(code):
    return job_code_to_category.get(code, np.nan)

def get_major_name(code):
    """Returns the job name for a given code."""
    return major_name_map.get(code, np.nan)

def get_major_class(code):
    """Returns the job class for a given code."""
    return major_class_map.get(code, np.nan)

