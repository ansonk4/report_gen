from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from read_csv import csv_reader
from conclusion_gen import llm
import plotter
import prompt_template
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
for name in ["choreographer", "kaleido"]:
    logging.getLogger(name).setLevel(logging.CRITICAL)

@dataclass
class Config:
    """Configuration settings for the document generator."""
    template_path: str = "doc/template.docx"
    output_path: str = "doc/filled_report.docx"
    # school_data_path: str = "data/School 10.xlsx"
    school_data_path: str = None
    # general_data_path: str = "data/school_all.xlsx"
    general_data_path: str = "data/2024 Final Data2.xlsx"
    image_dir: str = "img"
    year: int = 2024
    school_name: str = "High School"
    school_id: int = 12


class DocumentGenerator:
    """Main class for generating school survey reports."""
    
    def __init__(self, config: Config):
        self.config = config
        self.doc = DocxTemplate(config.template_path)
        self.llm = llm(stop_all=False)
        if config.school_data_path is None:
            self.school_reader = csv_reader(config.general_data_path, config.school_id)
        else:
            self.school_reader = csv_reader(config.school_data_path)

        self.general_reader = csv_reader(config.general_data_path)
        self.context = self._initialize_context()
        self.school = config.school_name

    def _initialize_context(self) -> Dict[str, Any]:
        """Initialize the document context with basic information."""
        return {
            "year": self.config.year,
            "school": self.config.school_name,
            "respondents": self.school_reader.sample_size,
        }
    
    def generate_report(self) -> None:
        """Generate the complete report."""
        logger.info(f"Starting report generation for school {self.school} {self.config.school_id}...")
        
        self._process_majors()
        self._process_occupations()
        self._process_stem_analysis()
        self._process_gba_analysis()
        self._process_stress_analysis()
        self._format_percentages()
        self._render_document()
        
        logger.info(f"Report generated successfully: {self.config.output_path}")
            
    
    def _get_topk_groupby(self, target: str, target_cols: List[str], 
                         group_by_col: str, k: int) -> Dict[str, List[str]]:
        """Get top-k items grouped by a specific column."""
        combined_df = self.school_reader.combine_target(target_cols, target)
        dis_df = self.school_reader.get_distribution(combined_df, target, group_by_col)

        groupby_results = self.school_reader.sort_distribution(dis_df)
        all_result = self.school_reader.get_distribution(combined_df, target)
        
        def get_topk(df, k=5):
            return df[target].head(k).tolist()
        
        ret = {"all": get_topk(all_result, k)}
        for group, df in groupby_results.items():
            ret[group] = get_topk(df, k)
        
        return ret

    def _plot_factors_graph(self, factors: list[str], title: str, suffix: str, output_path: str) -> None:
        # Calculate percentage for each factor
        factor_percent = []
        for factor in factors:
            if f"{factor}{suffix}" not in self.school_reader.df.columns:
                factor_percent.append(0)
                continue
            percents = self.school_reader.get_percent(f"{factor}{suffix}", [1.0, 2.0], drop_zero=False)
            factor_percent.append(percents[1.0] + percents[2.0])

        # Plot bar chart for major factors
        plotter.bar_chart(
            x_values=factors,
            y_values=factor_percent,
            title=title,
            xtitle="Factors",
            ytitle="Percentage",
            output_path=output_path
        )

    def _process_majors(self) -> None:
        """Process major preference data."""
        try:
            logger.info("Processing major preferences...")

            target_cols = ['target_major1', 'target_major2', 'target_major3']
            top_majors = self._get_topk_groupby("major", target_cols, "gender", 10)

            dislike_cols = ['dislike_major1', 'dislike_major2', 'dislike_major3']
            top_dislike_majors = self._get_topk_groupby("dislike_major", dislike_cols, "gender", 10)
            
            self._populate_context_with_topk(top_majors, "major", "male_major", "female_major", 5)
            self._populate_context_with_topk(top_dislike_majors, "unpopular_major", "male_unpopular_major", "female_unpopular_major", 5)
            self._populate_context_with_topk(top_majors, "top_major", "top_male_major", "top_female_major")
            self._populate_context_with_topk(top_dislike_majors, "top_unpopular_major", "top_unpopular_male_major", "top_unpopular_female_major")

            # Generate conclusion
            self.context["major_conclusion"] = self.llm.generate(
                prompt_template.major_prompt(top_majors, top_dislike_majors)
            )
            # Plot major factor graph
            major_factors = [
                "personal_interests", "institute", "tuition",
                "scholarship", "career_prospect", "peers_and_teacher",
                "family", "salary", "DSE_result",
                "high_school_electives"
            ]
            output_path = "img/major_factors.png"
            self._plot_factors_graph(major_factors, "Major Selection Factors", "_A", output_path)
            self.context["major_factors_graph"] = InlineImage(self.doc, output_path, width=Mm(150))

        except Exception as e:
            logger.error(f"Error processing major preferences: {e}")
    
    def _process_occupations(self) -> None:
        """Process occupation preference data."""
        try:
            logger.info("Processing occupation preferences...")
            
            target_cols = ['target_occupation1', 'target_occupation2', 'target_occupation3']
            top_occupations = self._get_topk_groupby("occupation", target_cols, "gender", 10)
            dislike_cols = ['dislike_occupation1', 'dislike_occupation2', 'dislike_occupation3']
            top_dislike_occupations = self._get_topk_groupby("dislike_occupation", dislike_cols, "gender", 10)            
            
            self._populate_context_with_topk(top_occupations, "occupation", "male_occupation", "female_occupation", 5)
            self._populate_context_with_topk(top_dislike_occupations, "unpopular_occupation", "male_unpopular_occupation", "female_unpopular_occupation", 5)
            self._populate_context_with_topk(top_occupations, "top_occupation", "top_male_occupation", "top_female_occupation")
            self._populate_context_with_topk(top_dislike_occupations, "top_unpopular_occupation", "top_unpopular_male_occupation", "top_unpopular_female_occupation")

            # Generate conclusion
            self.context["occupations_conclusion"] = self.llm.generate(
                prompt_template.occupations_prompt(top_occupations, top_dislike_occupations)
            )
             # Plot major factor graph
            occupation_factors = [
                "personal_ability", "personal_interest", "sense_of_achievement", "family",
                "interpresonal_relationship", "job_nature", "remote_work", "worload",
                "working_environment", "salary_and_benefit", "promotion_opportunites",
                "career_prospect", "social_contribution", "social_status"
            ]
            output_path = "img/occpuation_factors.png"
            self._plot_factors_graph(occupation_factors, "Occpuation Selection Factors", "_B", output_path)
            self.context["occupation_factors_graph"] = InlineImage(self.doc, output_path, width=Mm(150))
            
        except Exception as e:
            logger.error(f"Error processing occupation preferences: {e}")
        
    def _process_stem_analysis(self) -> None:
        """Process STEM-related analysis."""
        try:
            logger.info("Processing STEM analysis...")
            
            # STEM skills analysis
            skill_categories = ["leadership", "teamwork", "creativity", "sci_knowledge", "problem_solving"]
            skill_mapping = {
                "leadership": ("leadership_strong", "leadership_par"),
                "teamwork": ("teamwork_strong", "teamwork_par"),
                "creativity": ("creative_strong", "creative_par"),
                "sci_knowledge": ("knowledge_strong", "knowledge_par"),
                "problem_solving": ("prob_solving_strong", "prob_solving_par")
            }
            
            for skill in skill_categories:
                percentages = self.school_reader.get_percent(skill, [1.0, 2.0])
                strong_key, par_key = skill_mapping[skill]
                self.context[strong_key] = percentages[1]
                self.context[par_key] = percentages[2]
            
            self.context["have_stem"]  = self.school_reader.df['stem_participation'].sum()
            self.context["no_stem"]  = (~self.school_reader.df['stem_participation']).sum()

            # STEM major preferences
            self._analyze_stem_preferences("major", True, "_A", "img/stem_major.png", "stem_graph_1")
            
            # STEM job preferences
            self._analyze_stem_preferences("occupation", False, "_B", "img/stem_job.png", "stem_graph_2")
            
            # Generate STEM conclusion
            self.context['stem_conclusion'] = self.llm.generate(
                prompt_template.stem_conclusion_prompt(self.context)
            )

        except Exception as e:
            logger.error(f"Error processing STEM analysis: {e}")
    
    def _process_gba_analysis(self) -> None:
        """Process GBA (Global Business Administration) analysis."""
        try:
            logger.info("Processing GBA analysis...")
        
            # GBA major analysis
            gba_bus_major = self.school_reader.check_class_match("Business", "gba_understanding", major=True)
            gba_sci_major = self.school_reader.check_class_match("Science", "gba_understanding", major=True)

            self.context['gba_bus_A'], self.context['no_gba_bus_A'] = gba_bus_major
            self.context['gba_sci_A'], self.context['no_gba_sci_A'] = gba_sci_major
            self.context['bus_diff_A'] = self.context['gba_bus_A'] - self.context['no_gba_bus_A']
            self.context['gba_sci_diff_A'] = self.context['gba_sci_A'] - self.context['no_gba_sci_A']
            
            # GBA job analysis
            gba_jobs = {
                "Business": self.school_reader.check_class_match("Business", "gba_understanding", major=False),
                "Engineering": self.school_reader.check_class_match("Engineering", "gba_understanding", major=False),
                "Science": self.school_reader.check_class_match("Science", "gba_understanding", major=False)
            }
            
            self.context['gba_bus_B'], self.context['no_gba_bus_B'] = gba_jobs["Business"]
            self.context['gba_eng'], self.context['no_gba_eng'] = gba_jobs["Engineering"]
            self.context['gba_sci_B'], self.context['no_gba_sci_B'] = gba_jobs["Science"]
            
            # Calculate differences
            self.context['bus_diff_B'] = self.context['gba_bus_B'] - self.context['no_gba_bus_B']
            self.context['gba_eng_diff'] = self.context['gba_eng'] - self.context['no_gba_eng']
            self.context['gba_sci_diff_B'] = self.context['gba_sci_B'] - self.context['no_gba_sci_B']
            
            # Generate GBA conclusion
            self.context['gba_conclusion'] = self.llm.generate(
                prompt_template.gba_conclusion_prompt(self.context)
            )
        except Exception as e:
            logger.error(f"Error processing GBA analysis: {e}")

    
    def _process_stress_analysis(self) -> None:
        """Process stress-related analysis."""
        logger.info("Processing stress analysis...")
        
        # Stress source analysis
        stress_factor = self.school_reader.get_percent("stress_scource", ["personal", "external"])
        general_stress_factor = self.general_reader.get_percent("stress_scource", ["personal", "external"])
        
        self.context['personal_A'], self.context['external_A'] = stress_factor["personal"], stress_factor["external"]
        self.context['personal_B'], self.context['external_B'] = general_stress_factor["personal"], general_stress_factor["external"]
        
        # Detailed stress sources
        self._analyze_stress_sources()
        
        # Stress level distribution
        self._analyze_stress_levels()
        
        # Stress endurance levels
        self._analyze_endurance_levels()
        
        # Stress management methods
        self._analyze_stress_methods()
        
        # Generate stress conclusion
        self.context['stress_sources_conclusion'] = self.llm.generate(
            prompt_template.stress_sources_prompt(self.context)
        )
    
    def _populate_context_with_topk(self, data: Dict[str, List[str]], 
                                   all_key: str, male_key: str, female_key: str, k: int=99999) -> None:
        """Populate context with top-k data for all, male, and female categories."""
        for i, item in enumerate(data["all"]):
            if i >= k:
                break
            self.context[f'{all_key}_{i}'] = item

        if "m" in data:
            for i, item in enumerate(data["m"]):
                if i >= k:
                    break
                self.context[f'{male_key}_{i}'] = item

        if "f" in data:
            for i, item in enumerate(data["f"]):
                if i >= k:
                    break
                self.context[f'{female_key}_{i}'] = item

    def _analyze_stem_preferences(self, category: str, is_major: bool, suffix: str, 
                                 image_path: str, graph_key: str) -> None:
        """Analyze STEM preferences for majors or occupations."""
        stem_sci = self.school_reader.check_class_match("Science", "stem_participation", major=is_major)
        stem_eng = self.school_reader.check_class_match("Engineering", "stem_participation", major=is_major)
        
        # Store results in context
        self.context[f'stem_eng{suffix}'], self.context[f'no_stem_eng{suffix}'] = stem_eng
        self.context[f'stem_sci{suffix}'], self.context[f'no_stem_sci{suffix}'] = stem_sci
        
        # Calculate differences and totals
        self.context[f'eng_diff{suffix}'] = self.context[f'stem_eng{suffix}'] - self.context[f'no_stem_eng{suffix}']
        self.context[f'sci_diff{suffix}'] = self.context[f'stem_sci{suffix}'] - self.context[f'no_stem_sci{suffix}']
        self.context[f'stem_total{suffix}'] = self.context[f'stem_eng{suffix}'] + self.context[f'stem_sci{suffix}']
        self.context[f'no_stem_total{suffix}'] = self.context[f'no_stem_eng{suffix}'] + self.context[f'no_stem_sci{suffix}']
        self.context[f'total_diff{suffix}'] = self.context[f'eng_diff{suffix}'] + self.context[f'sci_diff{suffix}']
        
        # Generate chart
        x_values = ["Engineering", "Science", "Total"]
        stem_values = {
            "Engineering": self.context[f'stem_eng{suffix}'],
            "Science": self.context[f'stem_sci{suffix}'],
            "Total": self.context[f'stem_total{suffix}']
        }
        no_stem_values = {
            "Engineering": self.context[f'no_stem_eng{suffix}'],
            "Science": self.context[f'no_stem_sci{suffix}'],
            "Total": self.context[f'no_stem_total{suffix}']
        }
        
        title = f"{category.title()} Preference"
        plotter.double_bar_chart(x_values, stem_values, no_stem_values, title, None, 
                                "Have STEM", "No STEM", image_path)
        
        self.context[graph_key] = InlineImage(self.doc, image_path, width=Mm(80))
    
    def _analyze_stress_sources(self) -> None:
        """Analyze detailed stress sources."""
        stress_sources = [
            "family_expectations", "comparison", "tight_schedule", "test_scores",
            "relationships", "prospect", "expectation", "long_term_solitude",
            "covid_19", "unstable_class", "transfer_exam"
        ]
        
        stress_sources_values = {}
        avg_stress_sources_values = {}
        
        for source in stress_sources:
            school_value = self.school_reader.get_percent(source, [1.0], drop_zero=False)[1.0]
            general_value = self.general_reader.get_percent(source, [1.0], drop_zero=False)[1.0]
            
            self.context[f"{source}_A"] = school_value
            self.context[f"{source}_B"] = general_value
            stress_sources_values[source] = school_value
            avg_stress_sources_values[source] = general_value
        
        # Generate stress sources chart
        plotter.double_bar_chart(
            stress_sources, stress_sources_values, avg_stress_sources_values,
            f"Stress Sources: {self.config.school_name} vs Average", "Stress Sources",
            "Target School", 'Average', "img/stress_sources.png"
        )
        
        self.context["stress_sources_graph"] = InlineImage(
            self.doc, "img/stress_sources.png", width=Mm(150)
        )
    
    def _analyze_stress_levels(self) -> None:
        """Analyze stress level distribution."""
        stress_levels = ["none", "very_low", "low", "moderate", "high", "very_high"]
        
        stress_lv_distribution = self.school_reader.get_percent("stress_lv", stress_levels, drop_zero=False)
        general_stress_lv_distribution = self.general_reader.get_percent("stress_lv", stress_levels, drop_zero=False)
        
        for level in stress_levels:
            self.context[f"{level}_A"] = stress_lv_distribution[level]
            self.context[f"{level}_B"] = general_stress_lv_distribution[level]
        
        # Generate stress level chart
        plotter.double_bar_chart(
            stress_levels, stress_lv_distribution, general_stress_lv_distribution,
            f"Stress Level: {self.config.school_name} vs Average", "Stress Level",
            "Target School", 'Average', "img/stress_level_distribution.png"
        )
        
        self.context["stress_lv_graph"] = InlineImage(
            self.doc, "img/stress_level_distribution.png", width=Mm(150)
        )
    
    def _analyze_endurance_levels(self) -> None:
        """Analyze stress endurance levels."""
        endure_levels = ["totally_cannot", "mostly_cannot", "mostly_can", "totally_can"]
        
        endure_lv_distribution = self.school_reader.get_percent("endure_lv", endure_levels, drop_zero=False)
        general_endure_lv_distribution = self.general_reader.get_percent("endure_lv", endure_levels, drop_zero=False)

        for level in endure_levels:
            self.context[f"{level}_A"] = endure_lv_distribution[level]
            self.context[f"{level}_B"] = general_endure_lv_distribution[level]
        
        # Generate endurance level chart
        plotter.double_bar_chart(
            endure_levels, endure_lv_distribution, general_endure_lv_distribution,
            f"Endure Stress Level: {self.config.school_name} vs Average", "Level",
            "Target School", 'Average', "img/endure_level_distribution.png"
        )
        
        self.context["endure_graph"] = InlineImage(
            self.doc, "img/endure_level_distribution.png", width=Mm(150)
        )
    
    def _analyze_stress_methods(self) -> None:
        """Analyze stress management methods."""
        stress_methods = [
            "exercise", "family_communication", "friends_communication", "social_workers",
            "restructuring_ttb", "video_games", "sleep", "music", "no_idea"
        ]
        school_values = {}
        for method in stress_methods:
            school_value = self.school_reader.get_percent(method, [1.0], drop_zero=False)[1.0]
            general_value = self.general_reader.get_percent(method, [1.0], drop_zero=False)[1.0]
            school_values[method] = school_value
            self.context[f"{method}_A"] = school_value
            self.context[f"{method}_B"] = general_value

        plotter.pie_chart(stress_methods, school_values, f"Stress Relieve Method: {self.school}", "img/stress_method.png")
        self.context["stress_graph"] = InlineImage(
            self.doc, "img/stress_method.png", width=Mm(150)
        )

    def _format_percentages(self) -> None:
        """Format all float values as percentages."""
        for key, value in self.context.items():
            if isinstance(value, float):
                self.context[key] = f"{round(value, 1)}%"
    
    def _render_document(self) -> None:
        """Render and save the final document."""
        logger.info("Rendering document...")
        self.doc.render(self.context)
        self.doc.save(self.config.output_path)

def main():
    """Main function to run the document generator."""
    config = Config()
    generator = DocumentGenerator(config)
    generator.generate_report()


if __name__ == "__main__":
    main()