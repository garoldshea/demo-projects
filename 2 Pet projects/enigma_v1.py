refdict = {0: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
           1: 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
           2: 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
           3: 'ENKQAUYWJICOPBLMDXZVFTHRGS',
           4: 'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
          }

def plugboard(pairs = ""):
    # Реализует механизм коммутации разъемов.
    # pairs может принимать одно из 3 видов значений:
    # --- пустая строка, либо отсутствует в вызове - символы не заменяются 
    #     коммутационной панелью
    # --- строка из 2 символов - только эти 2 символа заменяются ДО и ПОСЛЕ
    #     шифрования
    # --- строка из n пар символов, разделённых пробелом. Замены производятся
    #     в парах ДО и ПОСЛЕ шифрования.
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    string_symbols = "".join(pairs.upper().split())
    for i in string_symbols:
        if i not in alphabet or string_symbols.count(i) > 1:
            return False
    for i in pairs.split():
        if len(i) % 2:
            return False
    return True

def rotor(symbol, n, reverse=False):
    # Реализует шифрование по первым 4 роторам из спецификации Энигмы.
    # symbol - символ, поступающий для шифрования
    # n - номер ротора
    # reverse - признак обратного направления.
    k = -1 if reverse else 1
    rdict = {1: ('AELTPHQXRU', 'BKNW', 'CMOY', 'DFG', 'IV', 'JZ', 'S'),
        2: ('FIXVYOMW', 'CDKLHUP', 'ESZ', 'BJ', 'GR', 'NT', 'A', 'Q'),
        3: ('ABDHPEJT', 'CFLVMZOYQIRWUKXSG', 'N'),
        4: ('AEPLIYWCOXMRFZBSTGJQNH', 'DV', 'KU'),
        }
    if n:
        for i in rdict[n]:
            if symbol in i:
                return i[(i.index(symbol) + k) % len(i)]
    return symbol

def reflector(symbol, n):
    # Реализация отражателя. Он аналогичен ротору, за 2 исключениями:
    # --- имеет только 1 направление    
    # --- отражатель с функцией шифрования всегда соединяет символы парами
    # symbol - символ, поступающий для шифрования
    # n - номер отражателя (1 - отражатель вида "B", 0 - без шифрования).
    return refdict[n][refdict[0].index(symbol)]

def caesar(text, key, alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    # Реализует алгоритм шифрования Цезаря.
    new_text = [i for i in text.upper() if i in alphabet]
    encrypt = [alphabet[(alphabet.index(i) +
    key) % len(alphabet)] for i in new_text]
    return ''.join(encrypt)

def enigma(text, ref, rot1, shift1, rot2, shift2, rot3, shift3, pairs=""):
    # Реализует аппарат Энигмы. Если атрибут pairs принял недопустимое 
    # значение (например 1 символ участвует в 2 или более парах) - возвращает
    # текст error.
    error = "Извините, невозможно произвести коммутацию"
    noutch_dict = {0: 0, 1: 17, 2: 5, 3: 22, 4: 10, 5: 0}
    if not plugboard(pairs):
        return error
    pairs_dict = {0: '', 1: ''}
    for pair in pairs.upper().split():
        pairs_dict[0] += pair[0]
        pairs_dict[1] += pair[1]
    output = ''
    for symbol in text.upper().replace(" ",""):
        shift3 += 1
        if shift3 % 26 == noutch_dict[rot3] or shift2 == noutch_dict[rot3] - 1:
            shift2 += 1
            if shift2 == noutch_dict[rot2]:
                shift1 += 1
        if symbol in pairs_dict[0]:
            symbol = pairs_dict[1][pairs_dict[0].index(symbol)]
        elif symbol in pairs_dict[1]:
            symbol = pairs_dict[0][pairs_dict[1].index(symbol)]
        symbol = rotor(caesar(symbol, shift3), rot3)
        symbol = rotor(caesar(symbol, shift2 - shift3), rot2)
        symbol = rotor(caesar(symbol, shift1 - shift2), rot1)
        symbol = reflector(caesar(symbol, shift1 * -1), ref)
        symbol = rotor(caesar(symbol, shift1), rot1, reverse=True)
        symbol = rotor(caesar(symbol, shift2 - shift1), rot2, reverse=True)
        symbol = rotor(caesar(symbol, shift3 - shift2), rot3, reverse=True)
        symbol = caesar(symbol, shift3 * -1)
        if symbol in pairs_dict[0]:
            symbol = pairs_dict[1][pairs_dict[0].index(symbol)]
        elif symbol in pairs_dict[1]:
            symbol = pairs_dict[0][pairs_dict[1].index(symbol)]
        output += symbol
    return output

# print(enigma('Welcome to Bletchley Park', 1, 1, 0, 2, 0, 3, 0))
