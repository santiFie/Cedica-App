import add, split, multiply, subtraction

def calculadora():
    try:
        num1 = float(input("Ingrese el primer número: "))
        num2 = float(input("Ingrese el segundo número: "))

        operador = input("Ingrese el operador (+, -, *, /): ")

        match operador:
            case '+':
                resultado = add(num1,num2)
            case '-':
                resultado = subtraction(num1,num2)
            case '*':
                resultado = multiply(num1,num2)
            case '/':
                resultado = split(num1,num2)
            case _:
                return "Operador no válido"

        return f"El resultado de {num1} {operador} {num2} es: {resultado}"

    except ValueError:
        return "Error: Ingrese un número válido"
