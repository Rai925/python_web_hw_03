import argparse
import logging
from pathlib import Path
from shutil import copyfile
from queue import Queue
from threading import Thread, RLock

parser = argparse.ArgumentParser(description="Сортування папки")
parser.add_argument("--source", "-s", help="Початкова папка", required=True)
parser.add_argument("--output", "-o", help="Вихідна папка", default="dist")
args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = Queue()
lock = RLock()


def master(path: Path):
    grabs_folder(path)
    logging.info("Завершено збирання папки")


def grabs_folder(path: Path) -> None:
    logging.info(f"Початок збирання папки {path}")
    for el in path.iterdir():
        if el.is_dir():
            folders.put(el)
            grabs_folder(el)
        elif el.is_file():
            folders.put(path)


def copy_file() -> None:
    logging.info("Початок копіювання...")
    while True:
        with lock:
            if folders.empty():
                break
            path = folders.get()

        for el in path.iterdir():
            if el.is_file():
                ext = el.suffix[1:]
                ext_folder = output / ext
                try:
                    ext_folder.mkdir(exist_ok=True, parents=True)
                    logging.info(f"Копіювання файлу {el} в {ext_folder / el.name}")
                    copyfile(el, ext_folder / el.name)
                except OSError as err:
                    logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    folders.put(source)

    master_grabs = Thread(target=master, args=(source,))
    master_grabs.start()

    threads = []
    for i in range(3):
        th = Thread(target=copy_file)
        th.start()
        threads.append(th)

    master_grabs.join()
    for th in threads:
        th.join()
    print(f"\nМожна видалити {source}")
