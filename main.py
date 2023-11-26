import numpy as np
import matplotlib.pyplot as plt
from pulp import LpMaximize, LpProblem, LpVariable

def plot_constraints_initial(x1_range, x2_range, step):
    x = np.arange(x1_range[0], x1_range[1] + step, step)
    plt.plot(x, (9 - 2 * x) / 1, label=r'$2x_1 + x_2 max $')
    plt.plot(x, (9 - x) / 2, label=r'$x_1 + 2x_2 max $')
    plt.plot(x, -x, label=r'$-x_1 - x_2 max $')

    # Додано обмеження x1 + x2 ≤ 5
    plt.fill_between(x, 0, 5 - x, color='gray', alpha=0.3, label=r'$x_1 + x_2 \leq 5$')

    # Додано обмеження x1 <= 4 та x2 <= 4
    plt.plot([4, 4], [0, 4], color='purple', linestyle='--', label=r'$x_1 \leq 4$')
    plt.plot([0, 4], [4, 4], color='orange', linestyle='--', label=r'$x_2 \leq 4$')

    # Додано обмеження x1 >= 0 та x2 >= 0
    plt.axhline(0, color='green', linestyle='--', label=r'$x_2 \geq 0$')
    plt.axvline(0, color='blue', linestyle='--', label=r'$x_1 \geq 0$')

    plt.xlim(x1_range)
    plt.ylim(x2_range)
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.legend()
    plt.grid(True)
    plt.title('Графіки з початковими обмеженнями')
    plt.show()


def plot_constraints_updated(x1_range, x2_range, step, e11, e13, a, x_point, y_point):
    x = np.arange(x1_range[0], x1_range[1] + step, step)

    # Змінено обмеження x1 + 2x2 ≥ e11 та -x1 - x2 ≥ e13
    plt.plot(x, (e11 - 2 * x) / 1, linestyle='--', color='red', label=r'$2x_1 + x_2 \geq {}$'.format(e11))
    plt.plot(x, -x - e13, linestyle='--', color='blue', label=r'$-x_1 - x_2 \geq {}$'.format(e13))

    # Додано обмеження x1 + x2 ≤ 5
    plt.fill_between(x, 0, 5 - x, color='gray', alpha=0.3, label=r'$x_1 + x_2 \leq 5$')

    # Додано обмеження x1 <= 4 та x2 <= 4
    plt.plot([4, 4], [0, 4], color='purple', linestyle='--', label=r'$x_1 \leq 4$')
    plt.plot([0, 4], [4, 4], color='orange', linestyle='--', label=r'$x_2 \leq 4$')

    # Додано обмеження x1 >= 0 та x2 >= 0
    plt.axhline(0, color='green', linestyle='--', label=r'$x_2 \geq 0$')
    plt.axvline(0, color='blue', linestyle='--', label=r'$x_1 \geq 0$')

    # Додано нове обмеження x1 + 2x2 ≥ a
    plt.plot(x, (a - x) / 2, linestyle='--', color='purple', label=r'$x_1 + 2x_2 \geq {}$'.format(a))

    plt.scatter(x_point, y_point, color='red', marker='x', label='Point (x, y)')

    plt.xlim(x1_range)
    plt.ylim(x2_range)
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.legend()
    plt.grid(True)
    plt.title('Графіки з оновленими обмеженнями')
    plt.show()



def main():
    while True:
        # Показати перший графік з початковими обмеженнями
        plot_constraints_initial((-1, 6), (-1, 6), step=0.5)

        # Введення значень е11 та е13
        e11 = float(input("Введіть значення епсилон_11: "))
        e13 = float(input("Введіть значення епсилон_13: "))

        # Створення задачі
        model = LpProblem(name="maximize_objective", sense=LpMaximize)

        # Визначення змінних рішення
        x1 = LpVariable(name="x1", lowBound=0, upBound=4)
        x2 = LpVariable(name="x2", lowBound=0, upBound=4)

        # Додавання цільової функції для максимізації
        model += x1 + 2 * x2, "Objective"

        # Додавання обмежень
        model += (2 * x1 + x2 >= e11, "Constraint_1")
        model += (-x1 - x2 >= e13, "Constraint_2")
        model += (x1 + x2 <= 5, "Constraint_3")
        model += (x1 + 2 * x2, "Constraint_4")  # додавання обмеження для максимального значення


        # Вирішення задачі
        model.solve()

        a = model.objective.value()
        x = x1.value()
        y = x2.value()

        # Виведення результатів
        print("-----------")
        print("Максимальне значення цільової функції:", model.objective.value())
        print("Значення x1 та x2:", x1.value(), x2.value())
        f1 = 2*x1.value()+x2.value()
        f2 = x1.value()+2*x2.value()
        f3 = -x1.value()-x2.value()

        input("Натисніть Enter для продовження...")

        # Показати другий графік з оновленими обмеженнями
        plot_constraints_updated((-1, 6), (-1, 6), step=0.5, e11=e11, e13=e13, a=a, x_point=x, y_point=y)

        print("Y1: (", f1, ", ", f2, ", ",f3, ")" )

        satisfaction = input("Чи подобаються вам ці значення? (Так/Ні): ").lower()

        if satisfaction == "так":
            print("Дякуємо за використання програми. Завершення...")
            break  # Завершити цикл і програму
        elif satisfaction == "ні":
            print("Будь ласка, введіть нові значення.")
        else:
            print("Невірний ввід. Будь ласка, введіть 'Так' або 'Ні'. Повторення введення...")

if __name__ == "__main__":
    main()
