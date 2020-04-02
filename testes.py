import csv

name_file = input("Digite o nome do arquivo csv: ")
with open('./files/' + name_file + '.txt', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    cont = 0
    categories = set()
    floors = set()
    uas = dict()
    brands = set()
    models = set()
    equipaments = dict()
    for row in reader:
        #Carrega as categorias
        category = row['Material'].split('-')[1]
        categories.add(category)
        #Carrega os andares
        floor = row['U.L.'].split('-')[2]
        floors.add(floor)
        #Carrega as UAs
        ua = row['U.A.'].split('-')
        uas[ua[0]] = ua[1:]
        #Carrega as marcas
        brand = row['Marca']
        brands.add(brand)
        #Carrega os modelos
        model = row['Modelo']
        models.add(model)
        #Carrega os equipamentos
        patrimony = row['Patrimônio']
        warranty = row['Garantia'].split('-')
        if len(warranty) == 6:
            start = warranty[0]+'/'+warranty[1]+'/'+warranty[2]
            end = warranty[3]+'/'+warranty[4]+'/'+warranty[5]
        else:
            start = end = None
        equipaments[patrimony] = [brand, category, model, None, start, end, ua, floor, None, None, False, False, False, False]

    print("Dados carregados com sucesso!")