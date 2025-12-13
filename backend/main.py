from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sqlite3
import json
from datetime import datetime
import os

app = FastAPI(title="Movie Recommendation API")

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple database class
class MovieDatabase:
    def __init__(self):
        self.db_path = "movie_recommendations.db"
        self.init_database()
        self.init_movies()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                recommended_movies TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def init_movies(self):
        # Predefined movie database
        self.movies = [
            {"title": "Inception", "genre": "Sci-Fi", "description": "A thief who steals corporate secrets through dream-sharing technology.", "year": 2010},
            {"title": "The Dark Knight", "genre": "Action", "description": "Batman faces the Joker, a criminal mastermind who seeks to undermine order and create chaos.", "year": 2008},
            {"title": "Pulp Fiction", "genre": "Crime", "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine.", "year": 1994},
            {"title": "Parasite", "genre": "Thriller", "description": "A poor family schemes to become employed by a wealthy family.", "year": 2019},
            {"title": "The Shawshank Redemption", "genre": "Drama", "description": "Two imprisoned men bond over a number of years.", "year": 1994},
            {"title": "Spirited Away", "genre": "Animation", "description": "A young girl wanders into a world ruled by gods and spirits.", "year": 2001},
            {"title": "Avengers: Endgame", "genre": "Action", "description": "The remaining Avengers must bring back their vanquished allies.", "year": 2019},
            {"title": "La La Land", "genre": "Musical", "description": "A jazz pianist falls for an aspiring actress in Los Angeles.", "year": 2016},
            {"title": "Get Out", "genre": "Horror", "description": "A young African-American visits his white girlfriend's parents.", "year": 2017},
            {"title": "Mad Max: Fury Road", "genre": "Action", "description": "A woman rebels against a tyrannical ruler in postapocalyptic Australia.", "year": 2015}
        ]
    
    def get_recommendations(self, user_input: str) -> List[Dict]:
        input_lower = user_input.lower()
        recommendations = []
        
        # Simple genre matching
        genre_keywords = {
            'action': ['action', 'fight', 'battle', 'war', 'superhero'],
            'sci-fi': ['sci-fi', 'science fiction', 'space', 'future'],
            'drama': ['drama', 'emotional', 'serious'],
            'comedy': ['comedy', 'funny', 'humor'],
            'horror': ['horror', 'scary', 'terror'],
            'crime': ['crime', 'gangster', 'mafia'],
            'animation': ['animation', 'animated', 'cartoon']
        }
        
        # Find matching genres
        matched_genres = []
        for genre, keywords in genre_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                matched_genres.append(genre)
        
        # Get movies matching the genres
        for movie in self.movies:
            if movie['genre'].lower() in matched_genres:
                recommendations.append(movie)
            if len(recommendations) >= 5:
                break
        
        # If no matches, return random movies
        if not recommendations:
            import random
            recommendations = random.sample(self.movies, min(3, len(self.movies)))
        
        return recommendations
    
    def save_recommendation(self, user_input: str, recommendations: List[Dict]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO recommendations (user_input, recommended_movies) VALUES (?, ?)',
            (user_input, json.dumps(recommendations))
        )
        conn.commit()
        conn.close()
    
    def get_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recommendations ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'user_input': row[1],
                'recommended_movies': json.loads(row[2]),
                'timestamp': row[3]
            })
        return result

# Initialize database
db = MovieDatabase()

# Pydantic models
class RecommendationRequest(BaseModel):
    user_input: str

class Movie(BaseModel):
    title: str
    genre: str
    description: str
    year: int

class RecommendationResponse(BaseModel):
    recommendations: List[Movie]

# Routes
@app.get("/")
def read_root():
    return {"message": "Movie Recommendation API is running!"}

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    """Get movie recommendations based on user input"""
    recommendations = db.get_recommendations(request.user_input)
    db.save_recommendation(request.user_input, recommendations)
    return RecommendationResponse(recommendations=recommendations)

@app.get("/history")
def get_history():
    """Get all previous recommendations"""
    return db.get_history()

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)