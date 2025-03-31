import os
import zipfile
import tempfile
import pandas as pd

def allowed_file(filename, allowed_extensions={'zip', 'csv', 'xlsx', 'txt', 'json', 'pdf'}):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_zip(zip_path):
    """Extract a zip file to a temporary directory and return the paths of extracted files."""
    extracted_files = []
    extract_dir = tempfile.mkdtemp()
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
        # Get all extracted files
        for root, _, files in os.walk(extract_dir):
            for file in files:
                extracted_files.append(os.path.join(root, file))
    
    return extracted_files

def process_csv(file_path):
    """Read and process a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        return f"Error processing CSV: {str(e)}"

def process_excel(file_path):
    """Read and process an Excel file."""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        return f"Error processing Excel file: {str(e)}"

def process_text_file(file_path):
    """Read and process a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def process_json_file(file_path):
    """Read and process a JSON file."""
    try:
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        # If the JSON can't be parsed properly, read it as plain text
        return process_text_file(file_path)

def process_file_content(file_path):
    """Process file based on extension."""
    _, extension = os.path.splitext(file_path)
    extension = extension.lower().lstrip('.')
    
    if extension == 'csv':
        return process_csv(file_path)
    elif extension in ['xls', 'xlsx']:
        return process_excel(file_path)
    elif extension == 'json':
        return process_json_file(file_path)
    elif extension in ['txt', 'md', 'py', 'java', 'c', 'cpp', 'html', 'css', 'js']:
        return process_text_file(file_path)
    else:
        return f"File type {extension} not supported for detailed processing."

def check_for_direct_answer(file_path, question):
    """Check if the file contains a direct answer to the question."""
    
    # Specific handling for CSV files with "answer" column
    if file_path.lower().endswith('.csv'):
        try:
            df = pd.read_csv(file_path)
            
            # Check if "answer" column exists
            if "answer" in df.columns:
                # If the question is asking for the value in the "answer" column
                if "what is the value in the \"answer\" column" in question.lower() or \
                   "what is the value in the 'answer' column" in question.lower():
                    if not df.empty:
                        # Return the first value in the "answer" column
                        return str(df["answer"].iloc[0])
        except Exception:
            pass
    
    # Return None if no direct answer found
    return None