# Este código foi comentado por ChatGPT

import os
import re
import sys
import curses

# Função para listar pastas dentro de um diretório
def listar_pastas(caminho):
    # Filtra apenas os diretórios no caminho especificado
    pastas = [pasta for pasta in os.listdir(caminho) if os.path.isdir(os.path.join(caminho, pasta))]
    # Separa as pastas que possuem um número no início do nome e as ordena
    pastas_numeradas = sorted([pasta for pasta in pastas if re.match(r'^\d+_', pasta)], key=lambda x: int(x.split('_')[0]))
    # Separa as pastas que não possuem um número no início do nome
    pastas_nao_numeradas = [pasta for pasta in pastas if not re.match(r'^\d+_', pasta)]
    return pastas_numeradas, pastas_nao_numeradas

# Função para criar uma nova pasta dentro do diretório
def criar_nova_pasta(stdscr, caminho):
    # Obtém as pastas numeradas e não numeradas
    pastas_numeradas, pastas_nao_numeradas = listar_pastas(caminho)

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Exibe uma mensagem solicitando o nome da nova pasta
        msg1 = "Digite o nome da nova pasta (ESC para voltar): "
        prompt_x = (width - len(msg1)) // 2
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(height // 2 - 2, prompt_x, msg1)
        curses.curs_set(1)
        curses.echo()

        nova_pasta = ''
        x_position = (width - len(nova_pasta)) // 2
        while True:
            # Captura a entrada do usuário para o nome da pasta
            char = stdscr.get_wch(height // 2, x_position + len(nova_pasta))
            if char == '\x1b':  # Tecla ESC para voltar
                return
            elif char == '\n':  # Tecla Enter para confirmar
                break
            elif char == '\b' or char == '\x7f':  # Tecla Backspace para apagar
                if len(nova_pasta) > 0:
                    nova_pasta = nova_pasta[:-1]
                    stdscr.addstr(height // 2, x_position + len(nova_pasta), ' ')
                    stdscr.move(height // 2, x_position + len(nova_pasta))
            elif isinstance(char, str) and char.isprintable():  # Adiciona caracteres imprimíveis
                nova_pasta += char
                stdscr.addstr(height // 2, x_position, nova_pasta)
                stdscr.refresh()

        curses.noecho()
        curses.curs_set(0)

        # Se o nome da pasta for válido, sai do loop
        if nova_pasta.strip() == '':
            continue
        else:
            break

    while True:
        stdscr.clear()
        stdscr.addstr(height // 2 - 2, prompt_x, f"Nome da nova pasta: {nova_pasta}")
        msg3 = "Digite a posição da nova pasta (ESC para voltar): "
        stdscr.addstr(height // 2, (width - len(msg3)) // 2, msg3)
        curses.curs_set(1)
        curses.echo()

        importancia_input = ''
        x_position = (width - len(importancia_input)) // 2
        while True:
            # Captura a entrada do usuário para a importância da pasta
            char = stdscr.get_wch(height // 2 + 2, x_position + len(importancia_input))
            if char == '\x1b':  # Tecla ESC para voltar
                return
            elif char == '\n':  # Tecla Enter para confirmar
                break
            elif char == '\b' or char == '\x7f':  # Tecla Backspace para apagar
                if len(importancia_input) > 0:
                    importancia_input = importancia_input[:-1]
                    stdscr.addstr(height // 2 + 2, x_position + len(importancia_input), ' ')
                    stdscr.move(height // 2 + 2, x_position + len(importancia_input))
            elif isinstance(char, str) and char.isdigit():  # Adiciona apenas dígitos
                importancia_input += char
                stdscr.addstr(height // 2 + 2, x_position, importancia_input)
                stdscr.refresh()

        curses.noecho()
        curses.curs_set(0)

        # Se a importância for válida, sai do loop
        if importancia_input.strip() == '':
            continue
        else:
            try:
                importancia_nova_pasta = int(importancia_input)
                break
            except ValueError:
                continue

    # Define o caminho completo da nova pasta
    nova_pasta_caminho = os.path.join(caminho, nova_pasta)

    # Cria a nova pasta se ela não existir
    if not os.path.exists(nova_pasta_caminho):
        try:
            os.makedirs(nova_pasta_caminho)
        except Exception as e:
            return

    # Remove a nova pasta da lista de pastas não numeradas, se necessário
    if nova_pasta in pastas_nao_numeradas:
        pastas_nao_numeradas.remove(nova_pasta)

    # Reordena as pastas numeradas para abrir espaço para a nova pasta
    for i in range(len(pastas_numeradas), importancia_nova_pasta - 1, -1):
        pasta_antiga = pastas_numeradas[i - 1]
        nova_num = i + 1
        if nova_num <= 9:
            nova_nome = f'0{nova_num}_{pasta_antiga.split("_", 1)[-1]}'
        else:
            nova_nome = f'{nova_num}_{pasta_antiga.split("_", 1)[-1]}'
        os.rename(os.path.join(caminho, pasta_antiga), os.path.join(caminho, nova_nome))
        pastas_numeradas[i - 1] = nova_nome

    # Renomeia e insere a nova pasta na posição correta
    if importancia_nova_pasta <= 9:
        pastas_numeradas.insert(importancia_nova_pasta - 1, f'0{importancia_nova_pasta}_{nova_pasta}')
        os.rename(nova_pasta_caminho, os.path.join(caminho, f'0{importancia_nova_pasta}_{nova_pasta}'))
    else:
        pastas_numeradas.insert(importancia_nova_pasta - 1, f'{importancia_nova_pasta}_{nova_pasta}')
        os.rename(nova_pasta_caminho, os.path.join(caminho, f'{importancia_nova_pasta}_{nova_pasta}'))


# Função para reorganizar pastas se houver conflito de importância
def reorganizar_pastas(caminho, pastas_numeradas, importancia_pasta):
    for i in range(len(pastas_numeradas), importancia_pasta - 1, -1):
        pasta_antiga = pastas_numeradas[i - 1]
        nova_num = i + 1
        if nova_num <= 9:
            nova_nome = f'0{nova_num}_{pasta_antiga.split("_", 1)[-1]}'
        else:
            nova_nome = f'{nova_num}_{pasta_antiga.split("_", 1)[-1]}'
        os.rename(os.path.join(caminho, pasta_antiga), os.path.join(caminho, nova_nome))
        pastas_numeradas[i - 1] = nova_nome


# Função para adicionar uma pasta existente e renomeá-la
def adicionar_pasta_existente(stdscr, caminho):
    while True:
        pastas_numeradas, pastas_nao_numeradas = listar_pastas(caminho)

        if len(pastas_nao_numeradas) == 0:
            stdscr.clear()
            stdscr.addstr(3, 0, "Nenhuma pasta disponível para adicionar!")
            stdscr.refresh()
            stdscr.getch()
            return

        current_row = 0
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            for idx, pasta in enumerate(pastas_nao_numeradas + ["Voltar"]):
                x = width // 2 - len(pasta) // 2
                y = height // 2 - len(pastas_nao_numeradas) // 2 + idx
                if idx == current_row:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, pasta)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(y, x, pasta)
                    stdscr.attroff(curses.color_pair(2))

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(pastas_nao_numeradas):
                current_row += 1
            elif key == 27:
                return
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == len(pastas_nao_numeradas):
                    return
                else:
                    pasta_selecionada = pastas_nao_numeradas[current_row]
                    break

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            msg_importancia = f"Digite a posição da pasta '{pasta_selecionada}' (ESC para voltar): "
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(height // 2, (width - len(msg_importancia)) // 2, msg_importancia)
            stdscr.attroff(curses.color_pair(2))

            curses.curs_set(1)
            curses.echo()

            importancia_input = ''
            x_position = (width - len(importancia_input)) // 2
            while True:
                char = stdscr.get_wch(height // 2 + 2, x_position + len(importancia_input))
                if char == '\x1b':
                    return
                elif char == '\n':
                    break
                elif char == '\b' or char == '\x7f':
                    if len(importancia_input) > 0:
                        importancia_input = importancia_input[:-1]
                        stdscr.addstr(height // 2 + 2, x_position + len(importancia_input), ' ')
                        stdscr.move(height // 2 + 2, x_position + len(importancia_input))
                elif isinstance(char, str) and char.isdigit():
                    importancia_input += char
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(height // 2 + 2, x_position, importancia_input)
                    stdscr.attroff(curses.color_pair(2))
                    stdscr.refresh()

            curses.noecho()
            curses.curs_set(0)

            if importancia_input.strip() == '':
                continue
            else:
                try:
                    importancia_pasta = int(importancia_input)
                    break
                except ValueError:
                    continue

        nova_num = importancia_pasta
        if nova_num <= 9:
            nova_nome = f'0{nova_num}_{pasta_selecionada}'
        else:
            nova_nome = f'{nova_num}_{pasta_selecionada}'

        pasta_selecionada_caminho = os.path.join(caminho, pasta_selecionada)
        nova_pasta_caminho = os.path.join(caminho, nova_nome)

        # Reorganiza pastas numeradas caso a importância já esteja sendo usada
        reorganizar_pastas(caminho, pastas_numeradas, importancia_pasta)

        if not os.path.exists(nova_pasta_caminho):
            try:
                os.rename(pasta_selecionada_caminho, nova_pasta_caminho)
            except Exception as e:
                stdscr.addstr(3, 0, f"Erro ao renomear a pasta {pasta_selecionada}: {e}")
                stdscr.refresh()
                stdscr.getch()


# Função para reordenar automaticamente as pastas numeradas
def reordenar_automaticamente(stdscr, caminho):
    pastas_numeradas, _ = listar_pastas(caminho)

    for i, pasta in enumerate(pastas_numeradas):
        nova_num = i + 1
        if nova_num <= 9:
            nova_nome = f'0{nova_num}_{pasta.split("_", 1)[-1]}' if '_' in pasta else f'{nova_num}_{pasta}'
        else:
            nova_nome = f'{nova_num}_{pasta.split("_", 1)[-1]}' if '_' in pasta else f'{nova_num}_{pasta}'
        try:
            os.rename(os.path.join(caminho, pasta), os.path.join(caminho, nova_nome))
        except Exception as e:
            stdscr.addstr(3, 0, f"Erro ao renomear a pasta {pasta}: {e}")

    stdscr.addstr(3, 0, "Pastas reordenadas com sucesso!")
    stdscr.refresh()
    stdscr.getch()

# Função para reordenar manualmente as pastas numeradas
def reordenar_manual(stdscr, caminho):
    pastas_numeradas, _ = listar_pastas(caminho)
    original_pastas = list(pastas_numeradas)
    current_row = 0
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Exibe a lista de pastas e a opção "Confirmar"
        for idx, pasta in enumerate(pastas_numeradas + ["Confirmar"]):
            x = width // 2 - len(pasta) // 2
            y = height // 2 - len(pastas_numeradas) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, pasta)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, pasta)
                stdscr.attroff(curses.color_pair(2))

        # Captura a entrada do usuário para mover o cursor
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(pastas_numeradas):
            current_row += 1
        elif key == 27:  # Tecla ESC para voltar sem salvar
            return
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Tecla Enter para selecionar
            if current_row == len(pastas_numeradas):  # Opção "Confirmar"
                break
            else:  # Modo de reordenação manual
                selected_row = current_row
                while True:
                    stdscr.clear()
                    for idx, pasta in enumerate(pastas_numeradas):
                        x = width // 2 - len(pasta) // 2
                        y = height // 2 - len(pastas_numeradas) // 2 + idx
                        if idx == selected_row:
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addstr(y, x, pasta)
                            stdscr.attroff(curses.color_pair(1))
                        elif idx == current_row:
                            stdscr.addstr(y, x, f"> {pasta} <")
                        else:
                            stdscr.attron(curses.color_pair(2))
                            stdscr.addstr(y, x, pasta)
                            stdscr.attroff(curses.color_pair(2))

                    key = stdscr.getch()

                    if key == curses.KEY_UP and selected_row > 0:
                        selected_row -= 1
                    elif key == curses.KEY_DOWN and selected_row < len(pastas_numeradas) - 1:
                        selected_row += 1
                    elif key == 27:  # Tecla ESC para voltar sem salvar
                        pastas_numeradas = list(original_pastas)
                        return
                    elif key == curses.KEY_ENTER or key in [10, 13]:  # Tecla Enter para mover
                        pastas_numeradas.insert(selected_row, pastas_numeradas.pop(current_row))
                        break

    # Renomeia as pastas de acordo com a nova ordem definida manualmente
    for i, pasta in enumerate(pastas_numeradas):
        nova_num = i + 1
        if nova_num <= 9:
            nova_nome = f'0{nova_num}_{pasta.split("_", 1)[-1]}'
        else:
            nova_nome = f'{nova_num}_{pasta.split("_", 1)[-1]}'
        os.rename(os.path.join(caminho, pasta), os.path.join(caminho, nova_nome))

    stdscr.addstr(3, 0, "Pastas reordenadas manualmente com sucesso!")
    stdscr.refresh()
    stdscr.getch()

# Função principal que gerencia o menu principal do programa
def main_menu(stdscr, caminho):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Define as opções do menu principal
    menu = ['Adicionar nova pasta', 'Adicionar pasta existente', 'Reordenar automaticamente', 'Reordenar manualmente', 'Sair']
    current_row = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Exibe as opções do menu
        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(2))

        # Captura a entrada do usuário para mover o cursor
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Tecla Enter para selecionar uma opção
            if menu[current_row] == 'Adicionar nova pasta':
                criar_nova_pasta(stdscr, caminho)
            elif menu[current_row] == 'Adicionar pasta existente':
                adicionar_pasta_existente(stdscr, caminho)
            elif menu[current_row] == 'Reordenar automaticamente':
                reordenar_automaticamente(stdscr, caminho)
            elif menu[current_row] == 'Reordenar manualmente':
                reordenar_manual(stdscr, caminho)
            elif menu[current_row] == 'Sair':
                break
        elif key == 27:  # Tecla ESC para sair do programa
            break

        stdscr.refresh()

# Função principal do programa
def main(stdscr):
    # Define o caminho do diretório atual, dependendo se o programa está congelado em um .exe ou não
    if getattr(sys, 'frozen', False):
        caminho = os.path.dirname(sys.executable)
    else:
        caminho = os.path.dirname(os.path.abspath(__file__))

    # Chama o menu principal
    main_menu(stdscr, caminho)

# Executa a função principal dentro do wrapper do curses
curses.wrapper(main)
