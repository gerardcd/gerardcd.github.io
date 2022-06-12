import pandas as pd
from tqdm import tqdm

tqdm.pandas()

N_PROBLEMS = 100

# Read the problems
problems = pd.read_csv("CodeNetSplit/metadata/problem_list.csv", nrows=N_PROBLEMS)


# Read problems descriptions
def read_description(problem):
    with open(f"CodeNetSplit/problem_descriptions/{problem['id']}.html", encoding="UTF-8") as fd:
        return fd.read()


problems["description"] = problems.apply(read_description, axis=1)

# Merge problems and submissions
problems_merged = pd.DataFrame()

print("Merging problems and submissions...")
for problem_id in tqdm(problems["id"]):
    submissions = pd.read_csv(f"CodeNetSplit/metadata/{problem_id}.csv")
    submissions_merge = pd.merge(left=problems, right=submissions, left_on="id", right_on="problem_id")

    problems_merged = pd.concat([problems_merged, submissions_merge])


# Calculate accuracy percentage
def calculate_accuracy_percentage(submission):
    accuracy = submission["accuracy"]

    if type(accuracy) is str:
        accuracy = accuracy.split("/")
        return (int(accuracy[0]) / int(accuracy[1])) * 100
    else:
        return 50


print("Calculating accuracy percentage...")
problems_merged["accuracy_percentage"] = problems_merged.progress_apply(calculate_accuracy_percentage, axis=1)


# Add submission codes
def read_submission_code(submission):
    problem_id, language, submission_id, file_ext = submission["problem_id"], submission["language"], submission["submission_id"], submission["filename_ext"]
    with open(f"CodeNetSplit/data/{problem_id}/{language}/{submission_id}.{file_ext}", encoding="UTF-8") as fd:
        return fd.read()


print("Adding submission codes...")
problems_merged["code"] = problems_merged.progress_apply(read_submission_code, axis=1)

print("Writing to CSV...")
problems_merged.to_csv("problems_merged.csv")