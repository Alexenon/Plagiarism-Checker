from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import nltk
nltk.download('punkt')
nltk.download('stopwords')

def jaccard_similarity(text1, text2):
    tokens1 = set(word_tokenize(text1.lower()))
    tokens2 = set(word_tokenize(text2.lower()))
    
    stop_words = set(stopwords.words('english'))
    tokens1 = {word for word in tokens1 if word not in stop_words}
    tokens2 = {word for word in tokens2 if word not in stop_words}
    
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1) + len(tokens2) - intersection
    
    return intersection / union

# Example texts
text1 = "The cat sat on the mat."
text2 = "A cat was sitting on the mat."

# Calculate Jaccard Similarity
similarity_score = jaccard_similarity(text1, text2)
print(f"Jaccard Similarity: {similarity_score}")
