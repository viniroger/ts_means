'''
Helper functions for work with time series
author: Vinicius Roggério da Rocha
e-mail: viniroger@monolitonimbus.com.br
version: 0.0.1
date: 2024-07-16
'''

import pandas as pd
import matplotlib.pyplot as plt

class Aux():

    @staticmethod
    def csv_to_df(filename):
        '''
        Read CSV file to dataframe
        '''
        df = pd.read_csv(filename)
        return df

    @staticmethod
    def selection(df, day):
        '''
        Selecionar valores de um determinado dia
        '''
        day1 = f'{day} 00:00:00'
        day2 = f'{day} 23:59:59'
        newdf = (df['timestamp'] >= day1) & (df['timestamp'] < day2)
        newdf = df.loc[newdf]
        return newdf

    def convert_timestamp(df):
        '''
        Converter a coluna timestamp para o formato de data/hora do pandas
        '''
        df = df.copy()
        df.loc[:,'timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S')
        return df

    @staticmethod
    def mean_month(df, varname):
        '''
        Calcular médias mensais
        '''
        # Converter a coluna timestamp para o formato de data/hora do pandas
        df = df.copy()
        df.loc[:,'timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S')
        # Definir o timestamp como índice
        df.set_index('timestamp', inplace=True)
        # Contar numero de amostras de cada mês
        #print(df[varname].resample('M').count())
        # Resample para calcular a média mensal
        mean_df = df[varname].resample('M').agg(['mean', 'std']).set_index(pd.date_range(start=df.index.min(), periods=len(df['cf'].resample('M')), freq='MS'))
        # Recriar coluna timestamp
        mean_df['timestamp'] = mean_df.index
        return mean_df

    @staticmethod
    def adjust_time(row):
        '''
        Função para ajustar segundos e minutos
        '''
        if 0 <= row['second'] <= 15:
            row['second'] = 0
        elif 16 <= row['second'] <= 45:
            row['second'] = 30
        elif 46 <= row['second'] <= 59:
            row['second'] = 0
            row['minute'] += 1
        # Verificação para o caso de minuto virar 60
        if row['minute'] == 60:
            row['minute'] = 0
            row['hour'] += 1
        return row

    @classmethod
    def mean_h(self, df):
        '''
        Diurnal pattern plot
        '''
        # Criar colunas de horas, minutos e segundos
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute
        df['second'] = df['timestamp'].dt.second
        # Arredondar horários para 0 ou 30 segundos
        df = df.apply(self.adjust_time, axis=1)
        # Agrupar por hora, minuto e segundo e calcular as médias
        mv = df.groupby(['hour', 'minute', 'second']).mean(numeric_only=True)
        # Criar coluna de tempo (para facilitar o plot)
        mv.reset_index(inplace=True)
        mv['timestamp'] = mv['hour'].astype(str).apply(lambda x: x.zfill(2)) + mv['minute'].astype(str).apply(lambda x: x.zfill(2)) + mv['second'].astype(str).apply(lambda x: x.zfill(2))
        # Ordenando os valores pelo tempo
        mv.sort_values(by='timestamp', inplace=True)
        mv.loc[:,'timestamp'] = pd.to_datetime(mv['timestamp'], format='%H%M%S')
        return mv

    def plot_ts(df, varname, fname, title_str):
        '''
        Plot de série temporal
        '''
        plt.figure(figsize=(10, 6))  # Define o tamanho da figura
        plt.plot(df['timestamp'], df[varname], linestyle='-',marker='.')
        plt.title(title_str)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.savefig(fname, bbox_inches='tight')
