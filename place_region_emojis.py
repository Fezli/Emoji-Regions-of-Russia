import svgwrite
import os
import pandas as pd

df = pd.read_csv('result_tables/total_table.csv', sep=';')
ranked_df = df.copy()
ranked_df["Ранг рождаемости"] = df["Рождаемость на 1000 человек населения"].rank(ascending=False, method="min")
ranked_df["Ранг образования"] = df["Доля населения с высшим образованием, %"].rank(ascending=False, method="min")
ranked_df["Ранг финансов"] = df["Рейтинговый балл финансового благополучия населения"].rank(ascending=False, method="min")
ranked_df["Ранг ЗОЖ"] = df["Рейтинговый балл приверженности населения ЗОЖ"].rank(ascending=False, method="min")
ranked_df["Ранг загрязнения"] = df["Объем выбросов загрязняющих веществ, тыс. тонн"].rank(ascending=True, method="min")
ranked_df["Ранг безработицы"] = df["Уровень безработицы населения в возрасте 15 лет и старше, %"].rank(ascending=True, method="min")

def get_region_info(region_name):
    region_data = ranked_df[ranked_df["Регион"] == region_name]
    region_name = region_name.title().replace('Автономный Округ', 'автономный округ').replace('Край', 'край').replace('Область', 'область')
    
    if region_data.empty:
        return "Нет данных"
    
    info = f"""
    {region_name}
    🚼 Рождаемость: {region_data["Рождаемость на 1000 человек населения"].values[0]}  #{int(region_data["Ранг рождаемости"].values[0])}
    🎓 Образование: {region_data["Доля населения с высшим образованием, %"].values[0]}%  #{int(region_data["Ранг образования"].values[0])}
    💰 Финансы: {region_data["Рейтинговый балл финансового благополучия населения"].values[0]}  #{int(region_data["Ранг финансов"].values[0])}
    🏋️‍♂️ ЗОЖ: {region_data["Рейтинговый балл приверженности населения ЗОЖ"].values[0]}  #{int(region_data["Ранг ЗОЖ"].values[0])}
    🌍 Загрязнение: {region_data["Объем выбросов загрязняющих веществ, тыс. тонн"].values[0]}  #{int(region_data["Ранг загрязнения"].values[0])}
    📉 Безработица: {region_data["Уровень безработицы населения в возрасте 15 лет и старше, %"].values[0]}%  #{int(region_data["Ранг безработицы"].values[0])}
    """
    return info.strip()

pos_df = pd.read_csv('result_tables/regions_positions.csv', sep=';')
region_positions = {row["Регион"]: (row["Координата X"], row["Координата Y"]) for _, row in pos_df.iterrows()}

x_coords = [x for x, y in region_positions.values()]
y_coords = [y for x, y in region_positions.values()]
min_x, max_x = min(x_coords), max(x_coords)
min_y, max_y = min(y_coords), max(y_coords)
width, height = max_x - min_x, max_y - min_y

output_file = "regions_emojis.svg"
dwg = svgwrite.Drawing(output_file, profile="tiny", viewBox="-50 -50 1800 1100")

for region, (x, y) in region_positions.items():
    emoji_path = os.path.join("region_emojis", f"{region}.svg")
    group = dwg.g()
    group.add(dwg.image(emoji_path, insert=(x, y)))
    group.add(svgwrite.base.Title(get_region_info(region)))
    dwg.add(group)

dwg.save()

