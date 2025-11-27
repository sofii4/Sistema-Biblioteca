# Sistema Biblioteca

Aplicação web simples para gerenciamento de um acervo de obras. Permite pesquisar, listar com paginação, adicionar, editar e excluir obras. Possui área administrativa protegida por senha.

Funcionalidades

- Listagem paginada de obras com busca por título/autor e filtro por tipo.
- Área administrativa para adicionar, editar e excluir obras (acesso por senha).
- Validação para evitar códigos de chamada duplicados.
- Banco SQLite local por padrão.
- Layout intuitivo e responsivo.

Pré-requisitos

- Python 3.x instalado

Instalação e uso

1. Abrir o Terminal de Comando e entrar na pasta do projeto:
   cd "C:\Users\Seu-User\Pasta\Sistema-Biblioteca"

2. Criar e ativar virtualenv:
   python -m venv venv
   .\venv\Scripts\Activate.ps1

3. Instalar dependências:
   pip install -r requirements.txt

4. Configurar variáveis de ambiente:

   - Copiar `.env.example` para `.env` e ajustar:
     SECRET_KEY, DATABASE, SENHA_RECEPCAO

5. Inicializar e rodar:
   python app.py
   - A aplicação roda em http://127.0.0.1:5000 por padrão.

Observação importante:

- O banco SQLite (biblioteca.db) é local; não comitar o arquivo no repositório.
