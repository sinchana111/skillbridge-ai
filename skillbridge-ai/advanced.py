"""Privacy preview, learning dependencies and transparent what-if calculations."""
import re

PREREQUISITES = {
    'Machine Learning': ['Python'], 'Deep Learning': ['Machine Learning'],
    'PyTorch': ['Python', 'Machine Learning'], 'TensorFlow': ['Python', 'Machine Learning'],
    'NLP': ['Python', 'Machine Learning'], 'Computer Vision': ['Python', 'Machine Learning'],
    'FastAPI': ['Python'], 'Flask': ['Python'], 'Docker': ['Linux'],
    'Kubernetes': ['Docker'], 'RAG': ['Python', 'LLM'], 'LLM': ['Python'],
    'AWS': ['Linux'], 'Scikit-learn': ['Python', 'Machine Learning'],
}

def mask_pii(text):
    """Best-effort masking, not guaranteed removal of all identifiers."""
    text = re.sub(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', '[EMAIL]', text)
    text = re.sub(r'(?<!\w)(?:\+?\d[\d\s().-]{8,}\d)(?!\w)', '[PHONE]', text)
    text = re.sub(r'https?://\S+|www\.\S+', '[URL]', text, flags=re.I)
    return text

def simulate(report, selected):
    """Recompute the original coverage formula with hypothetically added skills."""
    job = set(report['job_skills'])
    observed = set(report['resume_skills'])
    added = set(selected) & job
    if not job:
        return None, 0
    before = 100 * len(observed & job) / len(job)
    after = 100 * len((observed | added) & job) / len(job)
    return round(after, 1), round(after - before, 1)

def dependencies(skills):
    """Return graph edges for requested skills and curated suggested prerequisites."""
    edges = set()
    visited = set()
    def visit(skill):
        if skill in visited:
            return
        visited.add(skill)
        for prerequisite in PREREQUISITES.get(skill, []):
            edges.add((prerequisite, skill))
            visit(prerequisite)
    for skill in skills:
        visit(skill)
    return sorted(edges)
