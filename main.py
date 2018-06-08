import httplib2

url = "https://www.fnde.gov.br/siope/dadosInformadosMunicipio.do?acao=pesquisar&pag=result&anos={}&periodos=1&cod_uf={}&municipios={}&admin=3&planilhas=124&descricaoItem=Consolidado+de+Receita&descricaodoItem=&nivel="
h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

def getCityData(year, ufId, cityId):

    urlSend = str.format(url, year, ufId, cityId)
    response, content = h.request(urlSend)

    content = str(content)
    vet = content.split("<p><label>Munic&iacute;pios:</label>&nbsp;")
    name = ""
    for s in vet[1]:
        if s != '<':
            name += s
        else:
            break

    vet = content.split("<div class=\"number\"><strong>")
    value = ""
    for s in vet[2]:
        if s != '<':
            value += s
        else:
            break;

    cityData = {}
    cityData['name'] = name
    cityData['value'] = value
    return cityData


citiesDatas = list()
citiesError = list()
file = open('out.csv', 'a')
fileIn = open('cities.csv', 'r')

text = fileIn.read()

vText = text.split("\n")

cities = list()
for s in vText:
    line = s.split(",")

    if len(line) >= 2:
        city = dict()
        city['ufId'] = line[0]
        city['id'] = line[1]

        cities.append(city)

countError = 0
errorLimit = 10
countFound = 0
for city in cities:
    try:
        print("buscando cidade " + str(city['id']) + " | " + str(countFound) + " de " + str(len(cities)))
        cityData = getCityData(2015, city['ufId'], city['id'])
        text = str(city['ufId']) + ";" + str(city['id']) + ";" + cityData['name'] + ";" + cityData['value'] + ";\r\n"
        file.write(text)
        countFound += 1
    except IndexError:
        if countError > errorLimit:
            countError = 0
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> erro na cidade " + str(city['id']))
        else:
            countError += 1


file.close()