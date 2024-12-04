from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Função para ler a coluna A de uma planilha
def read_column_a_from_url(url):
    try:
        data = pd.read_excel(url, usecols="A", header=None)  # Lê somente a coluna A
        return data.dropna().squeeze()  # Remove valores nulos e retorna como série
    except Exception as e:
        return f"Erro ao ler o arquivo {url}: {e}"

@app.route('/process_excel', methods=['POST'])
def process_excel():
    try:
        # Obtendo os parâmetros da requisição
        data = request.get_json()
        url_1 = data.get('url_1')
        url_2 = data.get('url_2')
        
        if not url_1 or not url_2:
            return jsonify({"error": "Ambas as URLs (url_1 e url_2) devem ser fornecidas."}), 400

        # Lê os dados das planilhas
        data_1 = read_column_a_from_url(url_1)
        data_2 = read_column_a_from_url(url_2)

        if isinstance(data_1, str) or isinstance(data_2, str):  # Checa se houve erro
            return jsonify({"error": data_1 if isinstance(data_1, str) else data_2}), 400

        # Garante que ambas as séries têm o mesmo tamanho
        min_length = min(len(data_1), len(data_2))
        data_1 = data_1.iloc[:min_length]
        data_2 = data_2.iloc[:min_length]

        # Soma os valores correspondentes e verifica se são pares ou ímpares
        results = []
        for val1, val2 in zip(data_1, data_2):
            soma = val1 + val2
            parity = "par" if soma % 2 == 0 else "ímpar"
            results.append({
                "val1": val1,
                "val2": val2,
                "soma": soma,
                "parity": parity
            })

        # Retorna os resultados como JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
