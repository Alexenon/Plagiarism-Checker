import os
from jacard import jaccard_similarity
from tkinter.filedialog import askopenfiles

folder_with_unknown_data = "dataset/unknown"
folder_with_candidates_data = "dataset/candidates"

def collect_uknown_data(n):
    file_counter = 0
    files_with_uknown_data = {}
    for unknown_file_name in os.listdir(folder_with_unknown_data):
        file_path = os.path.join(folder_with_unknown_data, unknown_file_name)
        with open(file_path, 'r') as file:
            files_with_uknown_data[unknown_file_name] = file.read()
                
        file_counter += 1
        if file_counter >= n:
            break
        
    return files_with_uknown_data
    
    
    
def collect_data_comparation(uknown_data):
    collected_data_comparation = []
    for uknown_file_name, uknown_file_text in uknown_data.items():
        print(f"Searching plagialism for {uknown_file_name}")
        for candidate_name in os.listdir(folder_with_candidates_data):
            candidate_folder_path = os.path.join(folder_with_candidates_data, candidate_name)
            print(f"Scanning {candidate_name}")
            
            if os.path.isdir(candidate_folder_path):
                for candidate_file_name in os.listdir(candidate_folder_path):
                    file_path = os.path.join(candidate_folder_path, candidate_file_name)
                    
                    with open(file_path, 'r') as file:
                        candidate_file_text = file.read()
                        probability_plagiat = jaccard_similarity(candidate_file_text, uknown_file_text)
                        collected_data_comparation.append(PlagiarismDataComparation(candidate_name, uknown_file_name, candidate_file_name, probability_plagiat))       
        print("_" * 50)
    return collected_data_comparation


    
class PlagiarismDataComparation:
    def __init__(self, candidate, unknownFileName, candidateFileName, percentagePlagiat):
        self.candidate = candidate
        self.unknownFileName = unknownFileName
        self.candidateFileName = candidateFileName
        self.percentagePlagiat = percentagePlagiat
        
        
def best_matches(dataComparation, fileName, first_n_matches):
    filtered_matches_by_unknown_file_name = [match for match in dataComparation if match.unknownFileName == fileName]
    sorted_matches = sorted(filtered_matches_by_unknown_file_name, key=lambda x: x.percentagePlagiat, reverse=True)
    top_n_matches = sorted_matches[:first_n_matches]
    
    formatted_matches = []
    for i, match in enumerate(top_n_matches, start=1):
        # Convert percentage (e.g., 0.09948979591836735 -> 99.94%)
        formatted_percent = f"{match.percentagePlagiat * 100:.2f}%"
        formatted_matches.append((match.candidate, match.candidateFileName, formatted_percent))
    
    return formatted_matches


def display_best_matches_results(uknown_data, data_comparation, first_n_matches):
    print(" " * 25 + "RESULTS" + "\n" + "_" * 50)
    for file_name, file_text in uknown_data.items():
        matches = best_matches(data_comparation, file_name, first_n_matches)
        print(f"# Uknown File: {file_name}")
        for i, (candidate, candidateFileName, percent) in enumerate(matches, start=1):
            print(f"{i}. {candidate} {candidateFileName} {percent}")
        print("_" * 50)
    
    

# uknown_data = collect_uknown_data(4)
# data_comparation = collect_data_comparation(uknown_data)
# display_best_matches_results(uknown_data, data_comparation, 5)








    

        
    





