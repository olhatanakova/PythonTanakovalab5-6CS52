import csv

INPUT_FILE = "inflation_2018_2019.csv"     
OUTPUT_FILE = "search_results.csv"       


def read_csv_data(filename):
    """Читання даних з CSV-файлу"""
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        print(f"Файл '{filename}' успішно прочитано. Записів: {len(data)}")
        return data
    except FileNotFoundError:
        print(f"Помилка: файл '{filename}' не знайдено!")
        return None
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        return None


def search_by_countries(data, countries):
    """Пошук даних за назвами країн"""
    results = []
    countries_lower = [c.strip().lower() for c in countries]

    for row in data:
        country_name = row["Country"].strip().lower()
        if country_name in countries_lower:
            results.append(row)

    return results


def save_results(results, filename):
    """Збереження результатів пошуку у новий CSV-файл"""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            if not results:
                print("Немає даних для збереження.")
                return False

            fieldnames = ["Country", "Year", "Inflation, consumer prices (annual %)"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"Результати збережено у файл '{filename}'")
        return True
    except Exception as e:
        print(f"Помилка при збереженні файлу: {e}")
        return False


def main():
    print("=" * 60)
    print("Пошук даних Inflation (2018–2019) за назвами країн")
    print("=" * 60)

    data = read_csv_data(INPUT_FILE)
    if data is None:
        return

    print("\nВведіть назви країн через кому (наприклад: Ukraine, Poland, Germany)")
    user_input = input("Країни: ").strip()

    if not user_input:
        print("Ви нічого не ввели. Програму завершено.")
        return

    countries = [c.strip() for c in user_input.split(",") if c.strip()]

    if not countries:
        print("Некоректне введення. Програму завершено.")
        return

    results = search_by_countries(data, countries)

    if not results:
        print("\nДаних за введеними країнами не знайдено.")
        return

    print(f"\nЗнайдено записів: {len(results)}")
    print("-" * 60)
    print(f"{'Country':<30} {'Year':<8} {'Inflation %'}")
    print("-" * 60)
    for row in results:
        print(f"{row['Country']:<30} {row['Year']:<8} {row['Inflation, consumer prices (annual %)']}")

    save_results(results, OUTPUT_FILE)

    print("\nРоботу завершено успішно!")


if __name__ == "__main__":
    main()