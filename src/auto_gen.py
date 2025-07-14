from doc import Config, DocumentGenerator

id_2_name = {
    10: "SKH Bishop Mok Sau Tseng Secondary School",
    # 11: "HHCKLA Buddhist Leung Chik Wai College",
    # 12: "Kwun Tong Kung Lok Government Secondary School",
    # 13: "Kowloon Tong School (Secondary School)",
    # 14: "TWGHs Chen Zao Men College",
    # 15: "Caritas Ma On Shan Secondary School",
    # 16: "Salem-Immanuel Lutheran College",
    # 18: "Shun Tak Fraternal Association Tam Pak Yu College",
    # 19: "The Church of Christ in China Kei To Secondary School",
    # 20: "Tack Ching Girls' Secondary School"
}


for key, value in id_2_name.items():
    config = Config(school_id=key, school_name=value, general_data_path="data/school_all.xlsx", output_path=f"output/25report_{key}_{value}.docx")
    generator = DocumentGenerator(config)
    generator.generate_report()