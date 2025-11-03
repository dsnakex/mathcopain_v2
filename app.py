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

# [pas de modifications ici sur les fonctions de générateurs & utilitaires, inchangées...]

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
            st.session_state.memory_incorrect_pair = None
            st.rerun()

    st.markdown("---")

    # DROITE
    if st.session_state.get('jeu_type') == 'droite' and st.session_state.exercice_courant:
        # ... [code inchangé]
        pass

    # MEMORY SANS PAUSE BLOQUANTE
    elif st.session_state.get('jeu_type') == 'memory' and st.session_state.jeu_memory:
        st.subheader("🧠 Memory - Trouve les paires !")

        memory = st.session_state.jeu_memory
        total_pairs = len(memory['cards']) // 2
        pairs_found = len(memory['matched']) // 2

        st.write(f"Paires trouvées : **{pairs_found}/{total_pairs}**")
        st.progress(pairs_found / total_pairs)

        # Affichage des paires incorrectes à cacher après un mauvais coup
        if st.session_state.memory_incorrect_pair:
            memory['revealed'].difference_update(st.session_state.memory_incorrect_pair)
            st.session_state.memory_incorrect_pair = None

        # Affichage cartes (4 colonnes)
        cols = st.columns(4)
        for idx in range(len(memory['cards'])):
            col = cols[idx % 4]
            with col:
                card_value = memory['cards'][idx]

                if idx in memory['matched']:
                    st.markdown(f"<div style='aspect-ratio: 1; background: linear-gradient(135deg, #90EE90 0%, #28a745 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 38px;'>{card_value}</div>", unsafe_allow_html=True)
                    st.button("✓", key=f"mem_{idx}_matched", disabled=True, use_container_width=True)
                elif idx in memory['revealed']:
                    st.markdown(f"<div style='aspect-ratio: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 38px;'>{card_value}</div>", unsafe_allow_html=True)
                    st.button("✓", key=f"mem_{idx}_revealed", disabled=True, use_container_width=True)
                else:
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

        # VÉRIFIER PAIRE : nouvelle logique asynchrone
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
                st.info("⏳ Pas une paire... La carte sera cachée au prochain tour.")
                # On garde trace de la paire à cacher, mais sans pause
                st.session_state.memory_incorrect_pair = {first_idx, second_idx}

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
                st.session_state.memory_incorrect_pair = None
                st.rerun()

# [Reste du code parfaitement compatible - inchangé !]
# (toutes les autres fonctions et la boucle main sont inchangées)