
import reflex as rx


class SignupState(rx.State):
    """The state for the signup form."""
    email: str = ""
    password: str = ""
    agree_terms: bool = True

    def signup(self):
        """Handle the signup logic here."""
        if self.email and self.password and self.agree_terms:
            # Perform signup logic, e.g., saving to a database or calling an API
            print(f"Signup successful for: {self.email}")


def signup_default_icons() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.image(
                    src="/logo.jpg",
                    width="2.5em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.heading(
                    "Create an account",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Email address",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="user@reflex.dev",
                    type="email",
                    size="3",
                    width="100%",
                    on_change=SignupState.set_email,
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Password",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                    on_change=SignupState.set_password,
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.box(
                rx.checkbox(
                    "Agree to Terms and Conditions",
                    default_checked=True,
                    spacing="2",
                    on_change=SignupState.set_agree_terms,
                ),
                width="100%",
            ),
            rx.button("Sign in", size="3", width="100%", on_click=SignupState.signup),
            rx.center(
                rx.text("Already registered?", size="3"),
                rx.link("Sign in", href="#", size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        max_width="28em",
        size="4",
        width="100%",
    )

# Add the signup page to the app
def create_signup_page() -> rx.Component:
    return rx.container(
        signup_default_icons(),
        justify="center",
        align="center",
        height="100vh",
        background_color="#f9f9f9",
    )
