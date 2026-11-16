"""SkillBridge AI: a privacy-conscious explainable resume-analysis prototype."""
import json
import streamlit as st
from engine import SKILLS
from modules.matcher import analyze_hybrid
from modules.parser import parse_pdf
from modules.counterfactual import rank_actions
from advanced import mask_pii, simulate, dependencies

st.set_page_config(page_title='SkillBridge AI | FMH CodeSprint', page_icon='🧠', layout='wide')
st.markdown('''<style>
.block-container{padding-top:1.8rem;max-width:1220px}
.hero{padding:36px;border-radius:22px;background:linear-gradient(115deg,#101b40 0%,#34286c 65%,#6845a7 100%);color:white;box-shadow:0 14px 34px rgba(55,47,115,.16)}
.hero h1{font-size:2.7rem;color:#fff;margin:0}.hero p{color:#dce5ff;font-size:1.06rem;margin:.7rem 0 0}
.pill{display:inline-block;border:1px solid #b6a7ff;border-radius:100px;padding:5px 12px;color:#d9d1ff;font-size:.8rem;margin-bottom:12px}
[data-testid="stMetric"]{background:rgba(116,98,196,.08);border:1px solid rgba(116,98,196,.15);border-radius:16px;padding:16px}
</style>''', unsafe_allow_html=True)
st.markdown('<div class="hero"><span class="pill">FMH CODESPRINT 2026 · PS-04</span><h1>🧠 SkillBridge AI</h1><p>See the evidence. Understand the gap. Simulate your next skill.</p></div>', unsafe_allow_html=True)
st.caption('Privacy-first prototype · Explainable skill coverage · Not an ATS certification or hiring prediction')
with st.sidebar:
    st.header('✦ Project guide')
    st.markdown('**01** Upload or paste your resume\n\n**02** Paste a target job description\n\n**03** Explore your analysis and what-if scenarios')
    st.info('The score is recognized job-skill coverage. It is not a hiring probability.')
    st.caption('Built for the official PS-04 AI Resume Analyzer challenge.')

input_tab, match_tab, future_tab = st.tabs(['📄 ATS X-Ray & Blind Audit', '📊 Explainable Match', '🚀 Upskilling Simulator'])
with input_tab:
    st.subheader('Resume & job inputs')
    left, right = st.columns(2, gap='large')
    with left:
        upload = st.file_uploader('Resume: PDF or TXT (max 5 MB)', type=['pdf','txt'])
        uploaded_text = ''
        if upload:
            if upload.size > 5*1024*1024:
                st.error('File exceeds the 5 MB limit.')
            else:
                try:
                    if upload.name.lower().endswith('.pdf'):
                        uploaded_text, pdf_warnings = parse_pdf(upload.getvalue())
                        for warning in pdf_warnings: st.warning(warning)
                    else:
                        uploaded_text = upload.getvalue().decode('utf-8')
                    if not uploaded_text.strip():
                        st.warning('No extractable text. Scanned PDFs are not supported; paste text instead.')
                except Exception:
                    st.error('Could not read this file. Try a text-based PDF or TXT.')
        resume = st.text_area('Resume text', value=uploaded_text, height=280, placeholder='EDUCATION\n...\nSKILLS\nPython, SQL...\nPROJECTS\n...')
    with right:
        job = st.text_area('Target job description', height=280, placeholder='Seeking AI/ML intern with Python, Machine Learning, Git, Docker...')
        st.caption('For a quick demonstration, copy text from samples/resume.txt and samples/job.txt in the repository.')
    if resume.strip():
        with st.expander('🔒 Privacy preview — best-effort masked text'):
            st.code(mask_pii(resume)[:6000], language=None)
            st.caption('Emails, phone-like strings and URLs are masked. Names and other identifiers may remain; review before sharing.')
    if st.button('✨ Analyze resume', type='primary', use_container_width=True):
        try:
            st.session_state['report'] = analyze_hybrid(resume, job, use_semantic=semantic)
            st.success('Analysis ready! Open the Explainable Match and Upskilling Simulator tabs.')
        except ValueError as exc:
            st.error(str(exc))

report = st.session_state.get('report')
with match_tab:
    if report is None:
        st.info('Enter your resume and job description in the first tab, then click Analyze resume.')
    else:
        st.subheader('Transparent role alignment')
        a,b,c,d = st.columns(4)
        a.metric('Skill coverage', 'N/A' if report['coverage'] is None else f"{report['coverage']}%")
        b.metric('Matched skills', len(report['matched']))
        c.metric('Missing skills', len(report['missing']))
        d.metric('Resume words', report['word_count'])
        if report['coverage'] is not None:
            st.progress(report['coverage']/100)
        st.caption('Score = (number of recognized job skills found in resume ÷ recognized job skills) × 100. Equal weighting; not a hiring prediction.')
        col1,col2=st.columns(2)
        with col1:
            st.success('**Matched**: ' + (', '.join(report['matched']) or 'None identified'))
        with col2:
            st.warning('**Missing**: ' + (', '.join(report['missing']) or 'None identified'))
        if report.get('semantic_similarity') is not None:
            st.metric('Optional MiniLM semantic similarity', f"{report['semantic_similarity']}%")
            st.caption('Semantic similarity is a separate contextual indicator, not combined with the skill-coverage score.')
        st.markdown('#### Resume structure audit')
        st.write(' · '.join(('✅ ' if ok else '⚪ ') + name for name,ok in report['sections'].items()))
        st.markdown('#### Actionable improvements')
        for i, suggestion in enumerate(report['suggestions']):
            st.checkbox(suggestion, key=f'check_{i}')
        st.download_button('⬇️ Export analysis (JSON)', json.dumps(report, indent=2), 'skillbridge-analysis.json', 'application/json')
with future_tab:
    if report is None:
        st.info('Analyze a resume in the first tab to enable the simulator.')
    else:
        st.subheader('What if you developed these skills?')
        st.caption('This is a hypothetical skill-coverage calculation. Toggling a skill does not prove competence or predict employment.')
        selected = st.multiselect('Simulate acquiring missing skills', report['missing'], default=[])
        new_score, gain = simulate(report, selected)
        x,y,z = st.columns(3)
        x.metric('Current coverage', 'N/A' if report['coverage'] is None else f"{report['coverage']}%")
        y.metric('Simulated coverage', 'N/A' if new_score is None else f'{new_score}%')
        z.metric('Change', f'+{gain} percentage points')
        st.markdown('#### Counterfactual action ranking')
        st.dataframe(rank_actions(report), use_container_width=True, hide_index=True)
        st.markdown('#### Curated competency dependencies')
        edges = dependencies(report['missing'])
        if edges:
            try:
                import networkx as nx
                import plotly.graph_objects as go
                graph = nx.DiGraph(); graph.add_edges_from(edges)
                pos = nx.spring_layout(graph, seed=42)
                edge_x=[];edge_y=[]
                for u,v in graph.edges():
                    edge_x += [pos[u][0],pos[v][0],None]
                    edge_y += [pos[u][1],pos[v][1],None]
                fig=go.Figure()
                fig.add_trace(go.Scatter(x=edge_x,y=edge_y,mode='lines',line=dict(color='#9991c8',width=2),hoverinfo='skip'))
                fig.add_trace(go.Scatter(x=[pos[n][0] for n in graph.nodes()],y=[pos[n][1] for n in graph.nodes()],mode='markers+text',text=list(graph.nodes()),textposition='top center',marker=dict(size=19,color=['#7b61d8' if n in report['missing'] else '#39a9b5' for n in graph.nodes()]),hoverinfo='text'))
                fig.update_layout(height=420,showlegend=False,margin=dict(l=10,r=10,t=35,b=10),xaxis=dict(visible=False),yaxis=dict(visible=False),title='Arrows indicate suggested foundational dependencies')
                st.plotly_chart(fig, use_container_width=True)
            except ImportError:
                st.write('Suggested prerequisite → target skill:')
                for src,dst in edges: st.write(f'• {src} → {dst}')
        else:
            st.info('No curated dependencies for the currently missing skills.')
        if selected:
            st.markdown('#### Suggested portfolio challenge')
            st.write('Build one small project that genuinely demonstrates ' + ', '.join(selected) + '. Document your implementation, tests and measured outcomes before claiming these skills on a resume.')
        st.caption('Dependency edges are educational suggestions, not universal prerequisites. Skill coverage remains the scored metric; optional MiniLM similarity is displayed separately when enabled.')
