import pandas as pd
import emoji_generation as eg

bags_shape_groups = ['none', 'light', 'dark']
eye_size_groups = [2, 3, 4, 5, 6, 7]
mouth_shape_groups = ['sad', 'neutral', 'smile']
chin_size_groups = ['big', 'medium', 'small', 'none']
face_color_groups = ['#FFD700', '#EBCD00', '#D7C400', '#C4BA00']
brow_shape_groups = ['smile', 'neutral', 'frown']

def classify_region(df, region_name, method="quantiles"):
    if region_name not in df["Регион"].values:
        raise ValueError(f"Регион '{region_name}' не найден в данных.")
    
    groups = {}
    
    parameters = {
        "Рождаемость на 1000 человек населения": 3,
        "Доля населения с высшим образованием, %": 6,
        "Рейтинговый балл финансового благополучия населения": 3,
        "Рейтинговый балл приверженности населения ЗОЖ": 4,
        "Объем выбросов загрязняющих веществ, тыс. тонн": 4,
        "Уровень безработицы населения в возрасте 15 лет и старше, %": 3,
    }
    
    for column, n_groups in parameters.items():
        # Разбиение по квантилям
        labels = [i for i in range(n_groups)]
        group = pd.qcut(df[column], q=n_groups, labels=labels)[df["Регион"] == region_name].values[0]
        
        groups[column] = group

    bags_shape=bags_shape_groups[groups['Рождаемость на 1000 человек населения']]
    face_color=face_color_groups[groups['Объем выбросов загрязняющих веществ, тыс. тонн']]
    eye_size=eye_size_groups[groups['Доля населения с высшим образованием, %']]
    mouth_shape=mouth_shape_groups[groups['Рейтинговый балл финансового благополучия населения']]
    brow_shape=brow_shape_groups[groups['Уровень безработицы населения в возрасте 15 лет и старше, %']]
    chin_size=chin_size_groups[groups['Рейтинговый балл приверженности населения ЗОЖ']]
    

    eg.generate_emoji_svg(
        filename="emoji_custom.svg",
        face_color=face_color, 
        eye_size=eye_size, mouth_shape=mouth_shape,
        brow_shape=brow_shape,
        bags_shape=bags_shape,
        chin_size=chin_size
    )