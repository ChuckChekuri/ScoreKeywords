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
## Getting Started
1. go to : http://github.com/ChuckChekuri/ScoreKeywords

2. Download the Zip file and extract them to "ScoreKeywords" folder
   This is the project root (PROJECT_ROOT) folder  
   ![Download Git Source](git_download_zip.png)


3. Open Anconda Command Prompt to create python env
   `cd <PROJECT_ROOT> 
   `python -m venv skwenv`

4. Install dependencies:
   pip install -r requirements.txt --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org 

5. Run tests to verify that code is all there.
    - python manage.py test ui
    - pythom manage.py test encoder
    - python manage.py test vector_db


## Project Structure
```
ScoreKeywords/
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── skwenv/
├── encoders/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── langchain_service.py
│   │   └── vector_service.py
│   └── tests/
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
```
## Runing the dev server
Step 1: Run the Django Development Server
- `python manage.py runserver`

Step 2: Access the Views in the Browser
- Manage Corpus: http://127.0.0.1:8000/corpora/
- Create Corpus: http://127.0.0.1:8000/corpora/new/
- Corpus List: http://127.0.0.1:8000/corpora/list/
- Manage Keywords: http://127.0.0.1:8000/keywords/
- Create Keyword: http://127.0.0.1:8000/keywords/new/
- Keyword List: http://127.0.0.1:8000/keywords/list/


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


# Development workflow using dev container.

Here’s a concise development workflow using **Dev Containers** in Visual Studio Code, from initial setup to deployment:

| **Step**               | **Description**                                                                 |
|-------------------------|---------------------------------------------------------------------------------|
| **1. Project Setup**    | Clone the project repository and open it in VSCode.                             |
| **2. Dev Container Config** | Add or configure a `.devcontainer` folder with `Dockerfile` and `devcontainer.json`. |
| **3. Reopen in Container** | Use the **"Reopen in Container"** command to build and start the Dev Container. |
| **4. Develop**          | Write and test code inside the containerized environment.                       |
| **5. Debug**            | Use VSCode’s debugging tools within the container.                              |
| **6. Build & Test**     | Run build and test commands inside the container.                               |
| **7. Commit Changes**   | Commit code changes to version control (e.g., Git).                             |
| **8. CI/CD Integration**| Push changes to trigger CI/CD pipelines for automated testing and deployment.    |
| **9. Deploy**           | Deploy the application using containerized builds (e.g., Docker images).        |

This workflow ensures a consistent, isolated, and reproducible development environment.


## Contributing
Please read [CONTRIBUTING.md](link-to-contributing) for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the [MIT License](LICENSE.md).
