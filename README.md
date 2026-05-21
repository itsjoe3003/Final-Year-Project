# Hand Gesture Interactive Learning Platform

A multimodal learning platform that combines:
- hand-gesture interaction (MediaPipe + custom keypoint classifier),
- a Flask backend for user/course logic,
- and a React + TypeScript frontend for the student UI.

This repository is a legacy academic project that I am actively cleaning up and documenting for portfolio use.

## Why This Project

This app explores how natural input methods (hand gestures, speech/chat UI) can make learning content more interactive and accessible.

## Core Features

- User authentication and session-based access flows
- Course/topic content delivery
- Assignment-style learning pages (MCQ / matching / fill-in)
- Progress and leaderboard style tracking
- Gesture-recognition pipeline using MediaPipe landmarks + trained classifier
- Frontend web interface built with React + Vite

## Repository Structure

- `Frontend/` - React + TypeScript application (Vite)
- `Backend/` - Flask API backend and controller logic
- `hand/` - hand-gesture data/model scripts and notebooks
- `models/` - gesture model assets
- `webpage/` - older Flask-rendered web app variant and static template assets
- `MapUI/` - map/timeline related UI pages

## Tech Stack

- Frontend: React, TypeScript, Vite, Axios
- Backend: Python, Flask, Flask-CORS, PyMySQL
- CV/ML: OpenCV, MediaPipe, NumPy, Joblib
- Data: MySQL

## Quick Start

### 1) Clone

- Clone this repository and open it in VS Code.

### 2) Backend (Flask)

1. Create and activate a virtual environment.
2. Install dependencies (minimum expected set):
   - flask
   - flask-cors
   - pymysql
   - opencv-python
   - mediapipe
   - numpy
   - joblib
   - deep-translator
3. Configure database credentials:
   - The current code imports `PASS` from `Backend/sql_pwd.py` and `webpage/sql_pwd.py`.
   - Start by copying `Backend/sql_pwd.example.py` to `Backend/sql_pwd.py`.
   - If using the template-based app variant, also copy `webpage/sql_pwd.example.py` to `webpage/sql_pwd.py`.
   - Use local secrets only (do not commit real credentials).
4. Run backend:
   - from `Backend/`, run `python main.py`

### 3) Frontend (React)

1. Open terminal in `Frontend/`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`



## Acknowledgements

Parts of the gesture-recognition workflow are inspired by open MediaPipe gesture-recognition examples and adapted for this project context.
