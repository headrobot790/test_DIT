import multiprocessing
import os


def calculate_worker_count(task_type="IO") -> int :
    cpu_cores = multiprocessing.cpu_count()

    if task_type == "CPU":
        workers = max(1, cpu_cores // 2)
    else:
        workers = cpu_cores * 2
    return int(workers)


if __name__ == "__main__":
    task_type = os.getenv("TASK_TYPE", "CPU")
    worker_count = calculate_worker_count(task_type)
    print(f"type worker_count: {type(worker_count)}")
    print(f"Количество доступных ядер: {multiprocessing.cpu_count()}")
    print(f"Рекомендуемое количество воркеров для {task_type}-bound задач: {worker_count}")
