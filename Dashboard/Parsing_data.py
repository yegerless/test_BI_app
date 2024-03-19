import pandas as pd
from pathlib import Path

pd.set_option('display.max.columns', None)
pd.set_option('display.max.rows', None)


'Creating list of files with data'
p = Path(r'../Data')
file_list = [x for x in p.iterdir() if str(x).endswith('.xls')]





'Creating template for parsed table'
file = file_list[0]    # Need to chose file with max amount of columns. In ideal World there should be tables with same columns
df = pd.read_excel(file, engine='openpyxl')
columns = [col.replace('\n', ' ') for col in list(df.iloc[5])]
columns.insert(0, 'Source')    # Information about file-source of data in each row
df = pd.DataFrame(columns=columns)


'Unioning data from all files to one table'
for file in file_list:
    df_f = pd.read_excel(file, engine='openpyxl')
    columns = [col.replace('\n', ' ') for col in list(df_f.iloc[5])]    # Because we aren't in ideal World, it's important to create list of columns for each file
    df_f.columns = columns
    df_f = df_f[7:].reset_index(drop=True)    # Delete unuseless rows
    source = str(file)[str(file).rfind('\\') + 1:].replace('.xls', '')    # Creating comfortable name for file-source
    df_f['Source'] = source
    df_f.dropna(axis='index', subset=['Целевые показатели оценки эффективности реализации мероприятий'],
                inplace=True)    # Delete unuseless rows
    df = pd.concat([df, df_f])    # Unioning

df.reset_index(drop=True, inplace=True)
# df['№ п/п'] = df['№ п/п'].astype('str')


'Unpivotting df'
id_cols = ['Source', '№ п/п', 'Целевые показатели оценки эффективности реализации мероприятий', 'Единицы измерения', 'Периодичность представления']
val_cols = [col for col in df.columns if col.startswith('Фактическое')]
df = pd.melt(df, id_vars=id_cols, value_vars=val_cols, var_name='Attribute', value_name='Value_NI').dropna(axis='index', subset=['Value_NI']).reset_index(drop=True)


'Converting "X" -> 0 in column "Values" '
df.replace({'Value_NI':{'Х':0, '':0}}, inplace=True)
df['Value_NI'] = df['Value_NI'].fillna(value=0)

'Converting " " -> "_" in every string in column "Source" '
for i in range(len(df)):
    df.at[i, 'Source'] = df.at[i, 'Source'].replace(' ', '_')


'Creating date and previous year date column'
df[['Source_1', 'Source_2', 'Year', 'Hospital', 'Source_5', 'Source_6', 'Source_7', 'Source_8']] = df['Source'].str.split('_', expand=True)
df['Year'] = df['Year'].astype('int')
df['Month'] = 0
df['Day'] = 1

for i in range(len(df)):
    for j in range(1, 13):
        if str(j) in df.at[i, 'Attribute']:
            df.at[i, 'Month'] = j
    df.at[i, 'Year'] = df.at[i, 'Year'] + 2000

df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']], dayfirst=True)
df['Date_prev'] = df['Date'] - pd.DateOffset(months=1)

df.drop(columns=['Source', 'Year', 'Month', 'Day', 'Attribute', 'Source_1', 'Source_2',
                 'Source_5', 'Source_6', 'Source_7', 'Source_8'], inplace=True)


'Reorderind columns'
df = df[['Hospital', 'Date', 'Date_prev', 'Целевые показатели оценки эффективности реализации мероприятий',
         '№ п/п', 'Единицы измерения', 'Периодичность представления', 'Value_NI']]


'Merging df with copy of df to link the previous period'
df_prev = df[['Hospital', 'Date', 'Целевые показатели оценки эффективности реализации мероприятий',
         '№ п/п', 'Value_NI']].copy()
df_prev.rename({'Value_NI':'Value_prev', 'Date':'Date_prev'}, axis='columns', inplace=True)
df = df.merge(df_prev, how='left', on=['Hospital', 'Date_prev', 'Целевые показатели оценки эффективности реализации мероприятий', '№ п/п'])
df['Value_prev'] = df['Value_prev'].fillna(value=0)


'Changing hosp names to right'
hosp_dict = {'Боровичская':'ГОБУЗ "Боровичская ЦРБ"', 'Старорусская':'ГОБУЗ "Старорусская ЦРБ"', 'НОКБ':'ГОБУЗ "НОКБ"'}
df['Hospital'].replace(to_replace=hosp_dict, inplace=True)

'Creating actual value column'
def create_value(row):
    if row['Периодичность представления'] != '1 раз в месяц':
        val = row['Value_NI']
    elif row['Date'].month == 1:
        val = row['Value_NI']
    else:
        val = row['Value_NI'] - row['Value_prev']
    return val

df['Value'] = df.apply(create_value, axis=1)


df['Month_number'] = df['Date'].dt.month





if __name__ == '__main__':
    print(df.info())

    #df.to_excel(r'\\dfs-02\DKH_2\Gbmu\Новгород\Мониторинг_Новгород.xlsx')    # For cheking parsed table
