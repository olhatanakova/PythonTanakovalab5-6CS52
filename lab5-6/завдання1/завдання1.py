import requests
import json
import csv

INDICATOR = "FP.CPI.TOTL.ZG"          
YEARS = "2018:2019"                   
JSON_FILENAME = "inflation_2018_2019.json"
CSV_FILENAME = "inflation_2018_2019.csv"
PER_PAGE = 1000                       

URL = (
    f"https://api.worldbank.org/v2/country/all/"
    f"indicator/{INDICATOR}"
    f"?date={YEARS}&format=json&per_page={PER_PAGE}"
)


def get_data_from_api(url: str):
    """Отримання даних через API Світового банку"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()          

        data = response.json()

        if not isinstance(data, list) or len(data) < 2:
            raise ValueError("Некоректна структура відповіді API")

        if not data[1]:
            raise ValueError("Дані відсутні (порожній список)")

        print("Дані успішно отримано з API")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Помилка HTTP-запиту: {e}")
        return None
    except ValueError as e:
        print(f"Помилка даних: {e}")
        return None
    except Exception as e:
        print(f"Невідома помилка при отриманні даних: {e}")
        return None


def save_to_json(data, filename: str):
    """Збереження даних у JSON-файл"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Створено файл {filename}")
        return True
    except OSError as e:
        print(f"Помилка запису JSON-файлу: {e}")
        return False
    except Exception as e:
        print(f"Невідома помилка при збереженні JSON: {e}")
        return False


def convert_to_csv(data, filename: str):
    """Перетворення JSON-даних у CSV і збереження"""
    try:
        csv_data = []

        for item in data[1]:
         
            if item.get("value") is not None:
                csv_data.append([
                    item["country"]["value"],   
                    item["date"],               
                    item["value"]              
                ])

        if not csv_data:
            print("Немає валідних даних для запису в CSV")
            return False

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Country",
                "Year",
                "Inflation, consumer prices (annual %)"
            ])
            writer.writerows(csv_data)

        print(f"Створено файл {filename}")
        return csv_data

    except OSError as e:
        print(f"Помилка запису CSV-файлу: {e}")
        return None
    except KeyError as e:
        print(f"Помилка структури даних (відсутнє поле): {e}")
        return None
    except Exception as e:
        print(f"Невідома помилка при перетворенні в CSV: {e}")
        return None


def print_results(data, csv_data):
    """Виведення змісту JSON та CSV на екран"""
    print("\n" + "=" * 60)
    print("ЗМІСТ JSON (перші 5 записів):")
    print("=" * 60)

    for item in data[1][:5]:
        print(json.dumps(item, ensure_ascii=False, indent=4))
        print("-" * 40)

    print("\n" + "=" * 60)
    print("ЗМІСТ CSV (перші 5 записів):")
    print("=" * 60)
    print("Country, Year, Inflation, consumer prices (annual %)")

    for row in csv_data[:5]:
        print(f"{row[0]}, {row[1]}, {row[2]}")

def main():
    print("Завантаження даних Inflation, consumer prices (annual %) "
          "для всіх країн за 2018–2019 роки...\n")

    data = get_data_from_api(URL)
    if data is None:
        print("Програма завершена через помилку отримання даних.")
        return

    if not save_to_json(data, JSON_FILENAME):
        print("Програма завершена через помилку збереження JSON.")
        return

    csv_data = convert_to_csv(data, CSV_FILENAME)
    if csv_data is None:
        print("Програма завершена через помилку створення CSV.")
        return

    print_results(data, csv_data)

    print("\nРоботу завершено успішно!")


if __name__ == "__main__":
    main()
