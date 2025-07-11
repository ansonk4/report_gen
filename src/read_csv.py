import pandas as pd
import numpy as np
from mapping import get_major_name, get_major_class, get_job_name, get_job_class

class csv_reader:
    def __init__(self, path:str, school_id=None) -> pd.DataFrame:
        df = pd.read_excel(path, header=2)

        df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
        df = df.replace(999, np.nan)
        
        if school_id:
            df = df.loc[df["school_id"] == school_id] 

        self.sample_size = len(df)
        self.raw_df = df.copy()

        df['gender'] = df['gender'].replace({1.0: 'm', 2.0: 'f'})
        df['gba_understanding'] = df['gba_understanding'].replace({1.0: False, 2.0: False, 3.0: True, 4.0: True}).astype(bool)
        # df['gba_understanding'] = df['gba_understanding'].replace({1.0: False, 2.0: True}).astype(bool)
        df['stem_participation'] = df['stem_participation'].replace({1.0: True, 2.0: False}).astype(bool)
        df['stress_scource'] = df['stress_scource'].replace({1.0: "personal", 2.0: "external"}).astype(str)
        df['stress_lv'] = df['stress_lv'].replace({1.0: "none", 2.0:"very_low", 3.0:"low", 4.0: "moderate", 5.0: "high", 6.0: "very_high"}).astype(str)
        df['endure_lv'] = df['endure_lv'].replace({4.0: "totally_can", 3.0:"mostly_can", 2.0: "mostly_cannot", 1.0:"totally_cannot"}).astype(str)

        for major in ['target_major1', 'target_major2', 'target_major3', 'dislike_major1', 'dislike_major2', 'dislike_major3']:
            df[major] = df[major].apply(get_major_name)
        for job in ['target_occupation1','target_occupation2','target_occupation3', 'dislike_occupation1', 'dislike_occupation2', 'dislike_occupation3']:
            df[job] = df[job].apply(get_job_name)

        self.df = df
  
    
    def combine_target(self, target_cols: list, target: str):
        '''
        Combine target columns into a single column 
        '''
        combined_df = self.df.melt(
            id_vars=['id', 'gender', 'gba_understanding', 'stem_participation'],
            value_vars=target_cols,
            var_name=f'{target}_order',
            value_name=target
        ).dropna(subset=[target])

        return combined_df
    
    def get_distribution(self, combined_df, target: str, group_by_col: str = None):
        if combined_df is None:
            combined_df = self.df

        if group_by_col:
            dis_df = pd.crosstab(combined_df[target], combined_df[group_by_col])

            # Count unique IDs for each gender
            unique_ids = combined_df.drop_duplicates(subset=['id'])
            groups_count = unique_ids[group_by_col].value_counts()

            dis_df = (dis_df.div(groups_count, axis=1) * 100).round(2)

            return dis_df

        dis_df = combined_df[target].value_counts().reset_index()
        dis_df['percentage'] = (dis_df['count'] / self.sample_size) * 100
        return dis_df.drop(columns='count')

    def sort_distribution(self, dis_df) -> list[pd.DataFrame]:
        return {col: dis_df.iloc[:, i].sort_values(ascending=False).to_frame().reset_index() for i, col in enumerate(dis_df.columns)}

    def check_class_match(self, target_class: str, groupby: str, major=True) -> tuple:
        '''
        Create a column indicating whether the row's major/job preference belongs to the target class,
        and return the distribution of this column grouped by the specified groupby column.
        The "groupby" column is a boolean collumn
        '''
        matches = []
        if major:
            for majors in ['target_major1', 'target_major2', 'target_major3']:
                # matches in all target
                matches.append(self.raw_df[majors].apply(lambda x: get_major_class(x) == target_class))
            # OR operation to check if any of the target majors match the target class
            self.df[f"have_{target_class}"] = sum(matches) > 0

        else:
            for jobs in ['target_occupation1', 'target_occupation2', 'target_occupation3']:
                matches.append(self.raw_df[jobs].apply(lambda x: get_job_class(x) == target_class))
            self.df[f"have_{target_class}"] = sum(matches) > 0

        # Group by the specified column and count occurrences of True/False
        distribution = self.df[f"have_{target_class}"].groupby(self.df[groupby]).value_counts(normalize=True)
        distribution = distribution.mul(100).round(1).to_frame().reset_index()

        # Get the proportion of that have the target class
        distribution = distribution[distribution[f"have_{target_class}"] == True]
        
        have_groupby = distribution[distribution[groupby] == True]['proportion'].values[0].item()
        no_groupby = distribution[distribution[groupby] == False]['proportion'].values[0].item()

        return have_groupby, no_groupby

    def get_percent(self, target_col: str, target_values: list, drop_zero=True) -> dict:
        '''
        return a dict {target_value0: protion0},
        protion0 is the protion of rows in self.df that its target_col equal to target_value0 in target_values
        '''
        dis = self.get_distribution(None, target_col)
        if drop_zero:
            dis = dis[dis[target_col] != 0]
        
        dis = dis[dis[target_col] != "nan"]
        dis["percentage"] = dis["percentage"] / dis["percentage"].sum()
        dis["percentage"] = dis["percentage"].mul(100).round(1)

        ret = {}
        for target_value in target_values:
            # if not target_value in target_col, set 0
            if not (dis[target_col] == target_value).any():
                ret[target_value] = 0.0
            else:
                ret[target_value] = dis[dis[target_col] == target_value]["percentage"].item()

        return ret
        # return {target_value: dis[dis[target_col] == target_value]["percentage"].item() for target_value in target_values}
   
    
if __name__ == "__main__":
    # csv_reader = csv_reader("data/2024 Final Data2.xlsx")
    csv = csv_reader("data/2024 Final Data2.xlsx", 10)
    gba_bus_major = csv.check_class_match("Business", "gba_understanding", major=True)
    gba_sci_major = csv.check_class_match("Science", "gba_understanding", major=True)
    print



