import os
import chardet
import pandas as pd

def read_csv(file_name: str, fallback_encoding: str = 'utf-8'):
    path = os.path.join('../data', file_name)
    data, encoding = None, None

    try:
        with open(path, 'rb') as f:
            data = f.read(1000)
    except FileNotFoundError:
        print(f'File not found: {path}')
        return None    

    try:
        encoding_result = chardet.detect(data)
        encoding = encoding_result['encoding']
        confidence = encoding_result['confidence']
        print(f'Found encoding: {encoding} ({confidence * 100:.2f}% certainty)')
        if (confidence < 0.7):
            raise LookupError
    except LookupError:
        print(f'Failed to detect encoding. Using fallback encoding {fallback_encoding}...')
        encoding = fallback_encoding

    return pd.read_csv(path, encoding=encoding)