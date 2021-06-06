from flask import Flask, render_template, request
import urllib.request as req
import bs4
import urllib
import json
app = Flask(__name__)

@app.route('/')
def index():
    title='flask web site'
    return render_template('index.html',title=title)

@app.route('/news_api',methods=['GET'])
def api():
    q=request.args.get('q')
    n=request.args.get('n')
    w=request.args.get('w')
    n=int(n)
    w=int(w)
    a=urllib.parse.quote(q)
    url="https://www.google.com.tw/search?tbm=nws&q="+a
    
    re=req.Request(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"})
    with req.urlopen(re) as response:
        data=response.read().decode("utf-8")
        root=bs4.BeautifulSoup(data,"html.parser")

    l=root.find_all("div",class_="dbsr",limit=n)
    
    
    article={}
    c=0
    for sl in l:
        c+=1
        key="Airticle"+str(c)
        content=''
        link=sl.a.get('href')
        r=req.Request(link,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"})
        with req.urlopen(r) as response:
            data=response.read().decode("utf-8")
        roots=bs4.BeautifulSoup(data,"html.parser")
        text=roots.find_all("p")
        for txt in text:
            content += str(txt.string)
            if len(content)>w:
                break
        article[key]=content[0:w]
    
    
    
    
    return json.dumps(article,ensure_ascii=False) 



if __name__=='__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)