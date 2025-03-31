# TDS Solver API

A Flask-based API that automatically answers IIT Madras' Online Degree in Data Science graded assignment questions using the SambaNova LLM API.

## Features

- Accepts questions from any of the 5 graded assignments
- Processes file attachments, including zip files with CSV, Excel, TXT, and other data files
- Extracts information from fi{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}les to help answer the questions
- Returns answers in a simple JSON format ready to be entered in the assignments

## Project Setup

### Prerequisites

- Python 3.8 or higher
- SambaNova API key

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/tds-solver.git
cd tds-solver
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory:
```
SAMBANOVA_API_KEY=your_api_key_here
SAMBANOVA_API_URL=https://api.sambanova.ai/api/v1/completions
```

### Running Locally

Start the Flask development server:
```bash
python app.py
```

The API will be available at `http://localhost:5000/api/`

## API Usage

### Endpoint

POST request to `/api/`

### Request Format

Send a POST request with `multipart/form-data` containing:
- `question`: The assignment question text
- `file` (optional): Any file attachment needed to answer the question

### Example Request

Using cURL:
```bash
curl -X POST "https://your-app.vercel.app/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?" \
  -F "file=@abcd.zip"
```

Using Python requests:
```python
import requests

url = "https://your-app.vercel.app/api/"
files = {'file': open('abcd.zip', 'rb')}
data = {'question': "Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### Response Format

```json
{
  "answer": "1234567890"
}
```

## Deployment Options

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel --prod
```

4. Set environment variables in the Vercel dashboard.

### Alternative Deployment Options

#### Render

1. Create a new Web Service in the Render dashboard
2. Connect your GitHub repository
3. Set environment variables in the dashboard
4. Deploy

#### Railway

1. Create a new project in Railway
2. Connect your GitHub repository
3. Set environment variables
4. Deploy

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.