"""Transparent exact-skill analysis with optional semantic evidence."""
from engine import analyze

def analyze_hybrid(resume: str, job: str, use_semantic: bool = False):
    report = analyze(resume, job)
    report["semantic_similarity"] = None
    report["semantic_mode"] = "disabled"
    if use_semantic:
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            embeddings = model.encode([resume[:5000], job[:5000]])
            report["semantic_similarity"] = round(float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]) * 100, 1)
            report["semantic_mode"] = "MiniLM sentence embeddings (contextual evidence only)"
        except (ImportError, OSError, RuntimeError, ValueError) as exc:
            report["semantic_mode"] = "unavailable; exact skill analysis retained"
            report["semantic_error"] = type(exc).__name__
    return report
