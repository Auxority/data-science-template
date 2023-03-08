import os
import chardet
import pandas as pd
from DataVisualizer import *
from DataExplorer import *

def find_encoding(file_name: str, fallback_encoding: str = 'utf-8') -> str:
    path = os.path.abspath(os.path.join('../data', file_name))
    data, encoding = None, None

    try:
        with open(path, 'rb') as f:
            data = f.read(1000)
    except FileNotFoundError:
        print(f'File not found: {path}')
        return fallback_encoding

    if not data:
        print(f'File is empty: {path}')
        return fallback_encoding

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

    return encoding

def explore(df: pd.DataFrame, dv: DataVisualizer = None) -> None:
    if dv is None:
        dv = DataVisualizer()

    explorer = DataExplorer(dv)
    explorer.explore(df)
