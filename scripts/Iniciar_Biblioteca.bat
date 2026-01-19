@echo off
set PROJECT_DIR="C:\Users\Atendimento\Desktop\Projetos\Sistema-Biblioteca"
cd /d %PROJECT_DIR%

echo 🐍 Ativando ambiente...
call venv\Scripts\activate

echo ✨ Iniciando Servidores...
:: O /b inicia em segundo plano na mesma janela
start /b python app.py
echo [OK] Servidor Flask rodando na porta 8000
echo [OK] Dashboard Streamlit rodando na porta 8501
streamlit run relatorio.py --server.port 8501 --server.headless true

pause