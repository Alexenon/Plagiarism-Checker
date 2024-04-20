import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

folder_with_unknown_data = "dataset/unknown"
folder_with_candidates_data = "dataset/candidates"


def jaccard_similarity(text1, text2):
    tokens1 = set(word_tokenize(text1.lower()))
    tokens2 = set(word_tokenize(text2.lower()))

    stop_words = set(stopwords.words('english'))
    tokens1 = {word for word in tokens1 if word not in stop_words}
    tokens2 = {word for word in tokens2 if word not in stop_words}

    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1) + len(tokens2) - intersection

    return intersection / union


def collect_unknown_data(n):
    file_counter = 0
    files_with_unknown_data = {}
    for unknown_file_name in os.listdir(folder_with_unknown_data):
        file_path = os.path.join(folder_with_unknown_data, unknown_file_name)
        with open(file_path, 'r') as file:
            files_with_unknown_data[unknown_file_name] = file.read()

        file_counter += 1
        if file_counter >= n:
            break

    return files_with_unknown_data


def collect_data_comparation(unknown_data):
    collected_data_comparation = []
    for unknown_file_name, unknown_file_text in unknown_data.items():
        print(f"Searching plagiarism for {unknown_file_name}")
        for candidate_name in os.listdir(folder_with_candidates_data):
            candidate_folder_path = os.path.join(folder_with_candidates_data, candidate_name)
            print(f"Scanning {candidate_name}")

            if os.path.isdir(candidate_folder_path):
                for candidate_file_name in os.listdir(candidate_folder_path):
                    file_path = os.path.join(candidate_folder_path, candidate_file_name)

                    with open(file_path, 'r') as file:
                        candidate_file_text = file.read()
                        probability_plagiat = jaccard_similarity(candidate_file_text, unknown_file_text)
                        collected_data_comparation.append(
                            PlagiarismDataComparation(candidate_name, unknown_file_name, candidate_file_name,
                                                      probability_plagiat))
        print("_" * 50)
    return collected_data_comparation


class PlagiarismDataComparation:
    def __init__(self, candidate, unknown_file_name, candidate_file_name, percentage_plagiat):
        self.candidate = candidate
        self.unknownFileName = unknown_file_name
        self.candidateFileName = candidate_file_name
        self.percentagePlagiat = percentage_plagiat


def best_matches(data_comparation, file_name, first_n_matches):
    filtered_matches_by_unknown_file_name = [match for match in data_comparation if match.unknownFileName == file_name]
    sorted_matches = sorted(filtered_matches_by_unknown_file_name, key=lambda x: x.percentagePlagiat, reverse=True)
    top_n_matches = sorted_matches[:first_n_matches]

    formatted_matches = []
    for i, match in enumerate(top_n_matches, start=1):
        # Convert percentage (e.g., 0.09948979591836735 -> 99.94%)
        formatted_percent = f"{match.percentagePlagiat * 100:.2f}%"
        formatted_matches.append((match.candidate, match.candidateFileName, formatted_percent))

    return formatted_matches


def display_best_matches_results(unknown_data, data_comparation, first_n_matches):
    print(" " * 25 + "RESULTS" + "\n" + "_" * 50)
    for file_name, file_text in unknown_data.items():
        matches = best_matches(data_comparation, file_name, first_n_matches)
        print(f"# Unknown File: {file_name}")
        for i, (candidate, candidateFileName, percent) in enumerate(matches, start=1):
            print(f"{i}. {candidate} {candidateFileName} {percent}")
        print("_" * 50)