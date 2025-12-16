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
- PostgreSQL


## 🪟 Rodar em Produção no Windows (Waitress + NSSM)

### Instalar e Configurar PostgreSQL


### Configurando o Ambiente:

1. Criar e ativar um `venv`, instalar dependências:

    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2. Testar localmente (usa `0.0.0.0` por padrão em `run_server.py`):

    ```powershell
    python run_server.py
    ```

3. Abrir porta no Firewall (exemplo PowerShell como Administrador):

    ```powershell
    New-NetFirewallRule -DisplayName "Biblioteca" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000
    ```

4. Variáveis de ambiente e `.env`:

- Defina `DATABASE_URL`, `SECRET_KEY` etc. como variáveis de sistema (Painel de Controle → Sistema → Variáveis de Ambiente) 

6. Banco de dados remoto:

- Se o PostgreSQL estiver em outra máquina, ajuste `postgresql.conf` (`listen_addresses`) e `pg_hba.conf`, e abra a porta `5432` no firewall do host do banco.


## ⚙️ Rodar em Modo de Desenvolvimento Linux

### Configuração do Database 

Antes de iniciar a aplicação, você deve criar o usuário e o banco de dados no seu servidor PostgreSQL.

1.  **Acessar o terminal PostgreSQL** (como superusuário `postgres`):

    ```bash
    sudo -i -u postgres
    psql
    ```

2.  **Criar Usuário e Banco de Dados**
    ```sql
    CREATE USER app_biblioteca WITH ENCRYPTED PASSWORD 'SUA_SENHA_FORTE_APP';
    CREATE DATABASE biblioteca_db OWNER app_biblioteca;
    GRANT ALL PRIVILEGES ON DATABASE biblioteca_db TO app_biblioteca;
    \q
    exit
    ```

###  Preparação do Ambiente 

1.  Abrir o Terminal na pasta do projeto:

    ```bash
    cd /caminho/para/Sistema-Biblioteca
    ```

2.  Criar e ativar o Ambiente Virtual (`venv`):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Instalar dependências (incluindo o driver `psycopg2`):
    ```bash
    pip install -r requirements.txt
    ```

### Configuração de Variáveis de Ambiente

Crie o arquivo `.env` (a partir de `.env.example`) e ajuste as variáveis. **A `DATABASE_URL` é obrigatória.**

```ini
SECRET_KEY=sua_chave_secreta
SENHA_RECEPCAO=admin123
FLASK_DEBUG=False # Use True para desenvolvimento
FLASK_HOST=127.0.0.1
PORT=8000

# Formato: postgresql://USUARIO:SENHA@HOST/NOME_DO_BANCO
DATABASE_URL=postgresql://app_biblioteca:SUA_SENHA_FORTE_APP@localhost/biblioteca_db
```

### Inicializar a Tabela

O código irá criar a tabela `obras` no banco de dados `biblioteca_db` definido no `.env.`

```bash
(venv) python3 -c "from app import init_db; init_db()"
```

### Iniciando o Servidor Python

Para rodar o Flask diretamente (apenas para testes locais):

```bash
python3 app.py
```

- A aplicação roda em `http://127.0.0.1:8000`.

## 🚀 Rodar em Produção Linux (Gunicorn + Systemd)

Para um ambiente Linux, foi utilizado o Gunicorn gerenciado pelo Systemd.

### 1. Criar Arquivo de Serviço Systemd

Crie o arquivo de serviço (`biblioteca.service`) para que o Gunicorn seja iniciado no boot do sistema e rode de forma persistente.

```bash
sudo nano /etc/systemd/system/biblioteca.service
```

**Conteúdo (Ajuste o `User` e o `WorkingDirectory` para o seu usuário e caminho):**

```bash
[Unit]
Description=Servidor Gunicorn para o Sistema de Biblioteca
After=network.target

[Service]
User=sofia  # Seu usuário do sistema
Group=www-data
WorkingDirectory=/home/sofia/Sistema-Biblioteca # Seu caminho
Environment="PATH=/home/sofia/Sistema-Biblioteca/venv/bin" # Seu caminho
ExecStart=/home/sofia/Sistema-Biblioteca/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. Habilitar e Iniciar o Serviço

Execute os comandos para ativar e iniciar o servidor Gunicorn:

```bash
sudo systemctl daemon-reload
sudo systemctl enable biblioteca.service
sudo systemctl start biblioteca.service
```

### 3. Verificar e Acessar

- **Status:** Verifique se está ativo:

  ```bash
  sudo systemctl status biblioteca.service
  ```

- **Acesso:** O servidor estará acessível em `http://IP_DO_SERVIDOR:8000` (Use `127.0.0.1:8000` na máquina hospedeira com redirecionamento de porta).

### 4. Controle do Serviço

Para gerenciar o servidor (após mudanças de código):

| Ação                   | Comando                                     |
| :--------------------- | :------------------------------------------ |
| **Parar**              | `sudo systemctl stop biblioteca.service`    |
| **Reiniciar**          | `sudo systemctl restart biblioteca.service` |
| **Status**             | `sudo systemctl status biblioteca.service`  |
| **Logs em tempo real** | `sudo journalctl -u biblioteca.service -f`  |




