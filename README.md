# 📖 Sistema Biblioteca

Aplicação web simples para gerenciamento de um acervo de obras. Permite pesquisar, listar com paginação, adicionar, editar e excluir obras. Possui área administrativa protegida por senha.

## Funcionalidades

- Listagem paginada de obras com busca por título/autor e filtro por tipo.
- Área administrativa para adicionar, editar e excluir obras (acesso por senha).
- Validação para evitar códigos de chamada duplicados.
- Banco SQLite local por padrão.
- Layout intuitivo e responsivo.

## Pré-requisitos

- Python 3.x

## Instalação e uso em modo Desenvolvimento

1. Abrir o Terminal de Comando e entrar na pasta do projeto:

   ```bash
   cd "C:\Users\Seu-User\Pasta\Sistema-Biblioteca"
   ```

2. Criar e ativar virtualenv:

   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Instalar dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configurar variáveis de ambiente:

   - Copiar `.env.example` para `.env` e ajustar:
     SECRET_KEY, DATABASE, SENHA_RECEPCAO


5. (Opcional) - Criar banco de dados SQLite:
   
   Somente se o DB ainda não existir:

   ```bash
   .\venv\Scripts\python -c "from app import init_db; init_db()"
   ```

6. Inicializar e rodar:

   ```bash
   python app.py
   ```

   - A aplicação roda em http://127.0.0.1:8000 por padrão.





## Rodar em modo Produção 

 Usando servidor Gunicorn

1. Ativar venv:
   ```bash
   source venv/bin/activate
   ```

2. Criar DB:
   ```bash
   python -c "from app import init_db; init_db()"
   ```

3. Executar gunicorn (SQLite → 1 worker recomendado):
   ```bash
   venv/bin/gunicorn -w 1 -b 0.0.0.0:8000 --chdir /caminho/para/Sistema-Biblioteca app:app
   ```

   