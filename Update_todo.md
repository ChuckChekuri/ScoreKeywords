# Todo List  for Tracking Progress

## Step 1: UI Application – Foundation and Communication

### UI Design Wireframes and Concept Validation

- [X] Review and refine UI wireframes with stakeholders

#### Test: Verify that mockups meet design requirements

### Project and App Initialization (UI)

- [X] Create Django project and UI app
- [X] Configure settings and app registration in INSTALLED_APPS
- [X] Verify that the project starts without errors

#### Test: Confirm app registration and basic server startup

### Real-Time Communication Setup (UI)

- [X] Install and configure Django Channels
- [X] Define channel layers in settings.py (testing in-memory and production backends)
- [X] Implement basic consumer for WebSocket connectivity
- [X] Test connectivity with a simple echo endpoint  

#### Test: Confirm channel routing and basic websocket connection

## Step 2: UI Application – Template and View Implementation

### UI Templates Creation

- [X] Create Home page template with layout and navigation
- [X] Create Corpus Management template showing document lists
- [X] Create Keyword Management template with search and filters
- [ ] Create Scoring Results template with dynamic result display
- [ ] Create Search Corpus template for user queries
- [ ] Create Select Keywords template with available keywords list

#### Test: Render each template using a test view and check for expected content

### UI Views Implementation

- [X] Implement Home view returning the Home page template
- [X] Implement Corpus Management view retrieving document data
- [X] Implement Keyword Management view for keyword CRUD operations
- [ ] Implement Scoring Results view to display model output
- [ ] Implement Search Corpus view to process search queries
- [ ] Implement Select Keywords view to allow keyword selection

#### Test: Write unit tests for each view, verifying HTTP status codes and context data

### UI Integration Testing for Views and Templates

- [X] Write tests that simulate user navigation through the UI pages
- [ ] Automate testing to load each page and check for key HTML elements

### Test: Run the full UI test suite and document results

## Step 3: Database Design and Integration

### Database Schema for Document Chunks and Keywords

- [X] Design the schema for storing document chunks, including necessary fields (e.g., text, metadata, vector embeddings)
- [X] Design the schema for keyword storage and relationships to document chunks
- [X] Create Django models reflecting the designed schema
- [X] Create migrations and apply them to the development database

#### Test: Verify migrations by creating test records and retrieving them

### Vector Store Setup with FAISS

- [ ] Install and configure FAISS in the project environment
- [ ] Integrate FAISS with Django models to store vector embeddings
- [ ] Write helper functions for inserting and searching vectors in FAISS

#### Test: Write tests to insert document vectors, perform vector search, and validate search accuracy

### Advanced Vector Search Integration Using LangChain

- [ ] Research LangChain integration with FAISS for enhanced vector query capabilities
- [ ] Develop prototype integration and evaluate performance improvements

#### Test: Add integration tests comparing traditional FAISS search with LangChain-enhanced search

## Step 4: API Development – Encoder and Data Processing

### Base Encoder and Transformer Encoder Services

- [X] Define a base interface for encoder services in the interfaces folder
- [X] Implement TransformerEncoderBase in the services folder using settings for model configuration
- [X] Validate that the encode_text method is properly implemented for tokenization, inference, and pooling
- [X] Alias encode_text as encode (if needed) to support API testing calls

#### Test: Write unit tests for the TransformerEncoderBase to verify output format on sample input

### Specific Encoder Implementations (BERT, ALBERT, RoBERTa)

- [X] Implement BertEncoder extending TransformerEncoderBase with any model-specific customization
- [X] Implement AlbertEncoder extending TransformerEncoderBase with model-specific adjustments
- [X] Implement RobertaEncoder extending TransformerEncoderBase and include pooling verification

#### Test: Patch each encoder’s encode method in tests to simulate output and confirm correct behavior

### Encoding API Endpoint Creation

- [X] Create an API view (EncodingAPIView) using Django REST Framework that accepts POST requests with "text" and "model" parameters
- [X] In the view, validate the input and select the correct encoder (BERT, ALBERT, or RoBERTa)
- [X] Return the encoded text as a JSON response
- [ ] Handle and log exceptions appropriately

#### Test: Write API tests covering missing text, unsupported model, successful encoding for each encoder, and error conditions

## Step 5: Backend Logic for Data Processing and Storage

### Encoding Document Chunks

- [ ] Integrate encoder services with document processing logic to encode chunks of text
- [ ] Store encoded representations in the database and/or vector store

#### Test: Unit test document encoding and storage operations for a variety of sample inputs

### Keyword Scoring and Matching

- [ ] Implement keyword scoring logic based on model similarity
- [ ] Connect keyword matching to search UI and corpus management functions

#### Test: Write tests simulating keyword queries and verifying scoring accuracy

## Step 6: Configuration, DevOps, and Testing

### Application Configuration Improvements

- [ ] Refine Django settings for model cache, Redis cache integration, and FAISS configuration
- [ ] Add logging configuration for error tracking across modules

#### Test: Confirm configuration through environment-specific tests (development and production)

### Continuous Integration/Continuous Deployment (CI/CD)

- [ ] Develop CI/CD pipeline scripts (e.g., using GitHub Actions) to run test suites on push/PR
- [ ] Write scripts for automated deployment

#### Test: Validate the CI/CD pipeline on a dedicated branch

### Containerization and Deployment

- [ ] Create a Dockerfile to containerize the Django project
- [ ] Configure Docker Compose for multi-container setup (UI, DB, Redis, etc.)

#### Test: Build and run containers locally; verify service interconnection

### Comprehensive Testing and Documentation

- [ ] Write unit tests for each service, view, and model in the project
- [ ] Write integration tests for the entire workflow (from input to vector search result)
- [ ] Update project documentation, including setup, deployment, API usage, and troubleshooting guides
- [ ] Prepare CONTRIBUTING.md and LICENSE files

#### Test: Run full test suites and fix identified issues before a production release

## Step 7: Final Review and Refinement

### Code Review and Quality Assurance

- [ ] Perform full code reviews across modules (UI, API, DB, and services)
- [ ] Refactor code where necessary; improve error handling and logging

#### Test: Run linters and static analysis tools (e.g., flake8, pylint)

### Final Integration Testing and User Acceptance

- [ ] Deploy to a staging environment for end-to-end testing
- [ ] Conduct user acceptance tests with stakeholders and make refinements as needed

#### Test: Ensure all functionalities work as intended from UI to backend responses
