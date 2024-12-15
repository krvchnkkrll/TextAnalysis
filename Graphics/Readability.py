import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class ReadabilityPlotter:
    def __init__(self, marks):
        self.marks = marks

    def plot(self):
        plt.figure(figsize=(10, 6))

        plt.bar(
            range(1, len(self.marks) + 1),
            self.marks,
            color='b', label="Читабельность"
        )

        plt.title("Читабельность", fontsize=14)
        plt.xlabel("Предложения", fontsize=12)
        plt.ylabel("Оценка по Флешу", fontsize=12)
        plt.xticks(range(1, len(self.marks) + 1))
        plt.grid(True, linestyle='--', alpha=0.7, axis='y')
        plt.legend()
        plt.tight_layout()
        plt.savefig("readability.png")
        plt.show()


