import ujson, yaml

# Configuration
try:
	with open('config.yml') as ymlFile:
		conf = yaml.load(ymlFile)
except:
	print('Problemas na leitura do arquivo de configuração')
	exit(1)

# Upload messages
try:
	with open('lang.json') as jsonFile:
		message = ujson.load(jsonFile)
except:
	print('Problemas na leitura do arquivo de linguagem')
	exit(1)


# Default Lang
lang = 'en'