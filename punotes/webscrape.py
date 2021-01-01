import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)
values=[]

@app.route('/')
def notes():
    page=requests.get('http://pue.kar.nic.in/PUE/support_html/recogn/ncert_IIqb.htm')
    bSoup=BeautifulSoup(page.content,'html.parser')
    links_list=bSoup.find_all('a')
    for link in links_list:
        if 'href' in link.attrs:
            values.append(str(link.attrs['href'])+'\n')        
    return render_template('display.html', values=values)

if __name__ == '__main__':
    app.run(debug = True)
© 2021 GitHub, Inc.
