from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def retrieve():
    # Get the search type (internship, job, or course) from the form
    search_type = request.form['search_type']  # Assuming form field is named 'search_type'
    topic = request.form['topic']  # The user input for the specific topic

    # Construct the Google search URL based on user input
    url = f"https://www.google.com/search?q={topic}+{search_type}"
    
    # Set up the headers to mimic a browser
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Make a request to the Google search page
    response = requests.get(url, headers=headers)
    
    # Initialize an empty list for links
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
            if len(links) == 5:  # Limit to the top 5 results
                break
    else:
        print("Failed to retrieve search results.")
    
    # Render the results page with the list of links
    return render_template('results.html', links=links, search_type=search_type)

if __name__ == '__main__':
    app.run(debug=True)
