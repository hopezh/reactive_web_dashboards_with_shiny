from math import e
import polars as pl
from shiny.express import ui, input, render
from shiny import reactive
from shinywidgets import render_plotly
from data_import import df
import plotly.express as px

df_min = df.select(pl.min('body_mass_g')).item()
df_max = df.select(pl.max('body_mass_g')).item()

with ui.sidebar(bg='#f8f8f8'):
    ui.input_slider(
        'mass',
        'Max Body Mass',
        df_min, df_max, (df_min+df_max)/2
    )

    ui.input_checkbox_group(
        "species",
        "Species",
        ['Adelie', 'Chinstrap', 'Gentoo'],
        selected=['Adelie', 'Chinstrap', 'Gentoo'],
    )

    ui.input_text('new_label', 'New Label')
    ui.input_action_button('update', 'Update')


@reactive.effect()
@reactive.event(input.update)
def update_label():
    ui.update_checkbox_group(
        'species',
        label = input.new_label()
    )
    ui.update_text('new_label', value='')

# refactor filter func as a reactive calc
@reactive.calc
@reactive.event(input.update, ignore_none=False)
def filter_data():
    # print('filtered')
    df_subset = df.filter(
        pl.col('body_mass_g') < input.mass(),
        pl.col('species').is_in(input.species())
    )
    return df_subset


with ui.layout_columns():
    with ui.value_box(theme='blue'):
        'Mean Beak Length'
        @render.text
        def mean_beak_len():
            mbl = filter_data().select(pl.mean('bill_length_mm').round(2)).item()
            return mbl


with ui.layout_columns():
    with ui.card():
        'Plot'

        ui.input_checkbox('show_species', 'Show Species', value=True)

        @render_plotly
        def plot():
            # df_subset = df.filter(pl.col('body_mass_g') < input.mass())
            df_subset = filter_data()

            if input.show_species():
                return px.scatter(
                    df_subset, 
                    x='bill_depth_mm',
                    y='bill_length_mm',
                    color='species'
                )
            else:
                return px.scatter(
                    df_subset, 
                    x='bill_depth_mm',
                    y='bill_length_mm',
                )
        

    with ui.card():
        "Raw Data"
        
        @render.data_frame
        def data():
            # df_subset = df.filter(pl.col('body_mass_g') < input.mass())
            df_subset = filter_data()
            return df_subset