from advanced import mask_pii, simulate, dependencies

def test_mask():
    output = mask_pii('email jane@example.com website https://example.com')
    assert 'jane@example.com' not in output
    assert 'https://example.com' not in output

def test_simulator_consistency():
    report={'job_skills':['Python','Docker','Git'],'resume_skills':['Python'],'missing':['Docker','Git']}
    assert simulate(report, ['Docker']) == (66.7,33.3)
    assert simulate(report, ['Docker','Git']) == (100.0,66.7)

def test_dependency_graph():
    assert ('Linux','Docker') in dependencies(['Docker'])
