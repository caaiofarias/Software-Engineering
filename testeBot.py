import urllib.request
import xml.etree.ElementTree
import sys
import unicodedata
import datetime

TEMPO = {'ec':'Encoberto com Chuvas Isoladas',
         'ci':'Chuvas Isoladas',
         'c':'Chuva',
         'in':'Instável',
         'pp':'Possibilidade de Pancadas de Chuva',
         'cm':'Chuva pela Manhã',
         'cn':'Chuva à Noite',
         'pt':'Pancadas de Chuva à Tarde',
         'pm':'Pancadas de Chuva pela Manhã',
         'np':'Nublado e Pancadas de Chuva',
         'pc':'Pancadas de Chuva',
         'pn':'Parcialmente Nublado',
         'cv':'Chuvisco',
         'ch':'Chuvoso',
         't':'Tempestade',
         'ps':'Predomínio de Sol',
         'e':'Encoberto',
         'n':'Nublado',
         'cl':'Céu Claro',
         'nv':'Nevoeiro',
         'g':'Geada',
         'ne':'Neve',
         'nd':'Não Definido',
         'pnt':'Pancadas de Chuva à Noite',
         'psc':'Possibilidade de Chuva',
         'pcm':'Possibilidade de Chuva pela Manhã',
         'pct':'Possibilidade de Chuva à Tarde',
         'pcn':'Possibilidade de Chuva à Noite',
         'npt':'Nublado com Pancadas à Tarde',
         'npn':'Nublado com Pancadas à Noite',
         'ncn':'Nublado com Possibilidade de Chuva à Noite',
         'nct':'Nublado com Possibilidade de Chuva à Tarde',
         'ncm':'Nublado com Possibilidade de Chuva pela Manhã',
         'npm':'Nublado com Pancadas de Chuva pela Manhã',
         'npp':'Nublado com Possibilidade de Chuva',
         'vn':'Variação de Nebulosidade',
         'ct':'Chuva à Tarde',
         'ppn':'Possibilidade de Pancadas de Chuva à Noite',
         'ppt':'Possibilidade de Pancadas de Chuva à Tarde',
         'ppm':'Possibilidade de Pancadas de Chuva pela Manhã'}

def getxmlcodes(args):
    # Busca do código das cidades
    codigos = []
    for query in args:
        with urllib.request.urlopen('http://servicos.cptec.inpe.br/XML/listaCidades?city={0}'.format(query)) as url:
            content = url.read().decode('iso-8859-1')

        root = xml.etree.ElementTree.fromstring(content)
        codigos.extend([ elem.text for elem in root.findall('./cidade/id') ])

    if len(codigos) == 0:
        raise ValueError("A busca não retornou nenhuma cidade")
    return codigos

def RetornaClima():
    '''
        if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        print('Modo de uso: {0} "CIDADE[1]" "CIDADE[2]" ... "CIDADE[N]"\nO uso de aspas (") é obrigatório'\
               .format(sys.argv[0]))
        print('Exemplo: {0} "São Paulo"'.format(sys.argv[0]))
        print('Não digite o nome do estado')
        sys.exit(1)
    '''
    args = str('recife')
    # Formatar entrada, remover acentos e substituir espaço por %20
    #args = [ unicodedata.normalize('NFKD', elem).encode('ascii', 'ignore').decode('ascii').lower().replace(' ', '%20')
             #for elem in arg ]

    # Obter XML das cidades
    with urllib.request.urlopen('http://servicos.cptec.inpe.br/XML/cidade/{0}/previsao.xml'.format(239)) as url:
        content = url.read().decode('iso-8859-1')

    # Filtrar os dados
    root = xml.etree.ElementTree.fromstring(content)
    dias = [ elem.text for elem in root.findall('previsao/dia') ]
    dias = [ datetime.datetime.strptime(elem, '%Y-%m-%d').strftime('%d/%m/%Y') for elem in dias ]
    clima = [elem.text for elem in root.findall('previsao/tempo') ]
    temperaturas = [ (ma, mi) for ma, mi in zip([elem.text for elem in root.findall('previsao/maxima') ],
                                                   [elem.text for elem in root.findall('previsao/minima') ]) ]

    iuv = [ elem.text for elem in root.findall('previsao/iuv') ]


    # Imprimir resultado
    if root[0].text == "Recife":
        return [TEMPO[clima[1]],temperaturas[1][0],temperaturas[1][1]]#previsao,maxima e minima respectivamente

            

a = RetornaClima()
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from datetime import date
bot = ChatBot("Test")
dataHoje = date.today()
dataimprimir = dataHoje.strftime('%d/%m/%Y')
conversation = [
    "Oi","Ola","Tudo bem?","Tudo ótimo", "Você gosta de programar?",
    "Sim, eu programo em Python","Que dia é hoje?",str(dataimprimir),
    "Previsao do tempo",str(a[0]),"Temperatura Maxima",str(a[1]),
    "Temperatura Minima",str(a[2]),"Qual seu jogo preferido","Eu gosto de jogar Halo","Eu gosto de jogar God of War"
]

trainer = ListTrainer(bot)
trainer.train(conversation)


while True:
    pergunta = input("Usuario: ")
    if pergunta == "sair":
        break
    resposta = bot.get_response(pergunta)
    if float(resposta.confidence) > 0.5:
        print("Test Bot: ", resposta)
    else:
        print("Test Bot: Ainda nao sei responder esta pergunta")

