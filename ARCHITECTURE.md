# Search Engine - System Architecture

## 📋 Overview
A production-grade search engine with inverted indexing, JWT authentication, and fast document retrieval.

## 🎯 System Components

### 1. **Authentication Module**
- **Purpose**: Handle user registration, login, and JWT token management
- **Components**:
  - User model (MongoDB document)
  - Password hashing (bcrypt)
  - JWT token generation and validation
  - Protected route middleware

### 2. **Document Management Module**
- **Purpose**: Store, retrieve, and manage searchable documents
- **Components**:
  - Document model (title, content, metadata, user_id)
  - CRUD operations for documents
  - Document validation

### 3. **Indexing Service**
- **Purpose**: Build and maintain inverted index for fast searching
- **Components**:
  - Text preprocessing (tokenization, normalization, stop words)
  - Inverted index data structure (word → [doc_ids])
  - Index builder (runs when documents are added/updated)
  - Index storage in MongoDB

### 4. **Search Service**
- **Purpose**: Process search queries and retrieve relevant documents
- **Components**:
  - Query preprocessing (same as indexing)
  - Index lookup
  - Document retrieval from multiple word matches

### 5. **Ranking Service**
- **Purpose**: Score and rank search results by relevance
- **Components**:
  - TF-IDF (Term Frequency-Inverse Document Frequency)
  - BM25 algorithm (optional advanced version)
  - Score calculation and sorting

## 🔄 Data Flow

```
User Request → API Route → Service Layer → Database → Service Layer → API Response
```

### Example: Search Flow
1. **Frontend**: User types "python programming" → sends GET /api/search?q=python+programming
2. **API Route**: Validates request, extracts query
3. **Search Service**: 
   - Preprocesses query → ["python", "programming"]
   - Looks up inverted index for each term
   - Finds document IDs containing these terms
4. **Ranking Service**:
   - Calculates TF-IDF scores for each document
   - Sorts by relevance
5. **Document Service**: Retrieves top N documents from MongoDB
6. **API Response**: Returns JSON with ranked results
7. **Frontend**: Displays results

## 🗂️ Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "username": "string (unique)",
  "email": "string (unique)",
  "password_hash": "string",
  "created_at": "datetime"
}
```

### Documents Collection
```json
{
  "_id": "ObjectId",
  "title": "string",
  "content": "string",
  "author": "string",
  "url": "string (optional)",
  "user_id": "ObjectId (reference)",
  "created_at": "datetime",
  "updated_at": "datetime",
  "word_count": "int"
}
```

### Inverted Index Collection
```json
{
  "_id": "string (the word)",
  "doc_ids": ["ObjectId", "ObjectId", ...],
  "doc_count": "int",
  "positions": {
    "doc_id_1": [1, 5, 10],  // positions in document
    "doc_id_2": [2, 8]
  }
}
```

### Search Statistics Collection (Optional)
```json
{
  "_id": "ObjectId",
  "query": "string",
  "results_count": "int",
  "user_id": "ObjectId",
  "timestamp": "datetime"
}
```

## 🏛️ Folder Structure

```
search-engine/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app initialization
│   │   ├── config.py                 # Environment variables, settings
│   │   │
│   │   ├── models/                   # Database models (Pydantic + Motor)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   └── index.py
│   │   │
│   │   ├── schemas/                  # Request/Response schemas (Pydantic)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── document.py
│   │   │   └── search.py
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py       # JWT, password hashing
│   │   │   ├── document_service.py   # CRUD for documents
│   │   │   ├── indexing_service.py   # Build inverted index
│   │   │   ├── search_service.py     # Search execution
│   │   │   └── ranking_service.py    # TF-IDF, scoring
│   │   │
│   │   ├── routes/                   # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # /signup, /login
│   │   │   ├── documents.py          # /documents CRUD
│   │   │   └── search.py             # /search
│   │   │
│   │   ├── middleware/               # Custom middleware
│   │   │   ├── __init__.py
│   │   │   └── auth_middleware.py    # JWT verification
│   │   │
│   │   ├── database/                 # Database connection
│   │   │   ├── __init__.py
│   │   │   └── mongodb.py            # MongoDB client
│   │   │
│   │   └── utils/                    # Helper functions
│   │       ├── __init__.py
│   │       ├── text_processing.py    # Tokenization, stop words
│   │       └── security.py           # Password hashing, JWT
│   │
│   ├── tests/                        # Unit and integration tests
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_search.py
│   │   └── test_indexing.py
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variables template
│   └── README.md
│
├── frontend/                         # React Frontend (later upgrade)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Signup.jsx
│   │   │   ├── Search/
│   │   │   │   ├── SearchBar.jsx
│   │   │   │   └── SearchResults.jsx
│   │   │   └── Documents/
│   │   │       ├── DocumentList.jsx
│   │   │       └── DocumentUpload.jsx
│   │   ├── services/
│   │   │   └── api.js                # Axios API calls
│   │   ├── context/
│   │   │   └── AuthContext.jsx       # Global auth state
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── package.json
│   └── README.md
│
├── docs/                             # Documentation
│   ├── API.md                        # API endpoints documentation
│   ├── DEPLOYMENT.md                 # Deployment guide
│   └── INDEXING.md                   # Indexing algorithm explanation
│
└── README.md                         # Project overview
```

## 🔐 Security Considerations

1. **Password Security**: Bcrypt hashing with salt
2. **JWT**: Short-lived access tokens (15 min), refresh tokens optional
3. **Input Validation**: Pydantic schemas for all inputs
4. **CORS**: Configured for frontend domain only
5. **Rate Limiting**: Prevent abuse on search endpoints
6. **Environment Variables**: Sensitive data in .env files

## ⚡ Performance Optimizations

1. **Async/Await**: Use Motor (async MongoDB driver)
2. **Indexing**: 
   - Create MongoDB indexes on frequently queried fields
   - Cache inverted index in memory for ultra-fast lookups
3. **Pagination**: Limit search results (default 10, max 100)
4. **Connection Pooling**: Reuse database connections
5. **Text Processing**: Compile regex patterns once

## 📦 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation
- **PyJWT**: JWT token handling
- **Bcrypt**: Password hashing
- **Python-multipart**: File uploads
- **NLTK**: Text processing (optional)

### Frontend (Phase 2)
- **React**: UI library
- **Axios**: HTTP client
- **React Router**: Navigation
- **Tailwind CSS**: Styling
- **Context API**: State management

### Database
- **MongoDB Atlas**: Free tier (512 MB)

### Deployment
- **Backend**: Render / Railway (free tier)
- **Frontend**: Vercel / Netlify
- **Database**: MongoDB Atlas

## 🎓 Learning Outcomes

After completing this project, you'll understand:

1. **System Design**: How to architect a multi-component system
2. **Inverted Indexing**: How search engines work internally
3. **Text Processing**: Tokenization, normalization, stop words
4. **Ranking Algorithms**: TF-IDF, relevance scoring
5. **Async Programming**: Non-blocking I/O with async/await
6. **JWT Authentication**: Stateless authentication
7. **API Design**: RESTful principles, proper HTTP methods
8. **Database Design**: Schema design for search applications
9. **Frontend-Backend Integration**: Full-stack data flow
10. **Deployment**: Production deployment best practices

## 📊 Algorithm: Inverted Index

**What is it?**
A data structure that maps words to documents containing them.

**Example:**
```
Documents:
- Doc1: "python is great"
- Doc2: "python programming"
- Doc3: "great programming"

Inverted Index:
{
  "python": [Doc1, Doc2],
  "is": [Doc1],
  "great": [Doc1, Doc3],
  "programming": [Doc2, Doc3]
}
```

**Search for "python programming":**
1. Look up "python" → [Doc1, Doc2]
2. Look up "programming" → [Doc2, Doc3]
3. Intersection → [Doc2] (contains both words)
4. Return Doc2 with highest score

## 📊 Algorithm: TF-IDF Scoring

**TF (Term Frequency)**: How often a word appears in a document
**IDF (Inverse Document Frequency)**: How rare a word is across all documents

```
TF-IDF = TF × IDF

TF = (count of word in doc) / (total words in doc)
IDF = log(total documents / documents containing word)
```

**Why?**
- Common words (the, is, a) get low IDF → low score
- Rare words get high IDF → high score
- Documents with more occurrences get higher TF → higher score

## 🚀 Next Steps

We'll implement this in phases:
1. ✅ Architecture design (current)
2. ⏭️ Folder structure creation
3. ⏭️ Database models and schemas
4. ⏭️ Authentication system
5. ⏭️ Document management
6. ⏭️ Indexing service
7. ⏭️ Search and ranking
8. ⏭️ API routes
9. ⏭️ Frontend (HTML/CSS/JS)
10. ⏭️ React upgrade
11. ⏭️ Deployment

Each step will include:
- Code implementation
- Explanation of why and how
- Testing approach
- Best practices
