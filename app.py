# Importacao de bibliotecas
from shiny import App, ui
import pandas as pd

# IMportaçao de dados
dados = pd.read_csv("dados/dados.csv")

# Objetos uteis para inteface de usuario/servidor
nomes_variaveis = dados.variavel.unique().tolist()

# Parte 01: Interface de usuario...
app_ui = ui.page_fluid(
    ui.panel_title("⚽ Macro Copa ⚽"),
    ui.layout_sidebar(

        ui.sidebar(
            ui.p("Entra em campo a seleção de dados macroeconômicos! ⚽"),
            ui.p("Defina os times de países e indicadores, explore o jogo de visualizações e marque gol na análise de dados!"),
            ui.input_select(
                id= "btn_variavel",
                label= "Selecione uma variavel",
                choices= nomes_variaveis,
                selected= "PIB (%, cresc. anual)",
                multiple= False
            )
        ),
        ui.card(
            ui.input_select(
                id= "btn_pais1",
                label= "Selecione o 1o pais:",
                choices= [1, 2, 3]
            )
        )
    )
)


# Parte 02: Logica de servidor
def server(input, output, server):
    ...


# Parte 03: Shiny app/dashboard
app = App(app_ui, server)

# shiny run --reload