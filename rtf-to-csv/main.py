from pathlib import Path
from typing import List, Union
import csv

workingDir = Path.cwd()
outputPath = Path.cwd() / 'output'


def rtf_to_csv(file: Union[str, Path], header: str) -> None:
    """
    Convert a rtf file to csv file
    """

    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [line.strip().rstrip().replace(
            ",", "").replace("\\", "").replace(" ", "").replace("+", "") for line in lines if line.strip() != '']

        if not outputPath.exists():
            outputPath.mkdir(exist_ok=True)

        with open(outputPath / f'{file.stem}.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([header])
            for line in lines:
                csvwriter.writerow([line])


if __name__ == "__main__":
    relativePath = input(
        "Enter the relative path of the file (relative): ")

    filePath = workingDir / relativePath

    if not filePath.exists():
        print('File not found')
        exit(1)

    header = input('Enter the header of the csv file: ')

    rtf_to_csv(filePath, header)
    print('Done')
