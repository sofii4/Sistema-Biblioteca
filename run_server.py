from waitress import serve
from app import app, init_db
import os

if __name__ == '__main__':
    init_db()
    
    port = int(os.environ.get('PORT', 8000))
    # host='0.0.0.0' permite que outros PCs da biblioteca acessem pelo IP
    print(f"Servidor da Biblioteca iniciado em: http://localhost:{port}")
    serve(app, host='0.0.0.0', port=port)