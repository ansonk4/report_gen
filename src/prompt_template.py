# Example prompt
DEFAULT_PROMPT = "Please enter your query:"

def major_prompt(top_major, top_dislike_major):
    prompt = (
        "Based on the following data about students' major preference rankings, \n"
        "please write a concise and insightful conclusion that highlights notable trends, \n"
        "gender differences, and the least preferred majors:\n\n"
        f"Top 5 major choices among all students: {top_major['all']}\n"
    )
    if 'm' in top_major:
        prompt += f"Top 5 major choices among male students: {top_major['m']}\n"
    if 'f' in top_major:
        prompt += f"Top 5 major choices among female students: {top_major['f']}\n"
    prompt += (
        f"Top 2 least preferred majors among all students: {top_dislike_major['all']}\n\n"
        "Focus on similarities and differences between genders, and discuss any unexpected or significant findings.\n"
    )
    return prompt

def occupations_prompt(top_occupation, top_dislike_occupation):
    prompt = (
        "Based on the following data about students' occupational preferences, write a concise and insightful conclusion that highlights key patterns, gender differences, and notable trends:\n\n"
        f"- Top 5 occupations chosen by all students: {top_occupation['all']}\n"
    )
    if 'm' in top_occupation:
        prompt += f"- Top 5 occupations chosen by male students: {top_occupation['m']}\n"
    if 'f' in top_occupation:
        prompt += f"- Top 5 occupations chosen by female students: {top_occupation['f']}\n"
    prompt += (
        f"- 2 least preferred occupations among all students: {top_dislike_occupation['all']}\n\n"
        "Focus on similarities and differences between genders, and discuss any unexpected or significant findings.\n"
    )
    return prompt

def stem_conclusion_prompt(context):
    return f"""
            You are a data analyst tasked with evaluating the impact of STEM education based on survey data. The data includes three tables showing differences between participants who have attended STEM programs and those who have not.
            Please provide a clear and concise conclusion that summarizes the overall influence of STEM education. Your conclusion should synthesize insights across the three tables and highlight any major trends, improvements, or gaps.
            The tables are as follows:

            Table 1: Effectiveness of STEM Projects
            Effectiveness of STEM Project            | Strongly Improve                  | Partially Improve
            -----------------------------------------|-----------------------------------|-------------------
            Leadership                               | {context['leadership_strong']}    | {context['leadership_par']}
            Teamwork                                 | {context['teamwork_strong']}      | {context['teamwork_par']}
            Creative Thinking                        | {context['creative_strong']}      | {context['creative_par']}
            Science Knowledge and Understanding      | {context['knowledge_strong']}     | {context['knowledge_par']}
            Problem Solving Skills                   | {context['prob_solving_strong']}  | {context['prob_solving_par']}

            Table 2: STEM Majors Preference
            STEM Majors Preference          | Attended STEM (A=)           | Not Attended STEM (A=)           | Difference
            -------------------------------|------------------------------|----------------------------------|-----------
            Engineering                    | {context['stem_eng_A']}      | {context['no_stem_eng_A']}       | {context['eng_diff_A']}
            Science                        | {context['stem_sci_A']}      | {context['no_stem_sci_A']}       | {context['sci_diff_A']}
            Total                          | {context['stem_total_A']}    | {context['no_stem_total_A']}     | {context['total_diff_A']}

            Table 3: STEM Occupations Preference
            STEM Occupations Preference    | Attended STEM (A=)           | Not Attended STEM (A=)           | Difference
            ------------------------------|------------------------------|----------------------------------|-----------
            Engineering                    | {context['stem_eng_B']}      | {context['no_stem_eng_B']}       | {context['eng_diff_B']}
            Science                        | {context['stem_sci_B']}      | {context['no_stem_sci_B']}       | {context['sci_diff_B']}
            Total                          | {context['stem_total_B']}    | {context['no_stem_total_B']}     | {context['total_diff_B']}
            """

def gba_conclusion_prompt(context):
    return f"""
            You are an educational policy analyst. Based on the following two tables showing how students' familiarity with the Guangdong-Hong Kong-Macao Greater Bay Area (GBA) development policy influences their academic major and career preferences, write a concise conclusion that summarizes the key insights and differences.
            Use clear and objective language to compare the responses between students who are familiar with the GBA policy and those who are not. Highlight any major trends, significant differences, or implications that may affect education or career guidance policies.

            The tables are as follows:

            1. *Influence of Greater Bay Area Development Policy on Major Preferences*
            (*Results analyzed from respondents with high GBA familiarity and respondents with low familiarity*)
            | GBA Majors Preference | Familiar with GBA | Unfamiliar with GBA | Difference |
            |------------------------|-------------------|----------------------|------------|
            | Business               | {context['gba_bus_A']}   | {context['no_gba_bus_A']}   | {context['bus_diff_A']} |
            | Science                | {context['gba_sci_A']}   | {context['no_gba_sci_A']}   | {context['gba_sci_diff_A']} |

            2. *Influence of Greater Bay Area Development Policy on Career Preferences*
            | GBA Occupations Preference | Familiar with GBA | Unfamiliar with GBA | Difference |
            |----------------------------|-------------------|----------------------|------------|
            | Business                   | {context['gba_bus_B']}   | {context['no_gba_bus_B']}   | {context['bus_diff_B']} |
            | Engineering                | {context['gba_eng']}     | {context['no_gba_eng']}     | {context['gba_eng_diff']} |
            | Science                    | {context['gba_sci_B']}   | {context['no_gba_sci_B']}   | {context['gba_sci_diff_B']} |
            """

def stress_sources_prompt(context):
    return f"""
            You are an education researcher analyzing the stress sources among high school students in Hong Kong. The following table presents the percentage distribution of various stress sources for two groups of students: those from a specific target school (Individual School) and those from average schools (General). Please analyze the differences and similarities between the two groups and provide a concise conclusion that highlights any notable trends, unique findings, or possible explanations. Use the data below:

            ```
            Sources                        | Individual School                | General School
            -------------------------------------------------------------------------------
            Parent’s Expectation           | {context['family_expectations_A']}%     | {context['family_expectations_B']}%
            Peer Comparison                | {context['comparison_A']}%              | {context['comparison_B']}%
            Tight Study Schedule           | {context['tight_schedule_A']}%          | {context['tight_schedule_B']}%
            Examination Results            | {context['test_scores_A']}%             | {context['test_scores_B']}%
            Relationships                  | {context['relationships_A']}%           | {context['relationships_B']}%
            Own Prospect                   | {context['prospect_A']}%                | {context['prospect_B']}%
            Own Expectation                | {context['expectation_A']}%             | {context['expectation_B']}%
            Covid-19                       | {context['covid_19_A']}%                | {context['covid_19_B']}%
            Long Time Alone                | {context['long_term_solitude_A']}%      | {context['long_term_solitude_B']}%
            Changing Exam Time             | {context['unstable_class_A']}%          | {context['unstable_class_B']}%
            Unstable School Time           | {context['transfer_exam_A']}%           | {context['transfer_exam_B']}%
            ```

            Only provide the conclusion. Avoid repeating the table or listing all percentages again. Focus on patterns and implications related to student stress between the two school types.
            """