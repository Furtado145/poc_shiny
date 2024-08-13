# Importacao de bibliotecas
from shiny import App, ui


# Parte 01: Interface de usuario...
app_ui = ui.page_fluid(
    ui.panel_title("⚽ Macro Copa ⚽"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.p("Entra em campo a seleção de dados macroeconômicos! ⚽"),
            ui.p("Defina os times de países e indicadores, explore o jogo de visualizações e marque gol na análise de dados!"),
        )
    )
)



# Parte 02: Logica de servidor
def server(input, output, server):
    ...


# Parte 03: Shiny app/dashboard
app = App(app_ui, server)

# shiny run --reload