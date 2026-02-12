# 📊 Project Architecture Visual Summary

## 🎯 High-Level System Design

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                                   │
│                                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Login     │  │   Signup    │  │   Search    │  │  Documents  │    │
│  │    Page     │  │    Page     │  │     Bar     │  │    Upload   │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │                │             │
└─────────┼────────────────┼────────────────┼────────────────┼─────────────┘
          │                │                │                │
          │                │                │                │
          ▼                ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          API ROUTES LAYER                                 │
│                                                                           │
│  POST /auth/signup   POST /auth/login   GET /search?q=   POST /documents │
│         │                   │                 │                 │         │
└─────────┼───────────────────┼─────────────────┼─────────────────┼─────────┘
          │                   │                 │                 │
          │                   │                 │                 │
          ▼                   ▼                 ▼                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        SERVICES LAYER (Business Logic)                    │
│                                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │    Auth     │  │  Document   │  │  Indexing   │  │   Search    │    │
│  │   Service   │  │   Service   │  │   Service   │  │   Service   │    │
│  │             │  │             │  │             │  │             │    │
│  │ • Hash pwd  │  │ • Create    │  │ • Tokenize  │  │ • Query     │    │
│  │ • Verify    │  │ • Read      │  │ • Build idx │  │ • Lookup    │    │
│  │ • Gen JWT   │  │ • Update    │  │ • Update    │  │ • Rank      │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │                │             │
└─────────┼────────────────┼────────────────┼────────────────┼─────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         MONGODB DATABASE                                  │
│                                                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│  │     users       │  │    documents    │  │  inverted_index │          │
│  │                 │  │                 │  │                 │          │
│  │ • _id           │  │ • _id           │  │ • _id (word)    │          │
│  │ • username      │  │ • title         │  │ • doc_ids []    │          │
│  │ • email         │  │ • content       │  │ • positions {}  │          │
│  │ • password_hash │  │ • user_id       │  │ • doc_count     │          │
│  │ • created_at    │  │ • created_at    │  │                 │          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘          │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow: Search Request Example

```
User types "python tutorial" in search bar
         │
         ▼
┌────────────────────────────────────────┐
│ FRONTEND (SearchBar.jsx)               │
│ • Captures input                       │
│ • Calls: api.search("python tutorial") │
└────────┬───────────────────────────────┘
         │ HTTP GET /api/search?q=python+tutorial
         │ Headers: { Authorization: Bearer <JWT> }
         ▼
┌────────────────────────────────────────┐
│ BACKEND ROUTE (routes/search.py)       │
│ • Validates JWT token                  │
│ • Extracts user_id from token          │
│ • Calls search_service                 │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ SEARCH SERVICE (services/search.py)    │
│                                        │
│ Step 1: Preprocess query               │
│   "python tutorial"                    │
│   → ["python", "tutorial"]             │
│                                        │
│ Step 2: Lookup in inverted index       │
│   "python" → [doc1, doc2, doc5]        │
│   "tutorial" → [doc2, doc3, doc5]      │
│   Intersection → [doc2, doc5]          │
│                                        │
│ Step 3: Get documents from DB          │
│   Query MongoDB for doc2, doc5         │
│                                        │
│ Step 4: Calculate TF-IDF scores        │
│   doc2: score = 0.85                   │
│   doc5: score = 0.72                   │
│                                        │
│ Step 5: Sort by score                  │
│   [doc2, doc5]                         │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ RESPONSE (JSON)                        │
│ {                                      │
│   "results": [                         │
│     {                                  │
│       "id": "doc2",                    │
│       "title": "Python Tutorial",      │
│       "snippet": "Learn python...",    │
│       "score": 0.85                    │
│     },                                 │
│     {                                  │
│       "id": "doc5",                    │
│       "title": "Advanced Python",      │
│       "snippet": "Python tutorial...", │
│       "score": 0.72                    │
│     }                                  │
│   ],                                   │
│   "total": 2,                          │
│   "query_time_ms": 45                  │
│ }                                      │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ FRONTEND (SearchResults.jsx)           │
│ • Receives JSON                        │
│ • Renders results                      │
│ • Shows titles, snippets, scores       │
└────────────────────────────────────────┘
         │
         ▼
      USER sees results! 🎉
```

---

## 🔍 Inverted Index Deep Dive

### Before Indexing (Documents Collection)

```
┌─────────────────────────────────────────────────────┐
│ Document 1                                          │
│ Title: "Python Programming Basics"                  │
│ Content: "Python is a great language for beginners" │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Document 2                                          │
│ Title: "Learn Python"                               │
│ Content: "Python tutorial for data science"         │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Document 3                                          │
│ Title: "Data Science Guide"                         │
│ Content: "Data science with Python and R"           │
└─────────────────────────────────────────────────────┘
```

### Text Processing Pipeline

```
Document 1: "Python is a great language for beginners"
    │
    ▼ Step 1: Tokenization (split into words)
["Python", "is", "a", "great", "language", "for", "beginners"]
    │
    ▼ Step 2: Lowercase normalization
["python", "is", "a", "great", "language", "for", "beginners"]
    │
    ▼ Step 3: Remove stop words (is, a, for)
["python", "great", "language", "beginners"]
    │
    ▼ Step 4: Stemming (optional)
["python", "great", "languag", "begin"]
    │
    ▼ Step 5: Store in inverted index
```

### After Indexing (Inverted Index Collection)

```
┌───────────────────────────────────────────────────────────┐
│ Word: "python"                                            │
│ Documents: [doc1, doc2, doc3]                             │
│ Positions: {                                              │
│   doc1: [0, 15],    # Appears at position 0 and 15        │
│   doc2: [0, 10],    # Appears at position 0 and 10        │
│   doc3: [8]         # Appears at position 8               │
│ }                                                          │
│ Total docs containing: 3                                  │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│ Word: "data"                                              │
│ Documents: [doc2, doc3]                                   │
│ Positions: {                                              │
│   doc2: [5],        # Appears at position 5               │
│   doc3: [0, 3]      # Appears at position 0 and 3         │
│ }                                                          │
│ Total docs containing: 2                                  │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│ Word: "science"                                           │
│ Documents: [doc2, doc3]                                   │
│ Positions: {                                              │
│   doc2: [6],                                              │
│   doc3: [1]                                               │
│ }                                                          │
│ Total docs containing: 2                                  │
└───────────────────────────────────────────────────────────┘
```

### Search Execution

**Query**: "python data"

```
Step 1: Process query same way as documents
  → ["python", "data"]

Step 2: Lookup each term in index
  "python" → [doc1, doc2, doc3]
  "data"   → [doc2, doc3]

Step 3: Find intersection (documents with ALL terms)
  [doc1, doc2, doc3] ∩ [doc2, doc3] = [doc2, doc3]

Step 4: Calculate TF-IDF for each matched document
  doc2:
    TF(python) = 2/10 = 0.2    (2 occurrences, 10 total words)
    IDF(python) = log(3/3) = 0  (appears in all 3 docs)
    TF(data) = 1/10 = 0.1
    IDF(data) = log(3/2) = 0.18
    Total score = (0.2 × 0) + (0.1 × 0.18) = 0.018

  doc3:
    TF(python) = 1/8 = 0.125
    IDF(python) = 0
    TF(data) = 2/8 = 0.25
    IDF(data) = 0.18
    Total score = (0.125 × 0) + (0.25 × 0.18) = 0.045

Step 5: Sort by score (highest first)
  Results: [doc3 (0.045), doc2 (0.018)]
```

---

## 📁 Module Responsibilities

```
┌─────────────────────────────────────────────────────────┐
│ ROUTES (routes/)                                        │
│ Responsibility: Handle HTTP requests/responses          │
│ • Validate request data (via Pydantic schemas)          │
│ • Call appropriate service methods                      │
│ • Return JSON responses                                 │
│ • Apply middleware (auth, CORS, etc.)                   │
│                                                          │
│ SHOULD NOT:                                             │
│ ✗ Contain business logic                                │
│ ✗ Directly access database                              │
│ ✗ Perform calculations                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ SERVICES (services/)                                    │
│ Responsibility: All business logic                      │
│ • Process data                                          │
│ • Interact with database                                │
│ • Execute algorithms (search, ranking, indexing)        │
│ • Orchestrate multiple operations                       │
│                                                          │
│ SHOULD NOT:                                             │
│ ✗ Handle HTTP requests directly                         │
│ ✗ Know about request/response format                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ MODELS (models/)                                        │
│ Responsibility: Define data structure                   │
│ • Database schema                                       │
│ • Field types                                           │
│ • Relationships                                         │
│                                                          │
│ SHOULD NOT:                                             │
│ ✗ Contain validation logic                              │
│ ✗ Contain business logic                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ SCHEMAS (schemas/)                                      │
│ Responsibility: Validate API data                       │
│ • Request validation                                    │
│ • Response serialization                                │
│ • Type checking                                         │
│ • Auto-generate API docs                                │
│                                                          │
│ SHOULD NOT:                                             │
│ ✗ Know about database structure                         │
│ ✗ Contain business logic                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ UTILS (utils/)                                          │
│ Responsibility: Helper functions                        │
│ • Text processing (tokenization, stemming)              │
│ • Security (hashing, JWT)                               │
│ • Common utilities                                      │
│                                                          │
│ SHOULD BE:                                              │
│ ✓ Reusable across services                              │
│ ✓ Pure functions (no side effects)                      │
│ ✓ Well-tested                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Learning Concepts

### 1. **Separation of Concerns**
Each layer has ONE responsibility:
- **Routes**: HTTP handling
- **Services**: Business logic
- **Models**: Data structure
- **Schemas**: Validation

### 2. **Dependency Injection**
```python
# Routes depend on services
@router.get("/search")
async def search(q: str):
    return await search_service.search(q)  # Injected dependency

# Services depend on database
class SearchService:
    def __init__(self, db):
        self.db = db  # Injected dependency
```

### 3. **Async/Await**
All I/O operations are async for better performance:
```python
# Database calls
await db.users.find_one({"username": username})

# Service calls
results = await search_service.search(query)
```

### 4. **Clean Code Principles**
- **Single Responsibility**: Each function does ONE thing
- **DRY (Don't Repeat Yourself)**: Reuse code via utils
- **Clear Naming**: Functions/variables explain themselves
- **Small Functions**: <30 lines per function

---

## 🚀 Performance Optimizations

```
┌─────────────────────────────────────────────────────────┐
│ 1. DATABASE INDEXING                                    │
│ Create MongoDB indexes on frequently queried fields:    │
│ • users.username (unique)                               │
│ • users.email (unique)                                  │
│ • documents.user_id                                     │
│ • inverted_index._id (word)                             │
│                                                          │
│ Impact: 100x faster queries                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 2. CONNECTION POOLING                                   │
│ Reuse database connections instead of creating new ones │
│                                                          │
│ Bad:  Create connection → Query → Close (slow)          │
│ Good: Reuse connection pool (fast)                      │
│                                                          │
│ Impact: 10x faster database operations                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 3. ASYNC OPERATIONS                                     │
│ Don't block while waiting for I/O                       │
│                                                          │
│ Sync:  Request 1 → Wait → Request 2 → Wait              │
│ Async: Request 1 + Request 2 → Both complete together   │
│                                                          │
│ Impact: 5x more requests per second                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 4. PAGINATION                                           │
│ Don't return all results at once                        │
│                                                          │
│ Bad:  Return 10,000 documents                           │
│ Good: Return 10 documents per page                      │
│                                                          │
│ Impact: 1000x faster response time                      │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Technologies Chosen - Why?

| Technology | Why? | Alternatives |
|------------|------|--------------|
| **FastAPI** | • Async support<br>• Auto API docs<br>• Fast performance<br>• Modern Python | Flask, Django |
| **MongoDB** | • Flexible schema<br>• Easy scaling<br>• JSON-like docs<br>• Free tier | PostgreSQL, MySQL |
| **Motor** | • Async MongoDB driver<br>• Non-blocking I/O | PyMongo (sync) |
| **Pydantic** | • Auto validation<br>• Type checking<br>• Clear errors | Marshmallow |
| **JWT** | • Stateless auth<br>• Scalable<br>• Standard | Sessions |
| **Bcrypt** | • Secure hashing<br>• Slow by design<br>• Industry standard | SHA-256, MD5 |

---

## 🎓 What You'll Learn

By completing this project, you will deeply understand:

✅ **Backend Architecture**
- Clean code principles
- Separation of concerns
- Service-oriented architecture
- Async programming patterns

✅ **Search Algorithms**
- Inverted index implementation
- Text processing pipeline
- TF-IDF ranking
- Query optimization

✅ **Database Design**
- NoSQL schema design
- Index optimization
- Query performance
- Data relationships

✅ **API Development**
- RESTful design
- JWT authentication
- Request validation
- Error handling

✅ **Full-Stack Integration**
- Frontend-backend communication
- State management
- Authentication flow
- Deployment pipeline

---

Ready to start coding? Let's begin with **Phase 1: Configuration & Database Setup**! 🚀
