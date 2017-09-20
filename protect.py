#!/usr/bin/env python3
"""Generates key of 1024 bytes (2048 chars)"""


import hashlib
import os

from getpass import getpass
from sys import argv


# MD5_OF_SALT = "ENTER MD5 OF SHA512-HASHED FILE"
# For example enter passphrase "TEST"
MD5_OF_SALT = "3f9b68244ee31224131a71b536e72ae6"
SALT_FNAME = os.path.expanduser("/tmp/.salt")
KEY_FNAME = os.path.expanduser("/tmp/.key")
BIN_KEY_FNAME = os.path.expanduser("/tmp/.bin")
HEX = ('0', '1', '2', '3', '4', '5', '6', '7',
       '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')
STR_BLOCK_SIZE = len(HEX)
BLOCK_SIZE = STR_BLOCK_SIZE // 2
BLOCK_NUM = 128
KEY_SIZE = BLOCK_SIZE * BLOCK_NUM
STR_KEY_SIZE = STR_BLOCK_SIZE * BLOCK_NUM
READ_KB_NUM = 0
OPTS = []
for arg in argv:
    if arg.startswith('-'):
        OPTS.append(arg)
        argv.pop(argv.index(arg))
if len(argv) > 2:
    try:
        READ_KB_NUM = int(argv[2])
    except ValueError:
        print('arg must be integer')
        exit()
KB = 1024

MAX_ITER = 30
MAX_TEXT = 512

ALPHA_LIST = ('0', '1', '2', '3', '4', '5', '6', '7',
              '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
              'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
              'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V')
ALPHA_SIZE = (8, 4)
ALPHA_LEN = ALPHA_SIZE[0] * ALPHA_SIZE[1]


class File:
    '''Class-container for files handling'''
    @staticmethod
    def create_salt(file_name, pass_phrase):
        """Creates 64-bytes hashed file based on the user passphrase """
        hash_pass = hashlib.sha512(pass_phrase)
        with open(file_name, 'wb') as file_descr:
            file_descr.write(hash_pass.digest())

    @staticmethod
    def read_all(file_name):
        """Returns binary data of file_name file"""
        with open(file_name, 'rb') as file_descr:
            data = file_descr.read()
        return data

    @staticmethod
    def read_one_kb(file_name, last_kb, num=READ_KB_NUM):
        """Returns num-th binary data kB of file_name file"""
        if num < 1:
            num = last_kb
        with open(file_name, 'rb') as file_descr:
            file_descr.seek((num -1) * KB)
            data = file_descr.read(KB)
        return data

    @staticmethod
    def write(file_name, data):
        """Writes data into the file_name file"""
        if type(data) is not bytes:
            data = bytes(data, 'UTF-8')
        with open(file_name, 'wb')as file_descr:
            file_descr.write(data)

    @staticmethod
    def remove(file_name):
        """Removes file_name file or returns False"""
        if os.path.isfile(file_name):
            os.remove(file_name)
        else: return False


class View:
    '''Class-container for viewing static methods'''
    @staticmethod
    def get_base():
        """Returns DATA if data-based algorithm and TEXT if sitename-based"""
        if len(argv) < 2:
            base = str(input('Base\n1 - text,\n2 - data\n(1): '))
            if base in ('', '1',  't',  'text'):
                return 'TEXT'
            elif base in ('2',  'd',  'data'):
                return 'DATA'
            else:
                return View.get_base()
        else:
            return 'DATA'

    @staticmethod
    def get_pass_phrase():
        """Returns getting from user passphrase"""
        return bytes(getpass("Type the passphrase: "), 'UTF-8')

    @staticmethod
    def get_text():
        """Returns byte string of user@site form"""
        while True:
            user = str(input("User: "))
            site = str(input("Site: "))
            if (user and site) != '':
                text = bytes(user + "@" + site, 'UTF-8')
                break
            else: print("Enter not empty user and site")
        return text

    @staticmethod
    def get_iter():
        """Returns getting from user integer iteration count"""
        while True:
            try:
                iter_count = int(input("Password # "))
                if (iter_count < 1 or iter_count > MAX_ITER):
                    print("Must be from 1 to", MAX_ITER)
                else:
                    break
            except ValueError:
                print("Enter a number")
        return iter_count

    @staticmethod
    def get_file_name():
        """Returns getting from user string name of file"""
        return str(input('File: '))

    @staticmethod
    def get_options():
        """Returns True if user want to see additional options"""
        return View.get_yes_no('Show more options', 1)

    @staticmethod
    def get_denorm():
        """Returns True if user want to see denormalized key"""
        return View.get_yes_no('Show denormalized key', 1)

    @staticmethod
    def get_stat():
        """Returns True if user want to see statistic"""
        return View.get_yes_no('Show statistic', 1)

    @staticmethod
    def get_wind_size():
        """Returns tuple of window rows and window columns"""
        size = os.popen('stty size', 'r').read().split()
        rows = int(size[0])
        columns = int(size[1])
        return (rows, columns)

    @staticmethod
    def get_yes_no(phrase, default=0, truly=0, keywords=('yes', 'no')):
        """
        Returns True if user input is matching with keywords[truly].
        First char of keywords[default] showing as a capital char.
        """
        lst_keys = [k.lower() for key in keywords for k in key[0]]
        lst_keys[default] = lst_keys[default].upper()
        str_keys = '/'.join(lst_keys)
        answer = input("{} ({}): ".format(phrase.capitalize(), str_keys))
        if answer is '' or answer[0] not in (lst_keys):
            answer = lst_keys[default]
        return answer in (lst_keys[truly], lst_keys[truly].capitalize(),
                          keywords[truly], keywords[truly].capitalize(),
                          keywords[truly].upper(), keywords[truly].lower())

    @staticmethod
    def get_remove(file_name):
        """Returns True if user want to remove temp file file_name"""
        return View.get_yes_no("Remove {}".format(file_name), 0)

    @staticmethod
    def get_take_scr():
        """Returns True if user want to view alpha key with screenshoting"""
        return View.get_yes_no("Show Tk alpha key with screenshoting it?", 1)

    @staticmethod
    def decorate(str_key, columns):
        """Returns spaced str_key wrapped by header and footer"""
        header = ast  = " * "
        dash_count = int(columns / 2 - 17)
        header += dash_count * '-'
        header += "     This is the key     "
        header += dash_count * '-'
        header += ast
        footer = header = header.center(columns)
        str_key_spaced = ""
        blocks_in_line = columns // STR_BLOCK_SIZE
        if columns < (blocks_in_line * STR_BLOCK_SIZE) + blocks_in_line - 1:
            blocks_in_line -= 1
        for pos, i in enumerate(str_key):
            if pos not in [0, STR_KEY_SIZE] and pos % STR_BLOCK_SIZE == 0:
                if pos % (blocks_in_line *  STR_BLOCK_SIZE) == 0:
                    str_key_spaced += "\n"
                else:
                    str_key_spaced += " "
            str_key_spaced += str(i)
        result = header + str_key_spaced + '\n' + footer
        return result

    @staticmethod
    def decorate_alpha(str_key, size):
        """Returns spaced str_key wrapped by header and footer"""
        columns = size[0]
        str_key_spaced = ""
        for pos, i in enumerate(str_key):
            if pos not in [0, ALPHA_LEN] and pos % columns == 0:
                str_key_spaced += "\n"
            str_key_spaced += str(i)
        result = str_key_spaced
        return result

    @staticmethod
    def show(str_key, columns):
        """Prints to screen decorated str_key"""
        print(View.decorate(str_key, columns))

    @staticmethod
    def show_alpha(str_key, size):
        """Prints to screen decorated str_key"""
        print(View.decorate_alpha(str_key, size))

    @staticmethod
    def show_alpha_tk(title, str_key, fontsize, row_len):
        """Calls tk to display alpha key"""
        from tkview import alpha_tk_view
        alpha_tk_view(str(title), str(str_key), str(fontsize), str(row_len))

    @staticmethod
    def save_scrsht(title, interval):
        """Method for saving screenshot of TK window"""
        if os.path.exists(str(title)):
            print('File \'' + title + '\' is exists')
            title = title[:-4] + '_copy_' + str(int(os.times()[4])) + title[-4:]
        import subprocess
        subprocess.call(['gnome-screenshot',
                           '-w',                    # Grab a window
                           '-b',                    # Include the window border
                           '-d', str(interval),     # Delay [in seconds]
                           '-f', str(title)]        # Save to this file
                        )
        print('Saved as \'' + title + '\'')

    @staticmethod
    def stat_show_table(lst):
        """Prints to screen table of char frequency with position number"""
        print('\t\t' + '\t'.join([h for h in HEX]) + '\n')
        for pos in range(len(lst)):
            print("Position: " + str(pos) + '\t' +
                  ('\t'.join([str(lst[pos][h]) for h in HEX]) + '\n'))

    @staticmethod
    def stat_show_csv(lst):
        """Prints to screen csv-format table of average frequency of chars"""
        for pos in range(len(lst)):
            print(';'.join([str(lst[pos][h]) for h in HEX]))


class Key:
    '''Main class for key generation'''
    def run(self, *args):
        self.binary = self.generate(*args)
        self.string = self.to_string(self.binary)
        self.check(self.string)
        self.blocks = self.split(self.string)
        (self.normalized, self.norm_blocks) = self.normalize(self.blocks)
        self.check(self.normalized)
        self.stat = self.statistic(self.norm_blocks)
        self.alpha = self.to_alpha(self.normalized, ALPHA_SIZE)

    def to_string(self, bin_data):
        """Gets binary data and returns string in HEX format"""
        if type(bin_data) is not bytes:
            print("Internal error. Data is not binary")
            exit(1)
        str_data = ""
        for i in bin_data:
            str_data += '{:02X}'.format(i)
        return str_data

    def block_normalize(self, str_block):
        """Converts 16-length string to normalized HEX string"""
        str_block = str_block.upper()
        # Check string is correct
        if not all([i in HEX for i in str_block] +
                   [len(str_block) == STR_BLOCK_SIZE]):
            print('Internal error. Incorrect input data.')
            exit(1)

        counter = dict(zip(HEX, [str_block.count(i) for i in HEX]))
        nulled = [i for i in HEX if counter[i] == 0]
        s = []
        for char in str_block:
            if counter[char] == 1:
                s += char
            if counter[char] > 1:
                counter[char] -= 1
                o = ord(char)
                if o > 60: o -= 7
                n = nulled.pop(o % len(nulled))
                s += n
                counter[n] += 1

        if not all([i == 1 for i in counter.values()] + [nulled == []]):
            print('Internal counter error.')
            exit(1)

        return ''.join(s)

    def check(self, string):
        if len(string) % STR_BLOCK_SIZE != 0:
            print('Bad string length.')
            exit(1)
        elif type(string) is not str:
            print('Bad string type.')
            exit(1)
        elif not all([c in HEX for c in string]):
            print('Bad string content.')
            exit(1)

    def normalize(self, blocks):
        norm_blocks = []
        for block in blocks:
            norm_blocks.append(self.block_normalize(block))
        norm_str_key = self.join(norm_blocks)
        return (norm_str_key, norm_blocks)

    def join(self, blocks):
        str_key = ''.join(blocks)
        return str_key

    def split(self, string):
        blocks = []
        for i in range(BLOCK_NUM):
            start = STR_BLOCK_SIZE * i
            end = start + STR_BLOCK_SIZE
            blocks.append(string[start:end])
        return blocks

    def generate(self):
        raise NotImplementedError

    def statistic(self, blocks):
        stat = [dict((k,  0) for k in HEX) for i in range(STR_BLOCK_SIZE)]
        for pos in range(STR_BLOCK_SIZE):
            for b in blocks:
                stat[pos][b[pos]] += 1
        return stat

    def shift_char(self, char):
        return ALPHA_LIST[ALPHA_LIST.index(char) + ALPHA_LEN // 2]

    def to_alpha(self, str_block, size):
        """Converts 32-length string to normalized ALPHA string"""
        str_block = str_block.upper()[:size[0] * size[1]]
        # Check string is correct
        if not all([i in HEX for i in str_block] +
                   [len(str_block) == ALPHA_LEN]):
            print('Internal error. Incorrect input data.')
            exit(1)

        counter = dict(zip(ALPHA_LIST, [str_block.count(i) for i in ALPHA_LIST]))

        s = []
        for char in str_block:
            # Distance between two same chars
            dist = str_block.find(char, 16) - str_block.find(char)
            if char in s:
                s += self.shift_char(char)
                counter[self.shift_char(char)] += 1
                continue
            if counter[char] == 1:
                s += char
            if counter[char] == 2:
                if dist % 2 == 1:
                    s += self.shift_char(char)
                    counter[self.shift_char(char)] += 1
                    counter[char] -= 1
                else:
                    s += char
                    counter[char] -= 1

        if not all([i == 1 for i in counter.values()] + \
                   [len(set(s)) == len(s) == ALPHA_LEN] + \
                   [i in ALPHA_LIST for i in s]):
            print('Internal counter error.')
            exit(1)

        return ''.join(s)


class KeyFromData(Key):
    def __init__(self, data):
        self.data = data
        self.run(self.data)

    def generate(self, data):
        return data


class KeyFromText(Key):
    def __init__(self, salt, text, n):
        self.salt = salt
        self.text = text
        self.n = n
        self.run(self.salt, self.text, self.n)
        self.stat_avg = self.statistic_avg(self.n)

    def generate(self, salt, text, n):
        '''Takes salt, user@site, count of iterations.
        XORs salt text + x00. Returns binary key'''
        # Checking all parameters
        if not all((self._salt_check(salt),
                    self._text_check(text),
                    self._iter_check(n))):
            print('Internal error. Input parameters are corrupted.')
            exit(1)

        # Hashing
        for i in range(n - 1):
            text = hashlib.sha512(text).digest()
        text_hash = hashlib.sha512(text).digest() + text[:1]

        # XORing
        bin_key = b''
        for offset in range(KEY_SIZE):
            byte1 = salt[offset % len(salt)]
            byte2 = text_hash[offset % len(text_hash)]
            # XOR salt and (hashed text + b'\x00')
            curr_byte = (byte1 ^ byte2).to_bytes(1, 'big')
            bin_key += curr_byte

        return bin_key

    def statistic_avg(self, num):
        stat_iter = []
        for i in range(num):
            curr_bin_key = self.generate(self.salt, self.text, i + 1)
            curr_str_key = self.to_string(curr_bin_key)
            curr_blocks = self.split(curr_str_key)
            curr_norm_key, curr_norm_blocks = self.normalize(curr_blocks)
            curr_stat = self.statistic(curr_norm_blocks)
            stat_iter.append(curr_stat)
        stat = [dict((k, 0) for k in stat_iter[0][0].keys())
                for i in range(len(stat_iter[0]))]
        for c in stat[0].keys():
            for pos in range(len(stat)):
                s = []
                for iteration in stat_iter:
                    s.append(iteration[pos][c])
                stat[pos][c] = round(sum(s)/len(s), 2)
        return stat

    def _salt_check(self, salt):
        if not all((type(salt) is bytes, len(salt) is 64)):
            print('Internal error. Salt is corrupted')
            exit(1)
        else:
            return True

    def _text_check(self, text):
        if type(text) is not bytes:
            print("Internal error. Text is corrupted")
            exit(1)
        elif not all((len(text) > 2,
                    len(text) < MAX_TEXT,
                    b'@' in text)):
            print('Internal error. Text is corrupted')
            exit(1)
        else:
            return True

    def _iter_check(self, n):
        if type(n) is not int:
            print("Internal error. Iterations is corrupted")
            exit(1)
        elif any((n < 1,  n > MAX_ITER)):
            print("Internal error. Iterations number must be from 1 to",
                  MAX_ITER)
            exit(1)
        else:
            return True


class Check:
    '''Class-container for checking static methods'''
    @staticmethod
    def wind_size():
        """Verifies current window size"""
        rows, columns = View.get_wind_size()
        return (rows * columns) >= (STR_BLOCK_SIZE + 1) * 138

    @staticmethod
    def exist(file_name):
        return os.path.isfile(file_name)

    @staticmethod
    def md5_salt(file_name):
        md = hashlib.md5(open(file_name, 'rb').read()).hexdigest()
        return md == MD5_OF_SALT

    @staticmethod
    def file_length(file_name):
        return (os.path.getsize(file_name) >= READ_KB_NUM * KB)

    @staticmethod
    def duplicate(lst):
        return len(set(lst)) != BLOCK_NUM


class Controller:
    """Main logic class"""
    def __init__(self, base):
        # Get base and generate key
        self.base = base
        if self.base == 'TEXT':
            self.title, self.key = self.key_from_text()
        elif self.base == 'DATA':
            self.title, self.key = self.key_from_data()
        else:
            print('Internal error. Invalid base')
            exit(1)

        # Write key into file
        File.write(KEY_FNAME, self.key.normalized)

        # Write binary key into file
        File.write(BIN_KEY_FNAME, self.key.binary)

        # Show normalized key on the screen
        View.show(self.key.normalized, View.get_wind_size()[1])

        # Show recommended columns
        self.recommend()

        # Checking for duplicated blocks
        if Check.duplicate(self.key.blocks):
            print("WARNING: ONE OR MORE BLOCKS ARE DUPLICATED!")

        # Show normalized aplha key on the screen
        # View.show_alpha(self.key.alpha, ALPHA_SIZE)

        # Show normalized aplha key in TK window
        if ("-tk" in OPTS) or View.get_take_scr():
        # Show Tk alpha key and save the screenshot
            def save_in_backgrnd():
                """Calls gnome-screenshot in the background"""
                View.save_scrsht(
                    os.path.expanduser('~/' + \
                                       self.title.split('/')[-1] + \
                                       '.png'),
                    1)

            from threading import Timer
            timer = Timer(1.0, save_in_backgrnd)
            timer.start()
            View.show_alpha_tk(self.title, self.key.alpha, 50, ALPHA_SIZE[0])

        # Statistic showing
        # if ("-s" in OPTS) or View.get_stat():
            # View.stat_show_table(self.key.stat)

        if self.base == 'TEXT' and View.get_options():
            # Show denormalized key
            if View.get_denorm():
                View.show(self.key.string, View.get_wind_size()[1])

            # Average statistic showing
            if View.get_stat():
                View.stat_show_csv(self.key.stat_avg)

            # Files removing
            for file_name in (KEY_FNAME, SALT_FNAME):
                if View.get_remove(file_name):
                    File.remove(file_name)

    def key_from_text(self):
        while True:
            if Check.exist(SALT_FNAME) and Check.md5_salt(SALT_FNAME):
                salt = File.read_all(SALT_FNAME)
                break
            else:
                print(SALT_FNAME +
                        " is not OK. It's required for new creating")
                File.create_salt(SALT_FNAME, View.get_pass_phrase())
        text = View.get_text()
        iter = View.get_iter()

        return (text.decode() + ' #' + str(iter), KeyFromText(salt, text, iter))

    def key_from_data(self):
        while True:
            if len(argv) < 2:
                file_name = View.get_file_name()
            else: file_name = argv[1]

            if not Check.exist(file_name):
                print("File not found")
                break
            elif not Check.file_length(file_name):
                print("File size too small. Specify another one")
            else: break

        last_kb = os.stat(file_name).st_size // KB
        return (str(file_name), KeyFromData(File.read_one_kb(file_name,
                                                             last_kb)))

    def recommend(self):
        rows, columns = View.get_wind_size()
        if columns % 17 != 0:
            print('Columns:  ', columns, ', rows: ', rows)
            print("Columns recommended: 68, 102, 136, 170")


def main():
    if not Check.wind_size():
        print("Window is too small!")
        exit(1)

    Controller(View.get_base())

if __name__ == '__main__':
    main()
