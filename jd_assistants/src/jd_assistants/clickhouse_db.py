"""
ClickHouse database connection and operations
"""
import clickhouse_connect
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
import json


class ClickHouseDB:
    """ClickHouse database client wrapper"""
    
    def __init__(
        self,
        host: str = None,
        port: int = 8123,
        username: str = "default",
        password: str = "",
        database: str = "hr_system"
    ):
        self.host = host or os.getenv("CLICKHOUSE_HOST", "localhost")
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.client = None
    
    def connect(self):
        """Establish connection to ClickHouse"""
        if not self.client:
            self.client = clickhouse_connect.get_client(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                database=self.database
            )
        return self.client
    
    def close(self):
        """Close ClickHouse connection"""
        if self.client:
            self.client.close()
            self.client = None
    
    def execute(self, query: str, parameters: Dict = None):
        """Execute a query"""
        client = self.connect()
        return client.command(query, parameters=parameters)
    
    def query(self, query: str, parameters: Dict = None):
        """Execute a query and return results"""
        client = self.connect()
        return client.query(query, parameters=parameters)
    
    def insert(self, table: str, data: List[List], column_names: List[str] = None):
        """Insert data into table"""
        client = self.connect()
        return client.insert(table, data, column_names=column_names)
    
    def insert_dict(self, table: str, data: List[Dict]):
        """Insert data from list of dictionaries"""
        if not data:
            return
        
        client = self.connect()
        column_names = list(data[0].keys())
        rows = [[row.get(col) for col in column_names] for row in data]
        return client.insert(table, rows, column_names=column_names)


# Global ClickHouse instance
_clickhouse_instance: Optional[ClickHouseDB] = None


def get_clickhouse() -> ClickHouseDB:
    """Get or create ClickHouse instance"""
    global _clickhouse_instance
    if _clickhouse_instance is None:
        _clickhouse_instance = ClickHouseDB(
            host=os.getenv("CLICKHOUSE_HOST", "localhost"),
            port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
            username=os.getenv("CLICKHOUSE_USER", "default"),
            password=os.getenv("CLICKHOUSE_PASSWORD", ""),
            database=os.getenv("CLICKHOUSE_DATABASE", "hr_system")
        )
    return _clickhouse_instance


def init_clickhouse():
    """Initialize ClickHouse database and tables"""
    db = get_clickhouse()
    
    # Create database
    db.execute(f"CREATE DATABASE IF NOT EXISTS {db.database}")
    
    # Create users table for API key management
    db.execute(f"""
        CREATE TABLE IF NOT EXISTS {db.database}.users (
            id String,
            email String,
            password_hash String,
            role LowCardinality(String),
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (id)
    """)
    
    # Create api_keys table
    db.execute(f"""
        CREATE TABLE IF NOT EXISTS {db.database}.api_keys (
            id String,
            user_id String,
            provider LowCardinality(String),
            key_name String,
            api_key String,
            model String DEFAULT '',
            is_active UInt8 DEFAULT 1,
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (user_id, provider, id)
    """)
    
    # Create candidates table
    db.execute(f"""
        CREATE TABLE IF NOT EXISTS {db.database}.candidates (
            candidate_id String,
            name String,
            email String,
            phone String,
            bio String,
            skills String,
            personal_info String,
            education String,
            work_experience String,
            cv_file_path String,
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (candidate_id)
    """)
    
    # Create job_descriptions table
    db.execute(f"""
        CREATE TABLE IF NOT EXISTS {db.database}.job_descriptions (
            id String,
            title String,
            description String,
            skills String,
            requirements String,
            benefits String,
            is_active UInt8 DEFAULT 0,
            created_by String,
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (id)
    """)
    
    # Create candidate_scores table
    db.execute(f"""
        CREATE TABLE IF NOT EXISTS {db.database}.candidate_scores (
            id String,
            candidate_id String,
            jd_id String,
            score UInt8,
            reason String,
            scored_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (jd_id, candidate_id, scored_at)
    """)
    
    # Create jd_analysis table
    db.execute(f"""
        CREATE TABLE IF NOT EXISTS {db.database}.jd_analysis (
            id String,
            jd_id String,
            original_jd String,
            overall_score UInt8,
            key_recommendations Array(String),
            improvements String,
            analyzed_by String,
            analyzed_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (jd_id, analyzed_at)
    """)
    
    print(f"✅ ClickHouse database '{db.database}' initialized successfully")


# === User Operations ===

def create_user(user_data: Dict) -> Dict:
    """Create a new user"""
    db = get_clickhouse()
    user_id = user_data.get("id") or f"user_{int(datetime.utcnow().timestamp() * 1000)}"
    
    data = [{
        "id": user_id,
        "email": user_data["email"],
        "password_hash": user_data["password_hash"],
        "role": user_data.get("role", "user"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }]
    
    db.insert_dict(f"{db.database}.users", data)
    return {**user_data, "id": user_id}


def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email"""
    db = get_clickhouse()
    result = db.query(
        f"SELECT * FROM {db.database}.users WHERE email = %(email)s LIMIT 1",
        parameters={"email": email}
    )
    
    if result.result_rows:
        row = result.result_rows[0]
        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "role": row[3],
            "created_at": row[4],
            "updated_at": row[5]
        }
    return None


def get_user_by_id(user_id: str) -> Optional[Dict]:
    """Get user by ID"""
    db = get_clickhouse()
    result = db.query(
        f"SELECT * FROM {db.database}.users WHERE id = %(id)s LIMIT 1",
        parameters={"id": user_id}
    )
    
    if result.result_rows:
        row = result.result_rows[0]
        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "role": row[3],
            "created_at": row[4],
            "updated_at": row[5]
        }
    return None


# === API Key Operations ===

def create_api_key(key_data: Dict) -> Dict:
    """Create a new API key"""
    db = get_clickhouse()
    key_id = f"key_{int(datetime.utcnow().timestamp() * 1000)}"
    
    data = [{
        "id": key_id,
        "user_id": key_data["user_id"],
        "provider": key_data["provider"],
        "key_name": key_data.get("key_name", f"{key_data['provider']} Key"),
        "api_key": key_data["api_key"],
        "model": key_data.get("model", ""),
        "is_active": 1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }]
    
    db.insert_dict(f"{db.database}.api_keys", data)
    return {**key_data, "id": key_id}


def get_user_api_keys(user_id: str, provider: str = None) -> List[Dict]:
    """Get all API keys for a user"""
    db = get_clickhouse()
    
    if provider:
        query = f"""
            SELECT * FROM {db.database}.api_keys 
            WHERE user_id = %(user_id)s AND provider = %(provider)s AND is_active = 1
            ORDER BY created_at DESC
        """
        result = db.query(query, parameters={"user_id": user_id, "provider": provider})
    else:
        query = f"""
            SELECT * FROM {db.database}.api_keys 
            WHERE user_id = %(user_id)s AND is_active = 1
            ORDER BY created_at DESC
        """
        result = db.query(query, parameters={"user_id": user_id})
    
    keys = []
    for row in result.result_rows:
        keys.append({
            "id": row[0],
            "user_id": row[1],
            "provider": row[2],
            "key_name": row[3],
            "api_key": row[4],
            "model": row[5] if len(row) > 7 else "",
            "is_active": bool(row[6] if len(row) > 7 else row[5]),
            "created_at": row[7] if len(row) > 7 else row[6],
            "updated_at": row[8] if len(row) > 7 else row[7]
        })
    
    return keys


def get_active_api_key(user_id: str, provider: str) -> Optional[str]:
    """Get active API key for a user and provider"""
    keys = get_user_api_keys(user_id, provider)
    return keys[0]["api_key"] if keys else None


def delete_api_key(key_id: str, user_id: str) -> bool:
    """Delete (deactivate) an API key"""
    db = get_clickhouse()
    db.execute(
        f"""
        ALTER TABLE {db.database}.api_keys 
        UPDATE is_active = 0, updated_at = now()
        WHERE id = %(key_id)s AND user_id = %(user_id)s
        """,
        parameters={"key_id": key_id, "user_id": user_id}
    )
    return True


# === Candidate Operations ===

def create_candidate(candidate_data: Dict) -> Dict:
    """Create a new candidate"""
    db = get_clickhouse()
    candidate_id = candidate_data.get("candidate_id") or f"cand_{int(datetime.utcnow().timestamp() * 1000)}"
    
    data = [{
        "candidate_id": candidate_id,
        "name": candidate_data.get("name", ""),
        "email": candidate_data.get("email", ""),
        "phone": candidate_data.get("phone", ""),
        "bio": candidate_data.get("bio", ""),
        "skills": candidate_data.get("skills", ""),
        "personal_info": json.dumps(candidate_data.get("personal_info", {})),
        "education": json.dumps(candidate_data.get("education", [])),
        "work_experience": json.dumps(candidate_data.get("work_experience", [])),
        "cv_file_path": candidate_data.get("cv_file_path", ""),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }]
    
    db.insert_dict(f"{db.database}.candidates", data)
    return {**candidate_data, "candidate_id": candidate_id}


def get_all_candidates() -> List[Dict]:
    """Get all candidates"""
    db = get_clickhouse()
    result = db.query(f"SELECT * FROM {db.database}.candidates ORDER BY created_at DESC")
    
    candidates = []
    for row in result.result_rows:
        candidates.append({
            "candidate_id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "bio": row[4],
            "skills": row[5],
            "personal_info": json.loads(row[6]) if row[6] else {},
            "education": json.loads(row[7]) if row[7] else [],
            "work_experience": json.loads(row[8]) if row[8] else [],
            "cv_file_path": row[9],
            "created_at": row[10],
            "updated_at": row[11]
        })
    
    return candidates


def get_candidate_by_id(candidate_id: str) -> Optional[Dict]:
    """Get candidate by ID"""
    db = get_clickhouse()
    result = db.query(
        f"SELECT * FROM {db.database}.candidates WHERE candidate_id = %(id)s LIMIT 1",
        parameters={"id": candidate_id}
    )
    
    if result.result_rows:
        row = result.result_rows[0]
        return {
            "candidate_id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "bio": row[4],
            "skills": row[5],
            "personal_info": json.loads(row[6]) if row[6] else {},
            "education": json.loads(row[7]) if row[7] else [],
            "work_experience": json.loads(row[8]) if row[8] else [],
            "cv_file_path": row[9],
            "created_at": row[10],
            "updated_at": row[11]
        }
    return None


def delete_candidate(candidate_id: str) -> bool:
    """Delete a candidate"""
    db = get_clickhouse()
    db.execute(
        f"ALTER TABLE {db.database}.candidates DELETE WHERE candidate_id = %(id)s",
        parameters={"id": candidate_id}
    )
    return True


# === Job Description Operations ===

def create_job_description(jd_data: Dict) -> Dict:
    """Create a new job description"""
    db = get_clickhouse()
    jd_id = jd_data.get("id") or f"jd_{int(datetime.utcnow().timestamp() * 1000)}"
    
    data = [{
        "id": jd_id,
        "title": jd_data["title"],
        "description": jd_data["description"],
        "skills": jd_data.get("skills", ""),
        "requirements": jd_data.get("requirements", ""),
        "benefits": jd_data.get("benefits", ""),
        "is_active": jd_data.get("is_active", 0),
        "created_by": jd_data.get("created_by", ""),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }]
    
    db.insert_dict(f"{db.database}.job_descriptions", data)
    return {**jd_data, "id": jd_id}


def get_all_jds() -> List[Dict]:
    """Get all job descriptions"""
    db = get_clickhouse()
    result = db.query(f"SELECT * FROM {db.database}.job_descriptions ORDER BY created_at DESC")
    
    jds = []
    for row in result.result_rows:
        jds.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "skills": row[3],
            "requirements": row[4],
            "benefits": row[5],
            "is_active": bool(row[6]),
            "created_by": row[7],
            "created_at": row[8],
            "updated_at": row[9]
        })
    
    return jds


def get_jd_by_id(jd_id: str) -> Optional[Dict]:
    """Get job description by ID"""
    db = get_clickhouse()
    result = db.query(
        f"SELECT * FROM {db.database}.job_descriptions WHERE id = %(id)s LIMIT 1",
        parameters={"id": jd_id}
    )
    
    if result.result_rows:
        row = result.result_rows[0]
        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "skills": row[3],
            "requirements": row[4],
            "benefits": row[5],
            "is_active": bool(row[6]),
            "created_by": row[7],
            "created_at": row[8],
            "updated_at": row[9]
        }
    return None


def activate_jd(jd_id: str) -> bool:
    """Set a JD as active and deactivate all others"""
    db = get_clickhouse()
    
    # Deactivate all
    db.execute(f"ALTER TABLE {db.database}.job_descriptions UPDATE is_active = 0")
    
    # Activate the specified one
    db.execute(
        f"ALTER TABLE {db.database}.job_descriptions UPDATE is_active = 1 WHERE id = %(id)s",
        parameters={"id": jd_id}
    )
    return True


def get_active_jd() -> Optional[Dict]:
    """Get the active job description"""
    db = get_clickhouse()
    result = db.query(
        f"SELECT * FROM {db.database}.job_descriptions WHERE is_active = 1 LIMIT 1"
    )
    
    if result.result_rows:
        row = result.result_rows[0]
        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "skills": row[3],
            "requirements": row[4],
            "benefits": row[5],
            "is_active": bool(row[6]),
            "created_by": row[7],
            "created_at": row[8],
            "updated_at": row[9]
        }
    return None


def delete_jd(jd_id: str) -> bool:
    """Delete a job description"""
    db = get_clickhouse()
    db.execute(
        f"ALTER TABLE {db.database}.job_descriptions DELETE WHERE id = %(id)s",
        parameters={"id": jd_id}
    )
    return True


def update_jd(jd_id: str, jd_data: Dict) -> bool:
    """Update a job description"""
    db = get_clickhouse()
    
    update_fields = []
    params = {"id": jd_id}
    
    if "title" in jd_data:
        update_fields.append("title = %(title)s")
        params["title"] = jd_data["title"]
    if "description" in jd_data:
        update_fields.append("description = %(description)s")
        params["description"] = jd_data["description"]
    if "skills" in jd_data:
        update_fields.append("skills = %(skills)s")
        params["skills"] = jd_data["skills"]
    if "requirements" in jd_data:
        update_fields.append("requirements = %(requirements)s")
        params["requirements"] = jd_data["requirements"]
    if "benefits" in jd_data:
        update_fields.append("benefits = %(benefits)s")
        params["benefits"] = jd_data["benefits"]
    
    update_fields.append("updated_at = now()")
    
    query = f"""
        ALTER TABLE {db.database}.job_descriptions 
        UPDATE {', '.join(update_fields)}
        WHERE id = %(id)s
    """
    
    db.execute(query, parameters=params)
    return True


# === Candidate Scoring Operations ===

def save_candidate_score(score_data: Dict) -> Dict:
    """Save candidate score"""
    db = get_clickhouse()
    score_id = f"score_{int(datetime.utcnow().timestamp() * 1000)}"
    
    data = [{
        "id": score_id,
        "candidate_id": score_data["candidate_id"],
        "jd_id": score_data["jd_id"],
        "score": score_data["score"],
        "reason": score_data.get("reason", ""),
        "scored_at": datetime.utcnow()
    }]
    
    db.insert_dict(f"{db.database}.candidate_scores", data)
    return {**score_data, "id": score_id}


def get_candidate_scores(candidate_id: str) -> List[Dict]:
    """Get all scores for a candidate"""
    db = get_clickhouse()
    result = db.query(
        f"""
        SELECT * FROM {db.database}.candidate_scores 
        WHERE candidate_id = %(id)s 
        ORDER BY scored_at DESC
        """,
        parameters={"id": candidate_id}
    )
    
    scores = []
    for row in result.result_rows:
        scores.append({
            "id": row[0],
            "candidate_id": row[1],
            "jd_id": row[2],
            "score": row[3],
            "reason": row[4],
            "scored_at": row[5]
        })
    
    return scores


def get_scores_by_jd(jd_id: str) -> List[Dict]:
    """Get all scores for a job description"""
    db = get_clickhouse()
    result = db.query(
        f"""
        SELECT cs.*, c.name as candidate_name
        FROM {db.database}.candidate_scores cs
        LEFT JOIN {db.database}.candidates c ON cs.candidate_id = c.candidate_id
        WHERE cs.jd_id = %(id)s 
        ORDER BY cs.score DESC, cs.scored_at DESC
        """,
        parameters={"id": jd_id}
    )
    
    scores = []
    for row in result.result_rows:
        scores.append({
            "id": row[0],
            "candidate_id": row[1],
            "jd_id": row[2],
            "score": row[3],
            "reason": row[4],
            "scored_at": row[5],
            "candidate_name": row[6] if len(row) > 6 else ""
        })
    
    return scores


# === JD Analysis Operations ===

def save_jd_analysis(analysis_data: Dict) -> Dict:
    """Save JD analysis"""
    db = get_clickhouse()
    analysis_id = f"analysis_{int(datetime.utcnow().timestamp() * 1000)}"
    
    data = [{
        "id": analysis_id,
        "jd_id": analysis_data.get("jd_id", ""),
        "original_jd": analysis_data["original_jd"],
        "overall_score": analysis_data["overall_score"],
        "key_recommendations": analysis_data.get("key_recommendations", []),
        "improvements": json.dumps(analysis_data.get("improvements", [])),
        "analyzed_by": analysis_data.get("analyzed_by", ""),
        "analyzed_at": datetime.utcnow()
    }]
    
    db.insert_dict(f"{db.database}.jd_analysis", data)
    return {**analysis_data, "id": analysis_id}


def get_jd_analysis_history(jd_id: str) -> List[Dict]:
    """Get analysis history for a JD"""
    db = get_clickhouse()
    result = db.query(
        f"""
        SELECT * FROM {db.database}.jd_analysis 
        WHERE jd_id = %(id)s 
        ORDER BY analyzed_at DESC
        """,
        parameters={"id": jd_id}
    )
    
    analyses = []
    for row in result.result_rows:
        analyses.append({
            "id": row[0],
            "jd_id": row[1],
            "original_jd": row[2],
            "overall_score": row[3],
            "key_recommendations": row[4],
            "improvements": json.loads(row[5]) if row[5] else [],
            "analyzed_by": row[6],
            "analyzed_at": row[7]
        })
    
    return analyses
