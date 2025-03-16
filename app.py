import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="VitalEdge: Your AI-Powered Health & Fitness Companion 🌟",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown(
    """
    <style>
        .main { padding: 2rem; }
        .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
        .success-box, .warning-box {
            padding: 1rem; border-radius: 0.5rem;
        }
        .success-box { background-color: #f0fff4; border: 1px solid #9ae6b4; }
        .warning-box { background-color: #fffaf0; border: 1px solid #fbd38d; }
        div[data-testid="stExpander"] div[role="button"] p { font-size: 1.1rem; font-weight: 600; }
        .qa-box { margin-bottom: 1rem; padding: 1rem; background-color: #f9f9f9; border-radius: 0.5rem; border: 1px solid #ddd; }
        .qa-box h4 { margin: 0 0 0.5rem; }
    </style>
    """,
    unsafe_allow_html=True
)

def display_plan(title, content, key_details, tips=None):
    """Reusable function to display both Dietary and Fitness plans."""
    with st.expander(title, expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"### 🎯 {key_details['title']}")
            st.success(content.get(key_details['key'], "Information not available"))
            st.markdown(f"### {key_details['plan_title']}")
            st.write(content.get(key_details['plan_key'], "Plan not available"))
        with col2:
            if tips:
                st.markdown(f"### 💡 {tips['title']}")
                for tip in content.get(tips['key'], "").split('\n'):
                    if tip.strip():
                        st.info(tip)

def generate_ai_plan(user_profile, additional_input, model, instructions):
    """Function to generate AI-powered health and fitness plans."""
    context = f"Relevant Context:\n{user_profile}\nAdditional Input:\n{additional_input}"
    prompt_parts = [context, "\n".join(instructions)]
    response = model.generate_content(prompt_parts)
    return response.text

def main():
    st.title("VitalEdge: Your AI-Powered Health & Fitness Companion 🌟")
    st.markdown(
        """
        <div style='background-color: #00008B; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
        Achieve Your Best Self with AI-Powered Health & Fitness! 🌟
Get personalized dietary, fitness, and lifestyle plans tailored to your goals and preferences. Powered by Manojkumar Tech, our intelligent system delivers a holistic approach to wellness. 💪🍏✨
        </div>
        """,
        unsafe_allow_html=True
    )

    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.activity_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False

    # Sidebar - User Profile
    with st.sidebar:
        st.header("👤 Your Profile")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, step=1)
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
            dietary_preferences = st.selectbox("Dietary Preferences", ["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"])
        with col2:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
            sex = st.selectbox("Sex", ["Male", "Female", "Other"])
            fitness_goals = st.selectbox("Fitness Goals", ["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"])
            work_type = st.selectbox("Work Type", ["Student", "Desk Job", "Field Work", "Remote Work"])
            country = st.text_input("Country", placeholder="Enter your country")

        additional_input = st.text_area("📝 Additional Information", placeholder="Share any specific goals, challenges, or preferences...")

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if google_api_key:
        try:
            genai.configure(api_key=google_api_key)
            gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            st.error(f"❌ Error initializing Gemini model: {e}")
            return

    if st.button("🎯 Generate My Personalized Plan"):
        with st.spinner("Creating your perfect health and fitness routine..."):
            user_profile = f"""
            Age: {age}, Weight: {weight}kg, Height: {height}cm, Sex: {sex},
            Activity Level: {activity_level}, Dietary Preferences: {dietary_preferences},
            Fitness Goals: {fitness_goals}, Work Type: {work_type}, Country: {country}
            """

            dietary_instructions = [
                "Focus only on the provided user profile and context.",
                "Generate a meal plan relevant to their profile without unrelated details.",
                "Suggest a detailed meal plan for the day, including breakfast, lunch, dinner, and snacks.",
                "Explain why the plan is suited to the user's goals and country-specific considerations.",
                "Use Chain-of-Thought reasoning for high-quality recommendations."
            ]

            fitness_instructions = [
                "Focus only on the provided user profile and goals.",
                "Include warm-up, main workout, and cool-down exercises tailored to the user.",
                "Explain the benefits of each exercise, focusing on relevance to user goals.",
                "Ensure plans are specific and actionable with no unrelated information."
            ]

            activity_instructions = [
                "Suggest activities based only on the user's input and preferences.",
                "Provide country-specific recommendations for recreational and mental health activities.",
                "Explain the benefits of each activity and how it aligns with the user's goals.",
                "Avoid extraneous information outside the provided context."
            ]

            try:
                dietary_plan = generate_ai_plan(user_profile, additional_input, gemini_model, dietary_instructions)
                fitness_plan = generate_ai_plan(user_profile, additional_input, gemini_model, fitness_instructions)
                activity_plan = generate_ai_plan(user_profile, additional_input, gemini_model, activity_instructions)

                st.session_state.dietary_plan = {
                    "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                    "meal_plan": dietary_plan,
                    "important_considerations": "Hydration, Electrolytes, Fiber, and Adjusting Portion Sizes"
                }

                st.session_state.fitness_plan = {
                    "goals": "Build strength, improve endurance, and maintain overall fitness",
                    "routine": fitness_plan,
                    "tips": "Track progress, Rest adequately, Maintain proper form, Stay consistent"
                }

                st.session_state.activity_plan = {
                    "suggestions": activity_plan,
                    "why_these": "Activities selected to improve mental health, relaxation, and social interaction."
                }

                st.session_state.plans_generated = True

                display_plan("📋 Your Personalized Dietary Plan", st.session_state.dietary_plan, {"title": "Why this plan works", "key": "why_this_plan_works", "plan_title": "🍽️ Meal Plan", "plan_key": "meal_plan"})
                display_plan("💪 Your Personalized Fitness Plan", st.session_state.fitness_plan, {"title": "🎯 Goals", "key": "goals", "plan_title": "🏋️‍♂️ Exercise Routine", "plan_key": "routine"}, {"title": "💡 Pro Tips", "key": "tips"})
                display_plan("🌟 Suggested Activities", st.session_state.activity_plan, {"title": "Why these activities?", "key": "why_these", "plan_title": "🎉 Activity Suggestions", "plan_key": "suggestions"})
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

    if st.session_state.plans_generated:
        st.header("❓ Questions about your plan?")
        question_input = st.text_input("What would you like to know?")

        if st.button("Get Answer"):
            if question_input:
                with st.spinner("Finding the best answer for you..."):
                    dietary_plan = st.session_state.dietary_plan
                    fitness_plan = st.session_state.fitness_plan
                    activity_plan = st.session_state.activity_plan

                    context = f"Dietary Plan: {dietary_plan.get('meal_plan', '')}\n\nFitness Plan: {fitness_plan.get('routine', '')}\n\nActivity Plan: {activity_plan.get('suggestions', '')}"
                    full_context = f"{context}\nAdditional Input: {additional_input}\nUser Question: {question_input}"

                    try:
                        instructions = [
                            "Answer only based on the provided context and plans.",
                            "If the question is unrelated to the plans, respond with: 'This question is outside the scope of your personalized plan.'",
                            "Ensure clarity, conciseness, and accuracy in your response."
                        ]
                        prompt_parts = [full_context, "\n".join(instructions)]
                        response = gemini_model.generate_content(prompt_parts)

                        if response.text:
                            answer = response.text
                        else:
                            answer = "Sorry, I couldn't generate a response at this time."

                        st.session_state.qa_pairs.append((question_input, answer))
                    except Exception as e:
                        st.error(f"❌ An error occurred while getting the answer: {e}")

        if st.session_state.qa_pairs:
            st.header("💬 Q&A History")
            for question, answer in st.session_state.qa_pairs:
                with st.container():
                    st.markdown(f"**Q:** {question}")
                    st.markdown(f"**A:** {answer}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()