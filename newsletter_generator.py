import requests

def generate_newsletter_html(article_urls, api_endpoint):
    newsletter_html_parts = ['<div style="font-family: Arial, sans-serif;">']

    for url in article_urls:
        # Construct the API URL
        api_url = f"{api_endpoint}?url={url}"
        
        try:
            # Fetch the metadata from the API
            response = requests.get(api_url)
            if response.status_code == 200:
                # Parse the JSON response
                metadata = response.json()
                image_src = metadata['image']
                title = metadata['title']
                description = metadata['description']
                
                # HTML code for a single article thumbnail
                article_html = f'''
                <div style="border: 1px solid gray; border-radius: 10px; margin-bottom: 20px; padding: 10px;">
                    <img src="{image_src}" alt="{title}" style="width: 100%; border-radius: 10px;">
                    <h2>{title}</h2>
                    <p>{description}</p>
                    <a href="{url}" style="background-color: rgb(250, 204, 21); color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Voir +</a>
                </div>
                '''
                newsletter_html_parts.append(article_html)
            else:
                print(f"Failed to fetch metadata for {url}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    newsletter_html_parts.append('</div>')
    return ''.join(newsletter_html_parts)

# Example usage
api_endpoint = "http://127.0.0.1:5000/get-metadata"
article_urls = [
    "https://www.cline-research.com/articles-cline/psychiatrie/le-ptsd-a-l-honneur-au-congres-de-l-encephale/",
    "https://www.cline-research.com/articles-cline/recherche-clinique/nouvelles-technologies-et-essais-cliniques/"
]
newsletter_html = generate_newsletter_html(article_urls, api_endpoint)
print(newsletter_html)
