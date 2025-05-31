"""Shared auth layout."""

import reflex as rx

from ..components import container


def auth_layout(*args):
    """The shared layout for the login and sign up pages."""
    return rx.box(
        container(
            rx.vstack(
                rx.image(
                    src="/Logofondo.jpg",
                    width="100px",
                    height="auto",
                    border_radius="15px 50px",
                    # border="5px solid #FFFFFF",  # Change border color to white
                    style={
                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.2)",  # Add blur effect
                    },
                ),
                rx.heading("Bienvenido al gestor de negocios IM!", size="8"),
                rx.heading("Ingresa o registrate para empezar", size="8"),
                align="center",
            ),
            rx.text(
                "Asegurate de ingresar todos los datos de manera correcta, el código ID,"
                "y la contraseña son las mismas para ingresar al Backoffice, en este momento"
                "solo funciona para el BackOffice de Colombia, pero lo ampliaremos a todos los paises"
                "puedes verificar ID y contraseña en el Backoffice ",
                rx.link(
                    "acá",
                    href="https://colombia.ganoexcel.com/",

                ),
                ".",
                color="gray",
                font_weight="medium",
            ),
            *args,
            border_top_radius="10px",
            box_shadow="0 4px 60px 0 rgba(0, 0, 0, 0.08), 0 4px 16px 0 rgba(0, 0, 0, 0.08)",
            display="flex",
            flex_direction="column",
            align_items="center",
            padding_top="36px",
            padding_bottom="24px",
            padding_left="10%",
            padding_right="10%",
            spacing="4",
        ),
        height="100vh",
        padding_top="40px",
        background="url(bg.svg)",
        background_repeat="no-repeat",
        background_size="cover",
    )
