from flask import Flask, render_template, request
from googlesearch import search
import webbrowser
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def retrieve_internships():
    topic = request.form['topic']
    url = f"https://www.google.com/search?q={topic }+internships"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    #response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/url?q='):
                href = href.replace('/url?q=', '')
                href = href.split('&')[0]
                if 'http' in href or 'https' in href:
                    if 'google.com' not in href:  # Exclude links with google.com domain
                        links.append(href)
            if len(links) == 5:
                break
    else:
        print("Failed to retrieve search results.")
    
    # return links    

    return render_template('results.html', links=links)

if __name__ == '__main__':
    app.run(debug=True)
