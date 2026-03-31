import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """

    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    # Check empty input
    if filename == "":
        print("Error: No filename provided.")
        sys.exit(1)

    # Check file existence
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Check empty file
            if reader.fieldnames is None:
                print("Error: CSV file has no headers.")
                sys.exit(1)

            for row in reader:
                try:
                    assignments.append({
                        'assignment': row['assignment'],
                        'group': row['group'],
                        'score': float(row['score']),
                        'weight': float(row['weight'])
                    })
                except ValueError:
                    print(f"Error: Invalid data in row: {row}")
                    sys.exit(1)

        if len(assignments) == 0:
            print("Error: CSV file is empty.")
            sys.exit(1)

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Evaluate grades and print results
    """

    print("\n--- Processing Grades ---")

    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    total_score = 0
    formative_score = 0
    summative_score = 0

    failed_formative = []

    for item in data:
        score = item['score']
        weight = item['weight']
        group = item['group']

        # Validate score
        if score < 0 or score > 100:
            print(f"Error: Invalid score in '{item['assignment']}'")
            sys.exit(1)

        # Validate group
        if group not in ["Formative", "Summative"]:
            print(f"Error: Invalid group in '{item['assignment']}'")
            sys.exit(1)

        total_weight += weight
        total_score += (score * weight) / 100

        if group == "Formative":
            formative_weight += weight
            formative_score += (score * weight) / 100

            if score < 50:
                failed_formative.append(item)

        elif group == "Summative":
            summative_weight += weight
            summative_score += (score * weight) / 100

    # Validate weights
    if total_weight != 100:
        print(f"Error: Total weight is {total_weight}, must be 100.")
        sys.exit(1)

    if formative_weight != 60:
        print(f"Error: Formative weight is {formative_weight}, must be 60.")
        sys.exit(1)

    if summative_weight != 40:
        print(f"Error: Summative weight is {summative_weight}, must be 40.")
        sys.exit(1)

    # GPA calculation
    gpa = (total_score / 100) * 5

    # Category percentages
    formative_percent = (formative_score / formative_weight) * 100
    summative_percent = (summative_score / summative_weight) * 100

    print(f"\nFinal GPA: {gpa:.2f}")
    print(f"Formative Score: {formative_percent:.2f}%")
    print(f"Summative Score: {summative_percent:.2f}%")

    # Pass/Fail
    if formative_percent >= 50 and summative_percent >= 50:
        print("FINAL STATUS: PASSED")
    else:
        print("FINAL STATUS: FAILED")

    # Resubmission logic
    if failed_formative:
        print("\n--- Resubmission Required ---")

        max_weight = max(item['weight'] for item in failed_formative)

        for item in failed_formative:
            if item['weight'] == max_weight:
                print(f"- {item['assignment']} (Weight: {item['weight']})")
    else:
        print("\nNo resubmission needed.")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
