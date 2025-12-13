   # 🎬 Movie Recommendation Web App

A full-stack web application that recommends movies based on user preferences, built with React frontend and FastAPI backend.


## 📋 Features
- **Smart Recommendations**: Get movie suggestions based on genre preferences
- **Search History**: View all previous searches and recommendations
- **Responsive Design**: Works on desktop and mobile devices
- **Persistent Storage**: SQLite database stores all recommendations

## 🏗️ Tech Stack
- **Frontend**: React, Axios, CSS3
- **Backend**: FastAPI, SQLite, Python
- **Database**: SQLite
- **Deployment**: (Optional) Vercel/Render

## 📁 Project Structure

movie-recommender/  
├── backend/  
│ ├── main.py # FastAPI server  
│ ├── database.py # Database operations  
│ ├── requirements.txt # Python dependencies  
│ └── README.md # Backend setup instructions  
├── frontend/  
│ ├── public/  
│ │ └── index.html # HTML template  
│ ├── src/  
│ │ ├── App.js # Main React component  
│ │ ├── App.css # Styles  
│ │ └── index.js # React entry point  
│ ├── package.json # Node.js dependencies  
│ └── README.md # Frontend setup instructions  
├── .gitignore # Git ignore file  
└── README.md # This file  




## 🛠️ Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup
1. Navigate to backend folder:
   ```bash
   cd backend



2. Create virtual environment:

  python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate


3. Install dependencies:
pip install -r requirements.txt

4. Run the backend server:
python main.py

Backend will run at: http://localhost:8000


Frontend Setup

1. Navigate to frontend folder:
   cd frontend
2. Instal Dependencies
   npm install
3. Start the development server:
   npm start

   Frontend will run at: http://localhost:3000

   API Endpoints
GET / - API status

POST /recommend - Get movie recommendations

GET /history - Get all previous recommendations


Testing the Application
Open http://localhost:3000 in your browser

Enter a movie preference (e.g., "action movies", "sci-fi")

Click "Get Recommendations"

View the suggested movies

Use "Show History" to see previous searches




## 📸 Screenshots

### Home Page
<img width="1920" height="1080" alt="Screenshot (14)" src="https://github.com/user-attachments/assets/dab8122f-3f5c-4751-a350-fbfbe1b1011e" />
### Search Results
<img width="1920" height="1080" alt="Screenshot (15)" src="https://github.com/user-attachments/assets/6a796933-c968-4e67-a6d8-bc00e9f407b9" />
### History View
<img width="1920" height="1080" alt="Screenshot (16)" src="https://github.com/user-attachments/assets/c3622d58-1693-4531-8c71-9366e770e511" />


 Example Searches
"action movies with female lead"

"sci-fi thrillers"

"emotional dramas"

"animated films"

"horror movies"



Troubleshooting
Backend not starting: Check if port 8000 is free

Frontend not connecting: Ensure backend is running

Database issues: Delete movie_recommendations.db and restart


License
MIT License

👥 Authors
[Rohit Tiwari] - [Your GitHub Profile]
