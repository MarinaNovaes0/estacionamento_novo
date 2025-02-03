# importar o app pra executar a aplicação
from src.routes import app

if __name__ == '__main__':
    app.run(debug=True)
