"""
API routes for loading sample data
"""
from fastapi import APIRouter, HTTPException
from mongodb import get_database
from indexing_service import IndexingService
from security import hash_password
from datetime import datetime

router = APIRouter(prefix="/api", tags=["data"])

SAMPLE_DOCUMENTS = [
    {"title": "What is Artificial Intelligence?", "content": "Artificial Intelligence (AI) is the simulation of human intelligence by machines. AI systems can learn, reason, and self-correct. Common applications include virtual assistants, recommendation systems, and autonomous vehicles."},
    {"title": "Introduction to Machine Learning", "content": "Machine Learning is a subset of AI that enables computers to learn from data without explicit programming. It uses algorithms to identify patterns and make predictions. Popular techniques include supervised learning, unsupervised learning, and reinforcement learning."},
    {"title": "Deep Learning Explained", "content": "Deep Learning uses neural networks with multiple layers to process data. It powers image recognition, natural language processing, and speech recognition. Deep learning models require large datasets and significant computational power."},
    {"title": "Python Programming Guide", "content": "Python is a versatile, high-level programming language known for its simplicity and readability. It's widely used in web development, data science, automation, and AI. Python has extensive libraries like NumPy, Pandas, and TensorFlow."},
    {"title": "JavaScript for Beginners", "content": "JavaScript is the programming language of the web. It enables interactive websites and runs in browsers. Modern JavaScript includes ES6 features like arrow functions, promises, and async/await. Popular frameworks include React, Vue, and Angular."},
    {"title": "Web Development Basics", "content": "Web development involves creating websites and web applications. Frontend development uses HTML, CSS, and JavaScript. Backend development uses languages like Python, Node.js, or Java. Full-stack developers work on both frontend and backend."},
    {"title": "Data Science Fundamentals", "content": "Data Science combines statistics, programming, and domain expertise to extract insights from data. Key skills include data cleaning, visualization, statistical analysis, and machine learning. Common tools are Python, R, SQL, and Tableau."},
    {"title": "Big Data Analytics", "content": "Big Data refers to extremely large datasets that traditional tools cannot process. Technologies like Hadoop, Spark, and NoSQL databases handle big data. Applications include business intelligence, predictive analytics, and real-time processing."},
    {"title": "Data Visualization Techniques", "content": "Data visualization transforms data into visual formats like charts, graphs, and dashboards. Effective visualizations communicate insights clearly. Popular tools include Matplotlib, Seaborn, Plotly, and Tableau. Good design principles are essential."},
    {"title": "Cloud Computing Overview", "content": "Cloud computing delivers computing services over the internet. Major providers include AWS, Azure, and Google Cloud. Services include storage, databases, networking, and AI. Benefits are scalability, cost-efficiency, and accessibility."},
    {"title": "AWS Services Guide", "content": "Amazon Web Services (AWS) offers over 200 cloud services. Popular services include EC2 for computing, S3 for storage, RDS for databases, and Lambda for serverless computing. AWS dominates the cloud market."},
    {"title": "Docker and Containers", "content": "Docker packages applications into containers that run consistently across environments. Containers are lightweight, portable, and efficient. Docker simplifies deployment and scaling. Kubernetes orchestrates container management at scale."},
    {"title": "Cybersecurity Basics", "content": "Cybersecurity protects systems, networks, and data from digital attacks. Key concepts include encryption, authentication, firewalls, and intrusion detection. Common threats are malware, phishing, and ransomware. Security is everyone's responsibility."},
    {"title": "Blockchain Technology", "content": "Blockchain is a distributed ledger technology that ensures transparency and security. It powers cryptocurrencies like Bitcoin and Ethereum. Applications extend to supply chain, healthcare, and voting systems. Blockchain is immutable and decentralized."},
    {"title": "Mobile App Development", "content": "Mobile development creates applications for smartphones and tablets. Native development uses Swift for iOS and Kotlin for Android. Cross-platform frameworks like React Native and Flutter enable code reuse. Mobile apps must be responsive and user-friendly."},
    {"title": "React Native Tutorial", "content": "React Native allows building mobile apps using JavaScript and React. It provides native performance with cross-platform code. Popular for startups and rapid development. Supports both iOS and Android from a single codebase."},
    {"title": "SQL Database Fundamentals", "content": "SQL (Structured Query Language) manages relational databases. Common operations include SELECT, INSERT, UPDATE, and DELETE. Popular databases are MySQL, PostgreSQL, and SQL Server. SQL ensures data integrity and supports complex queries."},
    {"title": "NoSQL Databases", "content": "NoSQL databases handle unstructured data and scale horizontally. Types include document stores (MongoDB), key-value stores (Redis), column stores (Cassandra), and graph databases (Neo4j). NoSQL is flexible and high-performance."},
    {"title": "Agile Methodology", "content": "Agile is an iterative approach to software development. It emphasizes collaboration, flexibility, and customer feedback. Scrum and Kanban are popular Agile frameworks. Agile delivers working software in short sprints."},
    {"title": "Git Version Control", "content": "Git tracks changes in source code during development. It enables collaboration, branching, and merging. GitHub, GitLab, and Bitbucket host Git repositories. Essential commands include commit, push, pull, and merge."},
    {"title": "API Design Best Practices", "content": "APIs (Application Programming Interfaces) enable software communication. RESTful APIs use HTTP methods like GET, POST, PUT, DELETE. Good API design includes clear documentation, versioning, and error handling. GraphQL is an alternative to REST."},
    {"title": "Natural Language Processing", "content": "NLP enables computers to understand and generate human language. Applications include chatbots, translation, and sentiment analysis. Techniques use transformers, BERT, and GPT models. NLP is advancing rapidly with large language models."},
    {"title": "Computer Vision Applications", "content": "Computer Vision enables machines to interpret visual information. Applications include facial recognition, object detection, and autonomous driving. Convolutional Neural Networks (CNNs) are commonly used. OpenCV and TensorFlow are popular libraries."},
    {"title": "How to Learn Programming", "content": "Learning programming requires practice and patience. Start with fundamentals like variables, loops, and functions. Build projects to apply knowledge. Use resources like online courses, documentation, and coding challenges. Join communities for support."},
    {"title": "Tech Career Paths", "content": "Technology offers diverse career paths including software engineering, data science, cybersecurity, and DevOps. Skills needed vary by role but include programming, problem-solving, and communication. Continuous learning is essential in tech."},
]

@router.post("/load-sample-data")
async def load_sample_data():
    """Load 25 sample documents into the database"""
    db = get_database()
    
    # Create a default user if doesn't exist
    user = await db.users.find_one({"email": "sample@example.com"})
    if not user:
        user_doc = {
            "email": "sample@example.com",
            "username": "sampleuser",
            "hashed_password": hash_password("sample123"),
            "created_at": datetime.utcnow()
        }
        result = await db.users.insert_one(user_doc)
        user_id = str(result.inserted_id)
    else:
        user_id = str(user["_id"])
    
    # Insert documents
    count = 0
    for doc_data in SAMPLE_DOCUMENTS:
        # Check if document already exists
        existing = await db.documents.find_one({"title": doc_data["title"]})
        if existing:
            continue
        
        doc = {
            "title": doc_data["title"],
            "content": doc_data["content"],
            "author_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.documents.insert_one(doc)
        doc_id = str(result.inserted_id)
        
        # Index the document
        await IndexingService.build_index_for_document(doc_id, doc["title"], doc["content"])
        count += 1
    
    return {
        "message": f"Successfully loaded {count} new documents",
        "total_loaded": count,
        "topics": ["AI", "Machine Learning", "Web Development", "Data Science", "Cloud Computing", "Cybersecurity", "Mobile Development", "Databases", "Software Engineering"]
    }
