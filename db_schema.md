# ScoreKeywords Database Schema Documentation

## Table: `CorpusReport`
| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| ReportId    | INT       | PRIMARY KEY | Unique identifier for the corpus report |
| CorpusId    | INT       | FOREIGN KEY REFERENCES Corpus(CorpusId) | Reference to the corpus |
| Title       | VARCHAR(255) |           | Title of the report |
| Type        | VARCHAR(100) |           | Type of the report |
| Desc        | TEXT      |           | Description of the report |
| Summary     | TEXT      |           | Summary of the report content |
| Report      | TEXT      |           | The report content |
| Reviewer    | VARCHAR(100) |           | Name or identifier of the reviewer |

## Table: `Corpus`
| Column Name  | Data Type        | Constraints | Description |
|--------------|------------------|-------------|-------------|
| CorpusId     | INT              | PRIMARY KEY | Unique identifier for the corpus |
| CorpusName   | VARCHAR(255)     |           | Name of the corpus |
| CorpusType   | VARCHAR(100)     |           | Type of the corpus |
| CorpusPath   | VARCHAR(255)     |           | Path or location of the corpus |
| Username     | VARCHAR(100)     |           | Name or identifier of the user managing the corpus |
| IngestDate   | DATETIME         |           | Date when the corpus was ingested |

**Relationships:**
- Has many CorpusReports (1 to 0..n)
- Has many Documents (1 to 0..n)

## Table: `DocumentReport`
| Column Name  | Data Type        | Constraints | Description |
|--------------|------------------|-------------|-------------|
| ReportId     | INT              | PRIMARY KEY | Unique identifier for the document report |
| DocId        | INT              | FOREIGN KEY REFERENCES Document(DocId) | Reference to the document |
| Title        | VARCHAR(255)     |           | Title of the report |
| Type         | VARCHAR(100)     |           | Type of the report |
| Desc         | TEXT             |           | Description of the report |
| Summary      | TEXT             |           | Summary of the report content |
| Report       | TEXT             |           | The report content |
| Reviewer     | VARCHAR(100)     |           | Name or identifier of the reviewer |

## Table: `Document`
| Column Name  | Data Type        | Constraints | Description |
|--------------|------------------|-------------|-------------|
| DocId        | INT              | PRIMARY KEY | Unique identifier for the document |
| CorpusId     | INT              | FOREIGN KEY REFERENCES Corpus(CorpusId) | Reference to the corpus |
| Name         | VARCHAR(255)     |           | Name of the document |
| Description  | TEXT             |           | Description of the document |
| CreatedDate  | DATETIME         |           | Date when the document was created |

**Relationships:**
- Has many DocumentReports (1 to 0..n)
- Has many Chunks (1 to 1..n)

## Table: `Chunk`
| Column Name  | Data Type        | Constraints | Description |
|--------------|------------------|-------------|-------------|
| ChunkId      | INT              | PRIMARY KEY | Unique identifier for the chunk |
| DocId        | INT              | FOREIGN KEY REFERENCES Document(DocId) | Reference to the document |
| Name         | VARCHAR(255)     |           | Name of the chunk |
| Description  | TEXT             |           | Description of the chunk |
| CreatedDate  | DATETIME         |           | Date when the chunk was created |
| ChunkSize    | INT              |           | Size of the chunk |

**Relationships:**
- Has many Scores (1 to 0..n)

## Table: `Score`
| Column Name  | Data Type        | Constraints | Description |
|--------------|------------------|-------------|-------------|
| ChunkId      | INT              | FOREIGN KEY REFERENCES Chunk(ChunkId) | Reference to the chunk |
| KeywordId    | INT              | FOREIGN KEY REFERENCES Keyword(KeywordId) | Reference to the keyword |
| Score        | FLOAT            |           | Score value for the keyword |
| ScoreDate    | DATETIME         |           | Date when the score was calculated |

**Relationships:**
- Belongs to one Keyword (1 to 1)

## Table: `Keyword`
| Column Name  | Data Type        | Constraints | Description |
|--------------|------------------|-------------|-------------|
| KeywordId    | INT              | PRIMARY KEY | Unique identifier for the keyword |
| Keyword      | VARCHAR(50)      |           | The keyword |
| ShortDesc    | VARCHAR(255)     |           | Short description of the keyword |
| LongText     | TEXT             |           | Long text description or content related to the keyword |

**Relationships:**
- Has many Scores (1 to 0..n)
- Has many KeywordReports (1 to 0..n)

## Table: `KeywordReport`
| Column Name  | Data Type        | Constraints | Description |
|--------------|------------------|-------------|-------------|
| ReportId     | INT              | PRIMARY KEY | Unique identifier for the keyword report |
| KeywordId    | INT              | FOREIGN KEY REFERENCES Keyword(KeywordId) | Reference to the keyword |
| Title        | VARCHAR(255)     |           | Title of the report |
| Type         | VARCHAR(100)     |           | Type of the report |
| Summary      | TEXT             |           | Summary of the report content |
| Report       | TEXT             |           | The report content |
| Reviewer     | VARCHAR(100)     |           | Name or identifier of the reviewer |