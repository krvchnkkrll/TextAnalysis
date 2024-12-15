import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class SentimentPlotter:
    def __init__(self, sentiments):
        self.sentiments = sentiments

    def plot(self):
        plt.figure(figsize=(10, 6))

        colors = ['g' if val == 1 else 'r' if val == -1 else 'b' for val in self.sentiments]

        positions = range(1, len(self.sentiments) + 1)

        plt.bar(
            positions,
            self.sentiments,
            color=colors
        )

        plt.title("Сентиментальность текста", fontsize=14)
        plt.xlabel("Предложения", fontsize=12)
        plt.ylabel("Сентимент", fontsize=12)
        plt.xticks(positions)
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.grid(True, linestyle='--', alpha=0.7, axis='y')
        plt.tight_layout()
        plt.savefig("sentimental.png")
        plt.show()