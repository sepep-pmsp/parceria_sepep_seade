import pydeck as pdk

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

def gerar_pydeck(df):

    arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_width="total_casamentos * 0.1",
    get_source_position=["lon_origem", "lat_origem"],
    get_target_position=["lon_destino", "lat_destino"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=37.7576171,
        longitude=-122.5776844,
        bearing=45,
        pitch=50,
        zoom=8,
    )


    view_state = pdk.ViewState(
        latitude=-23.5558,
        longitude=-46.6396,
        bearing=45,
        pitch=50,
        zoom=6,
    )


    TOOLTIP_TEXT = {"html": "{nome_municipio_destino} : {total_casamentos}"}
    r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)

    return r