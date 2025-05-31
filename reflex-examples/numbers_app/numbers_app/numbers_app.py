import reflex as rx
from calc import calculate_sum, calculate_product, calculate_difference, calculate_quotient


class State(rx.State):
    number1: float = 0.0
    number2: float = 0.0
    sum: float = 0.0
    product: float = 0.0
    difference: float = 0.0
    quotient: float = 0.0

    def handle_submit(self, form_data: dict):
        self.number1 = float(form_data.get('number1', 0))
        self.number2 = float(form_data.get('number2', 0))
        self.sum = calculate_sum(self.number1, self.number2)
        self.product = calculate_product(self.number1, self.number2)
        self.difference = calculate_difference(self.number1, self.number2)
        self.quotient = calculate_quotient(self.number1, self.number2)


def index():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.input(name="number1", placeholder="Enter first number"),
                rx.input(name="number2", placeholder="Enter second number"),
                rx.button("Submit", type="submit"),
            ),
            on_submit=State.handle_submit
        ),
        rx.text(f"First Number: {State.number1}"),
        rx.text(f"Second Number: {State.number2}"),
        rx.text(f"Sum: {State.sum}"),
        rx.text(f"Product: {State.product}"),
        rx.text(f"Difference: {State.difference}"),
        rx.text(f"Quotient: {State.quotient}"),
    )


app = rx.App()
app.add_page(
        index,
        title="Numbers App",
        description="Calculate the sum, product, difference, and quotient of two numbers.",
        )
