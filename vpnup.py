import os
import curses
import subprocess
import signal

def list_udp_ovpn_files(directory):
    return sorted(set([f.split('.')[0] for f in os.listdir(directory) if f.endswith("udp.ovpn")]))

def choose_file(stdscr, files):
    curses.curs_set(0)  # Hide the cursor
    current_row = 0
    
    def print_menu():
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        num_cols = max(1, w // 22)
        col_width = w // num_cols
        for idx, file in enumerate(files):
            x = (idx % num_cols) * col_width + 1
            y = idx // num_cols + 1
            display_file = (file[:col_width-3] + '...') if len(file) > col_width-2 else file
            try:
                if idx == current_row:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, display_file)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, display_file)
            except curses.error:
                pass
        stdscr.refresh()
        return num_cols
    
    while True:
        num_cols = print_menu()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row >= num_cols:
            current_row -= num_cols
        elif key == curses.KEY_DOWN and current_row + num_cols < len(files):
            current_row += num_cols
        elif key == curses.KEY_LEFT and current_row % num_cols > 0:
            current_row -= 1
        elif key == curses.KEY_RIGHT and current_row % num_cols < num_cols - 1 and current_row < len(files) - 1:
            current_row += 1
        elif key == ord('\n'):
            return files[current_row]

def main(stdscr):
    home_directory = os.path.expanduser("~")
    directory = os.path.join(home_directory, '.local/openvpn')
    files = list_udp_ovpn_files(directory)
    if not files:
        stdscr.addstr(0, 0, "No files found in the directory.")
        stdscr.refresh()
        stdscr.getch()
        return
    selected_file = choose_file(stdscr, files)
    curses.endwin()  # Restore the terminal screen
    
    if selected_file:
        # disable ctr-c and -z
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
        
        cmd = f"sudo {os.path.join(home_directory, '.local/bin/startvpn')} {selected_file}"
        print(f"************* {selected_file.upper()} *************")
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.decode().strip())
        rc = process.poll()

if __name__ == "__main__":
    curses.wrapper(main)

