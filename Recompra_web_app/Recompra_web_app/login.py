import reflex as rx
import requests as rq


@rx.page(route="/login", title="Login")
def login() -> rx.Component:
    return rx.section(
            rx.image(src="/Logofondo.jpg", width="200px", border_radius="15px 50px"),
            rx.heading("Login Session"),
            rx.form.root(
                rx.flex(
                )
            )
        )

