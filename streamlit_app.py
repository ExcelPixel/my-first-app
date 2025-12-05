import streamlit as st
import random

# --- 1. CONFIGURATION & DARK MODE ---
# This sets the page title and ensures it looks good on mobile/iPad
st.set_page_config(page_title="Multiplication Master", page_icon="✖️", layout="centered")

# --- 2. CSS STYLING (For Dark Mode & Progress Bar) ---
# Streamlit respects your system's Dark Mode automatically. 
# We add a little custom CSS to make the progress bar look cool.
st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #00FF00;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE (SAVING PROGRESS) ---
# This keeps your progress safe even if you click buttons.
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'total_count' not in st.session_state:
    st.session_state.total_count = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'current_q' not in st.session_state:
    st.session_state.current_q = None

# --- 4. THE SIDEBAR (SETTINGS) ---
st.sidebar.header("⚙️ Game Settings")
st.sidebar.write("Customize your multiplication ranges:")

# Range 1 (e.g., 25-30)
col1, col2 = st.sidebar.columns(2)
with col1:
    min_1 = st.number_input("Range 1 Start", value=11, step=1)
with col2:
    max_1 = st.number_input("Range 1 End", value=30, step=1)

# Range 2 (e.g., 1-10)
col3, col4 = st.sidebar.columns(2)
with col3:
    min_2 = st.number_input("Range 2 Start", value=1, step=1)
with col4:
    max_2 = st.number_input("Range 2 End", value=10, step=1)

# Start/Reset Button
if st.sidebar.button("New Game / Reset", type="primary"):
    # Generate every possible combination (Cartesian product)
    all_pairs = []
    # We add +1 to max because Python ranges stop one number short
    for x in range(min_1, max_1 + 1):
        for y in range(min_2, max_2 + 1):
            all_pairs.append((x, y))
    
    # Randomize the order (No patterns!)
    random.shuffle(all_pairs)
    
    # Save to session state
    st.session_state.questions = all_pairs
    st.session_state.total_count = len(all_pairs)
    st.session_state.score = 0
    st.session_state.game_active = True
    st.session_state.current_q = st.session_state.questions.pop() if st.session_state.questions else None
    st.rerun()

# --- 5. THE MAIN GAME APP ---
st.title("🧠 Random Multiplier")

if not st.session_state.game_active:
    st.info("👈 Use the sidebar menu to set your ranges and click 'New Game' to start!")
    st.stop()

# Calculate Progress
if st.session_state.total_count > 0:
    progress = st.session_state.score / st.session_state.total_count
else:
    progress = 0

# Show Progress Bar
st.write(f"**Progress: {st.session_state.score} / {st.session_state.total_count} Completed**")
st.progress(progress)

# Check if game is finished
if st.session_state.current_q is None:
    st.balloons()
    st.success(f"🎉 MISSION COMPLETE! You solved all {st.session_state.total_count} problems!")
    if st.button("Play Again"):
        st.session_state.game_active = False
        st.rerun()
    st.stop()

# Display the Question
num1, num2 = st.session_state.current_q
correct_answer = num1 * num2

st.markdown(f"## What is **{num1}** x **{num2}**?")

# Answer Input form
with st.form(key='answer_form'):
    user_answer = st.number_input("Your Answer:", step=1, key="input_box")
    submit_btn = st.form_submit_button(label="Submit Answer")

if submit_btn:
    if user_answer == correct_answer:
        st.success("✅ Correct!")
        st.session_state.score += 1
        
        # Load next question
        if st.session_state.questions:
            st.session_state.current_q = st.session_state.questions.pop()
        else:
            st.session_state.current_q = None # End game
        
        st.rerun()
    else:
        st.error(f"❌ Incorrect. Try again! (Hint: It ends in {str(correct_answer)[-1]})")
