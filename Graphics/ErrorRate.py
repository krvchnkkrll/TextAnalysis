import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class ErrorRatePlotter:
    def __init__(self, error_counts):
        self.error_counts = error_counts

    def plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(
            range(1, len(self.error_counts) + 1),
            self.error_counts,
            marker='o', linestyle='-', color='b', label="Частотность ошибок"
        )

        plt.title("Частотность ошибок", fontsize=14)
        plt.xlabel("Слова", fontsize=12)
        plt.ylabel("Ошибок", fontsize=12)
        plt.xticks(range(1, len(self.error_counts) + 1))
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig("errorRate.png")
        plt.show()

