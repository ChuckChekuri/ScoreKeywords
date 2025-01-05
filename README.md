# Keyword Scoring in Corpus Analysis

## Overview
This project focuses on scoring keywords within a corpus to understand their relevance based on similarity criteria. It involves encoding document chunks into a vector database for analysis and scoring.

## Technologies Used
- **Python**: For backend logic and data manipulation.
- **Vector Database**: For storing document chunks (e.g., FAISS, Pinecone).
- **UI Framework**: Flask or Django for serving the user interface.

## Prerequisites
- Python 3.x
- Libraries: pandas, numpy, [vector_db_library], [ui_framework_library]

## Installation
1. Clone the repository: git@github.com:ChuckChekuri/ScoreKeywords.git

2. Install dependencies:
   pip install -r requirements.txt


## Project Structure
ScoreKeywords/
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── skwenv/
├── corpus/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── migrations/
│   └── templates/
├── vector_db/
│   ├── __init__.py
│   ├── faiss_db.py
│   ├── in_memory_db.py
│   └── tests.py
└── ui/
    ├── __init__.py
    ├── channels.py
    ├── consumers.py
    ├── routing.py
    ├── templates/
    └── static/

## Usage
1. **Setup Corpus**:
- Select 'New Corpus' from the UI.
- Name your corpus and upload or select document locations (Excel file or folder paths).
- Set chunk size.

2. **Keyword Management**:
- Add, edit, or remove keywords for analysis.

3. **Scoring**:
- Initiate scoring from the UI to use the in-memory vector DB for real-time analysis.

## Features
- Customizable UI for corpus and keyword management.
- Vector DB integration for document storage and retrieval.
- In-memory DB for quick keyword scoring.

## Contributing
Please read [CONTRIBUTING.md](link-to-contributing) for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the [MIT License](LICENSE.md).