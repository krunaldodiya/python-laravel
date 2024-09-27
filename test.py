import os

from pathlib import Path


def main(loopable_directory_path: Path):
    for root, dirs, files in os.walk(loopable_directory_path):
        dir_path = Path(root)

        init_file = dir_path / "__init__.py"

        if not init_file.exists():
            init_file.touch()

            print(f"Created: {init_file}")
        else:
            print(f"Exists: {init_file}")


if __name__ == "__main__":
    loopable_directory_path = Path("Illuminate")
    main(loopable_directory_path)
