import os
import pandas as pd
import classify_regions as cr

df = pd.read_csv('result_tables/total_table.csv', sep=';')

output_folder="region_emojis"

for region in df["Регион"]:
    filename = os.path.join(output_folder, f"{region}.svg")
    if not os.path.exists(filename):
        cr.classify_region(df, region)
        os.rename("emoji_custom.svg", filename)