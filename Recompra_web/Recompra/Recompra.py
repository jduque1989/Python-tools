import reflex as rx
from login import create_signup_page

# Other necessary imports and configurations
import sqlite_utils

# Connect to SQLite database (or create it if it doesn't exist)
db = sqlite_utils.Database('form_data.db')

# Create table if it doesn't exist
if 'submissions' not in db.table_names():
    db["submissions"].create({
        "nombre": str,
        "codigo_id": str,
        "email": str,
        "whatsapp": str,
        "oro_en_linea_de_auspicio": str
    })


class State(rx.State):
    """The app state."""
    nombre: str = ""
    codigo_id: str = ""
    email: str = ""
    whatsapp: str = ""
    oro_en_linea_de_auspicio: str = ""

    def submit_form(self):
        # Insert form data into the database
        db["submissions"].insert({
            "nombre": self.nombre,
            "codigo_id": self.codigo_id,
            "email": self.email,
            "whatsapp": self.whatsapp,
            "oro_en_linea_de_auspicio": self.oro_en_linea_de_auspicio
        })

        # Reset form fields
        self.nombre = ""
        self.codigo_id = ""
        self.email = ""
        self.whatsapp = ""
        self.oro_en_linea_de_auspicio = ""


def index() -> rx.Component:
    # Form Page (Index)
    return rx.container(
        rx.vstack(
            rx.heading("Formulario de Registro", size="9", margin_bottom="20px"),
            rx.input(placeholder="Nombre", value=State.nombre, on_change=State.set_nombre),
            rx.input(placeholder="Codigo ID", value=State.codigo_id, on_change=State.set_codigo_id),
            rx.input(placeholder="E-mail", value=State.email, on_change=State.set_email),
            rx.input(placeholder="WhatsApp", value=State.whatsapp, on_change=State.set_whatsapp),
            rx.input(placeholder="Oro en línea de auspicio", value=State.oro_en_linea_de_auspicio, on_change=State.set_oro_en_linea_de_auspicio),
            rx.button("Submit", on_click=State.submit_form, margin_top="20px"),
            spacing="5",  # Adjusted spacing to a valid value
            padding="20px",
            max_width="500px",
            border="1px solid #ccc",
            border_radius="10px",
            box_shadow="0 0 10px rgba(0, 0, 0, 0.1)",
        ),
        justify="center",
        align="center",
        padding="50px",
        background_color="#f9f9f9",
        height="100vh",
    )


app = rx.App()
app.add_page(index)
app.add_page(create_signup_page, path="/signup")
app.compile()

# Serve the app using Daphne
if __name__ == "__main__":
    from daphne.cli import CommandLineInterface
    CommandLineInterface.entrypoint(["daphne", "-b", "0.0.0.0", "-p", "3000", "app:app"])
