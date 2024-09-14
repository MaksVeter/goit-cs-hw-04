import threading
import time

# Функція для пошуку ключових слів у файлі


def search_keywords_in_file(file_path, keywords, results, lock):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for keyword in keywords:
                if keyword.lower() in content:
                    with lock:
                        results[keyword].append(file_path)
    except Exception as e:
        print(f"Помилка обробки файлу {file_path}: {e}")



def threaded_search(file_paths, keywords):
    results = {keyword: [] for keyword in keywords}
    lock = threading.Lock()
    threads = []

    for file_path in file_paths:
        thread = threading.Thread(target=search_keywords_in_file, args=(
            file_path, keywords, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results



def measure_threaded_search(file_paths, keywords):
    start_time = time.time()
    result = threaded_search(file_paths, keywords)
    end_time = time.time()
    print(f"Час виконання (threading): {end_time - start_time} секунд")
    return result


if __name__ == "__main__":
    files = ['./f1.txt', './f2.txt', './f3.txt']
    keywords = ['right', 'about']

    result_threading = measure_threaded_search(files, keywords)
    print("Результати (threading):", result_threading)
