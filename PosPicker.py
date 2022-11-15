import time
from datetime import datetime

import pyautogui


def f__DateTime():
    try:
        DateTime = f'{str(datetime.now()).split(" ")[0]} ' \
                   f'{str(datetime.now()).split(" ")[1].split(".")[0].split(":")[0]}' \
                   f':{str(datetime.now()).split(" ")[1].split(".")[0].split(":")[1]}' \
                   f':{str(datetime.now()).split(" ")[1].split(".")[0].split(":")[2]}'
    except:
        DateTime = f'yyyy-mm-dd HH:MM:SS'

    return DateTime


def f__PickPos():
    print(f'{f__DateTime()}  --> Posição -> {pyautogui.position()}')
    time.sleep(1)

    input(f'{f__DateTime()}  --> Pressione enter para prosseguir!')


if __name__ == '__main__':
    print("""
                               Script para pegar posição em tela dos cliques.

            Funcionamento: 1 - Execute o script e posicione a pointeira do mouse no local desejado.
                           2 - O script irá lhe retornar em tela a posição x e y. Ex: "Point(x=108, y=192)"
                           3 - Após lhe retornar a posição da ponteira, responda "s" caso deseje executar
                           novamente o script, caso responda "n" o script irá finalizar.  
        \n""")


    def f__innit():
        while True:
            time.sleep(3)
            print(f"{f__DateTime()}  --> Posicione a ponteira do mouse no local desejado.")
            time.sleep(5)
            f__PickPos()
            repeatPicker = input(f"{f__DateTime()}  --> Deseja pegar novamente a localização da ponteira do mouse? [s/n]: ")
            if repeatPicker.upper() == 'S':
                pass
            else:
                print(f'\n{f__DateTime()}  --> Obrigado pela utilização. Volte sempre! :)')
                time.sleep(1)
                input(f'{f__DateTime()}  --> Pressione enter para sair!')
                break
    f__innit()
