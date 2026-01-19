# Atuaizando o projeto 
 
### 1 - Limapndo o banco de dados 
No terminal do PgAdmin:
```bash
TRUNCATE TABLE obras RESTART IDENTITY;
```

### 2 - Baixar arquivo do projeto no GiHub

### 3 - Trocar variáveis do .env do novo projeto pelos valores antigos

### 4 - No terminal do projeto
(executado como admin no powershell)

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar o ambiente
.\venv\Scripts\activate

# 3. Instalar bibliotecas
pip install --no-index --find-links=./pacotes -r requirements.txt
```

### 5 - Atualizar caminhos no .bat e .vbs

- Testar execução do .bat e portas
    - localhost:8000
    - localhost:8501
    
- Testar cadastro e links com banco de dados.

### 6 - Adicionar novo serviço de inicialização do Windows

- Pressione `Win + R`, digite `shell:startup` e dê Enter.

- Coloque um atalho do seu arquivo `.vbs` dentro dessa pasta que abriu.

( Testar execução do .vbs)

### 7 - Adicionar atalho para dashboard na área de trabalho