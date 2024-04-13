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
        for candidate_name in os.listdir(folder_with_candidates):
            candidate_path = os.path.join(folder_with_candidates, candidate_name)
            
            if os.path.isdir(candidate_path):
                for file_name in os.listdir(candidate_path):
                    if file_name.endswith(".txt"):  # Filter text files
                        file_path = os.path.join(candidate_path, file_name)
                        
                        with open(file_path, 'r') as file:
                            candidate_file_text = file.read()
                            probability_plagiat = jaccard_similarity(candidate_file_text, uknown_file_text)
                            collected_data_comparison.append(PlagiarismDataComparison(candidate_name, uknown_file_name, file_name, probability_plagiat))  
    
    for data in collected_data_comparison:
        print("Candidate:", data.candidate)
        print("Unknown File Name:", data.unknownFileName)
        print("Candidate File Name:", data.candidateFileName)
        print("Percentage Plagiat:", data.percentagePlagiat)
        print("-" * 50)  # Separator
    
    

class PlagiarismDataComparison:
    def __init__(self, candidate, unknownFileName, candidateFileName, percentagePlagiat):
        self.candidate = candidate
        self.unknownFileName = unknownFileName
        self.candidateFileName = candidateFileName
        self.percentagePlagiat = percentagePlagiat
        
        

collect_uknown_data(2)
check_plagiat()



        







