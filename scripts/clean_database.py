from sqlalchemy import create_engine, text

# Conectar ao PostgreSQL
engine = create_engine("postgresql://admin:admin@localhost:5432/crypto_db")

def clear_database():
    try:
        with engine.connect() as conn:
            # Desativa restrições temporariamente para evitar problemas de chave estrangeira
            conn.execute(text("TRUNCATE TABLE bitcoin_prices, bitcoin_predictions RESTART IDENTITY CASCADE;"))
            conn.commit()
        print("✅ Todos os dados foram apagados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao apagar os dados: {e}")

# Chamando a função para limpar os dados
clear_database()