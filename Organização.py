import os
import shutil
import time
import curses
import subprocess

# Caminho da pasta de origem e da pasta de destino
source_folder = os.path.expanduser("C:\\Pasta\\A\\Ser\\Organizada")
destination_folder = "C:\\Pasta\\De\\Destino\\Da\\Organização"

# Cria as pastas de destino se não existirem
def criar_pastas():
    extensions = set()
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)
        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1].lower()
            if ext:
                extensions.add(ext)
    
    for ext in extensions:
        folder = os.path.join(destination_folder, f".{ext[1:].upper()}s")
        os.makedirs(folder, exist_ok=True)
    
    os.makedirs(os.path.join(destination_folder, "Outros"), exist_ok=True)

# Move os itens para as pastas de destino apropriadas
def mover_itens():
    for item in os.listdir(source_folder):
        src_path = os.path.join(source_folder, item)

        # Evitar mover o diretório de destino para dentro de si mesmo
        if os.path.abspath(src_path) == os.path.abspath(destination_folder):
            continue

        if os.path.isfile(src_path):
            ext = os.path.splitext(item)[1].lower()
            if ext:
                folder = os.path.join(destination_folder, f".{ext[1:].upper()}s")
            else:
                folder = os.path.join(destination_folder, "Outros")
            dest_path = os.path.join(folder, item)
            shutil.move(src_path, dest_path)
        elif os.path.isdir(src_path):
            # Move pastas para "Outros"
            dest_folder = os.path.join(destination_folder, "Outros", item)
            shutil.move(src_path, dest_folder)

# Menu interativo usando curses
def confirmation_menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    menu = ['Sim', 'Não']
    current_row = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        prompt = f"Você deseja mover os itens da pasta '{source_folder}' para '{destination_folder}'?"
        sub_prompt = "Os itens serão separados por tipo."
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(height // 2 - 3, (width - len(prompt)) // 2, prompt)
        stdscr.addstr(height // 2 - 1, (width - len(sub_prompt)) // 2, sub_prompt)
        stdscr.attroff(curses.color_pair(2))

        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(2))

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row] == 'Sim':
                return True
            else:
                return False

        stdscr.refresh()

# Função principal do programa
def main(stdscr):
    if confirmation_menu(stdscr):
        criar_pastas()
        mover_itens()
        stdscr.clear()
        success_msg = f"Itens movidos com sucesso de '{source_folder}' para '{destination_folder}'."
        stdscr.addstr(curses.LINES // 2, (curses.COLS - len(success_msg)) // 2, success_msg)
        stdscr.refresh()
        time.sleep(3)
        
        # Abrir a pasta de destino
        subprocess.Popen(f'explorer {destination_folder}')
    else:
        stdscr.clear()
        cancel_msg = "Operação cancelada."
        stdscr.addstr(curses.LINES // 2, (curses.COLS - len(cancel_msg)) // 2, cancel_msg)
        stdscr.refresh()
        time.sleep(3)

# Executa o programa dentro do wrapper do curses
curses.wrapper(main)
