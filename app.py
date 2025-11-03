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
    .categorie-header {
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0 10px 0;
        padding: 10px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
    .exercice-box {
        padding: 30px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 20px 0;
        border-left: 5px solid #667eea;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
    }
    .badge {
        display: inline-block;
        padding: 8px 12px;
        margin: 5px;
        border-radius: 15px;
        background-color: #FFD700;
        font-weight: bold;
        font-size: 14px;
    }
    .feedback-success {
        padding: 15px;
        border-radius: 10px;
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
        margin: 15px 0;
        font-weight: bold;
        font-size: 18px;
    }
    .feedback-error {
        padding: 15px;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
        margin: 15px 0;
        font-weight: bold;
        font-size: 18px;
    }
    .streak-box {
        padding: 15px;
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin: 10px 0;
    }
    .daily-challenge-box {
        padding: 15px;
        background-color: #e7f3ff;
        border: 2px solid #2196f3;
        border-radius: 10px;
        margin: 10px 0;
    }
    .leaderboard-box {
        padding: 15px;
        background-color: #f3e5f5;
        border: 2px solid #9c27b0;
        border-radius: 10px;
        margin: 10px 0;
    }
    .aller-loin-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #fff5f0;
        margin: 10px 0;
        border-left: 5px solid #ff6b6b;
    }
    </style>
    """, unsafe_allow_html=True)

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
    emojis = ['🍎', '🐶', '🎨', '🌟', '🎭', '🎸', '🚀', '🏆', 
              '🎮', '🍕', '🐱', '⚽', '🎪', '🎯', '🌈', '🍦']
    
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
    
    st.markdown('<div class="leaderboard-box">', unsafe_allow_html=True)
    st.write("### 🏆 MES TOP SCORES")
    
    top_scores = sorted(st.session_state.scores_history, key=lambda x: x['points'], reverse=True)[:5]
    
    for idx, score in enumerate(top_scores, 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        st.write(f"{medal} **{score['points']} pts** - {score['type']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def generer_daily_challenge():
    today = str(date.today())
    if st.session_state.daily_challenge.get('today_date') != today:
        random.seed(today)
        challenges = [
            {'type': 'addition', 'objectif': 5, 'text': 'Enchaîne 5 bonnes réponses en Addition'},
            {'type': 'soustraction', 'objectif': 5, 'text': 'Enchaîne 5 bonnes réponses en Soustraction'},
            {'type': 'tables', 'objectif': 5, 'text': 'Enchaîne 5 bonnes réponses aux Tables'},
            {'type': 'droite', 'objectif': 3, 'text': 'Fais 3 bonnes estimations à la Droite'},
        ]
        challenge = random.choice(challenges)
        st.session_state.daily_challenge = {
            'today_date': today,
            'completed': False,
            'challenge': challenge,
            'progress': 0
        }

def verifier_badges(points, badges_actuels):
    badges_disponibles = {
        'premier_pas': {'seuil': 1, 'nom': '🌟 Premier Pas'},
        'persistant': {'seuil': 10, 'nom': '💪 Persévérant'},
        'champion': {'seuil': 50, 'nom': '🏆 Champion'},
        'expert': {'seuil': 100, 'nom': '👑 Expert'},
    }
    
    nouveaux_badges = []
    for key, badge in badges_disponibles.items():
        if points >= badge['seuil'] and badge['nom'] not in badges_actuels:
            nouveaux_badges.append(badge['nom'])
    return nouveaux_badges

# ============================================
# ⚙️ SESSION
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
            'CE1': {'correct': 0, 'total': 0},
            'CE2': {'correct': 0, 'total': 0},
            'CM1': {'correct': 0, 'total': 0},
            'CM2': {'correct': 0, 'total': 0}
        }
    if 'streak' not in st.session_state:
        st.session_state.streak = {'current': 0, 'max': 0}
    if 'scores_history' not in st.session_state:
        st.session_state.scores_history = []
    if 'daily_challenge' not in st.session_state:
        st.session_state.daily_challenge = {'today_date': str(date.today()), 'completed': False, 'challenge': None, 'progress': 0}
    if 'exercice_courant' not in st.session_state:
        st.session_state.exercice_courant = None
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    if 'feedback_correct' not in st.session_state:
        st.session_state.feedback_correct = False
    if 'feedback_reponse' not in st.session_state:
        st.session_state.feedback_reponse = None
    if 'dernier_exercice' not in st.session_state:
        st.session_state.dernier_exercice = None
    if 'jeu_memory' not in st.session_state:
        st.session_state.jeu_memory = None
    if 'memory_first_flip' not in st.session_state:
        st.session_state.memory_first_flip = None
    if 'memory_second_flip' not in st.session_state:
        st.session_state.memory_second_flip = None
    if 'memory_incorrect_pair' not in st.session_state:
        st.session_state.memory_incorrect_pair = None
    
    # ✅ CORRECTION: Initialiser la catégorie active pour éviter l'erreur au démarrage
    if 'active_category' not in st.session_state:
        st.session_state.active_category = "📚 Exercice Rapide"

# ============================================
# 🎯 EXERCICE RAPIDE
# ============================================

def exercice_rapide_section():
    st.markdown('<div class="categorie-header">📚 Exercice Rapide - Calcul Mental</div>', unsafe_allow_html=True)
    st.write("⚡ Sois rapide et précis !")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Addition", key="btn_add", use_container_width=True):
            st.session_state.exercice_courant = generer_addition(st.session_state.niveau)
            st.session_state.show_feedback = False
            st.rerun()
    
    with col2:
        if st.button("➖ Soustraction", key="btn_sub", use_container_width=True):
            st.session_state.exercice_courant = generer_soustraction(st.session_state.niveau)
            st.session_state.show_feedback = False
            st.rerun()
    
    with col3:
        if st.button("🔢 Tables", key="btn_mult", use_container_width=True):
            st.session_state.exercice_courant = generer_tables(st.session_state.niveau)
            st.session_state.show_feedback = False
            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.exercice_courant:
        ex = st.session_state.exercice_courant
        st.markdown(f'<div class="exercice-box">{ex["question"]} = ?</div>', unsafe_allow_html=True)
        
        if not st.session_state.show_feedback:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Réponse :", key="input_ex", value=0, step=1)
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Valider", use_container_width=True, key="btn_val_ex"):
                    correct = reponse == ex['reponse']
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                        st.session_state.points += 10
                    maj_streak(correct)
                    bonus = calculer_bonus_streak(st.session_state.streak['current'])
                    if correct and bonus > 0:
                        st.session_state.points += bonus
                    st.session_state.feedback_correct = correct
                    st.session_state.feedback_reponse = reponse
                    st.session_state.dernier_exercice = ex
                    st.session_state.show_feedback = True
                    st.session_state.scores_history.append({'type': 'Calcul Mental', 'points': 10 + bonus, 'date': str(date.today())})
                    nouveaux = verifier_badges(st.session_state.points, st.session_state.badges)
                    st.session_state.badges.extend(nouveaux)
                    st.rerun()
        
        if st.session_state.show_feedback and st.session_state.dernier_exercice:
            st.markdown("---")
            if st.session_state.feedback_correct:
                bonus = calculer_bonus_streak(st.session_state.streak['current'])
                bonus_text = f" +{bonus} bonus!" if bonus > 0 else ""
                st.markdown(f'<div class="feedback-success">🎉 BRAVO !{bonus_text}</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Mauvais ! La réponse était {st.session_state.dernier_exercice["reponse"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Ton choix :** {st.session_state.feedback_reponse}")
                st.write(f"**Réponse :** {st.session_state.dernier_exercice['reponse']}")
            with col2:
                if st.button("➡️ SUIVANT", use_container_width=True, key="btn_next"):
                    if "+" in st.session_state.dernier_exercice.get('question', ''):
                        st.session_state.exercice_courant = generer_addition(st.session_state.niveau)
                    elif "-" in st.session_state.dernier_exercice.get('question', ''):
                        st.session_state.exercice_courant = generer_soustraction(st.session_state.niveau)
                    else:
                        st.session_state.exercice_courant = generer_tables(st.session_state.niveau)
                    st.session_state.show_feedback = False
                    st.rerun()

# ============================================
# 🎮 JEUX
# ============================================

def jeu_section():
    st.markdown('<div class="categorie-header">🎮 Jeux</div>', unsafe_allow_html=True)
    st.write("Sélectionne un jeu !")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Droite Numérique", use_container_width=True, key="btn_droite"):
            st.session_state.jeu_type = 'droite'
            st.session_state.exercice_courant = generer_droite_numerique(st.session_state.niveau)
            st.session_state.show_feedback = False
            st.rerun()
    
    with col2:
        if st.button("🧠 Memory", use_container_width=True, key="btn_memory"):
            st.session_state.jeu_type = 'memory'
            st.session_state.jeu_memory = generer_memory_emoji(st.session_state.niveau)
            st.session_state.memory_first_flip = None
            st.session_state.memory_second_flip = None
            st.rerun()
    
    st.markdown("---")
    
    # DROITE
    if st.session_state.get('jeu_type') == 'droite' and st.session_state.exercice_courant:
        dn = st.session_state.exercice_courant
        
        st.subheader(f"📍 Place le nombre {dn['nombre']} sur la droite")
        st.write(f"*De {dn['min']} à {dn['max']}*")
        
        if not st.session_state.show_feedback:
            st.write("⬇️ Déplace le curseur :")
            reponse = st.slider("Position", min_value=dn['min'], max_value=dn['max'], value=dn['max']//2, key="slider_dn", label_visibility="collapsed")
            
            if st.button("✅ Valider", use_container_width=True, key="btn_val_droite"):
                score, message = calculer_score_droite(reponse, dn['nombre'])
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                if score > 0:
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    st.session_state.points += score
                maj_streak(score > 0)
                bonus = calculer_bonus_streak(st.session_state.streak['current'])
                if score > 0 and bonus > 0:
                    st.session_state.points += bonus
                st.session_state.feedback_correct = score >= 20
                st.session_state.feedback_reponse = reponse
                st.session_state.dernier_exercice = {'nombre': dn['nombre'], 'message': message, 'score': score}
                st.session_state.show_feedback = True
                st.session_state.scores_history.append({'type': 'Droite Numérique', 'points': score + bonus, 'date': str(date.today())})
                nouveaux = verifier_badges(st.session_state.points, st.session_state.badges)
                st.session_state.badges.extend(nouveaux)
                st.rerun()
        
        if st.session_state.show_feedback and st.session_state.dernier_exercice:
            st.markdown("---")
            st.info(f"🎯 Tu as placé : **{st.session_state.feedback_reponse}**")
            
            if st.session_state.dernier_exercice.get('score', 0) >= 20:
                st.markdown(f'<div class="feedback-success">🎉 EXCELLENT ! {st.session_state.dernier_exercice.get("message", "")}</div>', unsafe_allow_html=True)
                st.balloons()
            elif st.session_state.dernier_exercice.get('score', 0) > 0:
                st.markdown(f'<div class="feedback-success">👍 Pas mal ! {st.session_state.dernier_exercice.get("message", "")}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="feedback-error">❌ {st.session_state.dernier_exercice.get("message", "")}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Ton placement :** {st.session_state.feedback_reponse}")
                st.write(f"**Distance :** {abs(st.session_state.feedback_reponse - st.session_state.dernier_exercice['nombre'])} unités")
            with col2:
                if st.button("➡️ SUIVANT", use_container_width=True, key="btn_next_droite"):
                    st.session_state.exercice_courant = generer_droite_numerique(st.session_state.niveau)
                    st.session_state.show_feedback = False
                    st.rerun()
    
    # ===== MEMORY SIMPLE =====
    elif st.session_state.get('jeu_type') == 'memory' and st.session_state.jeu_memory:
        st.subheader("🧠 Memory - Trouve les paires !")
        
        memory = st.session_state.jeu_memory
        total_pairs = len(memory['cards']) // 2
        pairs_found = len(memory['matched']) // 2
        
        st.write(f"Paires trouvées : **{pairs_found}/{total_pairs}**")
        st.progress(pairs_found / total_pairs)
        
        # ✅ CORRECTION SANS TIME.SLEEP :
        # Si une paire incorrecte a été retournée au tour précédent,
        # on la cache maintenant, avant de traiter le nouveau clic.
        if st.session_state.memory_incorrect_pair:
            memory['revealed'].difference_update(st.session_state.memory_incorrect_pair)
            st.session_state.memory_incorrect_pair = None
        
        # ✅ KEY: Affichage SIMPLE
        cols = st.columns(4)
        for idx in range(len(memory['cards'])):
            col = cols[idx % 4]
            
            with col:
                card_value = memory['cards'][idx]
                
                # Vérifier état de la carte
                if idx in memory['matched']:
                    # ✅ Paire trouvée
                    st.markdown(f"<div style='aspect-ratio: 1; background: linear-gradient(135deg, #90EE90 0%, #28a745 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 40px; border: 2px solid #28a745;'>{card_value}</div>", unsafe_allow_html=True)
                    st.button("✓", key=f"mem_{idx}_matched", disabled=True, use_container_width=True)
                
                elif idx in memory['revealed']:
                    # Carte révélée - afficher l'emoji
                    st.markdown(f"<div style='aspect-ratio: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 40px; border: 2px solid #667eea; color: white;'>{card_value}</div>", unsafe_allow_html=True)
                    st.button("✓", key=f"mem_{idx}_revealed", disabled=True, use_container_width=True)
                
                else:
                    # Carte cachée - cliquable
                    if st.button("?", key=f"mem_{idx}", use_container_width=True):
                        
                        # Premier clic
                        if st.session_state.memory_first_flip is None:
                            st.session_state.memory_first_flip = idx
                            memory['revealed'].add(idx)
                            st.rerun()
                        
                        # Deuxième clic
                        elif st.session_state.memory_second_flip is None and idx != st.session_state.memory_first_flip:
                            st.session_state.memory_second_flip = idx
                            memory['revealed'].add(idx)
                            st.rerun()
        
        # ===== VÉRIFIER PAIRE (après affichage) =====
        if st.session_state.memory_first_flip is not None and st.session_state.memory_second_flip is not None:
            first_idx = st.session_state.memory_first_flip
            second_idx = st.session_state.memory_second_flip
            
            if memory['cards'][first_idx] == memory['cards'][second_idx]:
                # ✅ PAIRE!
                memory['matched'].add(first_idx)
                memory['matched'].add(second_idx)
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.points += 5
                st.success("🎉 Paire trouvée!")
            else:
                # ❌ PAS PAIRE
                st.info("⏳ Pas une paire... reversal...")
                import time
                time.sleep(1.5)
                memory['revealed'].remove(first_idx)
                memory['revealed'].remove(second_idx)
            
            st.session_state.memory_first_flip = None
            st.session_state.memory_second_flip = None
            st.rerun()
        
        # ===== FIN DE JEU =====
        if len(memory['matched']) == len(memory['cards']):
            st.markdown("---")
            st.markdown(f'<div class="feedback-success">🎉 BRAVO ! Tu as trouvé toutes les paires !</div>', unsafe_allow_html=True)
            st.balloons()
            st.session_state.points += 50
            st.session_state.scores_history.append({'type': 'Memory', 'points': 50, 'date': str(date.today())})
            
            if st.button("➡️ Nouvelle partie", use_container_width=True, key="btn_new_memory"):
                st.session_state.jeu_memory = generer_memory_emoji(st.session_state.niveau)
                st.session_state.memory_first_flip = None
                st.session_state.memory_second_flip = None
                st.rerun()

# ============================================
# 🚀 DÉFI
# ============================================

def defi_section():
    st.markdown('<div class="categorie-header">🚀 Défi - Problèmes Contextualisés</div>', unsafe_allow_html=True)
    st.write("💡 Résous des problèmes du monde réel.")
    
    if st.button("🚀 Commencer Défi", use_container_width=True, key="btn_start_defi"):
        st.session_state.exercice_courant = generer_probleme(st.session_state.niveau)
        st.session_state.show_feedback = False
        st.rerun()
    
    st.markdown("---")
    
    if st.session_state.exercice_courant:
        ex = st.session_state.exercice_courant
        st.markdown(f'<div class="aller-loin-box"><h3>{ex["question"]}</h3></div>', unsafe_allow_html=True)
        
        if not st.session_state.show_feedback:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Réponse :", key="input_defi", value=0, step=1)
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Valider", use_container_width=True, key="btn_val_defi"):
                    correct = reponse == ex['reponse']
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                        st.session_state.points += 30
                    maj_streak(correct)
                    bonus = calculer_bonus_streak(st.session_state.streak['current'])
                    if correct and bonus > 0:
                        st.session_state.points += bonus
                    st.session_state.feedback_correct = correct
                    st.session_state.feedback_reponse = reponse
                    st.session_state.dernier_exercice = ex
                    st.session_state.show_feedback = True
                    st.session_state.scores_history.append({'type': 'Défi', 'points': (30 if correct else 0) + bonus, 'date': str(date.today())})
                    nouveaux = verifier_badges(st.session_state.points, st.session_state.badges)
                    st.session_state.badges.extend(nouveaux)
                    st.rerun()
        
        if st.session_state.show_feedback and st.session_state.dernier_exercice:
            st.markdown("---")
            if st.session_state.feedback_correct:
                st.markdown('<div class="feedback-success">🎉 EXCELLENT ! C\'est juste !</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ La réponse était {st.session_state.dernier_exercice["reponse"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Ton choix :** {st.session_state.feedback_reponse}")
                st.write(f"**Réponse :** {st.session_state.dernier_exercice['reponse']}")
            with col2:
                if st.button("➡️ SUIVANT", use_container_width=True, key="btn_next_defi"):
                    st.session_state.exercice_courant = generer_probleme(st.session_state.niveau)
                    st.session_state.show_feedback = False
                    st.rerun()

# ============================================
# 🎯 MAIN
# ============================================

def main():
    init_session_state()
    local_css()
    
    with st.sidebar:
        st.title("🎓 Session")
        st.markdown("---")
        st.session_state.niveau = st.selectbox("📚 Niveau :", ["CE1", "CE2", "CM1", "CM2"], key="select_niveau")
        
        st.markdown("---")
        st.subheader("⭐ Points & Engagement")
        col1, col2, col3 = st.columns(3)
        col1.metric("Points", st.session_state.points)
        col2.metric("Streak", f"🔥 {st.session_state.streak['current']}")
        col3.metric("Max", f"🏆 {st.session_state.streak['max']}")
        
        st.markdown("---")
        st.subheader("📊 Progression")
        progression = calculer_progression(st.session_state.stats_par_niveau)
        for niveau, pct in progression.items():
            st.write(f"**{niveau}** : {pct}%")
            st.progress(pct / 100)
        
        st.markdown("---")
        st.subheader("🏅 Badges")
        if st.session_state.badges:
            for badge in st.session_state.badges:
                st.markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)
        else:
            st.info("Gagne des points pour débloquer des badges !")
        
        st.markdown("---")
        st.subheader("🏆 Leaderboard")
        afficher_leaderboard()
        
        st.markdown("---")
        if st.button("🔄 Réinitialiser Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.title("🎓 MathCopain v4 - Le Leader du Calcul Mental")
    
    generer_daily_challenge()
    if st.session_state.daily_challenge['challenge']:
        challenge = st.session_state.daily_challenge['challenge']
        st.markdown(f'<div class="daily-challenge-box">', unsafe_allow_html=True)
        st.write(f"### 🎯 DÉFI DU JOUR")
        st.write(f"**{challenge['text']}**")
        st.progress(0.5)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.streak['current'] > 0:
        st.markdown(f'<div class="streak-box">🔥 STREAK ACTUEL : {st.session_state.streak["current"]} 🔥</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ✅ CORRECTION: Utiliser des noms simples et cohérents
    categories = ["Exercice", "Jeu", "Défi"]
    categorie_selectionnee = st.radio(
        "Choisis ce que tu veux faire :", 
        categories, 
        horizontal=True, 
        key="main_radio"
    )
    
    st.markdown("---")
    
    # ✅ CORRECTION: Logique de nettoyage simplifiée et fiabilisée
    if categorie_selectionnee != st.session_state.active_category:
        st.session_state.exercice_courant = None
        st.session_state.show_feedback = False
        st.session_state.jeu_type = None
        st.session_state.jeu_memory = None
        st.session_state.active_category = categorie_selectionnee
        st.rerun()
    
    if categorie_selectionnee == "Exercice":
        exercice_rapide_section()
    elif categorie_selectionnee == "Jeu":
        jeu_section()
    elif categorie_selectionnee == "Défi":
        defi_section()

if __name__ == "__main__":
    main()
