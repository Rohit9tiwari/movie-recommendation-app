import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [error, setError] = useState('');
  
  const API_URL = 'https://movie-recommendation-backend-5mbn.onrender.com';
  
  const handleSubmit = async (e) => {
  e.preventDefault();
  if (!input.trim()) {
    setError('Please enter a movie preference');
    return;
  }

  setLoading(true);
  setError('');
  
  try {
    console.log('Sending request to:', `${API_URL}/recommend`);
    
   
    const response = await axios.post(
      `${API_URL}/recommend`,  
      {
        user_input: input
      },
      {
        timeout: 45000, 
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    );
    
    console.log('Response received:', response.data);
    setRecommendations(response.data.recommendations);
    setShowHistory(false);
    
 
    fetchHistory();
    
  } catch (error) {
    console.error('Full error object:', error);
    
    if (error.code === 'ECONNABORTED') {
      setError('Backend is waking up (takes up to 60s on free tier). Please wait and try again.');
    } else if (error.response) {
      
      setError(`Server error: ${error.response.status} - ${error.response.data?.message || 'Unknown error'}`);
    } else if (error.request) {
      
      setError('No response from server. The backend might be asleep or the URL is wrong.');
    } else {
     
      setError(`Request error: ${error.message}`);
    }
    
    
    const fallbackMovies = [
      { title: "Inception", genre: "Sci-Fi", description: "A mind-bending thriller about dream-sharing technology.", year: 2010 },
      { title: "The Dark Knight", genre: "Action", description: "Batman faces the Joker in this epic superhero film.", year: 2008 },
      { title: "Parasite", genre: "Thriller", description: "A poor family schemes to become employed by a wealthy family.", year: 2019 }
    ];
    setRecommendations(fallbackMovies);
  } finally {
    setLoading(false);
  }
};

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}history`);
      setHistory(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const toggleHistory = () => {
    if (!showHistory) {
      fetchHistory();
    }
    setShowHistory(!showHistory);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🎬 Movie Recommender</h1>
        <p>Describe what kind of movies you like, and get recommendations!</p>
      </header>

      <main className="main-content">
        <div className="search-section">
          <form onSubmit={handleSubmit} className="search-form">
            <input
              type="text"
              value={input}
              onChange={(e) => {
                setInput(e.target.value);
                setError('');
              }}
              placeholder="E.g., 'action movies', 'sci-fi', 'drama'"
              className="search-input"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="search-button" 
              disabled={loading}
            >
              {loading ? 'Searching...' : 'Get Recommendations'}
            </button>
          </form>

          {error && <div className="error">{error}</div>}

          <button onClick={toggleHistory} className="history-button">
            {showHistory ? 'Hide History' : 'Show History'}
          </button>
        </div>

        {showHistory ? (
          <div className="history-section">
            <h2>Previous Recommendations</h2>
            {history.length === 0 ? (
              <p>No history yet.</p>
            ) : (
              <div className="history-list">
                {history.map((item) => (
                  <div key={item.id} className="history-item">
                    <div className="history-header">
                      <strong>Search:</strong> "{item.user_input}"
                      <span className="timestamp">
                        {new Date(item.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <div className="movie-tags">
                      {item.recommended_movies.map((movie, idx) => (
                        <span key={idx} className="movie-tag">
                          {movie.title}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="recommendations-section">
            {recommendations.length > 0 ? (
              <>
                <h2>Recommended Movies</h2>
                <div className="recommendations-grid">
                  {recommendations.map((movie, index) => (
                    <div key={index} className="movie-card">
                      <div className="movie-header">
                        <h3>{movie.title} ({movie.year})</h3>
                        <span className="genre">{movie.genre}</span>
                      </div>
                      <p className="description">{movie.description}</p>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="welcome">
                <p>Try searching for movies by genre or description!</p>
                <div className="examples">
                  <p>Examples:</p>
                  <ul>
                    <li>"action movies with female lead"</li>
                    <li>"sci-fi thrillers"</li>
                    <li>"emotional dramas"</li>
                    <li>"animated films"</li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Movie Recommendation App | Backend:https://movie-recommendation-backend-5mbn.onrender.com</p>
      </footer>
    </div>
  );
}

export default App;
