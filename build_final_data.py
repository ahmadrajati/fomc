import pandas as pd 
import os
import json

"""
D_FOMC_fomc_documents_monetarypolicy_files_FOMC20001003meeting            "Transcript",
D_FOMC_fomc_documents_boarddocs_press_monetary_2004_20040128_default    ==>   "Policy Statements"     , "Statement"   
D_FOMC_fomc_documents_boarddocs_press_general_2001_20010320_default    ==>   "Policy Statements"
_home_maoud_FOMC_fomc_documents_monetarypolicy_files_monetary20160727a1    ==>   "Policy Statements"
D_FOMC_fomc_documents_monetarypolicy_fomcpresconf20200429                        "Press Conference",
"""


import os
import json
import re
from collections import defaultdict
from glob import glob

def extract_date_from_path(path):
    match =  re.search(r"(\d{8})", path )
    return match.group(1) if match else "unknown"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sentiments = data['sentiment_analysis']
    scores_by_class = defaultdict(list)

    for s in sentiments:
        if isinstance(s, dict):
            scores_by_class[s['label']].append(s['score'])

    if len(scores_by_class) > 0:
        # Average score by sentiment
        #print(scores_by_class.items())
        avg_scores = {k: sum(v)/len(v) for k, v in scores_by_class.items()}
        dominant_class = max(avg_scores.items(), key=lambda x: x[1])[0]
        dominant_score = avg_scores[dominant_class]

        # Sentiment counts
        class_counts = {k: len(v) for k, v in scores_by_class.items()}

        original_file = data['original_file']
        date = extract_date_from_path(original_file)
        name = os.path.basename(original_file)

        # Return with top-level keys
        return {
            "class": dominant_class,
            "score": dominant_score,
            "date": date,
            "name": name,
            "full_path":original_file,
            "positive": class_counts.get("Positive", 0),
            "neutral": class_counts.get("Neutral", 0),
            "negative": class_counts.get("Negative", 0)
        }

    
    original_file = data['original_file']
    date = extract_date_from_path(original_file)
    name = os.path.basename(original_file)
    return {"class":0, "score":0, "date":date, "name":name,"positive": 0,
            "neutral": 0,
            "negative": 0}
        
    

if __name__ == "__main__":
    # Get all JSON files from the results folder
    results_folder = 'results'
    json_files = glob(os.path.join(results_folder, '*.json'))

    # Process all files
    summary = [process_file(f) for f in json_files]

    pd.DataFrame(summary).to_excel("final_tone.xlsx")
