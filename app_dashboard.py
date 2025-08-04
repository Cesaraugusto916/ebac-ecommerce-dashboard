#!/usr/bin/env python3
"""
Dashboard Interativo de Análise de E-commerce
Aplicação Dash para visualização dos dados de e-commerce
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
app.title = "Dashboard E-commerce Analytics"

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

# Funções para criar gráficos
def create_histogram_charts():
    """Cria gráficos de histograma"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Distribuição dos Preços', 'Distribuição das Notas', 
                       'Distribuição dos Descontos', 'Distribuição Log(Avaliações)'],
        vertical_spacing=0.1
    )
    
    # Histograma 1: Preços
    fig.add_trace(
        go.Histogram(x=df['Preço'], nbinsx=30, name='Preços', 
                    marker_color='skyblue', opacity=0.7),
        row=1, col=1
    )
    
    # Histograma 2: Notas
    fig.add_trace(
        go.Histogram(x=df['Nota'], nbinsx=20, name='Notas', 
                    marker_color='lightgreen', opacity=0.7),
        row=1, col=2
    )
    
    # Histograma 3: Descontos
    fig.add_trace(
        go.Histogram(x=df['Desconto'], nbinsx=25, name='Descontos', 
                    marker_color='coral', opacity=0.7),
        row=2, col=1
    )
    
    # Histograma 4: Log(Avaliações)
    log_avaliacoes = np.log1p(df['N_Avaliações'])
    fig.add_trace(
        go.Histogram(x=log_avaliacoes, nbinsx=25, name='Log(Avaliações)', 
                    marker_color='gold', opacity=0.7),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="📊 Distribuição de Variáveis Importantes",
        title_x=0.5,
        showlegend=False
    )
    
    # Atualizando eixos
    fig.update_xaxes(title_text="Preço (R$)", row=1, col=1)
    fig.update_xaxes(title_text="Nota (1-5)", row=1, col=2)
    fig.update_xaxes(title_text="Desconto (%)", row=2, col=1)
    fig.update_xaxes(title_text="Log(Avaliações + 1)", row=2, col=2)
    
    return fig

def create_scatter_charts():
    """Cria gráficos de dispersão"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Preço vs Nota', 'Nota vs Log(Avaliações)', 
                       'Desconto vs Preço', 'Preço vs Log(Vendas)'],
        vertical_spacing=0.1
    )
    
    # Scatter 1: Preço vs Nota
    fig.add_trace(
        go.Scatter(x=df['Preço'], y=df['Nota'], mode='markers',
                  marker=dict(color=df['Desconto'], colorscale='Viridis', size=8, opacity=0.6),
                  name='Preço vs Nota', hovertemplate='Preço: R$%{x}<br>Nota: %{y}<br>Desconto: %{marker.color}%'),
        row=1, col=1
    )
    
    # Scatter 2: Nota vs Log(Avaliações)
    log_avaliacoes = np.log1p(df['N_Avaliações'])
    fig.add_trace(
        go.Scatter(x=df['Nota'], y=log_avaliacoes, mode='markers',
                  marker=dict(color=df['Preço'], colorscale='Plasma', size=8, opacity=0.6),
                  name='Nota vs Avaliações', hovertemplate='Nota: %{x}<br>Log(Avaliações): %{y}<br>Preço: R$%{marker.color}'),
        row=1, col=2
    )
    
    # Scatter 3: Desconto vs Preço
    fig.add_trace(
        go.Scatter(x=df['Desconto'], y=df['Preço'], mode='markers',
                  marker=dict(color=df['Qtd_Vendidos_Numeric'], colorscale='RdYlBu', size=8, opacity=0.6),
                  name='Desconto vs Preço', hovertemplate='Desconto: %{x}%<br>Preço: R$%{y}<br>Vendas: %{marker.color}'),
        row=2, col=1
    )
    
    # Scatter 4: Preço vs Log(Vendas)
    log_vendas = np.log1p(df['Qtd_Vendidos_Numeric'])
    fig.add_trace(
        go.Scatter(x=df['Preço'], y=log_vendas, mode='markers',
                  marker=dict(color=df['Nota'], colorscale='RdYlGn', size=8, opacity=0.6),
                  name='Preço vs Vendas', hovertemplate='Preço: R$%{x}<br>Log(Vendas): %{y}<br>Nota: %{marker.color}'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="🎯 Análise de Correlações entre Variáveis",
        title_x=0.5,
        showlegend=False
    )
    
    return fig

def create_heatmap():
    """Cria mapa de calor de correlações"""
    correlation_data = df[['Preço', 'Nota', 'N_Avaliações', 'Desconto', 
                          'Qtd_Vendidos_Numeric']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_data.values,
        x=correlation_data.columns,
        y=correlation_data.columns,
        colorscale='RdBu_r',
        zmid=0,
        text=np.round(correlation_data.values, 3),
        texttemplate="%{text}",
        textfont={"size": 14, "color": "white"},
        hovertemplate='<b>%{y} vs %{x}</b><br>Correlação: %{z}<br><extra></extra>'
    ))
    
    fig.update_layout(
        title="🔥 Mapa de Calor - Correlações entre Variáveis",
        title_x=0.5,
        height=500,
        width=700,
        font=dict(size=12)
    )
    
    return fig

def create_bar_charts():
    """Cria gráficos de barras"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Top 10 Marcas por Preço', 'Produtos por Gênero', 
                       'Top 8 Materiais', 'Notas por Temporada'],
        vertical_spacing=0.15
    )
    
    # Gráfico 1: Top marcas
    top_marcas = df.groupby('Marca')['Preço'].agg(['mean', 'count']).reset_index()
    top_marcas = top_marcas[top_marcas['count'] >= 2].nlargest(10, 'mean')
    
    fig.add_trace(
        go.Bar(x=top_marcas['Marca'], y=top_marcas['mean'], 
               name='Preço Médio', marker_color='steelblue',
               hovertemplate='Marca: %{x}<br>Preço Médio: R$%{y:.2f}'),
        row=1, col=1
    )
    
    # Gráfico 2: Distribuição por gênero
    genero_counts = df['Gênero'].value_counts()
    fig.add_trace(
        go.Bar(x=genero_counts.index, y=genero_counts.values, 
               name='Quantidade', marker_color='lightcoral',
               hovertemplate='Gênero: %{x}<br>Quantidade: %{y}'),
        row=1, col=2
    )
    
    # Gráfico 3: Top materiais
    material_counts = df['Material'].value_counts().head(8)
    fig.add_trace(
        go.Bar(x=material_counts.index, y=material_counts.values, 
               name='Frequência', marker_color='gold',
               hovertemplate='Material: %{x}<br>Frequência: %{y}'),
        row=2, col=1
    )
    
    # Gráfico 4: Notas por temporada
    temporada_stats = df.groupby('Temporada')['Nota'].mean()
    fig.add_trace(
        go.Bar(x=temporada_stats.index, y=temporada_stats.values, 
               name='Nota Média', marker_color='mediumseagreen',
               hovertemplate='Temporada: %{x}<br>Nota Média: %{y:.2f}'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=700,
        title_text="📊 Análise por Categorias",
        title_x=0.5,
        showlegend=False
    )
    
    # Rotacionar labels dos eixos x
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_pie_charts():
    """Cria gráficos de pizza"""
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "pie"}, {"type": "pie"}],
               [{"type": "pie"}, {"type": "pie"}]],
        subplot_titles=['Faixa de Preço', 'Categoria de Nota', 
                       'Distribuição por Gênero', 'Categoria de Vendas'],
        vertical_spacing=0.1
    )
    
    # Pizza 1: Faixa de preço
    faixa_counts = df['Faixa_Preco'].value_counts()
    fig.add_trace(
        go.Pie(labels=faixa_counts.index, values=faixa_counts.values,
               name="Faixa Preço", hole=0.3),
        row=1, col=1
    )
    
    # Pizza 2: Categoria de nota
    nota_counts = df['Categoria_Nota'].value_counts()
    fig.add_trace(
        go.Pie(labels=nota_counts.index, values=nota_counts.values,
               name="Categoria Nota", hole=0.3),
        row=1, col=2
    )
    
    # Pizza 3: Gênero
    genero_counts = df['Gênero'].value_counts().head(6)
    fig.add_trace(
        go.Pie(labels=genero_counts.index, values=genero_counts.values,
               name="Gênero", hole=0.3),
        row=2, col=1
    )
    
    # Pizza 4: Categoria de vendas
    vendas_counts = df['Categoria_Vendas'].value_counts()
    fig.add_trace(
        go.Pie(labels=vendas_counts.index, values=vendas_counts.values,
               name="Vendas", hole=0.3),
        row=2, col=2
    )
    
    fig.update_layout(
        height=700,
        title_text="🥧 Distribuições Proporcionais",
        title_x=0.5
    )
    
    return fig

def create_regression_charts():
    """Cria gráficos de regressão"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Preço vs Nota', 'Log(Avaliações) vs Nota', 
                       'Desconto vs Preço', 'Preço vs Log(Vendas)'],
        vertical_spacing=0.1
    )
    
    # Regressão 1: Preço vs Nota
    fig.add_trace(
        go.Scatter(x=df['Preço'], y=df['Nota'], mode='markers',
                  marker=dict(color='steelblue', size=6, opacity=0.6),
                  name='Dados'),
        row=1, col=1
    )
    
    # Linha de tendência
    z = np.polyfit(df['Preço'], df['Nota'], 1)
    p = np.poly1d(z)
    fig.add_trace(
        go.Scatter(x=df['Preço'], y=p(df['Preço']), mode='lines',
                  line=dict(color='red', width=2), name='Tendência'),
        row=1, col=1
    )
    
    # Regressão 2: Log(Avaliações) vs Nota
    log_avaliacoes = np.log1p(df['N_Avaliações'])
    fig.add_trace(
        go.Scatter(x=log_avaliacoes, y=df['Nota'], mode='markers',
                  marker=dict(color='green', size=6, opacity=0.6),
                  name='Dados'),
        row=1, col=2
    )
    
    z2 = np.polyfit(log_avaliacoes, df['Nota'], 1)
    p2 = np.poly1d(z2)
    fig.add_trace(
        go.Scatter(x=log_avaliacoes, y=p2(log_avaliacoes), mode='lines',
                  line=dict(color='red', width=2), name='Tendência'),
        row=1, col=2
    )
    
    # Regressão 3: Desconto vs Preço
    fig.add_trace(
        go.Scatter(x=df['Desconto'], y=df['Preço'], mode='markers',
                  marker=dict(color='orange', size=6, opacity=0.6),
                  name='Dados'),
        row=2, col=1
    )
    
    z3 = np.polyfit(df['Desconto'], df['Preço'], 1)
    p3 = np.poly1d(z3)
    fig.add_trace(
        go.Scatter(x=df['Desconto'], y=p3(df['Desconto']), mode='lines',
                  line=dict(color='red', width=2), name='Tendência'),
        row=2, col=1
    )
    
    # Regressão 4: Preço vs Log(Vendas)
    log_vendas = np.log1p(df['Qtd_Vendidos_Numeric'])
    fig.add_trace(
        go.Scatter(x=df['Preço'], y=log_vendas, mode='markers',
                  marker=dict(color='purple', size=6, opacity=0.6),
                  name='Dados'),
        row=2, col=2
    )
    
    z4 = np.polyfit(df['Preço'], log_vendas, 1)
    p4 = np.poly1d(z4)
    fig.add_trace(
        go.Scatter(x=df['Preço'], y=p4(df['Preço']), mode='lines',
                  line=dict(color='red', width=2), name='Tendência'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="📈 Análise de Regressão e Tendências",
        title_x=0.5,
        showlegend=False
    )
    
    return fig

# Layout da aplicação
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🛒 Dashboard de Análise de E-commerce", 
                   className="text-center mb-4", 
                   style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            html.P("Análise interativa completa dos dados de produtos, vendas e avaliações",
                  className="text-center text-muted mb-5")
        ])
    ]),
    
    # Cards de resumo
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{len(df)}", className="card-title text-primary"),
                    html.P("Total de Produtos", className="card-text")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"R$ {df['Preço'].mean():.2f}", className="card-title text-success"),
                    html.P("Preço Médio", className="card-text")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{df['Nota'].mean():.2f}", className="card-title text-warning"),
                    html.P("Nota Média", className="card-text")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{df['Desconto'].mean():.1f}%", className="card-title text-danger"),
                    html.P("Desconto Médio", className="card-text")
                ])
            ], className="text-center")
        ], width=3)
    ], className="mb-5"),
    
    # Tabs para diferentes análises
    dbc.Tabs([
        dbc.Tab(label="📊 Histogramas", tab_id="histograms"),
        dbc.Tab(label="🎯 Dispersão", tab_id="scatter"),
        dbc.Tab(label="🔥 Correlações", tab_id="heatmap"),
        dbc.Tab(label="📊 Barras", tab_id="bars"),
        dbc.Tab(label="🥧 Pizza", tab_id="pie"),
        dbc.Tab(label="📈 Regressão", tab_id="regression"),
    ], id="tabs", active_tab="histograms"),
    
    # Conteúdo das tabs
    html.Div(id="tab-content", className="mt-4"),
    
    # Footer
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.P("🔍 Dashboard criado com Dash e Plotly | Análise de E-commerce 2025", 
                  className="text-center text-muted")
        ])
    ])
], fluid=True)

# Callback para atualizar conteúdo das tabs
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def update_tab_content(active_tab):
    if active_tab == "histograms":
        return dcc.Graph(figure=create_histogram_charts())
    elif active_tab == "scatter":
        return dcc.Graph(figure=create_scatter_charts())
    elif active_tab == "heatmap":
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=create_heatmap())
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Insights de Correlação"),
                    dbc.CardBody([
                        html.H6("🔥 Correlações Principais:", className="card-title"),
                        html.P("• Qtd_Vendidos ↔ N_Avaliações: 0.912 (muito forte)", 
                               className="card-text", style={'color': '#28a745'}),
                        html.P("• Preço ↔ Desconto: 0.158 (fraca positiva)", 
                               className="card-text", style={'color': '#ffc107'}),
                        html.P("• Preço ↔ Nota: 0.006 (inexistente)", 
                               className="card-text", style={'color': '#dc3545'}),
                        html.Hr(),
                        html.H6("💡 Interpretação:", className="card-title"),
                        html.P("🎯 Produtos com mais vendas têm mais avaliações", 
                               className="card-text small"),
                        html.P("💰 Produtos caros tendem a ter descontos maiores", 
                               className="card-text small"),
                        html.P("⚠️ Preço não determina qualidade percebida", 
                               className="card-text small"),
                        html.Hr(),
                        html.P("📊 A análise sugere que o preço pode estar desalinhado com a percepção de valor.", 
                              className="card-text small text-muted")
                    ])
                ], style={'height': '500px'})
            ], width=4)
        ])
    elif active_tab == "bars":
        return dcc.Graph(figure=create_bar_charts())
    elif active_tab == "pie":
        return dcc.Graph(figure=create_pie_charts())
    elif active_tab == "regression":
        return dcc.Graph(figure=create_regression_charts())
    
    return html.Div("Selecione uma aba para visualizar os gráficos")

# Executar a aplicação
if __name__ == '__main__':
    print("🚀 Iniciando Dashboard de E-commerce...")
    print("📊 Carregando dados e criando visualizações...")
    print("🌐 Acesse: http://127.0.0.1:8050")
    print("⏹️  Para parar: Ctrl+C")
    
    app.run(debug=True, host='127.0.0.1', port=8050)
