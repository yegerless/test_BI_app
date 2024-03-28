import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from Dashboard.Parsing_data import df

months_dict = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
               7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

def choose_hospital_ASC(year, month, input_hospital):
    month_range = range(month[0], month[1])
    # Всего ОКС
    total_ACS = df.loc[(df['№ п/п'] == 47) &
                       (df['Date'].dt.to_period('Y') == year) &
                       (df['Date'].dt.month.isin(month_range)) &
                       (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # Кол-во ОКС с подъемом ST
    ACS_with_elevation_ST = df.loc[(df['№ п/п'] == '47.1') &
                                   (df['Date'].dt.to_period('Y') == year) &
                                   (df['Date'].dt.month.isin(month_range)) &
                                   (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # Кол-во ОКС без подъема ST
    ACS_without_elevation_ST = df.loc[(df['№ п/п'] == '47.2') &
                                      (df['Date'].dt.to_period('Y') == year) &
                                      (df['Date'].dt.month.isin(month_range)) &
                                      (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # График ОКС
    months_ACS_with_eST = df.loc[(df['№ п/п'] == '47.1') &
                                 (df['Date'].dt.to_period('Y') == year) &
                                 (df['Date'].dt.month.isin(month_range)) &
                                 (df['Hospital'].isin(input_hospital)), 'Month_number'].replace(months_dict).unique()
    cnt_ACS_with_eST = df.loc[(df['№ п/п'] == '47.1') &
                                 (df['Date'].dt.to_period('Y') == year) &
                                 (df['Date'].dt.month.isin(month_range)) &
                                 (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                            groupby('Month_number')['Value'].sum().reset_index(). \
                            sort_values(by='Month_number', axis='index').replace(months_dict)
    months_ACS_without_eST = df.loc[(df['№ п/п'] == '47.2') &
                                 (df['Date'].dt.to_period('Y') == year) &
                                 (df['Date'].dt.month.isin(month_range)) &
                                 (df['Hospital'].isin(input_hospital)), 'Month_number'].replace(months_dict).unique()
    cnt_ACS_without_eST = df.loc[(df['№ п/п'] == '47.2') &
                                 (df['Date'].dt.to_period('Y') == year) &
                                 (df['Date'].dt.month.isin(month_range)) &
                                 (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                            groupby('Month_number')['Value'].sum().reset_index(). \
                            sort_values(by='Month_number', axis='index').replace(months_dict)
    cnt_all_ACS = df.loc[(df['№ п/п'] == 47) &
                         (df['Date'].dt.to_period('Y') == year) &
                         (df['Date'].dt.month.isin(month_range)) &
                         (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                        groupby('Month_number')['Value'].sum().reset_index()
    cnt_all_ACS_mortality = df.loc[(df['№ п/п'] == 44) &
                               (df['Date'].dt.to_period('Y') == year) &
                               (df['Date'].dt.month.isin(month_range)) &
                               (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                        groupby('Month_number')['Value'].sum().reset_index()
    df_ACS_mortality_rate = cnt_all_ACS.merge(cnt_all_ACS_mortality, how='inner', on=['Month_number'])
    df_ACS_mortality_rate['Value'] = round(df_ACS_mortality_rate['Value_y'] / df_ACS_mortality_rate['Value_x'] * 100, 2)
    df_ACS_mortality_rate = df_ACS_mortality_rate.sort_values(by='Month_number', axis='index')
    df_ACS_mortality_rate['Month'] = df_ACS_mortality_rate['Month_number'].replace(months_dict)
    ACS_fig = make_subplots(specs=[[{'secondary_y': True}]])
    ACS_fig.add_trace(go.Bar(name='ОКС с подъемом ST', x=months_ACS_with_eST, y=cnt_ACS_with_eST['Value'], text=cnt_ACS_with_eST['Value'],
                          textposition='auto', marker_color='SteelBlue', hoverinfo='text'), secondary_y=False)
    ACS_fig.add_trace(go.Bar(name='ОКС без подъема ST', x=months_ACS_without_eST, y=cnt_ACS_without_eST['Value'], text=cnt_ACS_without_eST['Value'],
                          textposition='auto',  marker_color='PaleTurquoise', hoverinfo='text'), secondary_y=False)
    ACS_fig.update_layout(barmode='stack')
    ACS_fig.update_traces(textfont_size=16)
    ACS_fig.add_trace(go.Scatter(x=df_ACS_mortality_rate['Month'], y=df_ACS_mortality_rate['Value'], mode='lines+text',
                                 name='Летальность ОКС', marker_color='red', text=[f'{x / 100:.1%}' for x in df_ACS_mortality_rate['Value']],
                                 textfont={'family': 'Arial', 'size': 10, 'color': 'Black'},
                                 textposition='top center', hoverinfo='text'),
                      secondary_y=True)
    ACS_fig.update_layout(yaxis={'visible': False, 'showticklabels': False}, yaxis2={'visible': False, 'showticklabels': False}, 
                          title={'text': '<b>Динамика количества ОКС и летальности при ОКС за выбранный год</b>',
                                 'font': {'family': 'Arial', 'size': 24, 'color': 'Black'}, 'x': 0.5, 'y': 0.85}, 
                          plot_bgcolor='white', margin={'l': 30, 'r': 0, 't': 100, 'b': 0}, 
                          legend={'x': 0.93, 'y': 0.5, 'traceorder': 'reversed', 'font': {'family': 'Arial', 'size': 14, 'color': 'Black'}, 
                                  'yanchor': 'top', 'xanchor': 'left'})


    # Охват ЧКВ
    PTCA_cnt = df.loc[(df['№ п/п'] == '39.1') &
                      (df['Date'].dt.to_period('Y') == year) &
                      (df['Date'].dt.month.isin(month_range)) &
                      (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    PCI_coverage = round(PTCA_cnt / total_ACS, 3) if total_ACS > 0 else 0

    # Летальность при ОКС
    ACS_mortality_abs = df.loc[(df['№ п/п'] == 44) &
                               (df['Date'].dt.to_period('Y') == year) &
                               (df['Date'].dt.month.isin(month_range)) &
                               (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_mortality_rate = round(ACS_mortality_abs / total_ACS, 3) if total_ACS > 0 else 0

    # Летальность при ИМ
    MI_mortality_abs = df.loc[(df['№ п/п'] == 48) &
                              (df['Date'].dt.to_period('Y') == year) &
                              (df['Date'].dt.month.isin(month_range)) &
                              (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    total_MI = df.loc[(df['№ п/п'] == 49) &
                      (df['Date'].dt.to_period('Y') == year) &
                      (df['Date'].dt.month.isin(month_range)) &
                      (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    MI_mortality_rate = round(MI_mortality_abs / total_MI, 3) if total_MI > 0 else 0

    # График динамики выбывших и летальности при ИМ
    months_MI = df.loc[(df['№ п/п'] == 49) &
                    (df['Date'].dt.to_period('Y') == year) &
                    (df['Date'].dt.month.isin(month_range)) &
                    (df['Hospital'].isin(input_hospital)), 'Month_number'].replace(months_dict).unique()
    cnt_MI = df.loc[(df['№ п/п'] == 49) &
                    (df['Date'].dt.to_period('Y') == year) &
                    (df['Date'].dt.month.isin(month_range)) &
                    (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                            groupby('Month_number')['Value'].sum().reset_index()
    cnt_MI_mortality = df.loc[(df['№ п/п'] == 48) &
                                   (df['Date'].dt.to_period('Y') == year) &
                                   (df['Date'].dt.month.isin(month_range)) &
                                   (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                            groupby('Month_number')['Value'].sum().reset_index()
    df_MI_mortality_rate = cnt_MI.merge(cnt_MI_mortality, how='inner', on=['Month_number'])
    df_MI_mortality_rate['Value'] = round(df_MI_mortality_rate['Value_y'] / df_MI_mortality_rate['Value_x'] * 100, 2)
    df_MI_mortality_rate = df_MI_mortality_rate.sort_values(by='Month_number', axis='index')
    df_MI_mortality_rate['Month'] = df_MI_mortality_rate['Month_number'].replace(months_dict)
    MI_fig = make_subplots(specs=[[{'secondary_y': True}]])
    MI_fig.add_trace(go.Bar(name='Кол-во выбывших при ИМ', x=months_MI, y=cnt_MI['Value'], text=cnt_MI['Value'],
                          textposition='auto', marker_color='Khaki', hoverinfo='text'), secondary_y=False)
    MI_fig.update_traces(textfont_size=16)
    MI_fig.add_trace(go.Scatter(x=df_MI_mortality_rate['Month'], y=df_MI_mortality_rate['Value'], mode='lines+text',
                                 name='Летальность ОКС', marker_color='red', text=[f'{x / 100:.1%}' for x in df_MI_mortality_rate['Value']],
                                 textfont={'family': 'Arial', 'size': 10, 'color': 'Black'},
                                 textposition='top center', hoverinfo='text'),
                      secondary_y=True)
    MI_fig.update_layout(yaxis={'visible': False, 'showticklabels': False}, yaxis2={'visible': False, 'showticklabels': False}, 
                         title={'text': '<b>Динамика количества выбывших и летальности при ИМ за выбранный год</b>', 
                                'font': {'family': 'Arial', 'size': 24, 'color': 'Black'}, 'x': 0.5, 'y': 0.85},
                                plot_bgcolor='white', margin={'l': 30, 'r': 0, 't': 100, 'b': 0}, 
                          legend={'x': 0.94, 'y': 0.5, 'traceorder': 'reversed', 'font': {'family': 'Arial', 'size': 14, 'color': 'Black'}, 
                                  'yanchor': 'top', 'xanchor': 'left'})

    # График путь больного ОКС с подъемом ST
    ACS_with_elevation_ST_12_h_delivery = df.loc[(df['№ п/п'] == 34) &
                                                 (df['Date'].dt.to_period('Y') == year) &
                                                 (df['Date'].dt.month.isin(month_range)) &
                                                 (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_with_elevation_ST_12_h_PCI = df.loc[(df['№ п/п'] == '39.1.2.1') &
                                            (df['Date'].dt.to_period('Y') == year) &
                                            (df['Date'].dt.month.isin(month_range)) &
                                            (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_path_data = {'number': [ACS_with_elevation_ST, ACS_with_elevation_ST_12_h_delivery,
                                ACS_with_elevation_ST_12_h_PCI],
                     'stage': ['Всего', 'Доставлено за 12 часов', 'ЧКВ за 12 часов']}
    ACS_path_funnel_fig = px.funnel(ACS_path_data, x='number', y='stage')
    ACS_path_funnel_fig.update_layout(plot_bgcolor='white', margin={'l': 0, 'r': 0, 't': 50, 'b': 0}, 
                                      title={'x': 0.5, 'y': 0.9, 'text': '<b>Путь больного с ОКСпST</b>', 'font': {'family': 'Arial', 'size': 20, 'color': 'Black'}, 
                                             'yanchor': 'bottom', 'xanchor': 'center'})

    # Кол-во умерших при ОКСпST
    cnt_deaths_ACS_with_eST = df.loc[(df['№ п/п'] == '44.1') &
                                     (df['Date'].dt.to_period('Y') == year) &
                                     (df['Date'].dt.month.isin(month_range)) &
                                     (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # Летальность при ОКСпST
    ACS_with_eST_mortality_rate = round(cnt_deaths_ACS_with_eST / ACS_with_elevation_ST, 3) if ACS_with_elevation_ST > 0 else 0

    # Летальность пациентов идеального пути при ОКСпST
    cnt_deaths_ACS_with_eST_ideal_path = df.loc[(df['№ п/п'] == '42.1.2.1') &
                                         (df['Date'].dt.to_period('Y') == year) &
                                         (df['Date'].dt.month.isin(month_range)) &
                                         (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_with_eST_ideal_path_mortality_rate = round(cnt_deaths_ACS_with_eST_ideal_path / ACS_with_elevation_ST, 3) if ACS_with_elevation_ST > 0 else 0

    # Доля умерших без реваскуляризации от всех пациентов с ОКСпST
    cnt_deaths_ACS_with_eST_CABG = df.loc[(df['№ п/п'] == '43.1.1') &
                                   (df['Date'].dt.to_period('Y') == year) &
                                   (df['Date'].dt.month.isin(month_range)) &
                                   (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_deaths_ACS_with_eST_PCI = df.loc[(df['№ п/п'] == '42.1.2') &
                                  (df['Date'].dt.to_period('Y') == year) &
                                  (df['Date'].dt.month.isin(month_range)) &
                                  (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_deaths_ACS_with_eST_Thrombolysis = df.loc[(df['№ п/п'] == '42.1.4') &
                                           (df['Date'].dt.to_period('Y') == year) &
                                           (df['Date'].dt.month.isin(month_range)) &
                                           (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_deaths_ACS_with_eST_without_revasc = cnt_deaths_ACS_with_eST - cnt_deaths_ACS_with_eST_CABG - \
                                      cnt_deaths_ACS_with_eST_PCI - cnt_deaths_ACS_with_eST_Thrombolysis
    ACS_with_eST_without_revasc_deaths_part = \
        round(cnt_deaths_ACS_with_eST_without_revasc / cnt_deaths_ACS_with_eST, 3) if cnt_deaths_ACS_with_eST > 0 else 0

    # График ОКСбпST высокого и низкого риска
    cnt_ACS_without_eST_high_risk = df.loc[(df['№ п/п'] == '47.2.1') &
                                           (df['Date'].dt.to_period('Y') == year) &
                                           (df['Date'].dt.month.isin(month_range)) &
                                           (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_ACS_without_eST_low_risk = df.loc[(df['№ п/п'] == '47.2.2') &
                                           (df['Date'].dt.to_period('Y') == year) &
                                           (df['Date'].dt.month.isin(month_range)) &
                                           (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_with_eST_risk_fig = go.Figure(
        data=[
            go.Bar(x=['Высокий риск', 'Низкий риск'], y=[cnt_ACS_without_eST_high_risk, cnt_ACS_without_eST_low_risk],
                   text=[cnt_ACS_without_eST_high_risk, cnt_ACS_without_eST_low_risk], textfont=dict(size=18, color="black"), marker_color=['#FFBAA0', '#8BDDB8'], 
                   hoverinfo='text')
        ])
    ACS_with_eST_risk_fig.update_layout(yaxis={'visible': False, 'showticklabels': False}, plot_bgcolor='white', margin={'l': 0, 'r': 0, 't': 50, 'b': 0}, 
                                        title={'x': 0.5, 'y': 0.9, 'text': '<b>ОКСбпST по степени риска</b>', 'font': {'family': 'Arial', 'size': 20, 'color': 'Black'}, 
                                               'yanchor': 'bottom', 'xanchor': 'center'})

    # Охват ЧКВ при ОКСбпST высокого риска
    cnt_PTCA_ACS_without_eST_high_risk = df.loc[(df['№ п/п'] == '39.1.1.1') &
                                                (df['Date'].dt.to_period('Y') == year) &
                                                (df['Date'].dt.month.isin(month_range)) &
                                                (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_without_eST_high_risk_PTCA_coverage = \
        round(cnt_PTCA_ACS_without_eST_high_risk / cnt_ACS_without_eST_high_risk, 3) \
            if cnt_ACS_without_eST_high_risk > 0 else 0

    # Летальность при ОКСбпST высокого риска
    cnt_deaths_ACS_without_eST_high_risk = df.loc[(df['№ п/п'] == '44.2.1') &
                                                  (df['Date'].dt.to_period('Y') == year) &
                                                  (df['Date'].dt.month.isin(month_range)) &
                                                  (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_without_eST_high_risk_mortality_rate = \
        round(cnt_deaths_ACS_without_eST_high_risk / cnt_ACS_without_eST_high_risk, 3) \
            if cnt_ACS_without_eST_high_risk > 0 else 0

    # Охват ЧКВ при ОКСбпST низкого риска
    cnt_PTCA_ACS_without_eST_low_risk = df.loc[(df['№ п/п'] == '39.1.1.2') &
                                                  (df['Date'].dt.to_period('Y') == year) &
                                                  (df['Date'].dt.month.isin(month_range)) &
                                                  (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_without_eST_low_risk_PTCA_coverage = \
        round(cnt_PTCA_ACS_without_eST_low_risk / cnt_ACS_without_eST_low_risk, 3) \
            if cnt_ACS_without_eST_low_risk > 0 else 0


    # Летальность при ОКСбпST низкого риска
    cnt_deaths_ACS_without_eST_low_risk = df.loc[(df['№ п/п'] == '44.2.1') &
                                                 (df['Date'].dt.to_period('Y') == year) &
                                                 (df['Date'].dt.month.isin(month_range)) &
                                                 (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_without_eST_high_risk_mortality_rate = \
        round(cnt_deaths_ACS_without_eST_low_risk / cnt_ACS_without_eST_low_risk, 3) \
            if cnt_ACS_without_eST_low_risk > 0 else 0

    # Кол-во ОКС с шоком
    cnt_shock = df.loc[(df['№ п/п'] == '47.3') &
                       (df['Date'].dt.to_period('Y') == year) &
                       (df['Date'].dt.month.isin(month_range)) &
                       (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # График шок
    cnt_shock_ACS_with_eST = df.loc[(df['№ п/п'] == '47.3.1') &
                                    (df['Date'].dt.to_period('Y') == year) &
                                    (df['Date'].dt.month.isin(month_range)) &
                                    (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_shock_ACS_without_eST = df.loc[(df['№ п/п'] == '47.3.2') &
                                       (df['Date'].dt.to_period('Y') == year) &
                                       (df['Date'].dt.month.isin(month_range)) &
                                       (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    part_shock_ACS_with_eST = round(cnt_shock_ACS_with_eST / cnt_shock, 3) if cnt_shock > 0 else 0
    part_shock_ACS_without_eST = round(cnt_shock_ACS_without_eST / cnt_shock, 3) if cnt_shock > 0 else 0
    Shock_fig = go.Figure(
        data=[
            go.Bar(name='Шок ОКСпST', y=[part_shock_ACS_with_eST], text=f'{part_shock_ACS_with_eST:.1%}',
                   marker_color='SteelBlue', textposition='inside', hoverinfo='text'),
            go.Bar(name='Шок ОКСбпST', y=[part_shock_ACS_without_eST], text=f'{part_shock_ACS_without_eST:.1%}',
                   marker_color='PaleTurquoise', textposition='inside', hoverinfo='text')
        ])
    Shock_fig.update_layout(barmode='stack', xaxis={'visible': False, 'showticklabels': False}, yaxis={'visible': False, 'showticklabels': False}, 
                            plot_bgcolor='white', margin={'l': 0, 'r': 0, 't': 50, 'b': 0}, 
                            title={'x': 0.5, 'y': 0.9, 'text': '<b>Доли типов ОКС в структуре шока</b>', 'font': {'family': 'Arial', 'size': 20, 'color': 'Black'}, 
                                   'yanchor': 'bottom', 'xanchor': 'center'}, 
                            legend={'x': 0.93, 'y': 0.5, 'traceorder': 'reversed', 'font': {'family': 'Arial', 'size': 14, 'color': 'Black'}, 
                                    'yanchor': 'middle', 'xanchor': 'left'})

    # Охват ЧКВ у пациентов с шоком
    cnt_PTCA_for_shock = df.loc[(df['№ п/п'] == '39.1.3') &
                                (df['Date'].dt.to_period('Y') == year) &
                                (df['Date'].dt.month.isin(month_range)) &
                                (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    shock_PTCA_coverage = round(cnt_PTCA_for_shock / cnt_shock, 3) if cnt_shock > 0 else 0

    # Летальность при ОКС с шоком
    cnt_deaths_shock = df.loc[(df['№ п/п'] == '44.3') &
                              (df['Date'].dt.to_period('Y') == year) &
                              (df['Date'].dt.month.isin(month_range)) &
                              (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    shock_mortality_rate = round(cnt_deaths_shock / cnt_shock, 3) if cnt_shock > 0 else 0

    # Доля пациентов с шоком от всех умерших при ОКС
    part_shock_for_deaths = round(cnt_deaths_shock / ACS_mortality_abs, 3) if ACS_mortality_abs > 0 else 0



    return total_ACS, ACS_with_elevation_ST, ACS_without_elevation_ST, ACS_fig, f'{PCI_coverage:.1%}', \
           f'{ACS_mortality_rate:.1%}', f'{MI_mortality_rate:.1%}', MI_fig, ACS_path_funnel_fig, \
           f'Умерших: {int(cnt_deaths_ACS_with_eST)}', f'Общая летальность при ОКСпST: {ACS_with_eST_mortality_rate:.1%}', \
           f'Летальность идеального пути: {ACS_with_eST_ideal_path_mortality_rate:.1%}', \
           f'Доля умерших без ЧКВ, АКШ и ТЛТ: {ACS_with_eST_without_revasc_deaths_part:.1%}', ACS_with_eST_risk_fig, \
           f'Охват ЧКВ: {ACS_without_eST_high_risk_PTCA_coverage:.1%}', \
           f'Летальность: {ACS_without_eST_high_risk_mortality_rate:.1%}', \
           f'Охват ЧКВ: {ACS_without_eST_low_risk_PTCA_coverage:.1%}', \
           f'Летальность: {ACS_without_eST_high_risk_mortality_rate:.1%}', Shock_fig, \
           f'Кол-во ОКС с шоком: {int(cnt_shock)}', f'Охват ЧКВ: {shock_PTCA_coverage:.1%}', \
           f'Летальность при шоке: {shock_mortality_rate:.1%}', \
           f'Доля пациентов с шоком среди всех умерших при ОКС {part_shock_for_deaths:.1%}'


if __name__ == '__main__':
    print(choose_hospital_ASC('2023', list(range(1, 13)), df['Hospital'].unique()), sep='\n\n\n')