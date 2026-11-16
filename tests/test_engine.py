import pytest
from engine import analyze,skill_set

def test_skills_and_aliases():
    assert {'Python','Scikit-learn','Machine Learning','C++'}<=skill_set('Python, sklearn, ML, C++')
def test_coverage():
    r=analyze('SKILLS\nPython SQL','We need Python, SQL and Docker')
    assert r['coverage']==67 and r['missing']==['Docker']
def test_no_skills():
    assert analyze('Hello world','Nice person')['coverage'] is None
def test_empty():
    with pytest.raises(ValueError):analyze('','Python')
def test_sections():
    assert analyze('EDUCATION\nUniversity\nSKILLS\nPython','Python')['sections']['Education']
