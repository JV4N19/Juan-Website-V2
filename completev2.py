import streamlit as st
import random
import ast
import operator

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="My School App",
    page_icon="🎓",
    layout="centered"
)

# =========================================================
# ANIMATED BLACK BACKGROUND
# =========================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(80,80,255,0.12), transparent 25%),
        radial-gradient(circle at 90% 80%, rgba(0,200,255,0.10), transparent 25%),
        #030303;
    color: white;
    overflow-x: hidden;
}

.stApp::before {
    content: "";
    position: fixed;
    width: 450px;
    height: 450px;
    border-radius: 50%;
    background: rgba(80,100,255,0.07);
    filter: blur(80px);
    top: -150px;
    left: -150px;
    z-index: -1;
    animation: moveGlow 12s ease-in-out infinite alternate;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: rgba(0,180,255,0.06);
    filter: blur(80px);
    bottom: -150px;
    right: -150px;
    z-index: -1;
    animation: moveGlow2 15s ease-in-out infinite alternate;
}

@keyframes moveGlow {
    0% { transform: translate(0px, 0px); }
    50% { transform: translate(180px, 100px); }
    100% { transform: translate(80px, 250px); }
}

@keyframes moveGlow2 {
    0% { transform: translate(0px, 0px); }
    50% { transform: translate(-150px, -100px); }
    100% { transform: translate(-80px, -220px); }
}

section[data-testid="stSidebar"] {
    background: #050505;
    border-right: 1px solid #222;
}

.stButton > button {
    background: #101010;
    color: white;
    border: 1px solid #333;
    border-radius: 12px;
    transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #666;
    box-shadow: 0 5px 15px rgba(100,150,255,0.15);
}

.stButton > button:active {
    transform: scale(0.96);
}

.calculator-display {
    background: #080808;
    color: white;
    padding: 22px;
    border-radius: 18px;
    text-align: right;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 18px;
    border: 1px solid #333;
    min-height: 45px;
    overflow-x: auto;
    white-space: nowrap;
}

.info-card,
.result-card {
    background: rgba(15,15,15,0.9);
    border: 1px solid #292929;
    border-radius: 16px;
    padding: 18px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.info-card:hover,
.result-card:hover {
    transform: translateY(-3px);
    border-color: #555;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# BACKGROUND & CUSTOM STYLING
# =========================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(10,12,16,0.82), rgba(10,12,16,0.92)),
                url("4kblackimg.jpg") center center / cover no-repeat fixed;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# QUESTION DATABASE
# =========================================================

if "questions" not in st.session_state:
    st.session_state.questions = {
        "Mathematics": [
            {
                "question": "What is 12 × 8?",
                "options": ["86", "96", "108", "112"],
                "answer": "96"
            },
            {
                "question": "What is 25 + 37?",
                "options": ["52", "62", "72", "82"],
                "answer": "62"
            }
        ],
        "English": [
            {
                "question": "What is the past tense of 'go'?",
                "options": ["Goed", "Gone", "Went", "Going"],
                "answer": "Went"
            }
        ],
        "Science": [
            {
                "question": "What organelle is known as the powerhouse of the cell?",
                "options": ["Nucleus", "Mitochondria", "Ribosome", "Cell wall"],
                "answer": "Mitochondria"
            }
        ]
    }

# =========================================================
# SESSION STATE
# =========================================================

if "profile_created" not in st.session_state:
    st.session_state.profile_created = False

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_number" not in st.session_state:
    st.session_state.quiz_number = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

# =========================================================
# NUMBER QUEST SESSION STATE
# =========================================================

if "nq_secret" not in st.session_state:
    st.session_state.nq_secret = random.randint(1, 20)
    st.session_state.nq_difficulty = "🟢 Easy"
    st.session_state.nq_active_difficulty = "🟢 Easy"
    st.session_state.nq_maximum = 20
    st.session_state.nq_max_lives = 10
    st.session_state.nq_lives = 10
    st.session_state.nq_guesses = []
    st.session_state.nq_finished = False
    st.session_state.nq_won = False
    st.session_state.nq_score = 0
    st.session_state.nq_games_played = 0
    st.session_state.nq_message = "Make your first guess!"

NQ_LEVELS = {
    "🟢 Easy": {"maximum": 20, "lives": 10, "multiplier": 10},
    "🟡 Medium": {"maximum": 50, "lives": 7, "multiplier": 20},
    "🔴 Hard": {"maximum": 100, "lives": 5, "multiplier": 40},
    "💀 Extreme": {"maximum": 500, "lives": 8, "multiplier": 100},
}

def nq_new_game(difficulty):
    settings = NQ_LEVELS[difficulty]

    st.session_state.nq_secret = random.randint(1, settings["maximum"])
    st.session_state.nq_difficulty = difficulty
    st.session_state.nq_active_difficulty = difficulty
    st.session_state.nq_maximum = settings["maximum"]
    st.session_state.nq_max_lives = settings["lives"]
    st.session_state.nq_lives = settings["lives"]
    st.session_state.nq_guesses = []
    st.session_state.nq_finished = False
    st.session_state.nq_won = False
    st.session_state.nq_message = "Make your first guess!"

# =========================================================
# SIDEBAR MENU
# =========================================================

st.sidebar.title("🎓 My School App")

page = st.sidebar.radio(
    "Choose a page:",
    [
        "👤 My Profile",
        "🧮 Calculator",
        "📊 Grade Calculator",
        "🧠 Quiz Master",
        "🎯 Number Quest",
        "✏️ Edit Questions"
    ]
)

# =========================================================
# PROFILE
# =========================================================

if page == "👤 My Profile":

    st.title("👋 My First Profile")
    st.write("Fill in your information and create your profile!")

    name = st.text_input("👤 Name")
    age = st.number_input("🎂 Age", min_value=1, max_value=100, step=1)
    school = st.text_input("🏫 School")
    subject = st.text_input("📚 Favorite Subject")
    hobby = st.text_input("🎮 Favorite Hobby")

    if st.button("✨ Create My Profile"):

        if name and school and subject and hobby:
            st.session_state.profile_created = True

            st.success("Profile created successfully!")
            st.subheader(f"Hello! My name is {name}.")
            st.write(f"🎂 I am {age} years old.")
            st.write(f"🏫 I go to {school}.")
            st.write(f"📚 My favorite subject is {subject}.")
            st.write(f"🎮 I enjoy {hobby}.")

            st.balloons()

        else:
            st.warning("Please fill in all the fields!")

# =========================================================
# CALCULATOR
# =========================================================

elif page == "🧮 Calculator":

    st.title("🧮 Calculator")

    if "calculator" not in st.session_state:
        st.session_state.calculator = ""

    def number_button(number):
        if st.session_state.calculator == "Error":
            st.session_state.calculator = ""
        st.session_state.calculator += number

    def operator_button(symbol):
        current = st.session_state.calculator

        if current == "Error" or current == "":
            return

        if current[-1] in "+-*/":
            return

        st.session_state.calculator += symbol

    def decimal_button():
        current = st.session_state.calculator

        if current == "Error":
            st.session_state.calculator = "0."
            return

        if current == "":
            st.session_state.calculator = "0."
            return

        parts = current.replace("+", " ").replace("-", " ")
        parts = parts.replace("*", " ").replace("/", " ")
        parts = parts.split()

        if len(parts) == 0 or "." not in parts[-1]:
            st.session_state.calculator += "."

    def clear_button():
        st.session_state.calculator = ""

    def delete_button():
        if st.session_state.calculator == "Error":
            st.session_state.calculator = ""
        else:
            st.session_state.calculator = st.session_state.calculator[:-1]

    def equals_button():

        expression = st.session_state.calculator

        if expression == "":
            return

        try:
            allowed = "0123456789+-*/. "

            if any(character not in allowed for character in expression):
                st.session_state.calculator = "Error"
                return

            tree = ast.parse(expression, mode="eval")

            operations = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv
            }

            def calculate(node):

                if isinstance(node, ast.Expression):
                    return calculate(node.body)

                if isinstance(node, ast.Constant):
                    if isinstance(node.value, (int, float)):
                        return node.value
                    raise ValueError

                if isinstance(node, ast.BinOp):
                    left = calculate(node.left)
                    right = calculate(node.right)
                    operation = operations.get(type(node.op))

                    if operation is None:
                        raise ValueError

                    return operation(left, right)

                raise ValueError

            result = calculate(tree)
            st.session_state.calculator = str(result)

        except:
            st.session_state.calculator = "Error"

    raw_display = st.session_state.calculator

    if raw_display == "":
        raw_display = "0"

    display = (
        raw_display
        .replace("*", " × ")
        .replace("/", " ÷ ")
        .replace("-", " − ")
        .replace("+", " + ")
    )

    st.markdown(
        f'<div class="calculator-display">{display}</div>',
        unsafe_allow_html=True
    )

    # 7 8 9 ÷
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.button("7", use_container_width=True, on_click=number_button, args=("7",))
    with c2:
        st.button("8", use_container_width=True, on_click=number_button, args=("8",))
    with c3:
        st.button("9", use_container_width=True, on_click=number_button, args=("9",))
    with c4:
        st.button("÷", use_container_width=True, on_click=operator_button, args=("/",))

    # 4 5 6 ×
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.button("4", use_container_width=True, on_click=number_button, args=("4",))
    with c2:
        st.button("5", use_container_width=True, on_click=number_button, args=("5",))
    with c3:
        st.button("6", use_container_width=True, on_click=number_button, args=("6",))
    with c4:
        st.button("×", use_container_width=True, on_click=operator_button, args=("*",))

    # 1 2 3 −
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.button("1", use_container_width=True, on_click=number_button, args=("1",))
    with c2:
        st.button("2", use_container_width=True, on_click=number_button, args=("2",))
    with c3:
        st.button("3", use_container_width=True, on_click=number_button, args=("3",))
    with c4:
        st.button("−", use_container_width=True, on_click=operator_button, args=("-",))

    # 0 . C +
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.button("0", use_container_width=True, on_click=number_button, args=("0",))
    with c2:
        st.button(".", use_container_width=True, on_click=decimal_button)
    with c3:
        st.button("C", use_container_width=True, on_click=clear_button)
    with c4:
        st.button("+", use_container_width=True, on_click=operator_button, args=("+",))

    # Backspace and equals
    c1, c2 = st.columns(2)

    with c1:
        st.button("⌫", use_container_width=True, on_click=delete_button)
    with c2:
        st.button("=", use_container_width=True, on_click=equals_button)

# =========================================================
# GRADE CALCULATOR
# =========================================================

elif page == "📊 Grade Calculator":

    st.title("📊 Grade Calculator")
    st.write("Enter your subjects and grades below.")

    number_of_subjects = st.number_input(
        "Number of subjects",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

    grades = []

    st.write("---")

    for i in range(number_of_subjects):

        col1, col2 = st.columns(2)

        with col1:
            subject_name = st.text_input(
                f"Subject {i + 1}",
                value=f"Subject {i + 1}",
                key=f"subject_name_{i}"
            )

        with col2:
            grade = st.number_input(
                "Grade",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                key=f"grade_{i}"
            )

        grades.append((subject_name, grade))

    st.write("---")

    if st.button("📊 Calculate Grades", use_container_width=True):

        total = sum(grade for subject, grade in grades)
        average = total / number_of_subjects

        # Exact GPA out of 4.00
        gpa = average / 25
        gpa = min(gpa, 4.00)

        st.subheader("📋 Results")

        with st.container(border=True):

            st.write("### Your Grades")

            for subject_name, grade in grades:
                st.write(f"📚 **{subject_name}:** {grade:.2f} / 100")

            st.write("---")

            st.metric("Average", f"{average:.2f} / 100")
            st.metric("GPA", f"{gpa:.2f} / 4.00")

        if average >= 90:
            st.success("🏆 Excellent! Keep up the amazing work!")
        elif average >= 80:
            st.success("🎉 Good job! You're doing really well!")
        elif average >= 70:
            st.info("👍 Nice work! Keep improving!")
        elif average >= 60:
            st.warning("💪 Nice try! You can improve with more practice.")
        else:
            st.error("📚 Keep studying and don't give up!")

# =========================================================
# QUIZ MASTER
# =========================================================

elif page == "🧠 Quiz Master":

    st.title("🧠 Quiz Master")
    st.write("Test your knowledge!")

    if not st.session_state.quiz_questions:

        subject = st.selectbox(
            "📚 Choose a subject",
            list(st.session_state.questions.keys())
        )

        max_questions = len(st.session_state.questions[subject])

        number = st.number_input(
            "🔢 Number of questions",
            min_value=1,
            max_value=max_questions,
            value=1,
            step=1
        )

        if st.button("🚀 Start Quiz", use_container_width=True):

            st.session_state.quiz_questions = random.sample(
                st.session_state.questions[subject],
                number
            )

            st.session_state.quiz_number = 0
            st.session_state.quiz_score = 0

            st.rerun()

    else:

        questions = st.session_state.quiz_questions
        current = st.session_state.quiz_number

        if current >= len(questions):

            score = st.session_state.quiz_score
            total = len(questions)
            percentage = (score / total) * 100

            st.balloons()
            st.title("🏆 Quiz Complete!")

            st.metric("Score", f"{score} / {total}")
            st.metric("Percentage", f"{percentage:.0f}%")

            if percentage >= 80:
                st.success("🎉 Excellent! Good job!")
            elif percentage >= 50:
                st.warning("👍 Nice try! Keep practicing!")
            else:
                st.error("💪 Don't give up! Try again!")

            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.quiz_questions = []
                st.session_state.quiz_number = 0
                st.session_state.quiz_score = 0
                st.rerun()

        else:

            question = questions[current]

            st.progress(current / len(questions))
            st.write(f"### Question {current + 1} / {len(questions)}")
            st.info(question["question"])

            answer = st.radio(
                "Choose your answer:",
                question["options"],
                key=f"quiz_answer_{current}"
            )

            if st.button("Next ➡️", use_container_width=True):

                if answer == question["answer"]:
                    st.session_state.quiz_score += 1

                st.session_state.quiz_number += 1
                st.rerun()

# =========================================================
# NUMBER QUEST
# =========================================================

elif page == "🎯 Number Quest":

    st.title("🎯 Number Quest")
    st.caption("THINK FAST • GUESS SMART • WIN BIG")

    st.markdown("""
    <div class="info-card" style="text-align:center; padding:22px;">
        <div style="font-size:48px;">🎮</div>
        <h2>Can You Beat The Computer?</h2>
        <p style="color:#b8b8b8;">
            I've picked a secret number. Guess it before you run out of lives!
        </p>
    </div>
    """, unsafe_allow_html=True)

    selected_difficulty = st.selectbox(
        "⚡ Choose your difficulty",
        list(NQ_LEVELS.keys()),
        index=list(NQ_LEVELS.keys()).index(st.session_state.nq_active_difficulty),
        key="nq_difficulty_picker"
    )

    if selected_difficulty != st.session_state.nq_active_difficulty:
        nq_new_game(selected_difficulty)
        st.rerun()

    stat1, stat2, stat3 = st.columns(3)

    with stat1:
        st.metric("❤️ Lives left", st.session_state.nq_lives)

    with stat2:
        st.metric("🎯 Guesses", len(st.session_state.nq_guesses))

    with stat3:
        st.metric("🏆 Total score", st.session_state.nq_score)

    st.markdown(f"""
    <div class="result-card" style="text-align:center; margin:18px 0;">
        <p style="color:#aaaaaa;">GUESS A NUMBER BETWEEN</p>
        <div style="font-size:42px; font-weight:900; color:#69d9ff;">
            1 – {st.session_state.nq_maximum}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.nq_finished:

        with st.form("number_quest_guess_form"):

            guess = st.number_input(
                "🔢 Your guess",
                min_value=1,
                max_value=st.session_state.nq_maximum,
                value=1,
                step=1,
                key="nq_guess_input"
            )

            submitted = st.form_submit_button(
                "🚀 SUBMIT GUESS",
                use_container_width=True
            )

        if submitted:

            if guess in st.session_state.nq_guesses:
                st.warning("You've already guessed that number. Try another!")

            else:

                st.session_state.nq_guesses.append(guess)
                st.session_state.nq_lives -= 1

                if guess == st.session_state.nq_secret:

                    st.session_state.nq_won = True
                    st.session_state.nq_finished = True
                    st.session_state.nq_games_played += 1

                    multiplier = NQ_LEVELS[
                        st.session_state.nq_active_difficulty
                    ]["multiplier"]

                    points = 50 + st.session_state.nq_lives * multiplier
                    st.session_state.nq_score += points

                    st.session_state.nq_message = (
                        f"🏆 Correct! You earned {points} points!"
                    )

                elif st.session_state.nq_lives == 0:

                    st.session_state.nq_finished = True
                    st.session_state.nq_games_played += 1
                    st.session_state.nq_won = False

                    st.session_state.nq_message = (
                        f"Game over! The secret number was {st.session_state.nq_secret}."
                    )

                elif guess < st.session_state.nq_secret:
                    st.session_state.nq_message = "⬆️ Too low! Try a HIGHER number."

                else:
                    st.session_state.nq_message = "⬇️ Too high! Try a LOWER number."

                st.rerun()

    if st.session_state.nq_finished:

        if st.session_state.nq_won:
            st.balloons()
            st.success(st.session_state.nq_message)
        else:
            st.error(st.session_state.nq_message)

        if st.button(
            "🔄 PLAY AGAIN",
            key="nq_play_again",
            use_container_width=True
        ):
            nq_new_game(st.session_state.nq_active_difficulty)
            st.rerun()

    else:
        st.info("💡 " + st.session_state.nq_message)

    if st.session_state.nq_guesses:

        st.subheader("📜 Guess History")

        for index, previous_guess in enumerate(
            st.session_state.nq_guesses,
            start=1
        ):

            if previous_guess == st.session_state.nq_secret and st.session_state.nq_won:
                result = "✅ Correct!"
            elif previous_guess < st.session_state.nq_secret:
                result = "⬆️ Too low"
            else:
                result = "⬇️ Too high"

            st.write(f"**Guess {index}:** {previous_guess} — {result}")

    st.caption(
        f"Games played: {st.session_state.nq_games_played} "
        f"• Difficulty: {st.session_state.nq_active_difficulty}"
    )

# =========================================================
# EDIT QUESTIONS
# =========================================================

elif page == "✏️ Edit Questions":

    st.title("✏️ Edit Quiz Questions")
    st.write("Add, edit, or delete questions.")

    subject = st.selectbox(
        "📚 Choose subject",
        list(st.session_state.questions.keys())
    )

    st.write("---")
    st.subheader("Existing Questions")

    for i, question in enumerate(st.session_state.questions[subject]):

        with st.expander(f"Question {i + 1}"):

            new_question = st.text_input(
                "Question",
                question["question"],
                key=f"edit_q_{subject}_{i}"
            )

            new_a = st.text_input(
                "A",
                question["options"][0],
                key=f"edit_a_{subject}_{i}"
            )

            new_b = st.text_input(
                "B",
                question["options"][1],
                key=f"edit_b_{subject}_{i}"
            )

            new_c = st.text_input(
                "C",
                question["options"][2],
                key=f"edit_c_{subject}_{i}"
            )

            new_d = st.text_input(
                "D",
                question["options"][3],
                key=f"edit_d_{subject}_{i}"
            )

            options = [new_a, new_b, new_c, new_d]
            current_answer = question["answer"]

            if current_answer in options:
                answer_index = options.index(current_answer)
            else:
                answer_index = 0

            new_answer = st.selectbox(
                "✅ Correct Answer",
                options,
                index=answer_index,
                key=f"edit_answer_{subject}_{i}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("💾 Save", key=f"save_{subject}_{i}"):

                    st.session_state.questions[subject][i] = {
                        "question": new_question,
                        "options": options,
                        "answer": new_answer
                    }

                    st.success("Question saved!")

            with col2:

                if st.button("🗑️ Delete", key=f"delete_{subject}_{i}"):

                    st.session_state.questions[subject].pop(i)
                    st.rerun()

    st.write("---")
    st.subheader("➕ Add New Question")

    new_question = st.text_input("Question", key="add_question")
    new_a = st.text_input("A", key="add_a")
    new_b = st.text_input("B", key="add_b")
    new_c = st.text_input("C", key="add_c")
    new_d = st.text_input("D", key="add_d")

    correct = st.selectbox(
        "✅ Correct Answer",
        ["A", "B", "C", "D"],
        key="add_correct"
    )

    if st.button("➕ Add Question", use_container_width=True):

        options = [new_a, new_b, new_c, new_d]

        if new_question and all(options):

            correct_answer = options[
                ["A", "B", "C", "D"].index(correct)
            ]

            st.session_state.questions[subject].append({
                "question": new_question,
                "options": options,
                "answer": correct_answer
            })

            st.success("🎉 Question added successfully!")

        else:
            st.warning("Please fill in every field.")

# =========================================================
# DARK ANIMATED DESIGN
# =========================================================

st.markdown("""
<style>

/* BLACK BACKGROUND */

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(70,70,120,0.18), transparent 25%),
        radial-gradient(circle at 85% 80%, rgba(30,90,120,0.15), transparent 25%),
        #050505;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050505, #0b0b0b, #050505);
    border-right: 1px solid #222;
}

/* PAGE ANIMATION */

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.main {
    animation: fadeIn 0.6s ease;
}

/* FLOATING ANIMATION */

@keyframes floating {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
    100% { transform: translateY(0px); }
}

/* GLOW ANIMATION */

@keyframes glow {
    0% {
        box-shadow: 0 0 5px rgba(100,150,255,0.15);
    }
    50% {
        box-shadow: 0 0 22px rgba(100,150,255,0.35);
    }
    100% {
        box-shadow: 0 0 5px rgba(100,150,255,0.15);
    }
}

/* TITLES */

.main-title {
    animation: fadeIn 0.7s ease;
    text-shadow: 0 0 10px rgba(120,150,255,0.4);
}

/* CARDS */

.info-card {
    animation: fadeIn 0.6s ease;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    background: rgba(15,15,15,0.85);
    border: 1px solid #292929;
    border-radius: 16px;
    padding: 18px;
}

.info-card:hover {
    transform: translateY(-5px);
    border-color: #444;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

/* BUTTONS */

.stButton > button {
    background: #111111;
    color: white;
    border: 1px solid #333;
    border-radius: 12px;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #777;
    box-shadow: 0 5px 18px rgba(0,0,0,0.5);
}

.stButton > button:active {
    transform: scale(0.96);
}

/* CALCULATOR DISPLAY */

.calculator-display {
    animation: glow 2.5s infinite;
    background: linear-gradient(145deg, #050505, #151515);
    color: #ffffff;
    padding: 22px;
    border-radius: 18px;
    text-align: right;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 18px;
    border: 1px solid #333;
    min-height: 45px;
    overflow-x: auto;
    white-space: nowrap;
}

/* RESULT CARDS */

.result-card {
    animation: fadeIn 0.5s ease;
    background: #101010;
    border: 1px solid #292929;
    border-radius: 16px;
    padding: 18px;
    margin-top: 12px;
}

/* METRICS */

[data-testid="stMetric"] {
    background: #101010;
    border: 1px solid #292929;
    border-radius: 14px;
    padding: 12px;
    animation: fadeIn 0.5s ease;
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    background-color: #101010 !important;
    color: white !important;
    border-color: #333 !important;
}

/* PROGRESS BAR */

.stProgress > div > div {
    transition: width 0.5s ease;
}

/* DIVIDERS */

hr {
    border-color: #292929;
}

/* REDUCE ANIMATION IF USER PREFERS */

@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}

</style>
""", unsafe_allow_html=True)
