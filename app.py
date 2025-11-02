import streamlit as st
import random
from datetime import datetime, date

# ============================================
# 🎓 MATHCOPAIN v4 - MEMORY APPROCHE SIMPLE
# ✅ Sans time.sleep() - Juste état visuel
# ============================================

st.set_page_config(
    page_title="MathCopain 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css():
    st.markdown("""
    <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            margin: 5px 0;
        }
        .success-text { color: #0f8419; font-weight: bold; }
        .error-text { color: #d91e1a; font-weight: bold; }
        .info-text { color: #0051ba; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ============================================
# 🎮 GÉNÉRATEURS
# ============================================

def generer_addition(niveau):
    if niveau == "CE1":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
    elif niveau == "CE2":
        a = random.randint(10, 50)
        b = random.randint(10, 50)
    elif niveau == "CM1":
        a = random.randint(50, 100)
        b = random.randint(50, 100)
    else:
        a = random.randint(100, 200)
        b = random.randint(100, 200)
    return {'question': f"{a} + {b}", 'reponse': a + b}

def generer_soustraction(niveau):
    if niveau == "CE1":
        a = random.randint(10, 20)
        b = random.randint(1, 10)
    elif niveau == "CE2":
        a = random.randint(50, 100)
        b = random.randint(10, 50)
    elif niveau == "CM1":
        a = random.randint(100, 500)
        b = random.randint(50, 100)
    else:
        a = random.randint(500, 1000)
        b = random.randint(100, 500)
    return {'question': f"{a} - {b}", 'reponse': a - b}

def generer_tables(niveau):
    if niveau == "CE1":
        table = random.randint(2, 5)
        mult = random.randint(1, 10)
    elif niveau == "CE2":
        table = random.randint(2, 9)
        mult = random.randint(1, 10)
    elif niveau == "CM1":
        table = random.randint(1, 12)
        mult = random.randint(1, 12)
    else:
        table = random.randint(1, 15)
        mult = random.randint(1, 15)
    return {'question': f"{table} × {mult}", 'reponse': table * mult}

def generer_droite_numerique(niveau):
    if niveau == "CE1":
        max_val = 100
    elif niveau == "CE2":
        max_val = 1000
    elif niveau == "CM1":
        max_val = 10000
    else:
        max_val = 100000
    nombre = random.randint(0, max_val)
    return {'nombre': nombre, 'min': 0, 'max': max_val}

def calculer_score_droite(reponse, correct):
    distance = abs(reponse - correct)
    max_val = correct if correct > 0 else 100
    if distance <= max_val * 0.10:
        return 20, "Excellent ! (±10%)"
    elif distance <= max_val * 0.20:
        return 5, "Presque ! (±20%)"
    else:
        return 0, f"Trop loin (distance: {distance})"

def generer_memory_emoji(niveau):
    emojis = ['🍎', '🐶', '🎨', '🌟', '🎭', '🎸', '🚀', '🏆', '🎮', '🍕', '🐱', '⚽', '🎪', '🎯', '🌈', '🍦']
    if niveau == "CE1":
        paires = emojis[:4]
    elif niveau == "CE2":
        paires = emojis[:6]
    elif niveau == "CM1":
        paires = emojis[:8]
    else:
        paires = emojis[:10]
    cards = paires + paires
    random.shuffle(cards)
    return {
        'cards': cards,
        'revealed': set(),  # ✅ Utiliser SET au lieu de liste!
        'matched': set(),
    }

def generer_probleme(niveau):
    contextes = [
        ("Marie a {a} billes. Son ami lui en donne {b}.", "Combien a-t-elle ?", "addition"),
        ("Théo a {a} euros. Il achète quelque chose qui coûte {b} euros.", "Combien lui reste-t-il ?", "soustraction"),
        ("Il y a {a} rangées de {b} chaises.", "Combien de chaises en tout ?", "multiplication"),
        ("On partage {a} bonbons entre {b} enfants.", "Combien chacun a ?", "division"),
    ]
    contexte_base, question, operation = random.choice(contextes)
    
    if niveau == "CE1":
        a, b = random.randint(5, 20), random.randint(2, 10)
    elif niveau == "CE2":
        a, b = random.randint(20, 50), random.randint(5, 30)
    elif niveau == "CM1":
        a, b = random.randint(50, 200), random.randint(10, 50)
    else:
        a, b = random.randint(100, 500), random.randint(20, 100)
    
    contexte = contexte_base.format(a=a, b=b)
    
    if operation == "addition":
        reponse = a + b
    elif operation == "soustraction":
        if a < b:
            a, b = b, a
        reponse = a - b
    elif operation == "multiplication":
        reponse = a * b
    else:
        reponse = a // b if b > 0 else 0
    
    return {'question': f"{contexte} {question}", 'reponse': reponse}

# ============================================
# 🎁 SYSTÈMES
# ============================================

def calculer_progression(stats_par_niveau):
    progression = {}
    for niveau in ['CE1', 'CE2', 'CM1', 'CM2']:
        total = stats_par_niveau[niveau]['total']
        correct = stats_par_niveau[niveau]['correct']
        pourcentage = (correct / total * 100) if total > 0 else 0
        progression[niveau] = min(int(pourcentage), 100)
    return progression

def maj_streak(correct):
    if correct:
        st.session_state.streak['current'] += 1
        st.session_state.streak['max'] = max(st.session_state.streak['current'], st.session_state.streak['max'])
    else:
        st.session_state.streak['current'] = 0

def calculer_bonus_streak(streak):
    if streak >= 10:
        return 25
    elif streak >= 5:
        return 10
    elif streak >= 3:
        return 5
    return 0

def afficher_leaderboard():
    if not st.session_state.scores_history:
        st.info("Pas de scores encore. Lance-toi !")
        return
    
    st.markdown("### 🏆 Top 5 Scores")
    top_scores = sorted(st.session_state.scores_history, key=lambda x: x['points'], reverse=True)[:5]
    
    for i, score in enumerate(top_scores, 1):
        col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
        with col1:
            st.write(f"**#{i}**")
        with col2:
            st.write(f"{score['activite']} ({score['niveau']})")
        with col3:
            st.write(f"**{score['points']} pts**")
        with col4:
            st.write(f"{score['date'].strftime('%H:%M')}")

def verifier_badges():
    badges_config = {
        "🌟": (1, "Premier Pas"),
        "💪": (10, "Persévérant"),
        "🏆": (50, "Champion"),
        "👑": (100, "Expert"),
    }
    
    for emoji, (seuil, nom) in badges_config.items():
        if st.session_state.points >= seuil and emoji not in st.session_state.badges:
            st.session_state.badges.append(emoji)

# ============================================
# 📋 SECTIONS
# ============================================

def exercice_rapide_section():
    st.header("🧮 Exercice Rapide")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        activite = st.selectbox("Choisir activité:", ["Addition", "Soustraction", "Tables"])
    with col2:
        st.write(f"**Points:** {st.session_state.points}")
    with col3:
        st.write(f"**Streak:** 🔥 {st.session_state.streak['current']}")
    
    st.markdown("---")
    
    if activite == "Addition":
        exercice = generer_addition(st.session_state.niveau)
    elif activite == "Soustraction":
        exercice = generer_soustraction(st.session_state.niveau)
    else:
        exercice = generer_tables(st.session_state.niveau)
    
    st.markdown(f"### {exercice['question']}")
    
    col1, col2 = st.columns(2)
    with col1:
        reponse = st.number_input("Votre réponse:", value=0, step=1)
    with col2:
        if st.button("✓ Vérifier"):
            if reponse == exercice['reponse']:
                st.success("✅ Correct!")
                st.session_state.points += 10
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                maj_streak(True)
                bonus = calculer_bonus_streak(st.session_state.streak['current'])
                if bonus > 0:
                    st.session_state.points += bonus
                    st.info(f"🔥 Bonus Streak +{bonus} pts!")
                verifier_badges()
                st.session_state.scores_history.append({
                    'date': datetime.now(),
                    'points': 10 + bonus,
                    'activite': activite,
                    'niveau': st.session_state.niveau
                })
            else:
                st.error(f"❌ Incorrect. La bonne réponse est {exercice['reponse']}")
                maj_streak(False)
            st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
            st.rerun()

def jeu_section():
    st.header("🎮 Jeu")
    
    tab1, tab2 = st.tabs(["Memory Emojis", "Droite Numérique"])
    
    with tab1:
        st.subheader("🧠 Memory Emojis")
        
        if 'jeu_memory' not in st.session_state or st.button("🔄 Nouvelle Partie Memory"):
            st.session_state.jeu_memory = generer_memory_emoji(st.session_state.niveau)
            st.session_state.memory_first_flip = None
            st.session_state.memory_second_flip = None
        
        jeu = st.session_state.jeu_memory
        
        cols = st.columns(4)
        for i, card in enumerate(jeu['cards']):
            with cols[i % 4]:
                if i in jeu['matched']:
                    st.button(f"✅ {card}", disabled=True, key=f"matched_{i}")
                elif i in jeu['revealed']:
                    st.button(f"👀 {card}", key=f"reveal_{i}")
                else:
                    if st.button("❓", key=f"card_{i}"):
                        if st.session_state.memory_first_flip is None:
                            st.session_state.memory_first_flip = i
                        elif st.session_state.memory_second_flip is None:
                            st.session_state.memory_second_flip = i
                        st.rerun()
        
        if st.session_state.memory_first_flip is not None:
            jeu['revealed'].add(st.session_state.memory_first_flip)
        if st.session_state.memory_second_flip is not None:
            jeu['revealed'].add(st.session_state.memory_second_flip)
        
        if (st.session_state.memory_first_flip is not None and 
            st.session_state.memory_second_flip is not None):
            idx1, idx2 = st.session_state.memory_first_flip, st.session_state.memory_second_flip
            if jeu['cards'][idx1] == jeu['cards'][idx2]:
                jeu['matched'].add(idx1)
                jeu['matched'].add(idx2)
                st.session_state.points += 5
                st.success("✅ Paire trouvée!")
                verifier_badges()
                st.session_state.scores_history.append({
                    'date': datetime.now(),
                    'points': 5,
                    'activite': 'Memory',
                    'niveau': st.session_state.niveau
                })
                if len(jeu['matched']) == len(jeu['cards']):
                    st.balloons()
                    st.success("🎉 Jeu terminé!")
            else:
                st.error("❌ Différent, retent!")
            
            st.session_state.memory_first_flip = None
            st.session_state.memory_second_flip = None
    
    with tab2:
        st.subheader("📍 Droite Numérique")
        
        if 'droite_actuelle' not in st.session_state or st.button("🔄 Nouvelle Droite"):
            st.session_state.droite_actuelle = generer_droite_numerique(st.session_state.niveau)
        
        droite = st.session_state.droite_actuelle
        
        st.markdown(f"### Place le nombre **{droite['nombre']}** sur la droite")
        st.markdown(f"Min: **{droite['min']}** --- Max: **{droite['max']}**")
        
        reponse = st.slider("Votre réponse:", min_value=droite['min'], max_value=droite['max'], value=droite['max']//2)
        
        if st.button("✓ Vérifier"):
            score, message = calculer_score_droite(reponse, droite['nombre'])
            
            if score > 0:
                st.success(f"✅ {message}")
                st.session_state.points += score
                maj_streak(True)
                bonus = calculer_bonus_streak(st.session_state.streak['current'])
                if bonus > 0:
                    st.session_state.points += bonus
                    st.info(f"🔥 Bonus +{bonus}!")
                verifier_badges()
                st.session_state.scores_history.append({
                    'date': datetime.now(),
                    'points': score + bonus,
                    'activite': 'Droite',
                    'niveau': st.session_state.niveau
                })
            else:
                st.error(message)
                maj_streak(False)
            
            st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
            st.rerun()

def defi_section():
    st.header("🎯 Défi")
    
    if 'defi_date' not in st.session_state or st.session_state.defi_date != date.today():
        st.session_state.defi_probleme = generer_probleme(st.session_state.niveau)
        st.session_state.defi_date = date.today()
    
    st.markdown(f"### {st.session_state.defi_probleme['question']}")
    
    col1, col2 = st.columns(2)
    with col1:
        reponse = st.number_input("Votre réponse:", value=0, step=1, key="defi_input")
    with col2:
        if st.button("✓ Résoudre le Défi"):
            if reponse == st.session_state.defi_probleme['reponse']:
                st.success("✅ Bravo!")
                st.session_state.points += 20
                maj_streak(True)
                bonus = calculer_bonus_streak(st.session_state.streak['current'])
                if bonus > 0:
                    st.session_state.points += bonus
                    st.info(f"🔥 Bonus +{bonus}!")
                verifier_badges()
                st.session_state.scores_history.append({
                    'date': datetime.now(),
                    'points': 20 + bonus,
                    'activite': 'Défi',
                    'niveau': st.session_state.niveau
                })
            else:
                st.error(f"❌ Incorrect. La réponse est {st.session_state.defi_probleme['reponse']}")
                maj_streak(False)
            st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
            st.rerun()

def accueil_section():
    st.header("🎓 Bienvenue à MathCopain!")
    st.markdown("""
    Pratiquez les mathématiques de manière ludique:
    - 🧮 **Exercice Rapide**: Addition, Soustraction, Tables
    - 🎮 **Jeu**: Memory, Droite Numérique
    - 🎯 **Défi**: Problème quotidien
    
    Gagnez des points, débloquez des badges, et améliorez votre progression! 🚀
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Points", st.session_state.points)
    with col2:
        st.metric("Streak", f"🔥 {st.session_state.streak['current']}")
    with col3:
        st.metric("Max Streak", st.session_state.streak['max'])
    with col4:
        st.metric("Badges", f"{len(st.session_state.badges)}/4")
    
    st.markdown("---")
    st.markdown("### 🏆 Vos Badges")
    if st.session_state.badges:
        st.write(" ".join(st.session_state.badges))
    else:
        st.info("Pas de badges encore. Continue!")

# ============================================
# 🔧 SESSION STATE
# ============================================

def init_session_state():
    if 'niveau' not in st.session_state:
        st.session_state.niveau = "CE1"
    if 'points' not in st.session_state:
        st.session_state.points = 0
    if 'badges' not in st.session_state:
        st.session_state.badges = []
    if 'stats_par_niveau' not in st.session_state:
        st.session_state.stats_par_niveau = {
            'CE1': {'total': 0, 'correct': 0},
            'CE2': {'total': 0, 'correct': 0},
            'CM1': {'total': 0, 'correct': 0},
            'CM2': {'total': 0, 'correct': 0},
        }
    if 'streak' not in st.session_state:
        st.session_state.streak = {'current': 0, 'max': 0}
    if 'scores_history' not in st.session_state:
        st.session_state.scores_history = []
    if 'jeu_memory' not in st.session_state:
        st.session_state.jeu_memory = None
    if 'memory_first_flip' not in st.session_state:
        st.session_state.memory_first_flip = None
    if 'memory_second_flip' not in st.session_state:
        st.session_state.memory_second_flip = None
    if 'defi_probleme' not in st.session_state:
        st.session_state.defi_probleme = generer_probleme("CE1")
    if 'defi_date' not in st.session_state:
        st.session_state.defi_date = date.today()

init_session_state()

# ============================================
# 🎯 MAIN APP
# ============================================

st.sidebar.title("🎓 MathCopain")
st.sidebar.write(f"**Niveau:** {st.session_state.niveau}")

st.session_state.niveau = st.sidebar.selectbox(
    "Changer de niveau:",
    ["CE1", "CE2", "CM1", "CM2"]
)

progression = calculer_progression(st.session_state.stats_par_niveau)
for niveau, pct in progression.items():
    st.sidebar.progress(pct / 100, text=f"{niveau}: {pct}%")

st.sidebar.markdown("---")

selected = st.sidebar.radio(
    "🎮 Activités",
    ["🏠 Accueil", "🧮 Exercice Rapide", "🎮 Jeu", "🎯 Défi", "🏆 Leaderboard"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"📊 **Points:** {st.session_state.points}")
st.sidebar.markdown(f"🔥 **Streak:** {st.session_state.streak['current']}")

if selected == "🏠 Accueil":
    accueil_section()
elif selected == "🧮 Exercice Rapide":
    exercice_rapide_section()
elif selected == "🎮 Jeu":
    jeu_section()
elif selected == "🎯 Défi":
    defi_section()
elif selected == "🏆 Leaderboard":
    afficher_leaderboard()