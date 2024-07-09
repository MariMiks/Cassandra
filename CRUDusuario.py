from astrapy.collection import Collection
from connect_database import db

def input_with_cancel(prompt, cancel_keyword="CANCELAR", cancel_on_n_for_specific_prompt=False):
    resposta = input(f"{prompt} (digite {cancel_keyword} para abortar): ")
    if resposta.upper() == cancel_keyword:
        print("Operação cancelada.")
        return None
    if cancel_on_n_for_specific_prompt and resposta.upper() == 'N':
        return resposta
    return resposta

def create_usuario():
    print("\nInserindo um novo usuário")
    nome = input_with_cancel("Nome")
    if nome is None:
        return

    sobrenome = input_with_cancel("Sobrenome")
    if sobrenome is None:
        return

    cpf = input_with_cancel("CPF")
    if cpf is None or cpf.strip() == "":
        print("CPF é obrigatório.")
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

        adicionar_outro = input_with_cancel("Deseja adicionar outro endereço? (S/N): ", cancel_on_n_for_specific_prompt=True)
        if adicionar_outro is None:
            return
        elif adicionar_outro.upper() != 'S':
            break

    print(f"\n{nome} {sobrenome} - {cpf} - {enderecos}")

    collection: Collection = db.get_collection("usuario")
    existing_user = collection.find_one({"cpf": cpf})
    if existing_user:
        print("Já existe um usuário cadastrado com este CPF.")
        return

    collection.insert_one(document={"nome": nome, "sobrenome": sobrenome, "cpf": cpf, "end": enderecos})
    print("Usuário inserido com sucesso.")
    return cpf

def list_usuarios_indexados():
    collection: Collection = db.get_collection("usuario")
    users = list(collection.find())

    if not users:
        print("Nenhum usuário encontrado.")
        return None

    print("Usuários cadastrados:")
    for i, user in enumerate(users):
        print(f"{i+1}. CPF: {user['cpf']}, Nome: {user['nome']}")

    while True:
        try:
            index = int(input("Digite o número do usuário que deseja atualizar: ")) - 1
            if 0 <= index < len(users):
                return users[index]['cpf']
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def update_usuario():
    cpf = list_usuarios_indexados()
    if cpf is None:
        return 

    collection: Collection = db.get_collection("usuario")
    existing_user = collection.find_one({"cpf": cpf})

    if existing_user:
        print("Dados atuais do usuário:", existing_user)

        nome = input_with_cancel(f"Novo nome (ou pressione Enter para manter '{existing_user['nome']}' ): ") or existing_user['nome']
        sobrenome = input_with_cancel(f"Novo sobrenome (ou pressione Enter para manter '{existing_user['sobrenome']}' ): ") or existing_user['sobrenome']

        print("Atualizar endereço?")
        atualizar_endereco = input_with_cancel("(S/N): ", cancel_on_n_for_specific_prompt=True)
        if atualizar_endereco is None: 
            return
        elif atualizar_endereco.upper() == 'S':
            rua = input("Rua: ")
            num = input("Num: ")
            bairro = input("Bairro: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            cep = input("CEP: ")

            end = {
                "rua": rua,
                "num": num,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "cep": cep
            }
        else:
            end = existing_user['end']

        collection.update_one(
            {"cpf": cpf},
            {
                "$set": {
                    "nome": nome, 
                    "sobrenome": sobrenome,
                    "end": end
                }
            }
        )
        print("Usuário atualizado com sucesso!")
    else:
        print("Usuário não encontrado.")

def read_usuario(cpf=None):
    collection: Collection = db.get_collection("usuario")

    if cpf:
        query = {"cpf": cpf}
        user = collection.find_one(query)
        if user:
            print(user)
        else:
            print("Usuário não encontrado.")
    else:
        users = collection.find()
        for user in users:
            print(user)
