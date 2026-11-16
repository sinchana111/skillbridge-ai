"""Deterministic, explainable NLP resume-to-job analysis."""
import re
from collections import Counter

SKILLS = {
 'Languages':['Python','Java','JavaScript','TypeScript','C++','SQL','R'],
 'AI & Data':['Machine Learning','Deep Learning','NLP','Computer Vision','TensorFlow','PyTorch','Scikit-learn','Pandas','NumPy','LLM','RAG'],
 'Web & APIs':['React','Node.js','FastAPI','Flask','Django','REST API','HTML','CSS'],
 'Cloud & Tools':['AWS','Azure','Docker','Kubernetes','Git','GitHub','Linux','Power BI','Tableau'],
 'Professional':['Communication','Leadership','Teamwork','Problem Solving','Agile']
}
ALIASES={'Scikit-learn':['scikit learn','sklearn'],'Node.js':['nodejs','node js'],'REST API':['restful api','rest apis'],'Machine Learning':['ml','machine-learning'],'Deep Learning':['dl'],'NLP':['natural language processing'],'LLM':['large language model','large language models'],'RAG':['retrieval augmented generation'],'AWS':['amazon web services'],'GitHub':['github'],'C++':['c++']}

def skill_set(text):
    found=set()
    for names in SKILLS.values():
        for skill in names:
            for term in [skill]+ALIASES.get(skill,[]):
                if re.search(r'(?<![\w])'+re.escape(term)+r'(?![\w])',text,re.I):
                    found.add(skill);break
    return found

def sections(text):
    labels={'Education':['education','academic background'],'Experience':['experience','work history','internship'],'Projects':['projects','project experience'],'Skills':['skills','technical skills'],'Certifications':['certifications','certificates']}
    return {name:any(re.search(r'(?im)^\s*(?:'+ '|'.join(re.escape(x) for x in variants)+r')\s*[:\-]?\s*$',text) for _ in [0]) for name,variants in labels.items()}

def analyze(resume,job):
    if not resume.strip() or not job.strip():raise ValueError('Both resume and job description are required.')
    rs=skill_set(resume);js=skill_set(job)
    matched=sorted(rs & js);missing=sorted(js-rs)
    coverage=round(100*len(matched)/len(js)) if js else None
    sec=sections(resume)
    words=len(re.findall(r'\b\w+\b',resume))
    tips=[]
    for s in missing[:6]:tips.append(f'If you have genuine experience with {s}, add a specific, verifiable example. Otherwise, consider learning it.')
    for name,present in sec.items():
        if not present:tips.append(f'Consider adding a clearly labeled {name} section if relevant.')
    if not re.search(r'\b\d+(?:%|\+|\s+(?:users|hours|projects|records|ms))\b',resume,re.I):tips.append('Quantify achievements with truthful metrics where possible.')
    if words<80:tips.append('Your resume is brief; add relevant accomplishments and project outcomes.')
    if words>900:tips.append('Consider shortening the resume and prioritizing role-relevant experience.')
    if not js:tips.append('No recognized skills were found in the job description; skill coverage cannot be calculated.')
    return {'resume_skills':sorted(rs),'job_skills':sorted(js),'matched':matched,'missing':missing,'coverage':coverage,'sections':sec,'word_count':words,'suggestions':tips,'method':'Rule-based skill extraction and transparent keyword coverage; not a hiring prediction.'}
