# TODO List for Test-Driven Development

## UI Design
- [X] Design wireframes for the UI  - 1 Chuck 12/30/2024 8:25 PM PST
- [X] Create Django project and app for UI - 2 Chuck 12/30/2024 8:35 PM PST
- [X] Set up Django Channels for real-time communication -3 Chuck 12/31/2024 2:38PM PST
- [X] Create templates for:   - 4 Chuck 1/2/2025 9:40 AM PST
  - [X] Home page
  - [X] Corpus management page
  - [X] Keyword management page
  - [X] Scoring results page
  - [X] Search corpus page
  - [X] Select keywords page
- [X] Implement views for:  -5 Chuck 1/2/2025 10:50 PM PST
  - [X] Home page
  - [X] Corpus management
  - [X] Keyword management
  - [X] Scoring results
  - [X] Search corpus
  - [X] Select keywords
- [X] Write tests for UI views and templates
  - [X] Run tests for the UI views and templates - 6 Chuck 1/2/2025 1:31 PM PST

## DB Design
- [X] Design schema for storing document chunks and keywords
- [X] Set up FAISS for vector database
- [X] Create Django models for:
  - [X] Corpus
  - [X] Document
  - [X] Chunk
  - [X] Keyword
  - [X] Score
  - [X] KeywordReport
  - [X] DocumentReport
  - [X] CorpusReport
- [X] Write tests for models and database interactions  - 7 Chuck 1/4/2025 10:37 AM PST

## Backend Logic
- [X] Implement logic for encoding document chunks
- [X] Implement logic for storing and retrieving document chunks from FAISS
  - [ ] Add chunk metadata storage system
  - [ ] Implement vector-to-chunk ID mapping
  - [ ] Add persistent storage mechanism
  - [ ] Implement bulk operations for large datasets
    - [ ] Batch insertions
    - [ ] Batch updates
    - [ ] Batch deletions
  - [ ] Add progress tracking for long operations
    - [ ] Batch processing progress
    - [ ] Index building progress
    - [ ] Search operation progress
  - [ ] Implement comprehensive error handling
    - [ ] Input validation
    - [ ] Resource availability checks
    - [ ] Recovery mechanisms
  - [ ] Index optimization
    - [ ] Implement index compression
    - [ ] Add memory usage optimization
    - [ ] Configure FAISS index parameters
- [ ] Implement logic for keyword scoring based on similarity criteria
- [ ] Implement logic for searching corpus
- [ ] Implement logic for selecting keywords from choices
- [ ] Write tests for backend logic

## Integration with LangChain
- [ ] Set up LangChain for using different LLMs
- [ ] Implement logic for vectorizing document chunks using LLMs
- [ ] Write tests for LangChain integration

## API Development
- [ ] Create REST API endpoints for:
  - [ ] Corpus management
  - [ ] Document chunk management
  - [ ] Keyword management
  - [ ] Scoring results
  - [ ] Search corpus
  - [ ] Select keywords
- [ ] Write tests for API endpoints

## DevOps
- [ ] Set up version control with Git
- [ ] Create and configure `requirements.txt` for dependencies
- [ ] Set up continuous integration (CI) with GitHub Actions
- [ ] Write tests for deployment scripts

## Documentation
- [ ] Write detailed documentation for:
  - [ ] Project setup
  - [ ] Usage instructions
  - [ ] API endpoints
  - [ ] Contribution guidelines
- [ ] Create `CONTRIBUTING.md`
- [ ] Create `LICENSE` file

## Testing
- [ ] Write unit tests for all components
- [ ] Write integration tests for end-to-end functionality
- [ ] Set up test coverage reporting

## Iterative Development
- [ ] Implement feature: UI design
- [ ] Implement feature: DB design
- [ ] Implement feature: Backend logic
- [ ] Implement feature: LangChain integration
- [ ] Implement feature: API development
- [ ] Implement feature: DevOps
- [ ] Implement feature: Documentation
- [ ] Implement feature: Testing

## Database Management Tasks
- [X] Define corpus and keywords in the database
- [X] Build UI for corpus and keyword management    - 8 Chuck 1/5/2025 5:00 PM PST
- [ ] Implement middleware logic to:
  - [ ] Search the corpus path
  - [ ] Find all documents in the corpus
  - [ ] Add documents to the database

## Encoder Integration Tasks                        - 9 Chuck 1/6/2025 10:37 AM PST     
- [X] Setup encoder app structure:
  - [X] Create encoder app with Django
  - [X] Create services and interfaces directories
  - [X] Write unit tests for app structure

- [X] Implement base encoder interface:
  - [X] Create BaseEncoder interface
  - [X] Define abstract methods for encoding
  - [X] Add type hints and docstrings
  - [X] Define encode_text and encode_batch methods 
  - [X] Create test class and write unit tests for interface methods
  - [X] Add validation tests for required methods

- [X] Implement Transformer Encoders:
  - [X] Create TransformerEncoderBase class
    - [X] Add initialization with model loading
    - [X] Implement pooling strategy
    - [X] Add caching mechanism
  - [X] Create specific encoder implementations
    - [X] BERT encoder
    - [X] ALBERT encoder
    - [X] RoBERTa encoder
  - [ ] Add vector store integration
    - [ ] Connect with FAISS
    - [ ] Implement vector storage
    - [ ] Add batch processing support
  - [X] Write unit tests
    - [X] Test model loading
    - [X] Test encoding functions
    - [X] Test vector dimensions
    - [X] Test batch processing
  - [X] Write integration tests
    - [X] Test model caching
    - [ ] Test FAISS integration
    - [ ] Test search functionality
    - [ ] Test performance metrics

- [ ] Implement LangChain service:
  - [ ] Create LangChainService class
  - [ ] Implement HuggingFace and OpenAI embeddings
  - [ ] Add vector store integration
  - [ ] Write unit tests for embeddings
  - [ ] Write integration tests for vector store

- [ ] Update FAISS database:
  - [ ] Modify FAISSDatabase to use LangChain
  - [ ] Add text storage functionality
  - [ ] Implement batch processing
  - [ ] Write unit tests for FAISS operations
  - [ ] Write integration tests for search functionality

- [ ] Create Django models:
  - [ ] Define EncodedDocument model
  - [ ] Add indexes and metadata fields
  - [ ] Write model unit tests
  - [ ] Create and test migrations

- [ ] Setup configuration:
  - [ ] Add LangChain settings
  - [ ] Configure embedding models
  - [ ] Write configuration tests

- [ ] Create API endpoints:
  - [ ] Add encode document endpoint
  - [ ] Add search endpoint
  - [ ] Write API tests
  - [ ] Document API usage

- [ ] Performance testing:
  - [ ] Benchmark encoding operations
  - [ ] Test vector store performance
  - [ ] Measure memory usage
  - [ ] Document performance results

## Integration Testing Tasks
- [X] Test encoder app:
  - [X] Test with different document types
  - [X] Verify vector dimensions
  - [X] Check error handling
  - [X] Validate search results

- [ ] Test LangChain integration:
  - [ ] Test HuggingFace embeddings
  - [ ] Test OpenAI embeddings
  - [ ] Verify vector store operations
  - [ ] Test batch processing

- [ ] End-to-end testing:
  - [ ] Test document upload flow
  - [ ] Test search functionality
  - [ ] Verify results accuracy
  - [ ] Test error scenarios

## Scaling/Logging TODO Items
- [ ] Implement logic for handling large datasets
- [ ] Optimize FAISS index for faster search
- [ ] Implement user authentication and authorization
- [ ] Add logging and monitoring for backend services
- [ ] Create a Dockerfile for containerization
- [ ] Set up deployment pipeline
- [ ] Document performance results
