from shiny.express import ui, render, input
from data_import import df

ui.input_text('password', 'Enter Password')

@render.express
def show_data():
    if input.password() == 'penguins':
        @render.data_frame
        def data():
            return df
    else:
        ui.h1('pls enter the pw...')

