import reflex as rx

class DisplayState(rx.State):
    num1: float = 0.0
    num2: float = 0.0

def display_page():
    return rx.vstack(
        rx.input(
            placeholder="Enter first number",
            type_="number",
            on_change=lambda value: DisplayState.set_num1(float(value)),
        ),
        rx.input(
            placeholder="Enter second number",
            type_="number",
            on_change=lambda value: DisplayState.set_num2(float(value)),
        ),
        rx.text(lambda: f"First Number: {DisplayState.num1}"),
        rx.text(lambda: f"Second Number: {DisplayState.num2}"),
    )

app = rx.App()
app.add_page(display_page)

if __name__ == '__main__':
    app.run()
