import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def correct_text(text, model, tokenizer, device=None, max_length=1024, temperature=0.1, system_prompt="You are a corrector of French texts. Correct the text without explaining."): 
    """
    Generates the corrected version of 'text' using the given model.
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    prompt = (
        f"[System]\n{system_prompt}\n\n"
        f"[Text]\n{text}\n\n"
        f"[Correction]"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    model.eval()
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=1024,
            temperature=0.1,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Extract the corrected text from the full string
    if "[Correction]" in decoded_output:
        corrected_text = decoded_output.split("[Correction]", 1)[1]
    else:
        corrected_text = decoded_output

    return corrected_text.strip()