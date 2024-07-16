from helpers.ts_means import *

# Nome do arquivo com dados
datafile = 'files/ex.csv'
varname = 'cf'
# Ler arquivo de dados
df = Aux.csv_to_df(datafile)
# Acertar formato timestamp
df = Aux.convert_timestamp(df)

# Gráfico da série temporal sem médias
Aux.plot_ts(df, varname, 'files/ts.png', 'Time series')

# Gráfico de um determinado dia
day = '20150101'
df_day = Aux.selection(df, day)
Aux.plot_ts(df_day, varname, 'files/ts_day.png', f'Time series - {day}')

# Gráfico das médias mensais
df_month = Aux.mean_month(df, varname)
Aux.plot_ts(df_month, 'mean', 'files/ts_month.png', 'Monthly means')

# Gráfico das médias para padrão diurno
df_h = Aux.mean_h(df)
Aux.plot_ts(df_h, 'cf', 'files/ts_h.png', 'Diurnal pattern')
