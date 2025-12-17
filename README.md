# 📖 Sistema Biblioteca

Aplicação web para gerenciamento de um acervo de obras. Permite pesquisar, listar com paginação, adicionar, editar e excluir obras. Possui área administrativa protegida por senha.

## Pré-requisitos

- Python 3.x
- PostgreSQL 

## Instalação

### 1. Instalar o Python
 - Execute o Instalador
 
  ✅ Marque a caixa **"Add Python.exe to PATH"** antes de clicar em *Install Now*

  ### 2. Instalar o PostgreSQL

  - Siga a instalação padrão
  - Defina uma senha para o usuário `postgres`.
  - Ao finalizar, abra o **pgAdmin 4.**
  - Clique com o botão direito em `Databases` > `Create` > `Database....`
  - Nomeie como: `biblioteca_db.`

### 3. Preparar a Pasta do Projeto

- Coloque a pasta do projeto em um local definitivo.

- Crie um arquivo chamado .env na raiz da pasta com o seguinte conteúdo:

    ```bash
    DATABASE_URL=postgresql://postgres:SUA_SENHA_AQUI@localhost:5432/biblioteca_db
    SECRET_KEY=uma_chave_segura_aleatoria
    FLASK_DEBUG=False 
    FLASK_HOST=127.0.0.1
    PORT=5000 #ou outra
    SENHA_RECEPCAO=admin123 (Sua senha de login)
    ```

### 4. Configurar o Ambiente Python

Abra o PowerShell dentro da pasta do projeto e execute:

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar o ambiente
.\venv\Scripts\activate

# 3. Instalar bibliotecas
pip install -r requirements.txt
```


## Liberação de Acesso (Rede Local)

Para que outras máquinas acessem o sistema:

- Abra o **Firewall do Windows com Segurança Avançada**.

- Em **Regras de Entrada**, crie uma "Nova Regra".

- Escolha **Porta** > **TCP** > Porta específica: **5000** (ou a porta configurada).

- Selecione **Permitir a conexão** e marque as opções *Particular e Público*.


## Automação para o Cliente

### 1. Criar Arquivo de Inicialização

Para facilitar o uso, crie um arquivo chamado `Iniciar_Sistema.bat` na área de trabalho do cliente:

```bash
@echo off
title SERVIDOR DA BIBLIOTECA - NAO FECHAR
cd /d "C:\Caminho\Para\A Pasta\Do\Projeto"
call venv\Scripts\activate
python run_server.py
pause
```

### 2. Inicializar Automaticamente com Windows

- Pressione `Win + R`, digite `shell:startup` e dê Enter.

- Coloque um **atalho** do seu arquivo `.bat`dentro dessa pasta que abriu.

### 3. Ícone de Acesso Fácil

Isso permite que o cliente abra a página do sistema sem precisar digitar o endereço.

- Clique com o botão direito na Área de Trabalho

- Vá em **Novo** > **Atalho**.]

- No campo "*Digite o local do item*", coloque: `http://localhost:5000` (ou a porta que você configurou).

- Clique em **Avançar** e dê o nome desejado.

- Clique em **Concluir**.

## Como acessar

- **No PC Servidor:** Abra o ícone na Área de Trabalho, ou o Chrome e acesse http://localhost:5000.

- **Em outros dispositivos:** Acesse `http://[IP_DO_SERVIDOR]:5000`. (Para descobrir o IP, use o comando `ipconfig` no terminal).
