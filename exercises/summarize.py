"""Solution for the Summarize exercise."""
import os
import csv
from pathlib import Path
import solution

# DATA = Path(__file__).parent / "data" / "customers-1000.csv"
DATA = Path(__file__).parent / "customers-1000.csv"

def summarize(data: Path, by: str) -> dict[str, int]:
  """Get the number of records in a .csv file that share the `by` column value.

  Args:
    path (str): The path to the .csv file.
    by (str): The column name to group by.
  """
  summary: dict[str, int] = {}

  # Implement the solution here
  with open(data, mode="r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    if by not in reader.fieldnames:
      raise ValueError(f"Column '{by}' does not exist in the .csv file.")

    for row in reader:
      value = row[by]
      if value in summary:
        summary[value] += 1
      else:
        summary[value] = 1

    sorted_summary = { key: summary[key] for key in sorted(summary) }

    with open("student_answer.py", mode="w", encoding="utf-8") as file:
      file.write("summary = {\n")
      for key, value in sorted_summary.items():
        file.write(f'   "{key}": {value},\n')
      file.write("}\n")

    print(sorted_summary)

    return sorted_summary

if __name__ == "__main__":
  BY_COLUMN = 'Country'
  try:
    assert summarize(DATA, BY_COLUMN) == solution.SOLUTION, "❌ Incorrect solution! ❌"
    print(f"✔️ Solution is correct! Good Job {os.environ.get('USERNAME', 'Person')}! ✔️")
  except AssertionError as e:
    print(e)
