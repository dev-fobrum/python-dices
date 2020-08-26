#! python
import matplotlib.pyplot as plt
import numpy as np

from random import randint
import sys


def roll_dice(jogadas, estatistica_por_numero):
    a = 0
    lista_de_jogadas = {}

    while a < jogadas:
        a += 1
        valor_dado = randint(1, 6)
        lista_de_jogadas.update({a: valor_dado})
        estatistica_por_numero[valor_dado] += 1

    return {
        'lista_de_jogadas': lista_de_jogadas,
        'estatistica_por_numero': estatistica_por_numero
    }


def print_plays(lista_de_jogadas):
    print()
    print('===== Lista de jogadas: =====')
    for numero_jogada, valor_jogada in lista_de_jogadas.items():
        print(f'Jogada #{numero_jogada}: {valor_jogada}')
    print()


def soma_aproveitamento(lista_de_jogadas):
    total_jogadas = len(lista_de_jogadas)
    valor_total_jogadas = int(0)

    for valor_jogada in lista_de_jogadas.values():
        valor_total_jogadas += int(valor_jogada)

    return {
        'total_jogadas': total_jogadas,
        'valor_total_jogadas': valor_total_jogadas
    }


def calcular_aproveitamento(total_jogadas, valor_total_jogadas, single_playround=True):
    if single_playround:
        valor_total_possivel = total_jogadas*6
    else:
        valor_total_possivel = total_jogadas

    # print(valor_total_possivel)

    aproveitamento = (valor_total_jogadas / valor_total_possivel) * 100

    return {
        'valor_total_jogadas': valor_total_jogadas,
        'valor_total_possivel': valor_total_possivel,
        'aproveitamento': aproveitamento
    }


def print_aproveitamento(valor_total_jogadas, valor_total_possivel, aproveitamento):
    print()
    print('===== Estatísticas das jogadas =====')
    print(f'O valor total das jogadas foi de {valor_total_jogadas}')
    print(f'O valor total possível é de {valor_total_possivel}')
    print(f'O aproveitamento foi de {aproveitamento}%')
    print()


def print_general_stats(valor_total_jogadas, valor_total_possivel):

    print()
    if int(valor_total_jogadas) > 0 and int(valor_total_possivel) > 0:
        aproveitamento = (valor_total_jogadas / valor_total_possivel) * 100

        print('===== Estatísticas Gerais das jogadas =====')
        print(f'O valor total das jogadas foi de {valor_total_jogadas}')
        print(f'O valor total possível é de {valor_total_possivel}')
        print(f'O aproveitamento foi de {aproveitamento}%')
    else:
        print('Ainda não há registros gerais.')
    print()


def print_estatistica_por_numero(estatistica_por_numero, total_jogadas):
    print()
    print('===== Estatísticas por número: =====')
    if float(total_jogadas) > 0:
        for face_dado, qty_jogadas in estatistica_por_numero.items():

            propabilidade = (qty_jogadas / (total_jogadas/6)) * 100

            print(
                f'Número #{face_dado}: {qty_jogadas} ({round(propabilidade, 2)}% das vezes)')
    else:
        print('Ainda não há registros gerais.')
    print()


# Vars
opcao = 0
sair = False
estatistica_geral = {
    'valor_total_jogadas_general': float(0),
    'valor_total_possivel_general': float(0)
}
estatistica_por_numero = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0
}


if __name__ == '__main__':
    while not sair:
        print('===== Menu: =====')
        opcao = input(
            '1 - Jogar dados \n2 - Estatísticas gerais \n3 - Estatística por números\n4 - Reiniciar estatísticas \n5 - Sair \n')
        # opcao = 4
        if int(opcao) == 1:
            ####### Jogar Dados #######
            jogadas = input('Informe quantas jogadas deseja realizar: ')
            # jogadas = 3

            # Gera o dicionário com todas as jogadas
            # requisitadas pelo usuário
            dic_jogadas = roll_dice(int(jogadas), estatistica_por_numero)

            # Atualiza estatística por número
            estatistica_por_numero = dic_jogadas.get('estatistica_por_numero')

            # Imprime as jogadas na tela
            print_plays(dic_jogadas.get('lista_de_jogadas'))

            # Calcula o aproveitamento das jogadas
            info_aproveitamento = soma_aproveitamento(
                dic_jogadas.get('lista_de_jogadas'))

            dados_aproveitamento = calcular_aproveitamento(
                info_aproveitamento.get('total_jogadas'),
                info_aproveitamento.get('valor_total_jogadas')
            )

            # Atualiza as informações globais
            valor_total_jogadas_temp = estatistica_geral.get(
                'valor_total_jogadas_general')
            valor_total_possivel_temp = estatistica_geral.get(
                'valor_total_possivel_general')

            estatistica_geral = {
                'valor_total_jogadas_general': dados_aproveitamento.get('valor_total_jogadas') + int(valor_total_jogadas_temp),
                'valor_total_possivel_general': dados_aproveitamento.get('valor_total_possivel') + int(valor_total_possivel_temp)
            }

            # Imprime o aproveitamento
            print_aproveitamento(
                dados_aproveitamento.get('valor_total_jogadas'),
                dados_aproveitamento.get('valor_total_possivel'),
                dados_aproveitamento.get('aproveitamento')
            )

        elif int(opcao) == 2:

            if estatistica_geral.get('valor_total_jogadas_general') > 0:
                print_general_stats(
                    estatistica_geral.get('valor_total_jogadas_general'),
                    estatistica_geral.get('valor_total_possivel_general'),
                )

                N = 1
                menMeans = estatistica_geral.get('valor_total_jogadas_general')
                womenMeans = estatistica_geral.get(
                    'valor_total_possivel_general') - estatistica_geral.get('valor_total_jogadas_general')
                ind = np.arange(N)    # the x locations for the groups
                # the width of the bars: can also be len(x) sequence
                width = 0.35

                p1 = plt.bar(ind, menMeans, width)
                p2 = plt.bar(ind, womenMeans, width,
                             bottom=menMeans)

                plt.ylabel('Número de Jogadas')
                plt.title('Estatística geral')
                plt.xticks(ind, (''))
                plt.yticks(np.arange(0, 81, 10))
                plt.legend((p1[0], p2[0]),
                           ('Valores sorteados', 'Valor máximo possível'))

                plt.show()
            else:
                print('Ainda não há registros.')

        elif int(opcao) == 3:

            if estatistica_geral.get('valor_total_jogadas_general') > 0:
                print_estatistica_por_numero(
                    estatistica_por_numero, estatistica_geral.get('valor_total_possivel_general'))

                # Fixing random state for reproducibility
                np.random.seed(19680801)

                plt.rcdefaults()
                fig, ax = plt.subplots()

                # Example data
                faces = ('1', '2', '3', '4', '5', '6')
                y_pos = np.arange(len(faces))

                performance = list(estatistica_por_numero.values())
                error = np.random.rand(len(faces))

                ax.barh(y_pos, performance, xerr=error, align='center')
                ax.set_yticks(y_pos)
                ax.set_yticklabels(faces)
                ax.invert_yaxis()
                ax.set_xlabel('Quantidades')
                ax.set_title('Estatística por números')

                plt.show()
            else:
                print('Ainda não há registros.')

        elif int(opcao) == 4:

            estatistica_geral = {
                'valor_total_jogadas_general': float(0),
                'valor_total_possivel_general': float(0)
            }

            estatistica_por_numero = {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0
            }

            print()
            print('As estatísticas foram reiniciadas.')
            print()

        elif int(opcao) == 5:
            break
