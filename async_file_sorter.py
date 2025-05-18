import asyncio
import aiofiles
import shutil
import argparse
import logging
from pathlib import Path

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Асинхронна функція копіювання файлу
async def copy_file(src_file: Path, dest_dir: Path):
    try:
        extension = src_file.suffix[1:] or "no_extension"
        target_folder = dest_dir / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        dest_file = target_folder / src_file.name
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.copy2, src_file, dest_file)
        logging.info(f"Copied {src_file} to {dest_file}")
    except Exception as e:
        logging.error(f"Failed to copy {src_file}: {e}")

# Асинхронна функція читання директорії
async def read_folder(source_dir: Path, dest_dir: Path):
    tasks = []
    for path in source_dir.rglob("*"):
        if path.is_file():
            tasks.append(copy_file(path, dest_dir))
    await asyncio.gather(*tasks)

# Головна функція
def main():
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source", type=Path, help="Шлях до вихідної папки")
    parser.add_argument("destination", type=Path, help="Шлях до папки призначення")
    args = parser.parse_args()

    if not args.source.exists() or not args.source.is_dir():
        logging.error("Невірна вихідна директорія")
        return

    args.destination.mkdir(parents=True, exist_ok=True)
    asyncio.run(read_folder(args.source, args.destination))

if __name__ == "__main__":
    main()
