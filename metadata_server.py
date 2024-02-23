from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

''' http://127.0.0.1:5000/get-metadata?url= '''

@app.route('/get-metadata', methods=['GET'])
def get_metadata():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraction des métadonnées
        title = soup.find('title').text if soup.find('title') else 'No title found'
        description = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if description:
            description = description['content']
        else:
            description = 'No description found'

        image = soup.find('meta', attrs={'property': 'og:image'})
        if image:
            image = image['content']
        else:
            image = 'No image found'

        metadata = {
            "title": title,
            "description": description,
            "image": image
        }

        return jsonify(metadata)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
