#!/usr/bin/env python3
"""
Dashboard Interativo Avançado de Análise de E-commerce
Versão com filtros e interatividade avançada
"""

import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import dash_bootstrap_components as dbc

# Configuração inicial
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "E-commerce Analytics Pro"

# Carregando e preparando os dados
def load_and_prepare_data():
    """Carrega e prepara os dados para análise"""
    df = pd.read_csv('ecommerce_estatistica.csv')
    
    # Tratando a coluna Qtd_Vendidos
    def convert_qtd_vendidos(value):
        if isinstance(value, str):
            if '+' in value:
                value = value.replace('+', '').replace('mil', '000')
                if 'k' in value.lower():
                    value = value.replace('k', '000').replace('K', '000')
            try:
                return float(value)
            except:
                return 0
        return value
    
    df['Qtd_Vendidos_Numeric'] = df['Qtd_Vendidos'].apply(convert_qtd_vendidos)
    
    # Criando categorias
    df['Faixa_Preco'] = pd.cut(df['Preço'], bins=4, labels=['Baixo', 'Médio', 'Alto', 'Premium'])
    df['Categoria_Nota'] = pd.cut(df['Nota'], bins=[0, 3.5, 4.0, 4.5, 5.0], 
                                  labels=['Ruim', 'Regular', 'Bom', 'Excelente'])
    
    # Categoria de vendas
    def categorize_sales(qtd):
        if qtd <= 100:
            return 'Baixas (≤100)'
        elif qtd <= 1000:
            return 'Médias (101-1K)'
        elif qtd <= 10000:
            return 'Altas (1K-10K)'
        else:
            return 'Muito Altas (>10K)'
    
    df['Categoria_Vendas'] = df['Qtd_Vendidos_Numeric'].apply(categorize_sales)
    
    return df

# Carregando dados
df = load_and_prepare_data()

# Layout principal
app.layout = dbc.Container([
    # Header estilizado
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🛒 E-commerce Analytics Pro", 
                       className="display-4 text-white font-weight-bold"),
                html.P("Dashboard Interativo para Análise Completa de Dados de E-commerce",
                      className="lead text-white-50")
            ], className="text-center py-5", 
            style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'borderRadius': '15px',
                'marginBottom': '30px'
            })
        ])
    ]),
    
    # Filtros interativos
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🔍 Filtros Interativos"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Selecione os Gêneros:", className="font-weight-bold"),
                            dcc.Dropdown(
                                id='genero-filter',
                                options=[{'label': genero, 'value': genero} 
                                        for genero in df['Gênero'].unique()],
                                value=df['Gênero'].unique().tolist(),
                                multi=True,
                                placeholder="Selecione os gêneros..."
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("Faixa de Preço:", className="font-weight-bold"),
                            dcc.RangeSlider(
                                id='preco-filter',
                                min=df['Preço'].min(),
                                max=df['Preço'].max(),
                                step=10,
                                marks={
                                    int(df['Preço'].min()): f"R${df['Preço'].min():.0f}",
                                    int(df['Preço'].max()): f"R${df['Preço'].max():.0f}"
                                },
                                value=[df['Preço'].min(), df['Preço'].max()],
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("Materiais:", className="font-weight-bold"),
                            dcc.Dropdown(
                                id='material-filter',
                                options=[{'label': material, 'value': material} 
                                        for material in df['Material'].unique()],
                                value=df['Material'].value_counts().head(5).index.tolist(),
                                multi=True,
                                placeholder="Selecione os materiais..."
                            )
                        ], width=4)
                    ])
                ])
            ], className="mb-4")
        ])
    ]),
    
    # Cards de estatísticas dinâmicas
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id="total-produtos", className="text-primary font-weight-bold"),
                    html.P("Produtos Filtrados", className="card-text")
                ])
            ], className="text-center h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id="preco-medio", className="text-success font-weight-bold"),
                    html.P("Preço Médio", className="card-text")
                ])
            ], className="text-center h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id="nota-media", className="text-warning font-weight-bold"),
                    html.P("Nota Média", className="card-text")
                ])
            ], className="text-center h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id="vendas-totais", className="text-info font-weight-bold"),
                    html.P("Vendas Totais", className="card-text")
                ])
            ], className="text-center h-100")
        ], width=3)
    ], className="mb-4"),
    
    # Gráficos principais
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="scatter-plot")
        ], width=8),
        dbc.Col([
            dcc.Graph(id="pie-chart")
        ], width=4)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="bar-chart")
        ], width=6),
        dbc.Col([
            dcc.Graph(id="box-plot")
        ], width=6)
    ], className="mb-4"),
    
    # Tabela de dados filtrados
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Dados Detalhados (Top 20)"),
                dbc.CardBody([
                    html.Div(id="data-table")
                ])
            ])
        ])
    ]),
    
    # Footer
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.P("🔬 Dashboard Avançado criado com Dash, Plotly e Bootstrap | E-commerce Analytics 2025", 
                  className="text-center text-muted")
        ])
    ])
], fluid=True)

# Callback para atualizar estatísticas
@app.callback(
    [Output("total-produtos", "children"),
     Output("preco-medio", "children"),
     Output("nota-media", "children"),
     Output("vendas-totais", "children")],
    [Input("genero-filter", "value"),
     Input("preco-filter", "value"),
     Input("material-filter", "value")]
)
def update_stats(generos, preco_range, materiais):
    # Filtrar dados
    filtered_df = df[
        (df['Gênero'].isin(generos)) &
        (df['Preço'] >= preco_range[0]) &
        (df['Preço'] <= preco_range[1]) &
        (df['Material'].isin(materiais))
    ]
    
    total_produtos = len(filtered_df)
    preco_medio = f"R$ {filtered_df['Preço'].mean():.2f}" if len(filtered_df) > 0 else "R$ 0,00"
    nota_media = f"{filtered_df['Nota'].mean():.2f}" if len(filtered_df) > 0 else "0,00"
    vendas_totais = f"{filtered_df['Qtd_Vendidos_Numeric'].sum():.0f}" if len(filtered_df) > 0 else "0"
    
    return total_produtos, preco_medio, nota_media, vendas_totais

# Callback para gráfico de dispersão
@app.callback(
    Output("scatter-plot", "figure"),
    [Input("genero-filter", "value"),
     Input("preco-filter", "value"),
     Input("material-filter", "value")]
)
def update_scatter(generos, preco_range, materiais):
    filtered_df = df[
        (df['Gênero'].isin(generos)) &
        (df['Preço'] >= preco_range[0]) &
        (df['Preço'] <= preco_range[1]) &
        (df['Material'].isin(materiais))
    ]
    
    fig = px.scatter(
        filtered_df, 
        x='Preço', 
        y='Nota',
        size='Qtd_Vendidos_Numeric',
        color='Gênero',
        hover_data=['Marca', 'Material', 'Desconto'],
        title="📊 Preço vs Nota (Tamanho = Vendas, Cor = Gênero)"
    )
    
    fig.update_layout(height=400)
    return fig

# Callback para gráfico de pizza
@app.callback(
    Output("pie-chart", "figure"),
    [Input("genero-filter", "value"),
     Input("preco-filter", "value"),
     Input("material-filter", "value")]
)
def update_pie(generos, preco_range, materiais):
    filtered_df = df[
        (df['Gênero'].isin(generos)) &
        (df['Preço'] >= preco_range[0]) &
        (df['Preço'] <= preco_range[1]) &
        (df['Material'].isin(materiais))
    ]
    
    fig = px.pie(
        values=filtered_df['Faixa_Preco'].value_counts().values,
        names=filtered_df['Faixa_Preco'].value_counts().index,
        title="🥧 Distribuição por Faixa de Preço"
    )
    
    fig.update_layout(height=400)
    return fig

# Callback para gráfico de barras
@app.callback(
    Output("bar-chart", "figure"),
    [Input("genero-filter", "value"),
     Input("preco-filter", "value"),
     Input("material-filter", "value")]
)
def update_bar(generos, preco_range, materiais):
    filtered_df = df[
        (df['Gênero'].isin(generos)) &
        (df['Preço'] >= preco_range[0]) &
        (df['Preço'] <= preco_range[1]) &
        (df['Material'].isin(materiais))
    ]
    
    top_marcas = filtered_df.groupby('Marca')['Preço'].mean().nlargest(10)
    
    fig = px.bar(
        x=top_marcas.index,
        y=top_marcas.values,
        title="📊 Top 10 Marcas por Preço Médio",
        labels={'x': 'Marca', 'y': 'Preço Médio (R$)'}
    )
    
    fig.update_layout(height=400, xaxis_tickangle=-45)
    return fig

# Callback para box plot
@app.callback(
    Output("box-plot", "figure"),
    [Input("genero-filter", "value"),
     Input("preco-filter", "value"),
     Input("material-filter", "value")]
)
def update_box(generos, preco_range, materiais):
    filtered_df = df[
        (df['Gênero'].isin(generos)) &
        (df['Preço'] >= preco_range[0]) &
        (df['Preço'] <= preco_range[1]) &
        (df['Material'].isin(materiais))
    ]
    
    fig = px.box(
        filtered_df,
        x='Gênero',
        y='Preço',
        title="📦 Distribuição de Preços por Gênero"
    )
    
    fig.update_layout(height=400)
    return fig

# Callback para tabela de dados
@app.callback(
    Output("data-table", "children"),
    [Input("genero-filter", "value"),
     Input("preco-filter", "value"),
     Input("material-filter", "value")]
)
def update_table(generos, preco_range, materiais):
    filtered_df = df[
        (df['Gênero'].isin(generos)) &
        (df['Preço'] >= preco_range[0]) &
        (df['Preço'] <= preco_range[1]) &
        (df['Material'].isin(materiais))
    ]
    
    # Selecionar colunas relevantes
    table_df = filtered_df[['Título', 'Marca', 'Material', 'Gênero', 'Preço', 'Nota', 'Desconto']].head(20)
    
    return dbc.Table.from_dataframe(
        table_df, 
        striped=True, 
        bordered=True, 
        hover=True,
        size='sm',
        responsive=True
    )

if __name__ == '__main__':
    print("🚀 Iniciando E-commerce Analytics Pro...")
    print("🔍 Dashboard com filtros interativos carregado!")
    print("🌐 Acesse: http://127.0.0.1:8051")
    print("⏹️  Para parar: Ctrl+C")
    
    app.run(debug=True, host='127.0.0.1', port=8051)
