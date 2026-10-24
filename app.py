from pathlib import Path
from datetime import date
import base64
import streamlit as st

st.set_page_config(
    page_title='Ebb — Find your own flow',
    page_icon='🌊',
    layout='wide',
    initial_sidebar_state='expanded'
)

logo = Path(__file__).resolve().parent / "ebb-logo.svg"
logo_data = base64.b64encode(logo.read_bytes()).decode("ascii")

# Ebb background
background = Path(__file__).resolve().parent / "ebb-background.png"
if background.exists():
    background_data = base64.b64encode(background.read_bytes()).decode("ascii")

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{background_data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
html,body,[class*="css"],button,input,textarea {font-family:'Poppins',sans-serif!important}
.stApp {background:#FFFFFF;color:#354A40}
[data-testid="stHeader"] {background:transparent}
[data-testid="stSidebar"] {background:#FBFCFC;border-right:1px solid #E9F1EF}
.block-container {max-width:1380px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3,p,label {color:#354A40!important;font-family:'Poppins',sans-serif!important}
h1,h2,h3 {font-weight:500!important;letter-spacing:-.035em}
h1 {font-size:2.3rem!important}
[data-testid="stMetric"] {background:#FFFFFF;border:1px solid #E9EFED;border-radius:20px;padding:15px 20px}
[data-testid="stMetricValue"] {font-size:1.6rem;color:#354A40}
[data-testid="stVerticalBlockBorderWrapper"]>div {border-radius:22px!important;border-color:#E9EFED!important}
.stButton>button {border-radius:12px!important;border:1px solid #DDEAE6!important;color:#354A40!important}
.stButton>button[kind="primary"] {background:#D7EEE9!important;border:none!important}
.stButton>button:hover {background:#F8E8F2!important;border-color:#EBC5DF!important}
[data-testid="stProgressBar"]>div>div {background:#CFA1C5!important}
.hero {padding:32px 36px;border-radius:26px;background:linear-gradient(105deg,#E2F4F0,#FFFFFF 63%,#F9EAF3);margin-bottom:22px}
.hero h1 {margin:7px 0!important;font-size:2.65rem!important}
.hero p {color:#72867F!important;max-width:680px}
.eyebrow {font-size:.7rem;letter-spacing:.15em;color:#71948A;text-transform:uppercase}
.brand {display:flex;align-items:center;gap:11px;margin:8px 0 22px}
.brand-name {font-size:1.55rem;color:#354A40}
.brand-tag {font-size:.7rem;color:#789088}
.soft-card {background:#F8EAF3;border-radius:20px;padding:18px 22px;color:#354A40}
.section {font-size:1.12rem;font-weight:500;color:#354A40;margin:8px 0 10px}
.muted {color:#80938C;font-size:.85rem}
/* Redesign: improved navigation contrast */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapsedControl"] button {
    color: #354A40 !important;
    background-color: #D7EEE9 !important;
    border-radius: 10px !important;
}

[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg {
    color: #354A40 !important;
    stroke: #354A40 !important;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }
}
/* Today's focus text area */
.stTextArea textarea {
    color: #F5F5F5 !important;
    -webkit-text-fill-color: #F5F5F5 !important;
    caret-color: #FFFFFF !important;
}

.stTextArea textarea::placeholder {
    color: #BFC8C3 !important;
    -webkit-text-fill-color: #BFC8C3 !important;
}

</style>''', unsafe_allow_html=True)

if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {'title':'Check emails','done':True},
        {'title':'Work on design project','done':False},
        {'title':'Plan the rest of the week','done':False},
    ]
if 'energy' not in st.session_state: st.session_state.energy = 3
if 'focus' not in st.session_state: st.session_state.focus = 'Finish my design and make time to unwind.'
if 'breaks' not in st.session_state: st.session_state.breaks = {}

break_options = ['Take a short walk', 'Hydrate', 'Take a break', 'Get some fresh air']

def task_list():
    if not st.session_state.tasks:
        st.caption('Nothing on your list yet. Add your first task below.')
    for idx, task in enumerate(st.session_state.tasks):
        a,b = st.columns([9,1],vertical_alignment='center')
        checked = a.checkbox(task['title'], value=task['done'], key=f'task_check_{idx}')
        if checked != task['done']:
            st.session_state.tasks[idx]['done'] = checked
            st.rerun()
        if b.button('×',key=f'delete_{idx}',help='Remove task'):
            st.session_state.tasks.pop(idx)
            st.rerun()
    with st.form('new_task',clear_on_submit=True):
        name, submit = st.columns([4,1],vertical_alignment='bottom')
        title = name.text_input('New task',placeholder='What would you like to do?')
        add = submit.form_submit_button('＋ Add',type='primary',use_container_width=True)
        if add and title.strip():
            st.session_state.tasks.append({'title':title.strip(),'done':False})
            st.rerun()

def break_checklist():
    st.caption('Small breaks make a big difference. Choose what works for you.')
    a,b = st.columns(2)
    for i, option in enumerate(break_options):
        with (a if i % 2 == 0 else b):
            st.checkbox(option,key=f'break_{i}')

with st.sidebar:
    st.markdown(f'<div class="brand"><img src="data:image/svg+xml;base64,{logo_data}" width="70"><div><div class="brand-name">Ebb</div><div class="brand-tag">Find your own flow.</div></div></div>',unsafe_allow_html=True)

    page = st.radio(
        'Navigation',
        [
            'My Day',
            'My Tasks',
            'My Schedule',
            'My Energy',
            'My Breaks'
        ],
        label_visibility='collapsed'
    )
    st.divider()
    st.markdown('<div class="soft-card">🌸 Your pace is personal.<br>Make room for what matters.</div>',unsafe_allow_html=True)

if page == 'My Day':
    st.markdown(f'<div class="eyebrow">{date.today().strftime("%A, %d %B")}</div>',unsafe_allow_html=True)
    st.markdown('<div class="hero"><span class="eyebrow">YOUR PERSONAL SPACE</span><h1>Let’s find your flow.</h1><p>A little more balance, a little less pressure.<br>Make room for what matters to you.</p></div>',unsafe_allow_html=True)
    tasks = st.session_state.tasks
    completed = sum(t['done'] for t in tasks)
    m1,m2,m3 = st.columns(3)
    m1.metric('Tasks today',len(tasks))
    m2.metric('Tasks completed',completed)
    m3.metric('Energy level',f'{st.session_state.energy}/5')
    st.write('')
    left,right = st.columns([1.1,1],gap='large')
    with left:
        with st.container(border=True):
            st.subheader('🌿 Today’s focus')
            st.caption('What would make today feel like a good day?')
            st.text_area('My focus',key='focus',label_visibility='collapsed',height=100)
        with st.container(border=True):
            st.subheader('💗 My energy')
            st.caption('How do you feel right now?')
            st.slider('Energy level',1,5,key='energy')
            levels = {1:'Take it gently today.',2:'A slower pace might help.',3:'Feeling steady.',4:'You have some energy to spare.',5:'Feeling energised!'}
            st.caption(levels[st.session_state.energy])
    with right:
        with st.container(border=True):
            st.subheader('✓ To do:')
            task_list()
        with st.container(border=True):
            st.subheader('☕ Break reminder')
            break_checklist()
    st.markdown('<div class="soft-card" style="text-align:center;margin-top:12px">“A balanced day is still a productive day.”</div>',unsafe_allow_html=True)

elif page == 'My Tasks':
    st.markdown(
        '<div class="hero"><span class="eyebrow">MAKE SPACE FOR WHAT MATTERS</span>'
        '<h1>My Tasks</h1>'
        '<p>A simple place for your tasks. Add what matters and tick things off at your own pace.</p></div>',
        unsafe_allow_html=True
    )
    with st.container(border=True):
        task_list()
    st.caption('Your tasks stay available while this app session is active.')

    
elif page == 'My Schedule':
    st.markdown(
        '<div class="hero"><span class="eyebrow">PLAN YOUR TIME</span>'
        '<h1>My Schedule</h1>'
        '<p>A calm space for meetings, appointments and plans.</p></div>',
        unsafe_allow_html=True
    )
    with st.container(border=True):
        st.subheader('📅 Your schedule')
        st.write('Your meetings and appointments will appear here soon.')

elif page == 'My Energy':
    st.markdown(
        '<div class="hero"><span class="eyebrow">LISTEN TO YOURSELF</span>'
        '<h1>My Energy</h1>'
        '<p>Understand your energy and find a pace that works for you.</p></div>',
        unsafe_allow_html=True
    )
    with st.container(border=True):
        st.subheader('💗 How are you feeling?')
        st.slider('Energy level', 1, 5, key='energy_page')
        st.caption('Your energy matters just as much as your productivity.')

elif page == 'My Breaks':
    st.markdown(
        '<div class="hero"><span class="eyebrow">A MOMENT FOR YOURSELF</span>'
        '<h1>My Breaks</h1>'
        '<p>Rest is part of your day, not something you need to earn.</p></div>',
        unsafe_allow_html=True
    )
    with st.container(border=True):
        break_checklist()
    st.info('These are optional suggestions, not scheduled device notifications.')
