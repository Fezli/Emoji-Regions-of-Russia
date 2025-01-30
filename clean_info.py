import pandas as pd
import numpy as np

from tabula import read_pdf


# Очистка таблицы "загрязнения 2020 стационар"
df_s = pd.read_excel('sources\загрязнения 2020 стационар.xlsx', header=1)
df_s = df_s.iloc[:, [0, 3]]
df_s = df_s.drop(index=0)
df_s.iloc[:, 0] = df_s.iloc[:, 0].str.strip().str.lower()

data_df = df_s.iloc[:, 0]


# Очистка таблицы "загрязнения 2020 передвиж"
tables = read_pdf('sources\загрязнения 2020 передвиж.pdf', pages='all', lattice=True)
df_p = pd.concat([tables[0], tables[1][2:]], ignore_index=True)
df_p = df_p.iloc[1:, [0, 24]]
df_p.iloc[:, 1] = df_p.iloc[:, 1].str.replace(' ', '').str.replace(',', '.').astype(float) * 1000

df_p = df_p.rename(columns={'Unnamed: 20': 'Объем выбросов загрязняющих веществ от передвижных источников за 2020 г., тонн'})

df_p.loc[df_p.iloc[:, 0] == 'г. Севастополь', 'Субъект РФ'] = 'Севастополь'
df_p.loc[df_p.iloc[:, 0] == 'Ханты-Мансийский автономный округ – Югра', 'Субъект РФ'] = 'Ханты-Мансийский автономный округ - Югра'
df_p.loc[df_p.iloc[:, 0] == 'Республика Северная Осетия-Алания', 'Субъект РФ'] = 'Республика Северная Осетия - Алания'

df_p.iloc[:, 0] = df_p.iloc[:, 0].str.strip().str.lower()


# Объединение таблиц "загрязнения 2020 стационар" и "загрязнения 2020 передвиж"
df = pd.merge(df_s, df_p, how='left', left_on='Регион', right_on='Субъект РФ')
df['Объем выбросов загрязняющих веществ, тонн'] = df.iloc[:, 1] + df.iloc[:, 3]
df['Объем выбросов загрязняющих веществ, тонн'] = (pd.to_numeric(df['Объем выбросов загрязняющих веществ, тонн'], errors='coerce') / 1000).round(2)
df = df.rename(columns={'Объем выбросов загрязняющих веществ, тонн': 'Объем выбросов загрязняющих веществ, тыс. тонн'})
df = df.iloc[:, [0, 4]]
df.to_csv('result_tables\\table_pollution.csv', index=False, sep=';')


# Очистка таблицы "безработица 17-23"
df = pd.read_excel('sources\безработица 17-23.xlsx', sheet_name=2, header=4)
df = df.iloc[:-2, [0, 4]]
df.iloc[:, 0] = df.iloc[:, 0].str.strip().str.lower()
df.iloc[:, 0] = df.iloc[:, 0].str.replace(r'^г\.\s*', '', regex=True).str.replace(r'"', '', regex=True).str.replace(r'^в том числе:\s*\n?', '', regex=True)
df = df.rename(columns={'Unnamed: 0': 'Регион', '20202)': 'Уровень безработицы населения в возрасте 15 лет и старше, %'})
df = pd.merge(data_df, df, how='left', left_on='Регион', right_on='Регион')
df.to_csv('result_tables\\table_unemploy.csv', index=False, sep=';')


# Очистка таблицы "образование 2020"
df = pd.read_excel('sources\образование 2020.xlsx', header=5)
df = df.iloc[:, [0, 2, 4]]
df = df.rename(columns={'Unnamed: 0': 'Регион', 'Unnamed: 2': 'Указавшие уровень образование', 'Unnamed: 4': 'Высшее'})

rows = df[(df['Регион'] == 'Городское и сельское население ')].index.tolist()
rows.extend((df[df['Регион'] == 'г. Санкт-Петербург'].index + 1).tolist())
rows.extend((df[df['Регион'] == 'г. Москва'].index + 1).tolist())
new_rows = []
for i in rows:
    new_rows.append(i - 1)
    new_rows.append(i)
    new_rows.append(i + 1)
result = df.iloc[new_rows]
df = result

df = df.reset_index()
df = df.drop('index', axis=1)

for i in range(len(result)):
    if i+2 < len(result) and pd.isna(df.iloc[i, 1]) and not pd.isna(df.iloc[i+2, 1]):
        df.iloc[i, 1] = df.iloc[i+2, 1]
        df.iloc[i, 2] = df.iloc[i+2, 2]
        df.iloc[i+2, 1] = np.nan
        df.iloc[i+2, 2] = np.nan

df = df[df.iloc[:, 1].notna()]
df = df.reset_index()
df = df.drop('index', axis=1)

df.iloc[:, 0] = df.iloc[:, 0].str.replace(r'^г\.\s*', '', regex=True).str.replace(' – Кузбасс', '').str.replace('–', '-').str.replace('\n', '')
df.iloc[:, 0] = df.iloc[:, 0].str.strip().str.lower()

df['Доля населения с высшим образованием, %'] = (df.iloc[:, 2] / df.iloc[:, 1]) * 100
df = df.drop(df.columns[[1, 2]], axis=1)
df['Доля населения с высшим образованием, %'] = pd.to_numeric(df['Доля населения с высшим образованием, %'], errors='coerce').round(2)

df = pd.merge(data_df, df, how='left', left_on='Регион', right_on='Регион')

df.to_csv('result_tables\\table_education.csv', index=False, sep=';')


# Очистка таблицы "рождаемость 2020"
df = pd.read_excel('sources\рождаемость 2020.xlsx', header=3)
df = df.iloc[:-1, [0, 4]]
df = df.rename(columns={'Unnamed: 0': 'Регион', 'родившихся.1': 'Рождаемость на 1000 человек населения'})
df.iloc[:, 0] = df.iloc[:, 0].str.replace(r'\s*г\.\s*', '', regex=True).str.replace(' – Кузбасс', '').str.replace('авт. округ – Югра', 'автономный округ - югра').str.replace('–', '-')
df.iloc[:, 0] = df.iloc[:, 0].str.strip().str.lower()

df = pd.merge(data_df, df, how='left', left_on='Регион', right_on='Регион')
df.to_csv('result_tables\\table_birth.csv', index=False, sep=';')

# Объединение всех таблиц в глобальную
df1 = pd.read_csv('result_tables\\table_birth.csv', sep=';')
df2 = pd.read_csv('result_tables\\table_education.csv', sep=';')
df3 = pd.read_csv('result_tables\\table_finance.csv', sep=';')
df4 = pd.read_csv('result_tables\\table_helth.csv', sep=';')
df5 = pd.read_csv('result_tables\\table_pollution.csv', sep=';')
df6 = pd.read_csv('result_tables\\table_unemploy.csv', sep=';')

df = df1.merge(df2, how='left', on='Регион').merge(df3, how='left', on='Регион').merge(df4, how='left', on='Регион').merge(df5, how='left', on='Регион').merge(df6, how='left', on='Регион')
df.to_csv('result_tables\\total_table.csv', index=False, sep=';')