import random
import pandas as pd


# Estrutura para vincular a alternativa ao peso
class Alternativa:
    def __init__(self, texto, peso):
        self.texto = texto
        self.peso = peso


class Pergunta:
    def __init__(self, texto="", alternativas=None):
        self.texto = texto
        self.alternativas = alternativas if alternativas else []

    # Atribui o peso a cada alternativa na ordem do ficheiro
    def carregar_pergunta(self, pergunta_dados):
        self.texto = pergunta_dados['texto']
        self.alternativas = [
            Alternativa(pergunta_dados['alt1'], 0),
            Alternativa(pergunta_dados['alt2'], 25),
            Alternativa(pergunta_dados['alt3'], 75),
            Alternativa(pergunta_dados['alt4'], 100),
        ]

    # Embaralha as alternativas mantendo o vínculo entre texto e peso
    def embaralhar_alternativas(self):
        random.shuffle(self.alternativas)

    # Exibe a pergunta no formato "1/10 - Pergunta" e respostas no formato "1. Alternativa"
    def mostrar_pergunta(self, numero_atual, total_perguntas):
        print(f"{numero_atual}/{total_perguntas} - {self.texto}")
        for idx, alternativa in enumerate(self.alternativas, 1):
            print(f"{idx}. {alternativa.texto}")


class Quiz:
    def __init__(self, perguntas_quiz, jogador_quiz):
        self.perguntas = perguntas_quiz[:10]
        self.pontuacao = 0
        self.jogador = jogador_quiz

    @staticmethod #ele não acessa ou modifica os atributos da instância (self)
    def limpar_tela():
        print("\n" * 6)

    def embaralhar_perguntas(self):
        random.shuffle(self.perguntas)

    def jogar(self):
        self.embaralhar_perguntas()
        total_perguntas = len(self.perguntas)

        for i, pergunta in enumerate(self.perguntas, start=1):
            self.limpar_tela()
            pergunta.embaralhar_alternativas()
            pergunta.mostrar_pergunta(i, total_perguntas)

            while True:
                try:
                    resposta = int(input("Escolha uma alternativa (1-4): ")) - 1
                    if 0 <= resposta < len(pergunta.alternativas):
                        break
                    else:
                        print("Escolha inválida. Tente novamente.")
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número entre 1 e 4.")

            # Traz o peso da alternativa selecionada e acumula no total
            self.pontuacao += pergunta.alternativas[resposta].peso

        self.limpar_tela()
        resultado = MostrarResultado(total_perguntas, self.jogador, self.pontuacao)
        resultado.mostrar_resultado()


        while True:
            jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower()
            if jogar_novamente in ['s', 'n']:
                break
            print("Entrada inválida. Por favor, digite 's' para sim ou 'n' para não.")

        if jogar_novamente == 's':
            self.pontuacao = 0
            self.jogar()


class MostrarResultado:
    def __init__(self, total_perguntas, jogador_resultado, pontuacao_resultado):
        self.nome = jogador_resultado.nome
        self.pontuacao = pontuacao_resultado
        self.total_perguntas = total_perguntas
        self.porcentagem = (self.pontuacao / (self.total_perguntas * 100)) * 100

    def mostrar_resultado(self):
        porcentagem = self.porcentagem
        nome = self.nome
        # Mostra resultado com mensagem final personalizada de acordo com a porcentagem
        if porcentagem >= 90:
            print("\n***********************************************************************************************************************************************************")
            print(f"\nParabéns {nome}, você arrasou! Sua consciência de igualdade de gênero inspira outros a mudar paradigmas ultrapassados. Continue assim!!! \nObrigada por jogar!!!\nVocê está {porcentagem:.2f}% adaptado(a) a um novo mundo de igualdade de gênero!")
            print("\n***********************************************************************************************************************************************************")
        elif porcentagem >= 70:
            print("\n***********************************************************************************************************************")
            print(f"\nMuito bem {nome}, Você tem uma boa base sobre o assunto. Obrigada por jogar!!! \nVocê está {porcentagem:.2f}% adaptado(a) a um novo mundo de igualdade de gênero!")
            print("\n***********************************************************************************************************************")
        elif porcentagem >= 40:
            print("\n*******************************************************************************************************************************")
            print(f"\nVocê está no caminho certo {nome}, pesquise um pouco mais sobre o tema e obrigada por jogar!!! \nVocê está {porcentagem:.2f}% adaptado(a) a um novo mundo de igualdade de gênero!")
            print("\n*******************************************************************************************************************************")
        else:
            print("\n***********************************************************************************************************************************************************")
            print(f"\nPoxa {nome}, não esperava por isso!!! Reflita sobre o tema, pesquise e conversa com as pessoas a sua volta. Nunca é tarde para aprender.\nObrigada por jogar!!! \nVocê está {porcentagem:.2f}% adaptado(a) a um novo mundo de igualdade de gênero!")
            print("\n***********************************************************************************************************************************************************")


class Jogador:
    def __init__(self):
        self.nome = ""
        self.pontuacao = 0

    def obter_nome(self):
        self.nome = input("Digite seu nome: ")

    def registrar_pontuacao(self, pontuacao_jogador):
        self.pontuacao += pontuacao_jogador


class ArquivoExcel:
    def __init__(self, arq_excel):
        self.arq_excel = arq_excel

    def carregar_perguntas_arquivo(self):
        df = pd.read_excel(self.arq_excel)
        perguntas_arquivo = []
        for _, row in df.iterrows():
            pergunta = Pergunta()
            pergunta.carregar_pergunta(row)
            perguntas_arquivo.append(pergunta)  # Adicionando a instância de Pergunta à lista
        return perguntas_arquivo


if __name__ == "__main__":
    arquivo_excel = ArquivoExcel('perguntasquiz.xlsx')
    perguntas = arquivo_excel.carregar_perguntas_arquivo()
    jogador = Jogador()
    jogador.obter_nome()
    quiz = Quiz(perguntas, jogador)
    quiz.jogar()
