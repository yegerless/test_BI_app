'''

Эта программа принимает для работы файлы excel (.xls, .xlsx).

Для этого скрипта требуются библиотеки: "pandas"- для работы с данными и модуль "pathlib" для работы с файловой системой

'''

import pandas as pd
from pathlib import Path

'''Установка параметров pandas для выведения без ограничений всех столбцов и строк'''
pd.set_option('display.max.columns', None)
pd.set_option('display.max.rows', None)


'''Создание списка файлов с данными типа .xls, находящиеся в папке Data'''
p = Path(r'./Data') #Создание объекта типа Path, представляющего путь к каталогу "Data" (с учетом текущей директории)
file_list = [x for x in p.iterdir() if str(x).endswith('.xls')] #Составление листа из объектов типа Path, которые указывают на файлы типа .xls
    # TODO добавить в перечень разрешенных форматов .xlsx (уточнить про .xlsm, .xlsb, .xltm, .xlam )
    # но если они не нужны, то строчку можно заменить на file_list = list(p.glob('*.xls'))


'''Создаем шаблон датафрейма на основе имеющихся таблиц'''
file = file_list[0] #Берем за основу первый файл Exel из списка
    # TODO Нужно выбрать файл с максимальным количеством столбцов
df = pd.read_excel(file, engine='openpyxl') #Cитывание данных из file в DataFrame pandas
columns = [col.replace('\n', ' ') for col in list(df.iloc[5])] #Редактируем и подготавливаем заголовки на основе имеющихся в таблице
columns.insert(0, 'Source')  # Добавляем в список будущих названий колонок 'Source', который будет содержать информацию об источнике данных каждой строки
df = pd.DataFrame(columns=columns) #Создаем новый DataFrame и присваиваем нужные названия колонок


'''Создаем DataFrame с данными из всех таблиц в корректном виде'''
for file in file_list: #С каждой таблицей по отдельности ...
    df_f = pd.read_excel(file, engine='openpyxl') #Cчитывание данных из file в DataFrame pandas
    columns = [col.replace('\n', ' ') for col in list(df_f.iloc[5])]#Редактируем и подготавливаем заголовки на основе имеющихся в таблице
                                                                    #Because we aren't in ideal World, it's important to create list of columns for each file
    df_f.columns = columns #Присваивание новых названий столбцов DataFrame
    df_f = df_f[7:].reset_index(drop=True)    # удаление ненужных строк и сброс индексов
    source = str(file)[str(file).rfind('\\') + 1:].replace('.xls', '')    # Creating comfortable name for file-source without ".xls"
    df_f['Source'] = source # Добавляем новую колонку,в которой лежит информация об источнике данных каждой строки
    df_f.dropna(axis='index', 
                subset=['Целевые показатели оценки эффективности реализации мероприятий'],
                inplace=True)    # Удаление строк, содержащих пустые значения в указанном столбце

    df = pd.concat([df, df_f],ignore_index=True)    # Объединение только что отредактированного DataFrame с основным
        #Скипнул строку df.reset_index(drop=True, inplace=True) #Сброс значений индексов
        #Заменил ее на ignore_index=True 

'''Переводим данные df в длинный формат'''
id_cols = ['Source', '№ п/п', 'Целевые показатели оценки эффективности реализации мероприятий', 'Единицы измерения', 'Периодичность представления'] 
# Создаем список заголовков для id
val_cols = [col for col in df.columns if col.startswith('Фактическое')] 
#Создаем список из всех заголовков, начинающихся с "Фактическое"
df = pd.melt(df, id_vars=id_cols, value_vars=val_cols, var_name='Attribute', value_name='Value_NI').dropna(axis='index', subset=['Value_NI']).reset_index(drop=True)
#Переформировываем данные из широкого формата в длинный с идентификаторами из списка id_cols и val_cols как столбцы отключения
#+ чистим строки с NaN

'''Чистим данные в df'''
df['Value_NI'].replace({'Х': 0, '': 0}, inplace=True) #Заменяем значений "X" и пустых строк в столбце "Value_NI" на 0
df['Value_NI'].fillna(value=0, inplace=True) #Удаляем строки с NaN

df['Source'] = df['Source'].str.replace(' ', '_') #Замещаем все пропуски в 'Source' символом '_'



'''Создание новых столбцов в том числе с датой'''
df[['Source_1', 'Source_2', 'Year', 'Hospital', 'Source_5', 'Source_6', 'Source_7', 'Source_8']] = df['Source'].str.split('_', expand=True)
#В новосозданные столбцы засовываем в том числе и данные из разбитого столбца 'Source'
df['Year'] = df['Year'].astype('int') #Делаем год int
df['Month'] = 0
df['Day'] = 1


'''Достаем корректную дату'''
'''Находим месяц и год'''
for index, row in df.iterrows():
    for j in range(1, 13):
        if str(j) in row['Attribute']: 
            df.at[index, 'Month'] = j #Находим месяц через совпадение в записях столбца 'Attribute' и вставляем совпавшее 
    df.at[index, 'Year'] = row['Year'] + 2000 #Корректируем год

df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']], dayfirst=True) #Собираем дату в одну колонку
df['Date_prev'] = df['Date'] - pd.DateOffset(months=1) #Создаем столбец 'Date_prev' с датой на один месяц меньше 

df.drop(columns=['Source', 'Year', 'Month', 'Day', 'Attribute', 'Source_1', 'Source_2',
                 'Source_5', 'Source_6', 'Source_7', 'Source_8'], inplace=True) #Чистим от лишних столбцов 


'''Reorderind columns'''
df = df[['Hospital', 'Date', 'Date_prev', 'Целевые показатели оценки эффективности реализации мероприятий',
         '№ п/п', 'Единицы измерения', 'Периодичность представления', 'Value_NI']]


'''??????????Merging df with copy of df to link the previous period'''
df_prev = df[['Hospital', 'Date', 'Целевые показатели оценки эффективности реализации мероприятий',
         '№ п/п', 'Value_NI']].copy() #Создали копию df, взяв только нужные столбцы 
df_prev.rename({'Value_NI':'Value_prev', 'Date':'Date_prev'}, axis='columns', inplace=True) #Переименовали колонны
df = df.merge(df_prev, how='left', on=['Hospital', 'Date_prev', 'Целевые показатели оценки эффективности реализации мероприятий', '№ п/п'])
df['Value_prev'] = df['Value_prev'].fillna(value=0) #Левым объединением добавили в основной df полученный малый


''''Changing hospital names to the correct ones'''
hosp_dict = {'Боровичская':'ГОБУЗ "Боровичская ЦРБ"', 'Старорусская':'ГОБУЗ "Старорусская ЦРБ"', 'НОКБ':'ГОБУЗ "НОКБ"'} 
#Создали словарь со старыми и новыми (корректными наименованиями)
df['Hospital'].replace(to_replace=hosp_dict, inplace=True) #Заменили значения строк на соотвествующие им в словаре



'????Creating actual value column'
def create_value(row):
    if row['Периодичность представления'] != '1 раз в месяц':
        val = row['Value_NI']
    elif row['Date'].month == 1:
        val = row['Value_NI']
    else:
        val = row['Value_NI'] - row['Value_prev']
    return val



df['Value'] = df.apply(create_value, axis=1) 
#Создаем новый столбец в df и заполняет его значениями из функции create_value


df['Month_number'] = df['Date'].dt.month #Добавляем месяц в окончательную таблицу


if __name__ == '__main__': #если мы в главной ветке, то сохраняем полученные данные в виде таблички 'Мониторинг_Новгород.xlsx'
    df.to_excel(r'Мониторинг_Новгород.xlsx') # For cheking parsed table
