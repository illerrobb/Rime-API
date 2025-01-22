from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Funzione per trovare rime
def trova_rime(parola):
    url = f"https://www.cercarime.it/{parola}.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": f"Impossibile accedere al sito. Status code: {response.status_code}"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    rime_tags = soup.find_all('li', class_='name')
    rime = [tag.p.a.text.strip() for tag in rime_tags]
    
    return rime

# Endpoint principale
@app.route('/rime', methods=['GET'])
def api_rime():
    parola = request.args.get('parola')
    if not parola:
        return jsonify({"error": "Specifica una parola usando il parametro 'parola'"}), 400
    
    rime = trova_rime(parola)
    return jsonify({"parola": parola, "rime": rime})

# Avvia il server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
