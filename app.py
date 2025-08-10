import streamlit as st
import pickle
import requests

# TMDB API Key
API_KEY = "b2ffc7a99165a61ef86850c2011ec0cf"

# Function to fetch movie details from TMDB
def fetch_movie_details(movie_id):
    """
    Fetch details of a movie, including poster, overview, and release date.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_url = f"https://image.tmdb.org/t/p/w500/{data.get('poster_path', '')}"
        overview = data.get('overview', 'Overview not available.')
        release_date = data.get('release_date', 'Release date not available.')
        return poster_url, overview, release_date
    else:
        return None, "Details not available.", "Unknown"

# Function to recommend movies based on the selected movie
def recommend(movie):
    """
    Recommend movies similar to the selected movie.
    Returns a list of movie details including names and posters.
    """
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]  # Top 5 similar movies (excluding the selected movie)

    recommended_movies = []
    for i in movie_indices:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster, overview, release_date = fetch_movie_details(movie_id)
        recommended_movies.append({
            "title": title,
            "poster": poster,
            "overview": overview,
            "release_date": release_date
        })
    return recommended_movies

# Load the data
movies = pickle.load(open('movies.pkl', 'rb'))  # Ensure the 'movie_id' column exists
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit App Layout
st.set_page_config(page_title="Movie Recommender System", layout="wide", page_icon="🎥")

# Sidebar
st.sidebar.title("⚙️ Options")
st.sidebar.write("Use the options below to interact with the app.")
selected_movie_name = st.sidebar.selectbox("🎬 Select a movie:", movies_list)

# Header
st.title("🎥 Movie Recommender System")
st.markdown("""
Welcome to the **Movie Recommender System**!  
Select a movie from the sidebar to get personalized recommendations.  
""")
st.markdown("---")

# Recommend button
if st.sidebar.button("Recommend"):
    st.subheader(f"Movies similar to **{selected_movie_name}**:")
    recommendations = recommend(selected_movie_name)

    # Display all recommendations side-by-side
    cols = st.columns(len(recommendations))  # Create columns dynamically

    for idx, movie in enumerate(recommendations):
        with cols[idx]:
            st.image(movie["poster"], use_container_width=True)
            st.write(f"**{movie['title']}**")
            st.write(f"📅 {movie['release_date']}")
            # Shorten overview to avoid long text
            short_overview = movie['overview'][:100] + "..." if len(movie['overview']) > 100 else movie['overview']
            st.caption(short_overview)
