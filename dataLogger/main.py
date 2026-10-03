import threading
import queue

from source import run_source
from processor import load_filters, process_data


data_queue = queue.Queue()

filters = load_filters()


def source_worker(source_id, values_per_second):
    run_source(
        source_id,
        values_per_second,
        data_queue
    )


def processor_worker():
    while True:
        data = data_queue.get()

        try:
            process_data(data, filters)
        finally:
            data_queue.task_done()


def main():
    print("Starting data logger...")

    processor = threading.Thread(
        target=processor_worker,
        daemon=True
    )

    processor.start()

    source_speeds = {
        1: 100,
        2: 200,
        3: 300,
        4: 400
    }

    for source_id, speed in source_speeds.items():
        thread = threading.Thread(
            target=source_worker,
            args=(source_id, speed),
            daemon=True
        )

        thread.start()

    print("4 data sources started.")

    while True:
        pass


if __name__ == "__main__":
    main()
