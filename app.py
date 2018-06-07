import redis
from flask import Flask, request, url_for
import urllib
import bs4
import re

app = Flask(__name__)
#conectando o banco de dados Redis
database = redis.Redis(host='redis', port=6379)

base_html = u"""
    <html>
    <head>
    <title>{title}</title>
    </head>
    <body align="center">
    {body}
    </body>
    </html>
    """

#funcao que recebe uma url, devolve um vetor com os links da pagina
#e armazena os links no database
def getLinksPage(url):
    pag = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(pag)
    
    links = []
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        database.rpush(url,link.get('href'))
        #esses dominios nao aceitam "request", não é possivel obter os links desses sites
        if not (link.get('href').startswith("https://www.linkedin.com/") or
            link.get('href').startswith("https://www.instagram.com/") or
            link.get('href').startswith("https://www.facebook.com/")):
                links.append(link.get('href'))
    
    return links



#pagina para escolher entre visualizar links ja registrados
#ou inserir um novo site para obter os links
@app.route('/')
def index():
  
    exibe = u"""
        <h1>Obtenha as URLs presentes na página de um site!</h1>
        <p>Essa aplicação recebe uma URL de um site desejado, coleta e armazena em um banco
        de dados todas as URLs presentes nessa página fornecida. Por fim, repete esse procedimento
        descrito para cada URL encontrada na página principal.
        </p>
        <p>Escolha abaixo as ações desejadas:
        </p>
        <a href="%s"> Inserir nova URL </a><br/><br/>
        <a href="%s"> Visualizar URLs já cadastradas </a>
        """ % (url_for('new_get'), url_for('view'))
   
    return base_html.format(title = u"Índice", body = exibe)



#pagina onde eh inserido um novo site para obter os links
@app.route('/new_get', methods=["GET", "POST"])
def new_get():
    
    if request.method == "POST":
         url = request.form['url']
         links = getLinksPage(url)#obtendo os links da pagina principal
         for i in links: #obtendo os links dentro de cada link da pagina inicial
             getLinksPage(i)
         
         exibe = u"""
              <h1>Obtenha as URLs presentes na página de um site!</h1>
              <h2>As URLs do site <i>"%s"</i> foram obtidas com sucesso!</h2>
              <a href="%s"> Inserir nova URL </a><br/><br/>
              <a href="%s"> Voltar ao Ínicio </a>
              """ % (url, url_for('new_get'),url_for('index') )

         return base_html.format(title=u"Inserir nova URL", body=exibe)
    
    else:
         exibe = u"""
            <h1>Obtenha as URLs presentes na página de um site!</h1>
            <form method="post" action="/new_get">
            <label>Digite aqui a URL do site:<br />
            (Formato da URL: https://exemplo.com.br)<br/>
            <input type="text" name="url" id="url" value="https://"/>
            </label><br/>
            <input type="submit" value="Enviar" />
            </form><br/>
            <a href="%s"> Voltar ao Ínicio </a>
             """ % (url_for('index'))
         return base_html.format(title=u"Inserir nova URL", body=exibe)


#aqui o usuario vai precisar fornecer uma "key" que será a url de consulta
#pagina para visualizar os links ja armazenados
@app.route('/view', methods=["GET", "POST"])
def view():

   if request.method == "POST":
       url = request.form['url']
       url_template = u"""
               <p>{link}</p>
               """
       busca_urls = [url_template.format(link = link)
                     for link in database.lrange(url, 0, -1)]
       
       todas_urls=u"<br />".join(busca_urls)
       
            
       exibe = u"""
                <h1>Obtenha as URLs presentes na página de um site!</h1>
                <h2>As URLs armazenadas para o site <i>"%s"</i> são:</h2>
                <p>%s</p>
                <a href="%s"> Pesquisar outra URL </a><br/><br/>
                <a href="%s"> Voltar ao Ínicio </a>
                """ % (url, todas_urls, url_for('view'), url_for('index') )
            
       return base_html.format(title=u"Resultado da pesquisa de URLs", body=exibe)
   
   else:
       exibe = u"""
            <h1>Obtenha as URLs presentes na página de um site!</h1>
            <p> Visualize as URLs armazenados para um determinado site
            já cadastrado!
            </p>
            <form method="post" action="/view">
            <label>Digite aqui a URL do site a ser buscado:<br />
            (Formato da URL: https://exemplo.com.br)<br/>
            <input type="text" name="url" id="url" value="https://"/>
            </label><br/>
            <input type="submit" value="Enviar" />
            </form><br/>
            <a href="%s"> Voltar ao Ínicio </a>
            """ % (url_for('index'))
       return base_html.format(title=u"Pesquisar URLs", body=exibe)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
