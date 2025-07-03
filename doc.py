from docxtpl import DocxTemplate
from read_csv import csv_reader
from conclusion_gen import llm
import prompt_template

doc = DocxTemplate("template.docx")

llm = llm(stop_all = True)
context = {
    "year": 2025,
    "school": "Springfield High School",
    "respondents": 150,
}

path_all = "school_all.xlsx"
general_school = csv_reader(path_all)

path = "School 10.xlsx"
csv_reader = csv_reader(path)


def get_topk_groupby(target:str, target_col:list, group_by_col:str, k:int) -> dict:
    combined_df = csv_reader.combine_target(target_cols, target)
    dis_df = csv_reader.get_distribution(combined_df, target, group_by_col)

    groupby_results = csv_reader.sort_distribution(dis_df)
    all_result = csv_reader.get_distribution(combined_df, target)
    
    def get_topk(df, k=5):
        return df[target].head(k).tolist()

    ret = {"all": get_topk(all_result, k)}
    for group, df in groupby_results.items():
        ret[group] = get_topk(df, k)

    return ret
    

target = "major"
target_cols = ['target_major1', 'target_major2', 'target_major3']
group_by_col = "gender"
top_major = get_topk_groupby(target, target_cols, group_by_col, 5)
for i, item in enumerate(top_major["all"]):
    context[f'major_{i}'] = item
for i, item in enumerate(top_major["m"]):
    context[f'male_major_{i}'] = item
for i, item in enumerate(top_major["f"]):
    context[f'female_major_{i}'] = item 

target = "dislike_major"
target_cols = ['dislike_major1', 'dislike_major2', 'dislike_major3']
group_by_col = "gender"
top_dislike_major = get_topk_groupby(target, target_cols, group_by_col, 2)
for i, item in enumerate(top_dislike_major["all"]):
    context[f'unpopular_majors_{i}'] = item

# major conclusion
prompt = "Wirte a conclusion based on the following data about major perference order of student \n\n"
prompt += f"top 5 major choices in all student: {top_major['all']} \n"
prompt += f"top 5 major choices in male student: {top_major['m']} \n"
prompt += f"top 5 major choices in female student: {top_major['f']} \n"
prompt += f"top 2 unpopular majors in all student: {top_dislike_major['all']}"
context["major_conclusion"] = llm.generate(prompt)

# major_appendic
target = "major"
target_cols = ['target_major1', 'target_major2', 'target_major3']
group_by_col = "gender"
top_major = get_topk_groupby(target, target_cols, group_by_col, 7)
for i, item in enumerate(top_major["all"]):
    context[f'top_major_{i}'] = item

# occupation 
target = "occupation"
target_cols = ['target_occupation1', 'target_occupation2', 'target_occupation3']
group_by_col = "gender"
top_occupation = get_topk_groupby(target, target_cols, group_by_col, 5)
for i, item in enumerate(top_occupation['all']):
    context[f"occupation_{i}"] = item
for i, item in enumerate(top_occupation['m']):
    context[f'male_occupation_{i}'] = item
for i, item in enumerate(top_occupation['f']):
    context[f'female_occupation_{i}'] = item 
    
target = "dislike_occupation"
target_cols = ['dislike_occupation1', 'dislike_occupation2', 'dislike_occupation3']
group_by_col = "gender"
top_dislike_occupation = get_topk_groupby(target, target_cols, group_by_col, 2)
for i, item in enumerate(top_dislike_occupation["all"]):
    context[f'unpopular_occupations_{i}'] = item
    
# occupations conclusion
prompt = "Wirte a conclusion based on the following data about occupation perference order of student \n\n"
prompt += f"top 5 occupation choices in all student: {top_major['all']} \n"
prompt += f"top 5 occupation choices in male student: {top_major['m']} \n"
prompt += f"top 5 occupation choices in female student: {top_major['f']} \n"
prompt += f"top 2 unpopular occupation in all student: {top_dislike_occupation['all']}"
context["occupations_conclusion"] = llm.generate(prompt)

# occupation appendic
target = "occupation"
target_cols = ['target_occupation1', 'target_occupation2', 'target_occupation3']
group_by_col = "gender"
top_occupation = get_topk_groupby(target, target_cols, group_by_col, 7)
for i, item in enumerate(top_occupation["all"]):
    context[f'top_occupation_{i}'] = item

# STEM
# Stem skill
leadership_percent = csv_reader.get_percent("leadership", [1.0, 2.0])
teamwork_percent = csv_reader.get_percent("teamwork", [1.0, 2.0])
creativity_percent = csv_reader.get_percent("creativity", [1.0, 2.0])
sci_knowledge_percent = csv_reader.get_percent("sci_knowledge", [1.0, 2.0])
problem_solving_percent = csv_reader.get_percent("problem_solving", [1.0, 2.0])

context['leadership_strong'], context['leadership_par'] = leadership_percent[1], leadership_percent[2]
context['teamwork_strong'], context['teamwork_par'] = teamwork_percent[1], teamwork_percent[2]
context['creative_strong'], context['creative_par'] = creativity_percent[1], creativity_percent[2]
context['knowledge_strong'], context['knowledge_par'] = sci_knowledge_percent[1], sci_knowledge_percent[2]
context['prob_solving_strong'], context['prob_solving_par'] = problem_solving_percent[1], problem_solving_percent[2]

# STEM Major
stem_sci_major = csv_reader.check_class_match("Science", "stem_participation", major=True)
stem_eng_major = csv_reader.check_class_match("Engineering", "stem_participation", major=True)

context['stem_eng_A'], context['no_stem_eng_A'] = stem_eng_major
context['stem_sci_A'], context['no_stem_sci_A'] = stem_sci_major
context['eng_diff_A'] = context['stem_eng_A'] - context['no_stem_eng_A']
context['sci_diff_A'] = context['stem_sci_A'] - context['no_stem_sci_A']
context['stem_total_A'] = context['stem_eng_A'] + context['stem_sci_A']
context['no_stem_total_A'] = context['no_stem_eng_A'] + context['no_stem_sci_A']
context['total_diff_A'] = context['eng_diff_A'] + context['sci_diff_A']

# Stem Job
stem_sci_job = csv_reader.check_class_match("Science", "stem_participation", major=False)
stem_eng_job = csv_reader.check_class_match("Engineering", "stem_participation", major=False)

context['stem_eng_B'], context['no_stem_eng_B'] = stem_eng_job
context['stem_sci_B'], context['no_stem_sci_B'] = stem_sci_job
context['eng_diff_B'] = context['stem_eng_B'] - context['no_stem_eng_B']
context['sci_diff_B'] = context['stem_sci_B'] - context['no_stem_sci_B']
context['stem_total_B'] = context['stem_eng_B'] + context['stem_sci_B']
context['no_stem_total_B'] = context['no_stem_eng_B'] + context['no_stem_sci_B']
context['total_diff_B'] = context['eng_diff_B'] + context['sci_diff_B']

context['stem_conclusion'] = llm.generate(prompt_template.stem_conclusion_prompt(context))


# GBA 
gba_bus_major = csv_reader.check_class_match("Business", "gba_understanding", major=True)
gba_sci_major = csv_reader.check_class_match("Science", "gba_understanding", major=True)

context['gba_bus_A'], context['no_gba_bus_A'] = gba_bus_major
context['gba_sci_A'], context['no_gba_sci_A'] = gba_sci_major
context['bus_diff_A'] = context['gba_bus_A'] - context['no_gba_bus_A']
context['gba_sci_diff_A'] = context['gba_sci_A'] - context['no_gba_sci_A']

gba_bus_job = csv_reader.check_class_match("Business", "gba_understanding", major=False)
gba_eng_job = csv_reader.check_class_match("Engineering", "gba_understanding", major=False)
gba_sci_job = csv_reader.check_class_match("Science", "gba_understanding", major=False)

context['gba_bus_B'], context['no_gba_bus_B'] = gba_bus_job
context['gba_eng'], context['no_gba_eng'] = gba_eng_job
context['gba_sci_B'], context['no_gba_sci_B'] = gba_sci_job
context['bus_diff_B'] = context['gba_bus_B'] - context['no_gba_bus_B']
context['gba_eng_diff'] = context['gba_eng'] - context['no_gba_eng']
context['gba_sci_diff_B'] = context['gba_sci_B'] - context['no_gba_sci_B']

context['gba_conclusion'] = llm.generate(prompt_template.gba_conclusion_prompt(context), output=True)

# Stress
stress_factor = csv_reader.get_percent("stress_scource", ["personal", "external"])
general_stress_factor = general_school.get_percent("stress_scource", ["personal", "external"])

context['personal_A'], context['external_A'] = stress_factor["personal"], stress_factor["external"]
context['personal_B'], context['external_B'] = general_stress_factor["personal"], general_stress_factor["external"]


stress_sources = [
    "family_expectations",
    "comparison",
    "dense_ttb",
    "test_scores",
    "relationships",
    "prospect",
    "expectation",
    "long_term_solitude",
    "covid_19",
    "unstable_class",
    "transfer_exam"
]
for item in stress_sources:
    context[f"{item}_A"] = csv_reader.get_percent(item, [1.0], drop_zero=False)[1.0]
    context[f"{item}_B"] = general_school.get_percent(item, [1.0], drop_zero=False)[1.0]


stress_lv = ["none", "very_low", "low", "moderate", "high", "very_high"]
stress_lv_distribution = csv_reader.get_percent("stress_lv", stress_lv, drop_zero=False)
general_stress_lv_distribution = general_school.get_percent("stress_lv", stress_lv, drop_zero=False)
for lv in stress_lv:
    context[f"{lv}_A"] = stress_lv_distribution[lv]
    context[f"{lv}_B"] = general_stress_lv_distribution[lv]


endure_lv = ["totally_can", "mostly_can", "mostly_cannot", "totally_cannot"]
endure_lv_distribution = csv_reader.get_percent("endure_lv", endure_lv, drop_zero=False)
general_endure_lv_distribution = general_school.get_percent("endure_lv", endure_lv, drop_zero=False)
for lv in endure_lv:
    context[f"{lv}_A"] = endure_lv_distribution[lv]
    context[f"{lv}_B"] = general_endure_lv_distribution[lv]


stress_method = ["exercise", "family_communication", "friends_communication", "social_workers", "restructuring_ttb", "video_games", "sleep", "music", "no_idea"]
for item in stress_method:
    context[f"{item}_A"] = csv_reader.get_percent(item, [1.0], drop_zero=False)[1.0]
    context[f"{item}_B"] = general_school.get_percent(item, [1.0], drop_zero=False)[1.0]

context[f"stress_sources_conclusion"] = llm.generate(prompt_template.stress_sources_prompt(context), output=True)



for key, value in context.items():
    if isinstance(value, float):
        context[key] = f"{round(value, 1)}%"

# Render the document
doc.render(context)
doc.save("filled_report.docx")
print("Document generated successfully: filled_report.docx")
