import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importa os dados, configurando a coluna 'date' como índice e formatando a data
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Limpa os dados removendo os valores fora do intervalo de 2,5% e 97,5%
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Desenha o gráfico de linha com Matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['value'], color='r', linewidth=1)
    
    # Configurações do gráfico
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # Salva a imagem e retorna a figura
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Modifica os dados para criar o gráfico de barras agrupados por ano e mês
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Agrupa por ano e mês, calculando a média
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Desenha o gráfico de barras com largura aumentada
    fig = df_bar.plot(kind='bar', figsize=(12, 6), legend=True).figure  # Aumentando a largura para 12
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')

    # Ajusta a legenda para exibir corretamente os meses
    plt.legend(title='Months', labels=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ], bbox_to_anchor=(1.05, 1), loc='upper left')

    # Ajusta o layout para evitar que elementos sejam cortados
    plt.tight_layout()

    # Salva a imagem e retorna a figura
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepara os dados para os box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    
    # Ordena os meses
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')
    
    # Desenha os box plots usando Seaborn
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Boxplot anual
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Boxplot mensal
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    # Salva a imagem e retorna a figura
    fig.savefig('box_plot.png')
    return fig
