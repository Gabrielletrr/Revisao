import zipfile
import csv
import hashlib

arquivo_zip = '/home/gabrielletrr/Downloads/bweb_1t_RN_051020221321.zip'
hash_oficial = '/home/gabrielletrr/Downloads/bweb_1t_RN_051020221321.zip.sha512'

with open(arquivo_zip, 'rb') as f:
    hash_calc = hashlib.sha256(f.read()).hexdigest()

with zipfile.ZipFile(arquivo_zip, 'r') as z:
    nome_csv = [n for n in z.namelist() if n.endswith('.csv')][0]
    print('Lendo arquivo:', nome_csv)
    f = z.open(nome_csv)
    leitor = csv.reader((line.decode('latin1') for line in f), delimiter=';')

    next(leitor)

    votos_presidente = {}
    votos_presidente_mun = {}
    votos_governador = {}
    votos_dep_fed = {}
    votos_partido_dep_fed = {}

    total_votos_dep_fed = 0

    for linha in leitor:
      
        if len(linha) < 32:
            continue

        municipio = linha[12].strip()
        cargo     = linha[17].strip().upper()
        partido   = linha[19].strip()
        candidato = linha[30].strip()

        try:
            votos = int(linha[31])
        except:
            continue

      
        if cargo == 'PRESIDENTE':
            votos_presidente[candidato] = votos_presidente.get(candidato, 0) + votos

            if municipio not in votos_presidente_mun:
                votos_presidente_mun[municipio] = {}

            votos_presidente_mun[municipio][candidato] = \
                votos_presidente_mun[municipio].get(candidato, 0) + votos

    
        if cargo == 'GOVERNADOR':
            votos_governador[candidato] = votos_governador.get(candidato, 0) + votos

        if cargo == 'DEPUTADO FEDERAL':
            votos_dep_fed[candidato] = votos_dep_fed.get(candidato, 0) + votos
            total_votos_dep_fed += votos
            votos_partido_dep_fed[partido] = votos_partido_dep_fed.get(partido, 0) + votos


print(' ----- PRESIDENTE MAIS VOTADO NO RN ----- ')
if votos_presidente:
    pres_ven = max(votos_presidente, key=votos_presidente.get)
    print(pres_ven, votos_presidente[pres_ven])
else:
    print('Nenhum dado encontrado para presidente.')

print(' ----- PRESIDENTE MAIS VOTADO POR MUNICÍPIO ----- ')
for mun, dados in votos_presidente_mun.items():
    if not dados:
        continue
    vencedor = max(dados, key=dados.get)
    print(mun, '-', vencedor, dados[vencedor])

print(' ----- GOVERNADOR MAIS VOTADO NO RN ----- ')
if votos_governador:
    gov_ven = max(votos_governador, key=votos_governador.get)
    print(gov_ven, votos_governador[gov_ven])
else:
    print('Nenhum dado encontrado para governador.')

print(' ----- DEPUTADOS FEDERAIS COM MAIS DE 6% DOS VOTOS ----- ')
if total_votos_dep_fed > 0:
    for candidato, votos in votos_dep_fed.items():
        perc = votos * 100 / total_votos_dep_fed
        if perc > 6:
            print(f'{candidato}: {votos} votos ({perc:.2f}%)')
else:
    print('Nenhum dado encontrado de deputado federal.')

print(' ----- TOP 10 DEPUTADOS FEDERAIS MAIS VOTADOS ----- ')
top10 = sorted(votos_dep_fed.items(), key=lambda x: x[1], reverse=True)[:10]
for c, v in top10:
    print(c, v)

print(' ----- VOTOS POR PARTIDO (DEPUTADO FEDERAL) ----- ')
for partido, v in sorted(votos_partido_dep_fed.items(), key=lambda x: x[1], reverse=True):
    print(partido, v)
