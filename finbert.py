

from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from bs4 import BeautifulSoup
import os
import json
import transformers



def download_model():
    from huggingface_hub import snapshot_download

    # ✅ Correct: Download from Hugging Face Hub
    snapshot_download(repo_id="yiyanghkust/finbert-tone", local_dir="finbert_model")

def test():
    #finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
    #tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

    #nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

    model_path = "./finbert_model"

    # Save the model and tokenizer
    #finbert.save_pretrained(save_directory)
    #tokenizer.save_pretrained(save_directory)

    # Load the model and tokenizer from local directory
    finbert = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    # Create the pipeline
    nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

    sentences = ["there is a shortage of capital, and we need extra financing",  
                "growth is strong and we have plenty of liquidity", 
                "there are doubts about our finances", 
                "profits are flat"]
    results = nlp(sentences)
    print(results)  #LABEL_0: neutral; LABEL_1: positive; LABEL_2: negative


def analyze_text_with_finbert(text_list):
    # Load FinBERT model and tokenizer
    
    
    # Analyze the text
    results = nlp(text_list)
    return results

def process_json_file(input_json_path):
    """finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
    tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
    
    # Create sentiment analysis pipeline
    nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

    model_path = "./finbert_model"

    # Save the model and tokenizer
    finbert.save_pretrained(save_directory)
    tokenizer.save_pretrained(save_directory)"""

    #transformers.utils.offline_mode(True)

    model_path = "./finbert_model"
    finbert = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)
    # Read the input JSON file
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        
        file_path = item['file_path']
        text = item['text']
        
        # Create output path by appending .json to the original file path
        output_path = f"results/{file_path.replace('\\','_').replace(':','').split('.')[0]}.json"
        
        if text is not None:
            #print(item)
            #print(text)
            #print(file_path)
            #print(text is None)
            # Check if output file already exists
            if not os.path.exists(output_path):
                try:
                    # Analyze the text
                    text = text.split('.')
                    results  = nlp(text)
                    
                    # Prepare the output data
                    output_data = {
                        'original_file': file_path,
                        'text': text,
                        'sentiment_analysis': results
                    }
                    
                    # Save the results
                    print(output_path)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(output_data, f, indent=2)
                    
                    #print(f"Processed and saved: {output_path}")
                except Exception as e:
                    raise e
                    print(f"Error processing {file_path}: {str(e)}")
          

            
        else:
            print(file_path)
if __name__ == "__main__":
    print(os.environ['TRANSFORMERS_OFFLINE'])
    
    input_json_path = "extracted_texts.json"
    #download_model()
    process_json_file(input_json_path)


