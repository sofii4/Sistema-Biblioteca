import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')
DATABASE_URL = os.environ.get('DATABASE_URL')
SENHA_RECEPCAO = os.environ.get('SENHA_RECEPCAO', 'admin123') 

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cursor 

def init_db():
    conn = None
    try:
        conn, cursor = get_db_connection()

        cursor.execute('CREATE EXTENSION IF NOT EXISTS unaccent;')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS obras (
                id SERIAL PRIMARY KEY,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                tipo TEXT,
                idioma TEXT,
                cod_chamada TEXT UNIQUE,
                situacao TEXT DEFAULT 'disponivel',
                estante TEXT,
                letra TEXT,
                cdd TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("--- Tabela 'obras' verificada/criada com sucesso no PostgreSQL ---")
    except psycopg2.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

TIPOS_LABELS = {
    'livro': 'Livro',
    'revista': 'Revista',
    'enciclopedia': 'Enciclopédia',
    'dicionario': 'Dicionário',
    'jornal': 'Jornal',
    'gibi': 'Gibi',
    'livrodidatico': 'Livro Didático'
}

@app.route('/')
def index():
    ITENS_POR_PAGINA = 7 
    pagina = request.args.get('page', 1, type=int)
    offset = (pagina - 1) * ITENS_POR_PAGINA 

    # Filtros de busca
    q = request.args.get('q', '')
    tipo = request.args.get('tipo', 'todos')
    idioma = request.args.get('idioma', 'todos') 
    situacao = request.args.get('situacao', 'todos')
    cod_chamada = request.args.get('cod_chamada', '').strip()
    cdd = request.args.get('cdd', '').strip()
    estante = request.args.get('estante', '').strip()
    letra = request.args.get('letra', '').strip()

    query_base = "FROM obras WHERE 1=1"
    params = []

    if q:
        # unaccent remove acentos do banco e da busca; ILIKE garante o case-insensitive
        query_base += " AND (unaccent(titulo) ILIKE unaccent(%s) OR unaccent(autor) ILIKE unaccent(%s))" 
        params.append(f'%{q}%')
        params.append(f'%{q}%')
    
    if tipo and tipo != 'todos':
        query_base += " AND tipo = %s"
        params.append(tipo)

    if idioma and idioma != 'todos':
        query_base += " AND idioma = %s"
        params.append(idioma)

    if situacao and situacao != 'todos':
        query_base += " AND situacao = %s"
        params.append(situacao)

    if cod_chamada:
        query_base += " AND cod_chamada ILIKE %s"
        params.append(f'%{cod_chamada}%')

    if cdd:
        query_base += " AND cdd ILIKE %s"
        params.append(f'%{cdd}%')

    if estante:
        query_base += " AND estante = %s"
        params.append(estante)

    if letra:
        query_base += " AND letra ILIKE %s"
        params.append(f'%{letra}%')
    
    conn = None
    try:
        conn, cursor = get_db_connection()
        cursor.execute(f"SELECT COUNT(*) AS count {query_base}", params) 
        total_obras = cursor.fetchone()['count']
        total_paginas = (total_obras + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA

        query_final = f"SELECT * {query_base} ORDER BY titulo ASC LIMIT %s OFFSET %s" 
        temp_params = params + [ITENS_POR_PAGINA, offset]
        
        cursor.execute(query_final, temp_params)
        obras = cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Erro na rota index: {e}")
        obras = []
        total_paginas = 0
    finally:
        if conn:
            conn.close()

    return render_template('index.html', 
                            obras=obras, 
                            pagina_atual=pagina, 
                            total_paginas=total_paginas,
                            # Passe os valores selecionados pelo usuário
                            q=q, 
                            tipo=tipo, 
                            idioma=idioma, 
                            situacao=situacao, 
                            cod_chamada=cod_chamada, 
                            cdd=cdd, 
                            estante=estante, 
                            letra=letra,
                            # Passe o dicionário de legendas com um nome diferente
                            tipos_labels=TIPOS_LABELS)

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
    dados_formulario = {}

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        tipo = request.form.get('tipo')
        idioma = request.form.get('idioma')
        situacao = request.form.get('situacao')
        cod_chamada = request.form.get('cod_chamada')
        estante = request.form.get('estante')
        letra = request.form.get('letra', '').strip()
        cdd = request.form.get('cdd')

        dados_formulario = {
            'titulo': titulo, 'autor': autor, 'tipo': tipo, 
            'idioma': idioma, 'situacao': situacao, 'cod_chamada': cod_chamada, 
            'estante': estante, 'letra': letra, 'cdd': cdd
        }

        if letra and not letra.isalpha():
            mensagem = "Erro: O campo 'Letra' deve conter apenas letras (A-Z)."
        elif titulo and autor and cod_chamada:
            conn = None
            try:
                conn, cursor = get_db_connection()
                cursor.execute('SELECT id FROM obras WHERE cod_chamada = %s', (cod_chamada,))
                if cursor.fetchone():
                    mensagem = f"Erro: O código de chamada '{cod_chamada}' já está em uso!"
                else:
                    cursor.execute(
                        '''INSERT INTO obras (titulo, autor, tipo, idioma, cod_chamada, situacao, estante, letra, cdd) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                        (titulo, autor, tipo, idioma, cod_chamada, situacao, estante, letra.upper(), cdd)
                    )
                    conn.commit()
                    mensagem = "Sucesso: Obra cadastrada com sucesso!"
                    dados_formulario = {} 
            except Exception as e:
                mensagem = f"Erro no banco de dados: {e}"
            finally:
                if conn: conn.close()
        else:
            mensagem = "Erro: Título, Autor e Código são obrigatórios."

    return render_template('admin.html', mensagem=mensagem, dados=dados_formulario)


@app.route('/editar/<int:id>', methods=['GET', 'POST']) 
def editar(id):
    if not session.get('usuario_logado'):
        return redirect(url_for('login'))
    
    conn = None
    mensagem = None
    obra = None
    
    try:
        conn, cursor = get_db_connection()
        
        if request.method == 'POST':
            titulo = request.form.get('titulo') 
            autor = request.form.get('autor')
            tipo = request.form.get('tipo')
            idioma = request.form.get('idioma')
            cod_chamada = request.form.get('cod_chamada')
            situacao = request.form.get('situacao')
            estante = request.form.get('estante')
            letra = request.form.get('letra', '').strip()
            cdd = request.form.get('cdd')

            if letra and not letra.isalpha():
                mensagem = "Erro: O campo 'Letra' deve conter apenas letras."
                # Recarrega os dados para não perder o que foi digitado
                obra = {'id': id, 'titulo': titulo, 'autor': autor, 'tipo': tipo, 'idioma': idioma, 
                        'cod_chamada': cod_chamada, 'situacao': situacao, 'estante': estante, 'letra': letra, 'cdd': cdd}
            else:
                cursor.execute('SELECT id FROM obras WHERE cod_chamada = %s AND id != %s', (cod_chamada, id))
                if cursor.fetchone():
                    mensagem = f"Erro: O código '{cod_chamada}' já está sendo usado!"
                    obra = {'id': id, 'titulo': titulo, 'autor': autor, 'tipo': tipo, 'idioma': idioma, 
                            'cod_chamada': cod_chamada, 'situacao': situacao, 'estante': estante, 'letra': letra, 'cdd': cdd}
                else:
                    cursor.execute(
                        '''UPDATE obras SET titulo=%s, autor=%s, tipo=%s, idioma=%s, cod_chamada=%s, situacao=%s, estante=%s, letra=%s, cdd=%s
                        WHERE id=%s''',
                        (titulo, autor, tipo, idioma, cod_chamada, situacao, estante, letra.upper(), cdd, id)
                    )
                    conn.commit()
                    return redirect(url_for('index')) 
        
        if obra is None:
            cursor.execute('SELECT * FROM obras WHERE id = %s', (id,)) 
            obra = cursor.fetchone()
            
    except psycopg2.Error as e:
        mensagem = f"Erro de banco de dados: {e}"
    finally:
        if conn:
            conn.close()

    return render_template('editar.html', obra=obra, mensagem=mensagem)

@app.route('/excluir/<int:id>')
def excluir(id):
    if not session.get('usuario_logado'):
        return redirect(url_for('login'))

    conn = None
    try:
        conn, cursor = get_db_connection()
        cursor.execute('DELETE FROM obras WHERE id = %s', (id,))
        conn.commit()

    except psycopg2.Error as e:
        print(f"Erro na rota excluir: {e}")

    finally:
        if conn:
            conn.close()

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None) 
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Certifica que a tabela existe no Postgre
    init_db() 
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=debug, host=host, port=port)