# Project Folder Structure

```
search-engine-project/
│
├── 📄 README.md                              # Project overview and setup guide
├── 📄 ARCHITECTURE.md                        # System design and architecture (already created)
│
├── 📁 backend/                               # FastAPI Backend Application
│   │
│   ├── 📄 requirements.txt                   # Python dependencies
│   ├── 📄 .env.example                       # Environment variables template
│   ├── 📄 README.md                          # Backend-specific documentation
│   │
│   ├── 📁 app/                               # Main application package
│   │   │
│   │   ├── 📄 __init__.py                    # Package initializer
│   │   ├── 📄 main.py                        # FastAPI app entry point, CORS, routers
│   │   ├── 📄 config.py                      # Configuration (env vars, settings)
│   │   │
│   │   ├── 📁 models/                        # Database models
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 user.py                    # User model (MongoDB document)
│   │   │   ├── 📄 document.py                # Document model
│   │   │   └── 📄 index.py                   # Inverted index model
│   │   │
│   │   ├── 📁 schemas/                       # Pydantic schemas (validation)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 auth.py                    # Login, signup, token schemas
│   │   │   ├── 📄 document.py                # Document create/update/response schemas
│   │   │   └── 📄 search.py                  # Search request/response schemas
│   │   │
│   │   ├── 📁 services/                      # Business logic layer
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 auth_service.py            # Authentication logic, JWT generation
│   │   │   ├── 📄 document_service.py        # Document CRUD operations
│   │   │   ├── 📄 indexing_service.py        # Build and update inverted index
│   │   │   ├── 📄 search_service.py          # Execute search queries
│   │   │   └── 📄 ranking_service.py         # Calculate TF-IDF, rank results
│   │   │
│   │   ├── 📁 routes/                        # API endpoints (controllers)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 auth.py                    # POST /signup, /login
│   │   │   ├── 📄 documents.py               # CRUD /documents endpoints
│   │   │   └── 📄 search.py                  # GET /search
│   │   │
│   │   ├── 📁 middleware/                    # Custom middleware
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 auth_middleware.py         # JWT verification dependency
│   │   │
│   │   ├── 📁 database/                      # Database connection
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 mongodb.py                 # MongoDB client, connection pool
│   │   │
│   │   └── 📁 utils/                         # Helper utilities
│   │       ├── 📄 __init__.py
│   │       ├── 📄 text_processing.py         # Tokenization, stop words, stemming
│   │       └── 📄 security.py                # Password hashing, JWT utilities
│   │
│   └── 📁 tests/                             # Unit and integration tests
│       ├── 📄 __init__.py
│       ├── 📄 test_auth.py                   # Authentication tests
│       ├── 📄 test_search.py                 # Search functionality tests
│       └── 📄 test_indexing.py               # Indexing tests
│
├── 📁 frontend/                              # Frontend Application
│   │
│   ├── 📁 public/                            # Static files
│   │   └── 📄 index.html                     # HTML entry point
│   │
│   └── 📁 src/                               # Source code
│       │
│       ├── 📁 components/                    # React components
│       │   ├── 📁 Auth/                      # Authentication components
│       │   │   ├── 📄 Login.jsx              # Login form
│       │   │   └── 📄 Signup.jsx             # Signup form
│       │   │
│       │   ├── 📁 Search/                    # Search components
│       │   │   ├── 📄 SearchBar.jsx          # Search input
│       │   │   └── 📄 SearchResults.jsx      # Results display
│       │   │
│       │   └── 📁 Documents/                 # Document management
│       │       ├── 📄 DocumentList.jsx       # List user documents
│       │       └── 📄 DocumentUpload.jsx     # Upload new documents
│       │
│       ├── 📁 services/                      # API integration
│       │   └── 📄 api.js                     # Axios instance, API calls
│       │
│       ├── 📁 context/                       # Global state management
│       │   └── 📄 AuthContext.jsx            # User authentication state
│       │
│       ├── 📄 App.jsx                        # Main app component
│       └── 📄 index.jsx                      # React DOM entry point
│
└── 📁 docs/                                  # Documentation
    ├── 📄 API.md                             # API endpoints reference
    ├── 📄 DEPLOYMENT.md                      # Deployment instructions
    └── 📄 INDEXING.md                        # Indexing algorithm details
```

## 📋 File Responsibilities Explained

### Backend Core Files

#### `main.py` - Application Entry Point
- Initializes FastAPI app
- Configures CORS middleware
- Registers all routers (auth, documents, search)
- Sets up exception handlers
- Connects to MongoDB on startup

#### `config.py` - Configuration Management
- Loads environment variables (.env)
- Defines settings class (database URL, JWT secret, etc.)
- Validates configuration on startup

### Models vs Schemas

**Models** (`models/`) - Database structure
- Define how data is stored in MongoDB
- MongoDB document structure
- No validation logic

**Schemas** (`schemas/`) - API validation
- Pydantic models for request/response
- Validate incoming data
- Auto-generate API documentation
- Type checking

Example:
- `models/user.py`: Database structure (what's in MongoDB)
- `schemas/auth.py`: API request/response (what client sends/receives)

### Service Layer - Business Logic

All business logic lives here, NOT in routes!

#### `auth_service.py`
- Hash passwords
- Verify passwords
- Generate JWT tokens
- Validate tokens

#### `document_service.py`
- Create, read, update, delete documents
- Interact with MongoDB documents collection
- Validate document ownership

#### `indexing_service.py` - **Core Search Engine Logic**
- Build inverted index when document is added
- Update index when document is modified
- Delete from index when document removed
- Text preprocessing pipeline

#### `search_service.py`
- Process search queries
- Look up terms in inverted index
- Find matching documents
- Call ranking service

#### `ranking_service.py`
- Calculate TF-IDF scores
- Sort documents by relevance
- Return top N results

### Routes Layer - API Endpoints

Thin layer that just handles HTTP!

#### `auth.py`
```
POST /api/auth/signup    - Register new user
POST /api/auth/login     - Login, get JWT token
```

#### `documents.py`
```
GET    /api/documents           - List user's documents
POST   /api/documents           - Upload new document
GET    /api/documents/{id}      - Get specific document
PUT    /api/documents/{id}      - Update document
DELETE /api/documents/{id}      - Delete document
```

#### `search.py`
```
GET /api/search?q=keyword       - Search documents
```

### Utilities

#### `text_processing.py`
- Tokenize text (split into words)
- Remove stop words (the, is, a, an, etc.)
- Lowercase normalization
- Stemming (running → run)

#### `security.py`
- Bcrypt password hashing
- JWT encoding/decoding
- Token expiration checks

### Frontend Structure

#### Components
- **Auth/**: Login and signup forms
- **Search/**: Search bar and results display
- **Documents/**: Manage user's uploaded documents

#### Services
- **api.js**: Centralized API calls using Axios
- Handles authentication headers
- Error handling

#### Context
- **AuthContext**: Global user state
- JWT token storage
- Login/logout functions

## 🔄 Request Flow Example

**User searches for "python tutorial":**

1. **Frontend** (`SearchBar.jsx`):
   ```javascript
   // User types and submits
   const results = await api.search("python tutorial");
   ```

2. **API Service** (`api.js`):
   ```javascript
   // Sends GET request with JWT token
   GET /api/search?q=python+tutorial
   Headers: { Authorization: "Bearer <token>" }
   ```

3. **Backend Route** (`routes/search.py`):
   ```python
   @router.get("/search")
   async def search(q: str, user_id: str = Depends(auth_middleware)):
       # Validates token, extracts user_id
       return await search_service.search(q, user_id)
   ```

4. **Search Service** (`services/search_service.py`):
   ```python
   # Preprocesses query
   terms = text_processing.tokenize(q)  # ["python", "tutorial"]
   # Looks up in index
   doc_ids = indexing_service.find_documents(terms)
   # Gets documents
   docs = await document_service.get_by_ids(doc_ids)
   # Ranks them
   ranked = ranking_service.rank(docs, terms)
   return ranked[:10]
   ```

5. **Response** flows back:
   ```
   Service → Route → Frontend → SearchResults.jsx
   ```

## 🎯 Why This Structure?

### Separation of Concerns
- **Routes**: Handle HTTP only
- **Services**: Business logic only
- **Models**: Data structure only
- **Schemas**: Validation only

### Benefits:
1. **Testable**: Each service can be tested independently
2. **Reusable**: Services can be called from multiple routes
3. **Maintainable**: Easy to find and fix bugs
4. **Scalable**: Add features without touching existing code
5. **Clean**: No mixing of concerns

### Example: Why Services?

**Bad** (logic in route):
```python
@router.post("/search")
async def search(q: str):
    # Tokenization
    words = q.lower().split()
    # Remove stop words
    words = [w for w in words if w not in stop_words]
    # Look up index
    results = await db.index.find({"_id": {"$in": words}})
    # Calculate scores...
    # This is 100+ lines in the route! ❌
```

**Good** (service):
```python
@router.post("/search")
async def search(q: str):
    return await search_service.search(q)  # Clean! ✅
```

## 📚 Next Steps

Now that you understand the structure, we'll implement:
1. Database configuration and models
2. Authentication system
3. Document management
4. Indexing service
5. Search and ranking
6. API routes
7. Frontend

Each step will include working code with explanations!
