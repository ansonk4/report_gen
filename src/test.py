import pandas as pd
from read_csv import csv_reader
import prompt_template
path = "data/2024 Final Data2.xlsx"
# df = pd.read_excel(path, header=2)

# df = df.loc[df["school_id"] == 10]

# combined_counts = (
#     pd.concat([
#         df['target_major1'],
#         df['target_major2'],
#         df['target_major3']
#     ])
#     .value_counts()
# )
top = {"all":0, "m":0, "f":0}
print(prompt_template.major_prompt(top, top))

# dis["percentage"] = dis["percentage"] / dis["percentage"].sum()
# dis["percentage"] = dis["percentage"].mul(100).round(1)
# print(dis)
# print(reader.df['family_expectations'].get_distribution())


