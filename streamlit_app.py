"""
Kineto - Streamlit Movie Recommender App
A natural language movie recommendation system with 6-signal hybrid architecture.
Multi-page flow: welcome → auth_menu → login/signup → profile → search
"""

import streamlit as st
import time
import pandas as pd
import re
import os

# Page config
st.set_page_config(
    page_title="Kineto - Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        'page': 'welcome',
        'search_results': None,
        'all_movies_list': [],
        'last_query': '',
        'user_info': {},
        'logged_in': False,
        'appearance': 'dark',
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# =============================================================================
# CUSTOM CSS STYLES
# =============================================================================
def get_theme_css():
    """Return CSS based on appearance setting."""
    if st.session_state.appearance == 'light':
        return """
        <style>
            .stApp { background-color: #ffffff; }
            .kineto-title { color: #1a1a1a; }
            .kineto-letter { color: #e50914; }
            .tagline { color: #444444; }
            .movie-card { background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin: 10px 0; }
            .track-header { background-color: #e0e0e0; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
            .demo-notice { background-color: #fff3cd; padding: 10px; border-radius: 5px; color: #856404; }
            .footer-text { color: #666666; }
        </style>
        """
    else:  # dark mode (default)
        return """
        <style>
            .kineto-title {
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin: 20px 0;
            }
            .kineto-letter {
                color: #e50914;
                display: inline-block;
                animation: pulse 2s ease-in-out infinite;
            }
            .kineto-letter:nth-child(1) { animation-delay: 0s; }
            .kineto-letter:nth-child(2) { animation-delay: 0.1s; }
            .kineto-letter:nth-child(3) { animation-delay: 0.2s; }
            .kineto-letter:nth-child(4) { animation-delay: 0.3s; }
            .kineto-letter:nth-child(5) { animation-delay: 0.4s; }
            .kineto-letter:nth-child(6) { animation-delay: 0.5s; }
            @keyframes pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.8; transform: scale(1.05); }
            }
            .tagline {
                text-align: center;
                font-size: 1.2rem;
                color: #cccccc;
                margin-bottom: 30px;
            }
            .movie-card {
                background-color: #1e1e1e;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }
            .track-header {
                background-color: #2d2d2d;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .demo-notice {
                background-color: #2d2d2d;
                padding: 10px;
                border-radius: 5px;
                color: #ffc107;
                text-align: center;
                margin: 10px 0;
            }
            .footer-text { color: #888888; }
            .center-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 60vh;
            }
            .auth-button {
                width: 200px;
                margin: 10px;
            }
        </style>
        """

st.markdown(get_theme_css(), unsafe_allow_html=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def render_kineto_title():
    """Render the animated Kineto title."""
    st.markdown("""
        <div class="kineto-title">
            <span class="kineto-letter">K</span>
            <span class="kineto-letter">I</span>
            <span class="kineto-letter">N</span>
            <span class="kineto-letter">E</span>
            <span class="kineto-letter">T</span>
            <span class="kineto-letter">O</span>
        </div>
    """, unsafe_allow_html=True)

def render_logo():
    """Render the Kineto logo."""
    logo_path = "kineto_logo.png"
    if os.path.exists(logo_path):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image(logo_path, width=200)
    else:
        st.markdown("<h1 style='text-align: center;'>🎬</h1>", unsafe_allow_html=True)

def navigate_to(page):
    """Navigate to a different page."""
    st.session_state.page = page
    st.rerun()

# =============================================================================
# PAGE: WELCOME
# =============================================================================
def page_welcome():
    """Welcome/landing page."""
    st.markdown("<br><br>", unsafe_allow_html=True)

    render_logo()
    render_kineto_title()

    st.markdown("""
        <p class="tagline">
            Your personalized movie recommendation assistant powered by hybrid AI.
        </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎬 Get Started", type="primary", use_container_width=True):
            navigate_to('auth_menu')

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="demo-notice">
                📢 <strong>Demo Mode</strong>: This is a demonstration version.
                No real authentication or data storage.
            </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: AUTH MENU
# =============================================================================
def page_auth_menu():
    """Authentication menu - choose login or signup."""
    st.markdown("<br><br>", unsafe_allow_html=True)

    render_kineto_title()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔑 Log In", use_container_width=True):
            navigate_to('login')

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🆕 Create Account", use_container_width=True):
            navigate_to('signup')

        st.markdown("<br><br>", unsafe_allow_html=True)

        if st.button("← Back", use_container_width=True):
            navigate_to('welcome')

# =============================================================================
# PAGE: SIGNUP
# =============================================================================
def page_signup():
    """Account creation page."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🆕 Create Account")
        st.markdown("""
            <div class="demo-notice">
                📢 <strong>Demo Mode</strong>: No real account will be created.
                Just fill in any valid format to proceed.
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        verify_password = st.text_input("Verify Password", type="password", placeholder="Re-enter password")

        error_msg = None
        if email and not validate_email(email):
            error_msg = "Please enter a valid email address."
        elif password and verify_password and password != verify_password:
            error_msg = "Passwords do not match."
        elif password and len(password) < 6:
            error_msg = "Password must be at least 6 characters."

        if error_msg:
            st.error(error_msg)

        st.markdown("<br>", unsafe_allow_html=True)

        col_back, col_create = st.columns(2)
        with col_back:
            if st.button("← Back", use_container_width=True):
                navigate_to('auth_menu')
        with col_create:
            can_create = email and password and verify_password and not error_msg
            if st.button("Create Account", type="primary", use_container_width=True, disabled=not can_create):
                st.session_state.user_info['email'] = email
                st.session_state.logged_in = True
                navigate_to('profile')

# =============================================================================
# PAGE: LOGIN
# =============================================================================
def page_login():
    """Login page."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🔑 Log In")
        st.markdown("""
            <div class="demo-notice">
                📢 <strong>Demo Mode</strong>: Enter any valid email format to proceed.
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        error_msg = None
        if email and not validate_email(email):
            error_msg = "Please enter a valid email address."

        if error_msg:
            st.error(error_msg)

        st.markdown("<br>", unsafe_allow_html=True)

        col_back, col_login = st.columns(2)
        with col_back:
            if st.button("← Back", use_container_width=True):
                navigate_to('auth_menu')
        with col_login:
            can_login = email and password and not error_msg
            if st.button("Log In", type="primary", use_container_width=True, disabled=not can_login):
                st.session_state.user_info['email'] = email
                st.session_state.logged_in = True
                navigate_to('profile')

# =============================================================================
# PAGE: PROFILE
# =============================================================================
def page_profile():
    """Profile setup page."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 👤 Let's personalize your experience")
        st.markdown("Tell us a bit about yourself to get better recommendations.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Name
        col_first, col_last = st.columns(2)
        with col_first:
            first_name = st.text_input("First Name", value=st.session_state.user_info.get('first_name', ''))
        with col_last:
            last_name = st.text_input("Last Name", value=st.session_state.user_info.get('last_name', ''))

        # Date of Birth
        st.markdown("**Date of Birth**")
        col_day, col_month, col_year = st.columns(3)
        with col_day:
            day = st.selectbox("Day", options=[''] + list(range(1, 32)), index=0)
        with col_month:
            months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
            month = st.selectbox("Month", options=months, index=0)
        with col_year:
            current_year = 2024
            year = st.selectbox("Year", options=[''] + list(range(current_year - 100, current_year - 10)), index=0)

        # Gender
        gender = st.selectbox("Gender", options=['', 'Male', 'Female', 'Non-binary', 'Prefer not to say'], index=0)

        # Phone
        st.markdown("**Phone Number** (optional)")
        col_code, col_phone = st.columns([1, 3])
        with col_code:
            country_codes = ['+1 (US)', '+44 (UK)', '+91 (IN)', '+61 (AU)', '+81 (JP)', '+86 (CN)', '+33 (FR)', '+49 (DE)']
            phone_code = st.selectbox("Code", options=[''] + country_codes, index=0)
        with col_phone:
            phone_number = st.text_input("Phone Number", placeholder="555-123-4567")

        # Location
        st.markdown("**Location** (optional)")
        col_city, col_state = st.columns(2)
        with col_city:
            city = st.text_input("City", placeholder="New York")
        with col_state:
            state = st.text_input("State/Province", placeholder="NY")

        countries = ['', 'United States', 'United Kingdom', 'Canada', 'Australia',
                    'Germany', 'France', 'Japan', 'India', 'Brazil', 'Mexico', 'Other']
        country = st.selectbox("Country", options=countries, index=0)

        st.markdown("<br>", unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Back", use_container_width=True):
                navigate_to('auth_menu')
        with col_next:
            if st.button("Next →", type="primary", use_container_width=True):
                # Store user info
                st.session_state.user_info.update({
                    'first_name': first_name,
                    'last_name': last_name,
                    'dob_day': day,
                    'dob_month': month,
                    'dob_year': year,
                    'gender': gender,
                    'phone_code': phone_code,
                    'phone_number': phone_number,
                    'city': city,
                    'state': state,
                    'country': country
                })
                navigate_to('search')

# =============================================================================
# PAGE: SEARCH (Main Recommendation Interface)
# =============================================================================
@st.cache_resource(show_spinner=True)
def load_recommender():
    """Load the movie recommender system."""
    with st.spinner("Loading recommendation engine... (this may take 30-60 seconds on first load)"):
        from src.recommender_interactive_v4 import MovieRecommenderInteractiveV4
        return MovieRecommenderInteractiveV4()


def get_movie_details(recommender, movie_title):
    """Look up movie details from TMDB data."""
    movies_df = recommender.movies

    # Try exact match first
    match = movies_df[movies_df['title'].str.lower() == movie_title.lower()]

    # If no exact match, try contains
    if match.empty:
        match = movies_df[movies_df['title'].str.lower().str.contains(movie_title.lower(), na=False)]

    if match.empty:
        return None

    movie = match.iloc[0]

    def safe_get(key, default='N/A'):
        val = movie.get(key, default)
        if val is None:
            return default
        if isinstance(val, (list, tuple)):
            return val if len(val) > 0 else default
        if isinstance(val, float):
            try:
                if pd.isna(val):
                    return default
            except (ValueError, TypeError):
                pass
        return val

    return {
        'title': safe_get('title', movie_title),
        'year': safe_get('year', 'N/A'),
        'directors': safe_get('directors', []),
        'cast': safe_get('cast', []),
        'production_companies': safe_get('production_companies', []),
        'overview': safe_get('overview', 'No overview available.'),
        'genres': safe_get('genres', []),
        'runtime': safe_get('runtime', 'N/A'),
        'vote_average': safe_get('vote_average', 'N/A'),
    }


def display_movie_details(details):
    """Display formatted movie details."""
    st.markdown("---")
    st.subheader(f"📽️ {details['title']} ({details['year']})")

    col1, col2 = st.columns(2)

    with col1:
        directors = details['directors']
        if isinstance(directors, list) and directors:
            st.markdown(f"**Director(s):** {', '.join(str(d) for d in directors[:3])}")
        elif directors and directors != 'N/A':
            st.markdown(f"**Director(s):** {directors}")

        cast = details['cast']
        if isinstance(cast, list) and cast:
            st.markdown(f"**Cast:** {', '.join(str(c) for c in cast[:6])}")
        elif cast and cast != 'N/A':
            st.markdown(f"**Cast:** {cast}")

        studios = details['production_companies']
        if isinstance(studios, list) and studios:
            st.markdown(f"**Studio:** {', '.join(str(s) for s in studios[:3])}")

    with col2:
        genres = details['genres']
        if isinstance(genres, list) and genres:
            st.markdown(f"**Genres:** {', '.join(str(g) for g in genres)}")

        if details['runtime'] and details['runtime'] != 'N/A':
            st.markdown(f"**Runtime:** {details['runtime']} min")

        if details['vote_average'] and details['vote_average'] != 'N/A':
            st.markdown(f"**TMDB Rating:** {details['vote_average']}/10")

    st.markdown("**Overview:**")
    overview = details['overview']
    if len(str(overview)) > 600:
        overview = str(overview)[:600] + "..."
    st.markdown(f"*{overview}*")


def display_movie_row(movie, index):
    """Display a single movie row."""
    col_rank, col_info, col_score = st.columns([0.5, 5, 1])

    with col_rank:
        st.markdown(f"### {index}")

    with col_info:
        year = getattr(movie, 'year', 'N/A')
        st.markdown(f"**{movie.movie_title}** ({year})")

        overview = getattr(movie, 'overview', '')
        if overview and len(str(overview)) > 150:
            overview = str(overview)[:150] + "..."
        if overview:
            st.caption(overview)

    with col_score:
        score = getattr(movie, 'final_score', 0)
        st.metric("Score", f"{score:.2f}")

    return (index, movie.movie_title, movie)


def page_search():
    """Main search/recommendation page."""
    # Get user's first name for greeting
    first_name = st.session_state.user_info.get('first_name', 'there')
    if not first_name:
        first_name = 'there'

    # Personalized greeting
    st.title(f"Hi {first_name}! 👋")
    st.markdown("### What do you feel like watching?")

    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ Settings")

        # Appearance
        appearance = st.selectbox(
            "Appearance",
            options=["dark", "light", "system"],
            index=["dark", "light", "system"].index(st.session_state.appearance),
            help="Choose your preferred theme"
        )
        if appearance != st.session_state.appearance:
            st.session_state.appearance = appearance
            st.rerun()

        st.markdown("---")

        preference_mode = st.selectbox(
            "Preference Mode",
            options=["balanced", "accuracy", "ratings"],
            index=0,
            help="""
            - **Balanced**: Mix of relevance and quality (recommended)
            - **Accuracy**: Pure content matching, ignores ratings
            - **Ratings**: Prioritizes highly-rated/popular movies
            """
        )

        top_n = st.slider(
            "Results per Track",
            min_value=5,
            max_value=20,
            value=10
        )

        st.markdown("---")
        st.markdown("### Example Queries")
        example_queries = [
            "Julia Roberts romances from the 90s",
            "Dark psychological thrillers with a strong female lead",
            "My girlfriend broke up with me - something to cheer me up",
            "Epic war movies set in ancient times",
            "90s action movies with Arnold Schwarzenegger",
            "Coming-of-age movies from the 2010s",
        ]
        for eq in example_queries:
            if st.button(eq, key=f"example_{eq[:20]}"):
                st.session_state.query_input = eq
                st.session_state.search_results = None
                st.session_state.all_movies_list = []

        st.markdown("---")

        # User info display
        if st.session_state.user_info.get('email'):
            st.markdown(f"**Logged in as:** {st.session_state.user_info['email']}")

        if st.button("🚪 Log Out"):
            st.session_state.logged_in = False
            st.session_state.user_info = {}
            st.session_state.page = 'welcome'
            st.session_state.search_results = None
            st.rerun()

    # Main content
    st.markdown("---")

    # Query input
    query = st.text_input(
        "Describe what you're looking for:",
        value=st.session_state.get("query_input", ""),
        placeholder="e.g., 'sci-fi movies from the 80s with great special effects'",
        key="query_box"
    )

    # Search buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)
    with col2:
        if st.button("🎲 Random", use_container_width=True):
            import random
            query = random.choice(example_queries)
            st.session_state.query_input = query
            st.session_state.search_results = None
            st.session_state.all_movies_list = []
            st.rerun()

    # Load recommender
    recommender = load_recommender()

    # Run search
    if search_clicked and query:
        try:
            with st.spinner(f"Finding movies matching: '{query}'..."):
                start_time = time.time()
                result = recommender.recommend(
                    query=query,
                    preference_mode=preference_mode,
                    top_n=top_n
                )
                elapsed = time.time() - start_time

            st.session_state.search_results = result
            st.session_state.last_query = query
            st.session_state.search_time = elapsed
            st.session_state.top_n = top_n

            # Build movie list for dropdown
            all_movies = []
            is_dual = (hasattr(result, 'dual_track_mode') and result.dual_track_mode and
                       hasattr(result, 'entity_track') and result.entity_track and
                       hasattr(result, 'mood_track') and result.mood_track)

            if is_dual:
                for i, m in enumerate(result.entity_track[:top_n], 1):
                    all_movies.append((i, m.movie_title, m))
                start_idx = len(result.entity_track[:top_n]) + 1
                for i, m in enumerate(result.mood_track[:top_n], start_idx):
                    all_movies.append((i, m.movie_title, m))
            else:
                for i, m in enumerate(result.recommendations[:top_n], 1):
                    all_movies.append((i, m.movie_title, m))

            st.session_state.all_movies_list = all_movies

        except Exception as e:
            st.error(f"Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

    # Display results
    if st.session_state.search_results is not None:
        result = st.session_state.search_results
        top_n = st.session_state.get('top_n', 10)

        if result.recommendations:
            st.success(f"Found movies in {st.session_state.get('search_time', 0):.1f}s for: \"{st.session_state.last_query}\"")

            # Show interpretation if available
            if hasattr(result, 'parsed_query') and result.parsed_query:
                with st.expander("Query Interpretation", expanded=False):
                    pq = result.parsed_query
                    cols = st.columns(4)
                    genres = getattr(pq, 'genres', []) or []
                    decades = getattr(pq, 'decades', []) or []
                    actors = getattr(pq, 'actors', []) or []
                    moods = getattr(pq, 'moods', []) or []
                    if genres:
                        cols[0].markdown(f"**Genres:** {', '.join(str(x) for x in genres)}")
                    if decades:
                        cols[1].markdown(f"**Decades:** {', '.join(str(x) for x in decades)}")
                    if actors:
                        cols[2].markdown(f"**Actors:** {', '.join(str(x) for x in actors)}")
                    if moods:
                        cols[3].markdown(f"**Moods:** {', '.join(str(x) for x in moods)}")

            st.markdown("---")

            # Check for DUAL-TRACK mode
            is_dual_track = (hasattr(result, 'dual_track_mode') and result.dual_track_mode and
                             hasattr(result, 'entity_track') and result.entity_track and
                             hasattr(result, 'mood_track') and result.mood_track)

            if is_dual_track:
                st.markdown("### 🎯 Dual-Track Results")
                st.info("Your query has both **content elements** and **mood elements**. Here are recommendations from both perspectives:")

                col_entity, col_mood = st.columns(2)

                with col_entity:
                    st.markdown("#### 📌 Entity Track")
                    st.caption("Content-focused (actors, themes, genres)")
                    for i, movie in enumerate(result.entity_track[:top_n], 1):
                        display_movie_row(movie, i)

                with col_mood:
                    st.markdown("#### 💭 Mood Track")
                    st.caption("Theme/sentiment-focused")
                    start_idx = len(result.entity_track[:top_n]) + 1
                    for i, movie in enumerate(result.mood_track[:top_n], start_idx):
                        display_movie_row(movie, i)

            else:
                st.markdown(f"### 🎬 Top {min(top_n, len(result.recommendations))} Recommendations")
                for i, movie in enumerate(result.recommendations[:top_n], 1):
                    display_movie_row(movie, i)
                    st.markdown("---")

            # Movie details section
            st.markdown("---")
            st.markdown("### 📖 Learn More About a Movie")

            if st.session_state.all_movies_list:
                movie_options = ["Select a movie..."] + [f"{idx}. {title}" for idx, title, _ in st.session_state.all_movies_list]

                selected = st.selectbox(
                    "Choose a movie to see details:",
                    movie_options,
                    key="movie_detail_select"
                )

                if selected != "Select a movie...":
                    selected_title = selected.split(". ", 1)[1] if ". " in selected else selected
                    details = get_movie_details(recommender, selected_title)

                    if details:
                        display_movie_details(details)
                    else:
                        st.warning(f"Could not find details for '{selected_title}'")

        else:
            st.warning("No movies found matching your query. Try a different search!")

    elif not search_clicked:
        if st.session_state.search_results is None:
            st.info("👆 Enter a query above and click Search to get movie recommendations!")

# =============================================================================
# FOOTER
# =============================================================================
def render_footer():
    """Render the footer with links."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center;' class='footer-text'>
            <p>Built with 6-signal hybrid architecture: Collaborative Filtering, Content Similarity,
            Theme Matching, Sentiment Analysis, Zero-shot Tags, and Query Relevance</p>
            <p>Data: TMDB (43,858 movies) | Models: SpaCy NER, Sentence-BERT, LDA, NeuMF</p>
            <p>
                <a href="https://github.com/Anabasis2025/Capstone_Movie_Recommender_Final" target="_blank">
                    📦 GitHub Repository
                </a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# MAIN APP ROUTER
# =============================================================================
def main():
    """Main app router based on current page."""
    page = st.session_state.page

    if page == 'welcome':
        page_welcome()
    elif page == 'auth_menu':
        page_auth_menu()
    elif page == 'signup':
        page_signup()
    elif page == 'login':
        page_login()
    elif page == 'profile':
        page_profile()
    elif page == 'search':
        page_search()
    else:
        page_welcome()

    render_footer()

if __name__ == "__main__":
    main()
