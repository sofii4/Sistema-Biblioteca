import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['DATABASE'] = os.environ.get('DATABASE', 'biblioteca.db')
SENHA_RECEPCAO = os.environ.get('SENHA_RECEPCAO', 'admin123') 

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(app.config['DATABASE']):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS obras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                tipo TEXT,
                idioma TEXT,
                cod_chamada TEXT,
                situacao TEXT DEFAULT 'disponivel',
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("--- Banco de dados verificado/criado com sucesso ---")

# Rotas
@app.route('/')
def index():
    
    # Configuração paginação
    ITENS_POR_PAGINA = 7 
    pagina = request.args.get('page', 1, type=int)
    offset = (pagina - 1) * ITENS_POR_PAGINA

    q = request.args.get('q', '')
    tipo = request.args.get('tipo', 'todos')
    idioma = request.args.get('idioma', 'todos') 
    situacao = request.args.get('situacao', 'todos')   
    cod_chamada = request.args.get('cod_chamada', '').strip() 
    query_base = "FROM obras WHERE 1=1"
    params = []

    if q:
        query_base += " AND (titulo LIKE ? OR autor LIKE ?)"
        params.append(f'%{q}%')
        params.append(f'%{q}%')
    
    if tipo and tipo != 'todos':
        query_base += " AND tipo = ?"
        params.append(tipo)

    if idioma and idioma != 'todos':
        query_base += " AND idioma = ?"
        params.append(idioma)

    if situacao and situacao != 'todos':
        query_base += " AND situacao = ?"
        params.append(situacao)

    if cod_chamada:
        # busca parcial por código de chamada; use '=' se preferir correspondência exata
        query_base += " AND (cod_chamada = ? OR cod_chamada LIKE ?)"
        params.append(cod_chamada)
        params.append(f'{cod_chamada}%')
    
    conn = get_db_connection()

    total_obras = conn.execute(f"SELECT COUNT(*) {query_base}", params).fetchone()[0]
    total_paginas = (total_obras + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA

    query_final = f"SELECT * {query_base} ORDER BY titulo ASC LIMIT ? OFFSET ?"
    params.append(ITENS_POR_PAGINA)
    params.append(offset)
    
    obras = conn.execute(query_final, params).fetchall()
    conn.close()
    
    return render_template('index.html', 
                           obras=obras, 
                           pagina_atual=pagina, 
                           total_paginas=total_paginas,
                           q=q,
                           tipo=tipo,
                           idioma=idioma,
                           situacao=situacao,
                           cod_chamada=cod_chamada)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == SENHA_RECEPCAO:
            session['usuario_logado'] = True
            return redirect(url_for('index')) 
        else:
            flash('Senha incorreta!')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('usuario_logado'):
        return redirect(url_for('login'))
    
    mensagem = None
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        tipo = request.form.get('tipo')
        idioma = request.form.get('idioma')
        cod_chamada = request.form.get('cod_chamada')

        if titulo and autor and cod_chamada:
            conn = get_db_connection()

            # Verifica se o código já está em uso
            livro_existente = conn.execute('SELECT id FROM obras WHERE cod_chamada = ?', (cod_chamada,)).fetchone()

            if livro_existente:
                mensagem = f"Erro: O código '{cod_chamada}' já está em uso por outro livro!"
            else:
                conn.execute('INSERT INTO obras (titulo, autor, tipo, idioma, cod_chamada) VALUES (?, ?, ?, ?, ?)',
                             (titulo, autor, tipo, idioma, cod_chamada))
                conn.commit()
                mensagem = "Sucesso: Obra adicionada ao acervo!"
            
            conn.close()
        else:
            mensagem = "Erro: Título, Autor e Código de Chamada são obrigatórios."

    return render_template('admin.html', mensagem=mensagem)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not session.get('usuario_logado'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    mensagem = None
    obra = None
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        tipo = request.form.get('tipo')
        idioma = request.form.get('idioma')
        cod_chamada = request.form.get('cod_chamada')
        situacao = request.form.get('situacao')

        # Verifica se o código já está em uso
        livro_existente = conn.execute(
            'SELECT id FROM obras WHERE cod_chamada = ? AND id != ?', 
            (cod_chamada, id)
        ).fetchone()

        if livro_existente:
            mensagem = f"Erro: O código '{cod_chamada}' já está sendo usado por outro livro!"
            # Recarrega os dados do form para não perder o que foi digitado
            obra = {
                'id': id, 'titulo': titulo, 'autor': autor, 
                'tipo': tipo, 'idioma': idioma, 
                'cod_chamada': cod_chamada, 'situacao': situacao
            }
        else:
            conn.execute('''
                UPDATE obras 
                SET titulo=?, autor=?, tipo=?, idioma=?, cod_chamada=?, situacao=?
                WHERE id=?
            ''', (titulo, autor, tipo, idioma, cod_chamada, situacao, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index')) 
    
    if obra is None:
        obra = conn.execute('SELECT * FROM obras WHERE id = ?', (id,)).fetchone()
        conn.close()

    return render_template('editar.html', obra=obra, mensagem=mensagem)

@app.route('/excluir/<int:id>')
def excluir(id):
    if not session.get('usuario_logado'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM obras WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=debug, host=host, port=port)

