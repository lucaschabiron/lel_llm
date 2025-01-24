from transformers import AutoTokenizer
from typing import Dict, List

def generate_template(examples: Dict[str, List[str]], tokenizer=None, system_message = "You are a corrector of French texts. Correct the text without explaining.", max_length=512):
    """
    This function prepares the dataset examples into the format
    required by the model for training.
    If no tokenizer is provided, the function will return the prompts untokenized.
    """
    
    prompts = []
    for input_text, output_text in zip(examples["input"], examples["output"]):
        
        prompt = (
            f"[System]\n{system_message}\n\n"
            f"[Text]\n{input_text}\n\n"
            f"[Correction]{output_text}{tokenizer.eos_token}" 
        )
        prompts.append(prompt)
    
    if tokenizer is not None:
        tokenizer.pad_token = tokenizer.eos_token

        # Tokenize the chat texts
        tokenized = tokenizer(
            prompts,
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
    
    return prompts 