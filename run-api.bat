@echo off
echo Iniciando Tracky STT API...
call venv\Scripts\activate
uvicorn app.main:app --reload --port 8080
