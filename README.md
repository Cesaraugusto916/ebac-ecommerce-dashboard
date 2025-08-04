# 🛒 E-commerce Analytics Dashboard

## 📋 Visão Geral

Este projeto contém uma análise completa de dados de e-commerce com dashboards interativos criados usando **Dash** e **Plotly**. Os usuários podem visualizar todos os insights da análise através de uma interface web amigável, sem necessidade de conhecimento em Python.

## 🚀 Aplicações Disponíveis

### 1. **Dashboard Principal** (`app_dashboard.py`)
- **URL**: http://127.0.0.1:8050
- **Características**:
  - Todos os 7 tipos de gráficos da análise original
  - Interface com abas organizadas por tipo de visualização
  - Cards informativos com estatísticas principais
  - Design responsivo com Bootstrap

### 2. **Dashboard Interativo** (`app_interativo.py`)
- **URL**: http://127.0.0.1:8051
- **Características**:
  - Filtros dinâmicos (Gênero, Preço, Material)
  - Estatísticas que se atualizam em tempo real
  - Gráficos interativos que respondem aos filtros
  - Tabela de dados filtrados
  - Interface moderna com gradientes

## 📊 Tipos de Visualizações

### Dashboard Principal:
1. **📊 Histogramas** - Distribuição de preços, notas, descontos e avaliações
2. **🎯 Dispersão** - Correlações entre variáveis principais
3. **🔥 Correlações** - Mapa de calor com insights detalhados
4. **📊 Barras** - Análise por categorias (marcas, gêneros, materiais)
5. **🥧 Pizza** - Distribuições proporcionais
6. **📈 Regressão** - Análise de tendências e relações lineares

### Dashboard Interativo:
- **Scatter Plot** dinâmico (Preço vs Nota)
- **Gráfico de Pizza** filtrado (Faixa de Preço)
- **Gráfico de Barras** (Top 10 Marcas)
- **Box Plot** (Distribuição por Gênero)
- **Tabela de Dados** filtrada

## 🛠️ Como Executar

### Pré-requisitos
Certifique-se de que todas as bibliotecas estão instaladas:
```bash
pip install dash plotly pandas numpy seaborn matplotlib scipy scikit-learn dash-bootstrap-components
```

### Executando as Aplicações

#### Dashboard Principal:
```bash
python app_dashboard.py
```
Acesse: http://127.0.0.1:8050

#### Dashboard Interativo:
```bash
python app_interativo.py
```
Acesse: http://127.0.0.1:8051

## 📈 Principais Insights Descobertos

### 🔍 **Dados Gerais**
- **295 produtos** analisados
- **Preço médio**: R$ 130,84
- **Nota média**: 4,48/5,0
- **Desconto médio**: 16,0%

### 📊 **Descobertas Principais**
1. **Disparidade de gênero**: Produtos masculinos custam 47% mais que femininos
2. **Baixo volume**: 50,8% dos produtos têm vendas ≤100 unidades
3. **Qualidade consistente**: 47,1% dos produtos têm nota "Excelente"
4. **Correlação fraca**: Preço não determina qualidade (R² = 0,000)

### ⚠️ **Problemas Identificados**
- Preços masculinos possivelmente inflacionados
- Muitos produtos com baixas vendas
- Estratégia de precificação desalinhada
- Oportunidade não explorada no mercado feminino

### 🎯 **Recomendações**
1. Revisar preços masculinos (-15%)
2. Expandir portfólio feminino (+25%)
3. Descontinuar produtos com baixas vendas
4. Implementar precificação baseada em valor

## 🎨 Funcionalidades dos Dashboards

### Dashboard Principal:
- ✅ Navegação por abas intuitiva
- ✅ Cards com métricas principais
- ✅ Gráficos estáticos de alta qualidade
- ✅ Insights contextuais por seção
- ✅ Design responsivo

### Dashboard Interativo:
- ✅ Filtros em tempo real
- ✅ Estatísticas dinâmicas
- ✅ Múltiplos gráficos sincronizados
- ✅ Tabela de dados filtrados
- ✅ Interface moderna e intuitiva

## 🔧 Estrutura dos Arquivos

```
📁 Projeto E-commerce Analytics/
├── 📄 ecommerce_estatistica.csv      # Dados originais
├── 📄 atividade.ipynb                # Análise completa em Jupyter
├── 📄 app_dashboard.py               # Dashboard principal
├── 📄 app_interativo.py              # Dashboard com filtros
├── 📄 relatorio.md                   # Relatório executivo
└── 📄 README.md                      # Esta documentação
```

## 🌐 Acesso aos Dashboards

### Para o Cliente Final:
1. **Sem conhecimento técnico necessário**
2. **Interface web intuitiva**
3. **Acesso via navegador**
4. **Interação através de cliques e filtros**

### Links de Acesso:
- **Dashboard Completo**: http://127.0.0.1:8050
- **Dashboard Interativo**: http://127.0.0.1:8051

## 💡 Próximos Passos

### Melhorias Possíveis:
- [ ] Deploy em servidor web (Heroku, AWS)
- [ ] Autenticação de usuários
- [ ] Exportação de gráficos em PDF
- [ ] Integração com banco de dados
- [ ] Alertas automáticos por email
- [ ] Dashboard mobile responsivo

### Expansões de Análise:
- [ ] Análise de sazonalidade
- [ ] Previsão de vendas
- [ ] Análise de sentimento dos reviews
- [ ] Clustering de produtos similares
- [ ] Recomendação de produtos

## 📞 Suporte

Para dúvidas ou sugestões sobre os dashboards:
- Verifique se todas as dependências estão instaladas
- Confirme se o arquivo CSV está no diretório correto
- Teste as URLs nos navegadores Chrome, Firefox ou Edge

---

**🎯 Objetivo Alcançado**: Transformar análise técnica em interface amigável para tomada de decisões de negócio!

*Dashboard criado com ❤️ usando Dash, Plotly e Bootstrap*
