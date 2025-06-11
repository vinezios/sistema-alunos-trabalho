import json
import os

ARQUIVO_JSON = "dados.json"
dados_iniciais = {"alunos": [], "disciplinas": [], "notas": []}

# --- FUNÇÕES BASE ---
def carregar_dados():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados_iniciais, f, indent=4)
        return dados_iniciais

def salvar_dados(dados):
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# --- FUNÇÃO GENÉRICA PARA CRUD ---
def gerenciar_entidade(entidade, campos, chave):
    dados = carregar_dados()
    while True:
        print(f"\n--- MENU {entidade.upper()} ---")
        print("1. Cadastrar\n2. Listar\n3. Alterar\n4. Excluir\n5. Voltar")
        op = input("Opção: ").strip()
        
        if op == "1":  # CADASTRAR
            novo = {}
            for campo in campos:
                novo[campo] = input(f"{campo.replace('_', ' ').title()}: ").strip()
            if any(item[chave] == novo[chave] for item in dados[entidade]):
                print(f"Erro: {chave.replace('_', ' ')} já existe!")
                continue
            dados[entidade].append(novo)
            salvar_dados(dados)
            print(f"{entidade.title()} cadastrado(a) com sucesso!")
        
        elif op == "2":  # LISTAR
            print(f"\n--- LISTA DE {entidade.upper()} ---")
            for item in dados[entidade]:
                print(" | ".join(f"{k}: {v}" for k, v in item.items()))
        
        elif op == "3":  # ALTERAR
            busca = input(f"Digite a {chave.replace('_', ' ')} para alterar: ").strip()
            for item in dados[entidade]:
                if item[chave] == busca:
                    for campo in campos:
                        novo_valor = input(f"{campo.replace('_', ' ').title()} (atual: {item[campo]}): ").strip()
                        if novo_valor: item[campo] = novo_valor
                    salvar_dados(dados)
                    print(f"{entidade.title()} alterado(a) com sucesso!")
                    break
            else: print(f"Erro: {entidade[:-1]} não encontrado(a)!")
        
        elif op == "4":  # EXCLUIR
            busca = input(f"Digite a {chave.replace('_', ' ')} para excluir: ").strip()
            for i, item in enumerate(dados[entidade]):
                if item[chave] == busca:
                    dados[entidade].pop(i)
                    salvar_dados(dados)
                    print(f"{entidade.title()} excluído(a) com sucesso!")
                    break
            else: print(f"Erro: {entidade[:-1]} não encontrado(a)!")
        
        elif op == "5": break

# --- FUNÇÕES ESPECÍFICAS PARA NOTAS (DECIMAIS) ---
def gerenciar_notas():
    dados = carregar_dados()
    while True:
        print("\n--- MENU NOTAS ---")
        print("1. Cadastrar\n2. Listar\n3. Voltar")
        op = input("Opção: ").strip()
        
        if op == "1":  # CADASTRAR NOTA
            print("\n--- ALUNOS ---")
            for aluno in dados["alunos"]:
                print(f"Matrícula: {aluno['matricula']} | Nome: {aluno['nome']}")
            matricula = input("\nMatrícula do aluno: ").strip()
            
            print("\n--- DISCIPLINAS ---")
            for disciplina in dados["disciplinas"]:
                print(f"Código: {disciplina['codigo']} | Nome: {disciplina['nome']}")
            codigo = input("\nCódigo da disciplina: ").strip()
            
            if not any(aluno["matricula"] == matricula for aluno in dados["alunos"]) or \
               not any(disciplina["codigo"] == codigo for disciplina in dados["disciplinas"]):
                print("Erro: Aluno ou disciplina não encontrados!")
                continue
            
            try:
                nota = float(input("Nota (0.0 a 10.0): "))
                if 0.0 <= nota <= 10.0:
                    dados["notas"].append({
                        "matricula": matricula,
                        "codigo_disciplina": codigo,
                        "valor": nota
                    })
                    salvar_dados(dados)
                    print("Nota cadastrada!")
                else: print("Erro: Nota deve ser entre 0.0 e 10.0!")
            except ValueError: print("Erro: Insira um número válido (ex.: 7.5)!")
        
        elif op == "2":  # LISTAR NOTAS
            print("\n--- NOTAS ---")
            for nota in dados["notas"]:
                aluno = next(a for a in dados["alunos"] if a["matricula"] == nota["matricula"])
                disciplina = next(d for d in dados["disciplinas"] if d["codigo"] == nota["codigo_disciplina"])
                print(f"Aluno: {aluno['nome']} | Disciplina: {disciplina['nome']} | Nota: {nota['valor']:.1f}")
        
        elif op == "3": break

# --- MENU PRINCIPAL ---
def menu_principal():
    while True:
        print("\n=== SISTEMA ACADÊMICO ===")
        print("1. Alunos\n2. Disciplinas\n3. Notas\n4. Sair")
        op = input("Opção: ").strip()
        
        if op == "1": 
            gerenciar_entidade("alunos", ["matricula", "nome", "data_nascimento"], "matricula")
        elif op == "2": 
            gerenciar_entidade("disciplinas", ["codigo", "nome"], "codigo")
        elif op == "3": 
            gerenciar_notas()
        elif op == "4": 
            print("Sistema encerrado.")
            break

if __name__ == "__main__":
    menu_principal()