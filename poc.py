from flask import Flask, request, jsonify, after_this_request
import requests
import uuid
import json
import re

app = Flask(__name__)

@app.route('/proxy', methods=['GET'])
def proxy():
    @after_this_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*' 
        return response

    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Brak zapytania'}), 400

    encoded_query = requests.utils.quote(query)
    search_id = str(uuid.uuid4())

# diffrent url for turbo mode -->
#turbo mode:  -   url = f"https://explorer-search.fly.dev/submitSearch?queryData=%5B%7B\"searchbox_query\"%3A\"{encoded_query}\"%2C\"search_id\"%3A\"{search_id}\"%2C\"index%22%3A0%2C%22type%22%3A%22initial_searchbox%22%2C%22clicked_category%22%3Anull%2C%22staged_image%22%3Anull%2C%22location%22%3Anull%7D%5D&userid_auth="YOUR AUTH USERID HERE"&userid_local="YOUR LOCAL USERID HERE"&model=turbo&search_id={search_id}"

#advanced mode:    
    url = f"https://explorer-search.fly.dev/submitSearch?queryData=[{{\"searchbox_query\":\"{encoded_query}\",\"search_id\":\"{search_id}\",\"index\":0,\"type\":\"initial_searchbox\",\"clicked_category\":null,\"staged_image\":null,\"location\":null}}]&userid_auth=test&userid_local=test&model=advanced&search_id={search_id}"
    try:
        response = requests.get(url, headers={'Accept': 'application/json'}, timeout=5)
        response.encoding = 'utf-8'


        print(f"Żądanie do API: {url}")
        print(f"Odpowiedź z API (status): {response.status_code}")


        response.raise_for_status()


        raw_data = response.text

        print(f"Odpowiedź z API (treść): {raw_data}")



        data = []
        for line in raw_data.splitlines():
            if line.startswith("data: "):
                try:
                    json_part = json.loads(line[6:])
                    data.append(json_part)
                except json.JSONDecodeError as e:
                    print(f"Błąd parsowania JSON w linii: {line}")
                    print(f"Szczegóły błędu JSON: {e}")
                    return jsonify({'error': f'Błąd parsowania JSON w linii: {line}'}), 500
            elif line.strip(): 
               print(f"Nieoczekiwana linia: {line}")



        return jsonify(data)


    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas żądania do API: {e}")
        return jsonify({'error': 'Błąd podczas żądania do API'}), 500

    except json.JSONDecodeError as e:  
        print(f"Błąd parsowania JSON (przed czyszczeniem): {e}")
        return jsonify({'error': 'Nieprawidłowy JSON (przed czyszczeniem)'}), 500



if __name__ == '__main__':

    from flask import send_from_directory
    import os



    static_file_dir = os.path.join(os.path.dirname(__file__), '')

    @app.route('/') 
    def serve_proxy_html():
        return send_from_directory(static_file_dir, 'proxy.html')

    app.run(debug=True, port=5000)
