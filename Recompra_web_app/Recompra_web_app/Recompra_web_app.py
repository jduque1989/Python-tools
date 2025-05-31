
import reflex as rx

class State(rx.State):
    code_id = ""
    password = ""

    def set_code_id(self, value):
        self.code_id = value

    def set_password(self, value):
        self.password = value


def render_user_entries(title:str, is_password:bool=False):
    return rx.vstack(
        rx.text(title, color="grey", font_size="16px", weight="bold"),
        rx.chakra.input(color="white",
                        type_="text" if not is_password else "password"),
        width="100%",
    )


def render_event_trigger():
    return rx.badge(rx.text("Login", text_align="center", width="100%"), color_scheme="gold", variant="outline", size="3",
                    width="100%", radius="none", padding="1em ")


def render_main_component():
    return rx.vstack(
            rx.flex(
                rx.image(src="/Logofondo.jpg", width="100px", border_radius="15px 30px"),
                justify="center",
                width="100%",
                ),
            rx.hstack(
                rx.icon(tag="lock", size=28, color="rgba(127, 127, 127, 1)"),
                width="100%",
                height="55px",
                bg="#181818",
                display="flex",
                justify_content="center",
                align_items="center", 


                ),
            rx.vstack(
                render_user_entries("Code ID"),
                render_user_entries("Password", is_password=True),
                render_event_trigger(),
                width="100%",
                padding="2em 2em 4em 2em",
                spacing="6",
                ),
            width=["100%","100%","65%","50%","35%"],
            bg="rgba(21, 21, 21, 0.55)",
            border="0.75px solid #2e2e2e",
            border_radius="10px 10px 0px 0px",
            box_shadow="0 8px 16px 6px rgba(0, 0, 0, 0.25)",
            )


def print_form():
    return rx.vstack(
        rx.text(f"Code ID: {State.code_id}", color="white", font_size="16px"),
        rx.text(f"Password: {State.password}", color="white", font_size="16px"),
        width="100%",
        padding="2em",
        spacing="6",
    )


def index() -> rx.Component:
    return rx.center(
            render_main_component(),
            width="100%",
            height="100vh",
            padding="2em",
            bg="#121212",
            ),



app = rx.App()
app.add_page(index)

