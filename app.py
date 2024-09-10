# Importacao de bibliotecas
from shiny import App, ui, render
import pandas as pd
import plotnine as p9

# IMportaçao de dados
dados = (
    pd.read_csv("dados/dados.csv")
    .assign(
        data = lambda x: pd.to_datetime(x.data),
        index = lambda x : x.data
    )
    .set_index("index")
)

# Objetos uteis para inteface de usuario/servidor
nomes_variaveis = sorted(dados.variavel.unique().tolist())
nomes_paises = sorted(dados.pais.unique().tolist())
datas = dados.data.dt.date


# Parte 01: Interface de usuario...
app_ui = ui.page_fluid(
    ui.panel_title("⚽ Macro Copa ⚽"),
    ui.hr(),
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
            ),
            ui.input_date_range(
                id="btn_periodo",
                label= "Filtre os Anos",
                start = "2000-01-01",
                end = datas.max(),
                min = datas.min(),
                max = datas.max(),
                format= "yyyy",
                startview= "year",
                language= "pt-br",
                separator= " - "
            ),
            ui.input_radio_buttons(
                id= "btn_tipo_grafico",
                label= "Selecione o tipe de grafico:",
                choices=['Área', 'Coluna', 'Linha'],
                selected= "Linha"
            )
            
        ),
        ui.card(
            ui.row(
                ui.column(
                    6,
                    ui.input_select(
                        id= "btn_pais1",
                        label= "Selecione o 1o pais:",
                        choices= nomes_paises,
                        selected= "Brazil",
                        multiple= False
                    )
                ),
                ui.column(
                    6,
                    ui.input_select(
                        id= "btn_pais2",
                        label= "Selecione o 2o pais:",
                        choices= nomes_paises,
                        selected= "Argentina",
                        multiple= False
                    )
                )
            ),
            ui.row(
                ui.column(6,ui.output_plot("plt_pais1")),
                ui.column(6,ui.output_plot("plt_pais2"))
            )
        )
    )
)


# Parte 02: Logica de servidor
def server(input, output, server):
    @output
    @render.plot

    def plt_pais1():

        tipo_plt = input.btn_tipo_grafico()
        
        variavel_selecionada = input.btn_variavel()
        pais_selecionado = input.btn_pais1()
        data_inicial = input.btn_periodo()[0]
        data_final = input.btn_periodo()[1]
        df1 = dados.query(
            "variavel == @variavel_selecionada " + 
            "and data >= @data_inicial and data <= @data_final " + 
            "and pais == @pais_selecionado")

        plt1 = (
            p9.ggplot(data = df1) +
            p9.aes(x="data", y= "valor") +
            p9.scale_x_date(date_labels = '%Y') +
            p9.ggtitle(pais_selecionado + " - " + variavel_selecionada) +
            p9.ylab('') + 
            p9.xlab('Ano') + 
            p9.labs( caption= "Dados: Banco Mundial | Elaboração: Felipe Furtado")
        )

        if tipo_plt == 'Área':
            plt1 = plt1 + p9.geom_area()
        elif tipo_plt == 'Coluna':
            plt1 = plt1 + p9.geom_col()
        elif tipo_plt == 'Linha':
            plt1 = plt1 + p9.geom_line()
        
        return plt1
    
    @output
    @render.plot

    def plt_pais2():

        tipo_plt = input.btn_tipo_grafico()
        
        variavel_selecionada = input.btn_variavel()
        pais_selecionado = input.btn_pais2()
        data_inicial = input.btn_periodo()[0]
        data_final = input.btn_periodo()[1]
        df1 = dados.query(
            "variavel == @variavel_selecionada " + 
            "and data >= @data_inicial and data <= @data_final " + 
            "and pais == @pais_selecionado")

        plt2 = (
            p9.ggplot(data = df1) +
            p9.aes(x="data", y= "valor") +
            p9.scale_x_date(date_labels = '%Y') +
            p9.ggtitle(pais_selecionado + " - " + variavel_selecionada) +
            p9.ylab('') + 
            p9.xlab('Ano') + 
            p9.labs( caption= "Dados: Banco Mundial | Elaboração: Felipe Furtado")
        )

        if tipo_plt == 'Área':
            plt2 = plt2 + p9.geom_area()
        elif tipo_plt == 'Coluna':
            plt2 = plt2 + p9.geom_col()
        elif tipo_plt == 'Linha':
            plt2 = plt2 + p9.geom_line()
        
        return plt2



# Parte 03: Shiny app/dashboard
app = App(app_ui, server)

# shiny run --reload
# rsconnect deploy shiny . --name felipeffurtado --new --title macroCopa_AM