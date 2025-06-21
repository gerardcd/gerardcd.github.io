import re
import pandas as pd
from tqdm import tqdm

N_PROBLEMS = 100
N_SUBMISSIONS = 30
N_WORDS = 20
N_LINES = 20
LANGUAGE = "Go"

WORD_SEPARATORS = "[ \t;\n\.,\"\[\]{}\(\)]+"

tqdm.pandas()

print("Reading submissions...")
submissions = pd.read_csv("problems_merged.csv")
submissions = submissions[submissions["language"] == LANGUAGE]

submissions_words = pd.DataFrame(columns=["submission_id", "description", "word"])
submissions_lines = pd.DataFrame(columns=["submission_id", "description", "line"])

seen_problems = set()
submission_i = 0

print("Generating lines and words...")
for i, submission in submissions.iterrows():
    if submission["problem_id"] not in seen_problems:
        seen_problems.add(submission["problem_id"])
        submission_i = 0

    if len(seen_problems) == N_PROBLEMS:
        break

    submission_i += 1

    if submission_i > N_SUBMISSIONS:
        continue


    code = submission["code"]

    try:
        lines = list(filter(len, code.split("\n")))
        words = list(filter(len, re.split(WORD_SEPARATORS, code)))
    except:
        lines = words = []

    for line in lines[-N_LINES:]:
        submissions_lines = submissions_lines.append({
            "submission_id": submission["submission_id"],
            "description": submission["description"],
            "line": line
        }, ignore_index=True)

    for word in words[-N_WORDS:]:
        submissions_words = submissions_words.append({
            "submission_id": submission["submission_id"],
            "description": submission["description"],
            "word": word
        }, ignore_index=True)

    print(i)

submissions_lines.to_csv("submission_lines.csv", index=False, header=True)
submissions_words.to_csv("submission_words.csv", index=False, header=True)