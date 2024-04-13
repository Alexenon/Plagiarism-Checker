import os
from jacard import jaccard_similarity
from tkinter.filedialog import askopenfiles

folder_with_unknown = "dataset/unknown"
folder_with_candidates = "dataset/candidates"

# Dictionary to store file name and text 
files_uknown_data = {}

def collect_uknown_data(n):
    file_counter = 0
    for unknown_file_name in os.listdir(folder_with_unknown):
        file_path = os.path.join(folder_with_unknown, unknown_file_name)
        with open(file_path, 'r') as file:
            files_uknown_data[unknown_file_name] = file.read()
                
        file_counter += 1
        
        if file_counter >= n:
            break
    

collected_data_comparison = []


def check_plagiat():
    for uknown_file_name, uknown_file_text in files_uknown_data.items():
        print(f"Searching plagialism for {uknown_file_name}")
        for candidate_name in os.listdir(folder_with_candidates):
            candidate_folder_path = os.path.join(folder_with_candidates, candidate_name)
            print(f"Scanning {candidate_name}")
            
            if os.path.isdir(candidate_folder_path):
                for candidate_file_name in os.listdir(candidate_folder_path):
                    file_path = os.path.join(candidate_folder_path, candidate_file_name)
                    
                    with open(file_path, 'r') as file:
                        candidate_file_text = file.read()
                        probability_plagiat = jaccard_similarity(candidate_file_text, uknown_file_text)
                        collected_data_comparison.append(PlagiarismDataComparison(candidate_name, uknown_file_name, candidate_file_name, probability_plagiat))       
        print("_" * 50)

    
    

class PlagiarismDataComparison:
    def __init__(self, candidate, unknownFileName, candidateFileName, percentagePlagiat):
        self.candidate = candidate
        self.unknownFileName = unknownFileName
        self.candidateFileName = candidateFileName
        self.percentagePlagiat = percentagePlagiat
        
        
def bestMatches(unknownFileName, n):
    filtered_matches_by_unknown_file_name = [match for match in collected_data_comparison if match.unknownFileName == unknownFileName]
    sorted_matches = sorted(filtered_matches_by_unknown_file_name, key=lambda x: x.percentagePlagiat, reverse=True)
    top_n_matches = sorted_matches[:n]
    
    formatted_matches = []
    for i, match in enumerate(top_n_matches, start=1):
        # Convert percentage (e.g., 0.09948979591836735 -> 99.94%)
        formatted_percent = f"{match.percentagePlagiat * 100:.2f}%"
        formatted_matches.append((match.candidate, match.candidateFileName, formatted_percent))
    
    return formatted_matches
    

collect_uknown_data(4)
check_plagiat()


print(" " * 25 + "RESULTS" + "\n" + "_" * 50)
for file_name, file_text in files_uknown_data.items():
    matches = bestMatches(file_name, 5)
    print(f"# Uknown File: {file_name}")
    for i, (candidate, candidateFileName, percent) in enumerate(matches, start=1):
        print(f"{i}. {candidate} {candidateFileName} {percent}")
    print("_" * 50)
    





    

        
    





