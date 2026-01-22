# What is Language Lilypad?

In this project, we leverage Rust to make a dictionary via async API calls to a text box. The definitions are loaded as they are typed.

Furthermore, for every word in the definition, a definition is provided via hyperlink.

Hence, when using this dictionary, one may leap-frog from word to word, as if they were lilypads.


## Getting Started

The project consists of three main components:
1.  **Dictionary Backend (Node.js/Express):** Handles word definitions using a SQLite database.
2.  **Translation Backend (Python/Flask):** Provides translation services using `argos-translate`.
3.  **Frontend (Next.js):** The user interface for interacting with the dictionary and translator.

### 1. Dictionary Backend
Navigate to the backend directory and start the server:
```bash
cd react_version/backend
npm install
node server.js
```
The server runs on [http://localhost:3000](http://localhost:3000).

### 2. Translation Backend
The translation server requires Python 3 and several dependencies. Navigate to the `react_version` directory:
```bash
cd react_version
pip install flask flask-cors argos-translate
python3 translation_server.py
```
The server runs on [http://localhost:5000](http://localhost:5000).

### 3. Frontend
Navigate to the frontend directory, install dependencies, and start the development server:
```bash
cd react_version/frontend/langlilypad
npm install
npm run dev -- --port 3333
```
Open [http://localhost:3333](http://localhost:3333) with your browser to see the result.


![ejemplo](language_lilypad.gif)