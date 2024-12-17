from ActivateTextAnalysis import TextAnalysis
from Graphics.ErrorRate import ErrorRatePlotter
from Graphics.Readability import ReadabilityPlotter
from Graphics.Sentimentality import SentimentPlotter

# Текст для анализа
text = ("Утро началось с яркого солнца, которое заливало город своим светом. "
        "Люди спешили по делам, радуясь хорошей погоде. "
        "В парке играли дети, слышался звонкий смех. "
        "Дети кричали очень громко, и это раздражало всех и портило настроение. "
        "Прохожие спрятались под навесами, ожидая, когда стихнет ливень. "
        "Через час дождь закончиился, и на горизонте появилась красивая радуга. "
        "Дети снова побежали играть, наполняя город шумом и движеением.")

# Слова для проверки
user_words = ["взрослые", "грусть", "тишина", "снег"],

# Вызов анализа техта
result = TextAnalysis.process_text(
    text=text,
    user_words=user_words,
    min_accuracy=80,
    make_correct=True,
    custom_stop_words_file="Packages/CustomWords.txt"
)

# Параметр text - Исходный текст, который нужно проанализировать
# Параметр user_words - Массив пользовательских слов, с которыми необходима проверка текста на близость
# Параметр min_accuracy - Минимальная точность текста для его отображения
# Параметр make_correct - Если True, текст будет исправлен
# Параметр custom_stop_words_file - Путь к пользовательскому файлу со нежелательными словами

# Вывод результатов анализа
print(f"Исходный текст: {result['original_text']}")
# Исправленный текст, если были обнаружены ошибки.
print(f"Исправленный текст: {result['corrected_text']}")

# Построение графика частотности ошибок
plotter = ErrorRatePlotter(result["error_counts"])
plotter.plot()

# Указание на наличие в тексте стоп-слов.
print(f"Содержит стоп-слова: {'Да' if result['contains_stop_words'] else 'Нет'}")
# Процент точности текста.
print(f"Точность текста: {result['accuracy']}%")
# Список орфографических ошибок и их исправления, если они обнаружены.
print(f"Найденные ошибки: {', '.join(result['misspelled_words'].keys()) if result['misspelled_words'] else 'Нет'}")
# Анализ тональности текста
sentiment = result['sentiment_analysis']
# Определение тональности текста: позитивная, нейтральная или негативная.
print(f"Тональность текста: {sentiment['sentiment']}")

# Диаграмма оценки тональности предложений
plotter = SentimentPlotter(result['sentimental'])
plotter.plot()

# Анализ читабельности текста
readability = result['readability_analysis']
# Индекс Флеша, числовая оценка читабельности текста.
print(f"Рейтинг Флэша: {readability['flesch_score']}")
# Числовая оценка читабельности текста (от 1 до 5).
print(f"Оценка читабельности: {readability['readability_rating']}")
# Описание сложности текста.
print(f"Оценка читабельности: {readability['readability_description']}")

# Диаграмма оценки читабельности предложений
plotter = ReadabilityPlotter(result["marks"])
plotter.plot()

semantic = result['semantic']
for item in semantic:
    print(f"Слова: {item['word']}, Сходство: {item['similarity']:.2f}, Результат: {item['result']}")
