from connect_database import db
from astrapy.collection import Collection
from CRUDusuario import input_with_cancel

def create_vendedor():
    print("\nInserindo um novo vendedor")
    nome = input_with_cancel("Nome")
    if nome is None: return

    sobrenome = input_with_cancel("Sobrenome")
    if sobrenome is None: return
    
    cpf = input_with_cancel("CPF")
    if cpf is None or cpf.strip() == "":
        print("CPF é obrigatório.")
        return

    collection: Collection = db.get_collection("vendedor")
    existing_vendedor = collection.find_one({"cpf": cpf})
    if existing_vendedor:
        print("Já existe um vendedor cadastrado com este CPF.")
        return

    cnpj = input_with_cancel("CNPJ")
    if cnpj is None: return

    existing_vendedor = collection.find_one({"cnpj": cnpj})
    if existing_vendedor:
        print("Já existe um vendedor cadastrado com este CNPJ.")
        return

    enderecos = []
    while True:
        print("\nEndereço:")
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")

        enderecos.append({
            "rua": rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        })

        adicionar_outro = input_with_cancel("Deseja cadastrar um novo endereço (S/N)? ", cancel_on_n_for_specific_prompt=True)
        if adicionar_outro is None:
            return
        elif adicionar_outro.upper() != 'S':
            break

    collection.insert_one(document={"nome": nome, "sobrenome": sobrenome, "cpf": cpf, "cnpj": cnpj, "end": enderecos})
    print("Vendedor inserido com sucesso.")
    return cpf

def list_vendedores_indexados():
    collection: Collection = db.get_collection("vendedor")
    vendedores = list(collection.find())

    if not vendedores:
        print("Nenhum vendedor encontrado.")
        return None

    print("Vendedores cadastrados:")
    for i, vendedor in enumerate(vendedores):
        print(f"{i+1}. CPF: {vendedor['cpf']}, Nome: {vendedor['nome']}")

    while True:
        try:
            index = int(input("Digite o número do vendedor que deseja atualizar: ")) - 1
            if 0 <= index < len(vendedores):
                return vendedores[index]['cpf']
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def update_vendedor():
    cpf = list_vendedores_indexados()
    if cpf is None:
        return

    collection: Collection = db.get_collection("vendedor")
    vendedor = collection.find_one({"cpf": cpf})

    if vendedor:
        print("Dados atuais do vendedor:", vendedor)

        nome = input_with_cancel(f"Novo nome (ou pressione Enter para manter '{vendedor['nome']}' ): ") or vendedor['nome']
        sobrenome = input_with_cancel(f"Novo sobrenome (ou pressione Enter para manter '{vendedor['sobrenome']}' ): ") or vendedor['sobrenome']
        cnpj = input_with_cancel(f"Novo CNPJ (ou pressione Enter para manter '{vendedor['cnpj']}' ): ") or vendedor['cnpj']

        collection.update_one(
            {"cpf": cpf},
            {
                "$set": {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "cnpj": cnpj,
                }
            }
        )
        print("Vendedor atualizado com sucesso!")
    else:
        print("Vendedor não encontrado.")

def read_vendedor(cpf=None):
    collection: Collection = db.get_collection("vendedor")

    if cpf:
        query = {"cpf": cpf}
        vendedor = collection.find_one(query)
        if vendedor:
            print(vendedor)
        else:
            print("Vendedor não encontrado.")
    else:
        vendedores = collection.find()
        for vendedor in vendedores:
            print(vendedor)