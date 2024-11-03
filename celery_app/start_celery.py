import os

from calculate_workers import calculate_worker_count


def main():
    workers = calculate_worker_count('CPU')
    print(f'Количество воркеров: {workers}')
    os.system(f'celery -A tasks.celery worker --loglevel=info --concurrency={workers}')

if __name__ == "__main__":
    main()
