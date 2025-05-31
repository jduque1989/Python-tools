import reflex as rx

def calculate_operations(number1, number2):
    addition = number1 + number2
    subtraction = number1 - number2
    multiplication = number1 * number2
    if number2 != 0:
        division = number1 / number2
    else:
        division = "undefined (cannot divide by zero)"
    return addition, subtraction, multiplication, division

def main():
    number1 = rx.state('number1', 0.0)
    number2 = rx.state('number2', 0.0)
    results = rx.state('results', None)

    def calculate():
        n1 = float(number1.get())
        n2 = float(number2.get())
        results.set(calculate_operations(n1, n2))

    return rx.container(
        rx.heading("Basic Operations Calculator"),
        rx.paragraph("Enter two numbers to see the results of basic operations"),
        rx.form(
            rx.input(placeholder="Enter the first number", type="number", bind=number1),
            rx.input(placeholder="Enter the second number", type="number", bind=number2),
            rx.button("Calculate", type="submit", on_click=calculate)
        ),
        rx.if_(results, lambda: display_results(results.get()))
    )

def display_results(results):
    addition, subtraction, multiplication, division = results
    return rx.container(
        rx.paragraph(f"Addition: {addition}"),
        rx.paragraph(f"Subtraction: {subtraction}"),
        rx.paragraph(f"Multiplication: {multiplication}"),
        rx.paragraph(f"Division: {division}")
    )


app = rx.App()
app.run()
