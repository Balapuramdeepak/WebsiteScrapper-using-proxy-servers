import csv
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    
    url = request.form['url']

   
    response = requests.get(url)

    
    if response.status_code == 200:
      
        soup = BeautifulSoup(response.content, "html.parser")

       
        scraped_data = defaultdict(list)

     
        anchors = soup.find_all("a")
        for anchor in anchors:
            anchor_text = anchor.text.strip()
            href_link = anchor.get("href")
            scraped_data['anchors'].append((anchor_text, href_link))

        paragraphs = soup.find_all("p")
        for paragraph in paragraphs:
            scraped_data['paragraphs'].append(paragraph.text.strip())

      
        divs = soup.find_all("div")
        for div in divs:
            scraped_data['divs'].append(div.text.strip())

        
        images = soup.find_all("img")
        for img in images:
            src = img.get("src")
            scraped_data['images'].append(src)

        
        videos = soup.find_all("video")
        for video in videos:
            src = video.get("src")
            scraped_data['videos'].append(src)

     
        save_to_csv(scraped_data)

       
        host_ip = request.host.split(':')[0]

       
        return render_template('result.html', scraped_data=scraped_data, host_ip=host_ip)

    else:
        return render_template('error.html', error_message="Request failed with status code: " + str(response.status_code))


def save_to_csv(data):
    with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Data'])
        for category, items in data.items():
            for item in items:
                writer.writerow([category, item])

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True)
