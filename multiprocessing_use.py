import multiprocessing
import time



def search_keywords_in_file(file_path, keywords, queue):
    try:
        results = {keyword: [] for keyword in keywords}
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for keyword in keywords:
                if keyword.lower() in content:
                    results[keyword].append(file_path)
        queue.put(results)
    except Exception as e:
        print(f"Помилка обробки файлу {file_path}: {e}")
        queue.put({keyword: [] for keyword in keywords})



def multiprocessing_search(file_paths, keywords):
    queue = multiprocessing.Queue()
    processes = []

    for file_path in file_paths:
        process = multiprocessing.Process(
            target=search_keywords_in_file, args=(file_path, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        result = queue.get()
        for keyword, files in result.items():
            final_results[keyword].extend(files)

    return final_results



def measure_multiprocessing_search(file_paths, keywords):
    start_time = time.time()
    result = multiprocessing_search(file_paths, keywords)
    end_time = time.time()
    print(f"Час виконання (multiprocessing): {end_time - start_time} секунд")
    return result


if __name__ == "__main__":
    files = ['./f1.txt', './f2.txt', './f3.txt']
    keywords = ['right', 'about']
    result_multiprocessing = measure_multiprocessing_search(files, keywords)
    print("Результати (multiprocessing):", result_multiprocessing)
