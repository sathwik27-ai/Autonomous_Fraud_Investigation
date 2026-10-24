from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(REPO_ROOT / ".env"), extra="ignore")

    # LLM — leave the key empty to run the deterministic rule-based agent
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-latest"

    # API auth — leave empty to disable (dev mode). Set both in production.
    api_key: str = ""
    webhook_secret: str = ""

    # CORS — comma-separated origins, or "*" to allow all (including Vercel deployments)
    cors_origins: str = "*"

    # Storage
    database_url: str = "sqlite:///./fraud.db"


    # Graph — falls back to an in-memory graph when Neo4j is unreachable
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "fraudgraph"

    # Decision thresholds
    fraud_block_threshold: float = 0.8
    fraud_review_threshold: float = 0.5

    # CORS
    cors_origins: str = "*"

    # Agent loop
    agent_max_steps: int = 8

    data_dir: Path = REPO_ROOT / "data"

    @property
    def sqlalchemy_database_url(self) -> str:
        """Render, Neon, and Supabase often provide postgres:// URLs.
        SQLAlchemy requires postgresql://."""
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url


settings = Settings()
