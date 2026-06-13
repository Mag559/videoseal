from pathlib import Path
from collections.abc import Callable

def recursive_process(input_directory: Path, output_directory, task: Callable[[Path, Path], None]) -> None:
    for item in input_directory.iterdir():
        if item.is_dir():
            recursive_process(item, output_directory / item.name, task)
            continue

        print(f"Processing {item}")
        task(item, output_directory / item.name)