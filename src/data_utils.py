import random
import re

def delete_random_char(word):
    if len(word) == 0:
        return word
    index = random.randint(0, len(word) - 1)
    return word[:index] + word[index + 1:]

def insert_random_char(word):
    index = random.randint(0, len(word))
    random_char = random.choice('abcdefghijklmnopqrstuvwxyzéèêëàâäôöùûüîïç')
    return word[:index] + random_char + word[index:]

def substitute_random_char(word):
    if len(word) == 0:
        return word
    index = random.randint(0, len(word) - 1)
    random_char = random.choice('abcdefghijklmnopqrstuvwxyzéèêëàâäôöùûüîïç')
    return word[:index] + random_char + word[index + 1:]

def remove_random_punctuation(text):
    punctuation_marks = ['.', ',', ';', ':', '!', '?', '-', '—', '(', ')', '[', ']', '{', '}', '"', "'"]
    text_list = list(text)
    indices = [i for i, ch in enumerate(text_list) if ch in punctuation_marks]
    if indices:
        index = random.choice(indices)
        del text_list[index]
    return ''.join(text_list)

def add_random_punctuation(text):
    punctuation_marks = ['.', ',', ';', ':', '!', '?']
    index = random.randint(0, len(text) - 1)
    punct = random.choice(punctuation_marks)
    return text[:index] + punct + text[index:]

def remove_random_space(text):
    indices = [i for i, ch in enumerate(text) if ch == ' ']
    if indices:
        index = random.choice(indices)
        return text[:index] + text[index + 1:]
    return text

def add_extra_space(text):
    index = random.randint(0, len(text) - 1)
    return text[:index] + ' ' + text[index:]

def random_case_change(text):
    return ''.join(ch.upper() if random.random() < 0.05 else ch for ch in text)

ocr_confusions = {
    '0': 'O',
    'O': '0',
    '1': 'l',
    'l': '1',
    'rn': 'm',
    'm': 'rn',
    'I': '1',
    'S': '5',
    '5': 'S',
    'B': '8',
    '8': 'B',
    'a': 'à',
    'e': 'é',
    'c': 'ç',
}


def simulate_ocr_errors(text, error_probability=0.2):
    result = ''
    i = 0
    while i < len(text):
        applied_confusion = False
        # Check for multi-character confusions first
        for k, v in ocr_confusions.items():
            # Ensure we don't go out of bounds and check if substring matches
            if text[i:i+len(k)] == k:
                # Randomly decide whether to apply the confusion
                if random.random() < error_probability:
                    result += v
                else:
                    result += k
                i += len(k)
                applied_confusion = True
                break  # Exit the loop after applying a confusion
        if not applied_confusion:
            result += text[i]
            i += 1
    return result

def introduce_errors(text, word_error_prob=0.2, char_error_prob=0.1, ocr_error_prob=0.1):
    unk_placeholder = '<<UNK_PLACEHOLDER>>'

    text_with_placeholders = text.replace('[unk]', unk_placeholder)
    tokens = re.findall(r'\S+|\s+', text_with_placeholders)
    new_tokens = []
    
    for token in tokens:
        if token.isspace():
            new_tokens.append(token)
        # Si le token est le placeholder [unk], le laisser tel quel
        elif token == unk_placeholder:
            new_tokens.append(token)
        else:
            word = token
            if random.random() < char_error_prob:
                error_type = random.choice(['delete', 'insert', 'substitute'])
                if error_type == 'delete':
                    word = delete_random_char(word)
                elif error_type == 'insert':
                    word = insert_random_char(word)
                elif error_type == 'substitute':
                    word = substitute_random_char(word)
            new_tokens.append(word)

    
    text_with_errors = ''.join(new_tokens)
    protected_text = text_with_errors
    
    if random.random() < word_error_prob:
        protected_text = simulate_ocr_errors(protected_text, error_probability=ocr_error_prob) 
        if random.random() < 0.5:
            protected_text = remove_random_punctuation(protected_text)
        else:
            protected_text = add_random_punctuation(protected_text)
        if random.random() < 0.5:
            protected_text = remove_random_space(protected_text)
        else:
            protected_text = add_extra_space(protected_text)
        protected_text = random_case_change(protected_text)

    final_text = protected_text.replace(unk_placeholder, '[unk]')
    
    return final_text