from ActivateTextAnalysis import TextAnalysis

text = "Это пример текста, содержащий слова с ошшиббками, который может быть скорректирован."

result = TextAnalysis.process_text(
    text=text,
    min_accuracy=80,
    make_correct=True,
    custom_stop_words_file="Packages/CustomWords.txt",
)

print(f"Исходный текст: {result['original_text']}")
print(f"Исправленный текст: {result['corrected_text']}")
print(f"Содержит стоп-слова: {'Да' if result['contains_stop_words'] else 'Нет'}")
print(f"Точность текста: {result['accuracy']}%")
print(f"Найденные ошибки: {', '.join(result['misspelled_words'].keys()) if result['misspelled_words'] else 'Нет'}")

sentiment = result['sentiment_analysis']
print(f"Тональность текста: {sentiment['sentiment']}")

readability = result['readability_analysis']
print(f"Рейтинг Флэша: {readability['flesch_score']}")
print(f"Оценка читабельности: {readability['readability_rating']}")
print(f"Оценка читабельности: {readability['readability_description']}")


