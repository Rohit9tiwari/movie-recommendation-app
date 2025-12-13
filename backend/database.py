import sqlite3
import json
from datetime import datetime
from typing import List, Dict
import os

class Database:
    def __init__(self):
        # Create database in the current directory
        db_path = os.path.join(os.path.dirname(__file__), 'movie_recommendations.db')
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()
        self.load_movies()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                recommended_movies TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def load_movies(self):
        # Predefined movie database with more variety
        self.movies = [
            {"title": "Inception", "genre": "Sci-Fi", "description": "A thief who steals corporate secrets through dream-sharing technology.", "year": 2010},
            {"title": "The Dark Knight", "genre": "Action", "description": "Batman faces the Joker, a criminal mastermind who seeks to undermine order and create chaos.", "year": 2008},
            {"title": "Pulp Fiction", "genre": "Crime", "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.", "year": 1994},
            {"title": "Parasite", "genre": "Thriller", "description": "A poor family schemes to become employed by a wealthy family by infiltrating their household and posing as unrelated, highly qualified individuals.", "year": 2019},
            {"title": "The Shawshank Redemption", "genre": "Drama", "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "year": 1994},
            {"title": "Spirited Away", "genre": "Animation", "description": "A young girl wanders into a world ruled by gods, witches, and spirits.", "year": 2001},
            {"title": "Avengers: Endgame", "genre": "Action", "description": "The remaining Avengers must figure out a way to bring back their vanquished allies for a final showdown with Thanos.", "year": 2019},
            {"title": "La La Land", "genre": "Musical", "description": "A jazz pianist falls for an aspiring actress in Los Angeles.", "year": 2016},
            {"title": "Get Out", "genre": "Horror", "description": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.", "year": 2017},
            {"title": "Mad Max: Fury Road", "genre": "Action", "description": "A woman rebels against a tyrannical ruler in postapocalyptic Australia.", "year": 2015},
            {"title": "The Godfather", "genre": "Crime", "description": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son.", "year": 1972},
            {"title": "Forrest Gump", "genre": "Drama", "description": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man with an IQ of 75.", "year": 1994},
            {"title": "The Matrix", "genre": "Sci-Fi", "description": "A computer hacker learns about the true nature of his reality.", "year": 1999},
            {"title": "Goodfellas", "genre": "Crime", "description": "The story of Henry Hill and his life in the mob.", "year": 1990},
            {"title": "Interstellar", "genre": "Sci-Fi", "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "year": 2014},
            {"title": "The Lord of the Rings: The Fellowship of the Ring", "genre": "Fantasy", "description": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth.", "year": 2001},
            {"title": "Toy Story", "genre": "Animation", "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.", "year": 1995},
            {"title": "The Social Network", "genre": "Drama", "description": "As Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, he is sued by the twins who claimed he stole their idea.", "year": 2010},
            {"title": "Whiplash", "genre": "Drama", "description": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.", "year": 2014},
            {"title": "Joker", "genre": "Thriller", "description": "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society.", "year": 2019}
        ]
    
    def get_recommendations(self, user_input: str) -> List[Dict]:
        """Get movie recommendations based on user input"""
        input_lower = user_input.lower()
        
        # More comprehensive keyword matching
        keyword_matches = []
        
        # Check each movie for keyword matches
        for movie in self.movies:
            score = 0
            
            # Check genre keywords
            if 'action' in input_lower and movie['genre'] == 'Action':
                score += 3
            if 'sci-fi' in input_lower or 'science fiction' in input_lower or 'space' in input_lower:
                if movie['genre'] == 'Sci-Fi':
                    score += 3
            if 'drama' in input_lower or 'emotional' in input_lower:
                if movie['genre'] == 'Drama':
                    score += 3
            if 'comedy' in input_lower or 'funny' in input_lower:
                if movie['genre'] in ['Comedy', 'Animation']:
                    score += 2
            if 'horror' in input_lower or 'scary' in input_lower:
                if movie['genre'] == 'Horror':
                    score += 3
            if 'crime' in input_lower or 'gangster' in input_lower:
                if movie['genre'] == 'Crime':
                    score += 3
            if 'animation' in input_lower or 'animated' in input_lower or 'cartoon' in input_lower:
                if movie['genre'] == 'Animation':
                    score += 3
            if 'fantasy' in input_lower or 'magic' in input_lower:
                if movie['genre'] == 'Fantasy':
                    score += 3
            if 'thriller' in input_lower or 'suspense' in input_lower:
                if movie['genre'] == 'Thriller':
                    score += 3
            
            # Check title and description
            if any(word in movie['title'].lower() for word in input_lower.split()):
                score += 2
            if any(word in movie['description'].lower() for word in input_lower.split()):
                score += 1
            
            # Strong female lead
            if ('female' in input_lower or 'woman' in input_lower or 'girl' in input_lower) and \
               ('strong' in input_lower or 'lead' in input_lower):
                female_lead_movies = ['Mad Max: Fury Road', 'Spirited Away', 'La La Land', 'Get Out']
                if movie['title'] in female_lead_movies:
                    score += 3
            
            if score > 0:
                keyword_matches.append((score, movie))
        
        # Sort by score and get top 5
        keyword_matches.sort(key=lambda x: x[0], reverse=True)
        recommendations = [movie for score, movie in keyword_matches[:5]]
        
        # If no matches, return random movies
        if not recommendations:
            import random
            recommendations = random.sample(self.movies, min(5, len(self.movies)))
        
        return recommendations
    
    def save_recommendation(self, user_input: str, recommendations: List[Dict]):
        """Save recommendation to database"""
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO recommendations (user_input, recommended_movies) VALUES (?, ?)',
            (user_input, json.dumps(recommendations))
        )
        self.conn.commit()
    
    def get_all_recommendations(self):
        """Get all historical recommendations"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM recommendations ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        return [
            {
                'id': row[0],
                'user_input': row[1],
                'recommended_movies': json.loads(row[2]),
                'timestamp': row[3]
            }
            for row in rows
        ]