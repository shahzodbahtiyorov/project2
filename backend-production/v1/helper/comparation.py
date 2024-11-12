def compare(fio_1, fio_2):
    min_length = min(len(fio_1), len(fio_2))
    fio_1 = list(fio_1[:min_length])
    fio_2 = list(fio_2[:min_length])

    for item in fio_1:
        for key, val in enumerate(fio_2):
            if item == val:
                del fio_2[key]
                break

    return 100 - int(len(fio_2) * 100 / min_length) if min_length != 0 else 100


def convert_text_latin(text):
    cyr = [
        'қ', 'Қ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
        'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
        'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
        'Р', 'С', 'Т', 'У', 'Ў', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'
    ]
    lat = [
        'q', 'Q', 'a', 'b', 'v', 'g', 'd', 'e', 'yo', 'j', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p',
        'r', 's', 't', 'u', 'f', 'h', 'ts', 'ch', 'sh', 'sh', 'a', 'i', 'y', 'e', 'yu', 'ya',
        'A', 'B', 'V', 'G', 'D', 'E', 'Yo', 'J', 'Z', 'I', 'Y', 'K', 'L', 'M', 'N', 'O', 'P',
        'R', 'S', 'T', 'U', 'O', 'F', 'H', 'Ts', 'Ch', 'Sh', 'Sh', 'A', 'I', 'Y', 'e', 'Yu', 'Ya'
    ]

    # Zip the cyrillic and latin lists into a dictionary for character replacement
    cyr_to_lat = dict(zip(cyr, lat))

    # Replace characters based on the dictionary mapping
    return ''.join(cyr_to_lat.get(c, c) for c in text)


def remove_chars(value):
    chars_to_remove = ['\'', '"', "'", "`", ',', ';', '.', '’', '-', '‘', '/', '+', ')', '(', ' ']
    # Replace or remove specific characters as required
    title = ''.join(char for char in value if char not in chars_to_remove)
    return title


def compare_strings(a, b):
    a = remove_chars(convert_text_latin(a).lower())
    b = remove_chars(convert_text_latin(b).lower())

    if a == b:
        return 100

    ex_list = {
        "'": '',
        'u': 'o',
        'q': 'k',
        'kh': 'h',
        'x': 'h',
        'dj': 'j',
        'ie': 'iye',
        'oev': 'oyev',
        'ae': 'aye',
    }

    for key, value in ex_list.items():
        a = a.replace(key, value)
        b = b.replace(key, value)

        a_first = a[:1]
        b_first = b[:2]
        if a_first == 'e' and b_first == 'ye':
            a = 'y' + a

        a_first = a[:2]
        b_first = b[:1]
        if b_first == 'e' and a_first == 'ye':
            b = 'y' + b

    if a[:3] != b[:3]:
        return -1
    else:
        return compare(a, b)  # Recursive call


def compare_fio(user, fio_1, fio_2, type=1):
    fio_1 = [part for part in fio_1.replace('/', ' ').split(' ') if part]
    fio_2 = [part for part in fio_2.replace('/', ' ').split(' ') if part]
    fio_1.sort()
    fio_1 = fio_1[:2]
    fio_2.sort()
    fio_2 = fio_2[:2]
    # print(fio_1[1], fio_2[2])
    if len(fio_1) < 2 or len(fio_2) < 2:
        return -2

    x = compare_strings(fio_1[0], fio_2[0])
    y = compare_strings(fio_1[1], fio_2[1])

    fio_2[0], fio_2[1] = fio_2[1], fio_2[0]

    x2 = compare_strings(fio_1[0], fio_2[0])
    y2 = compare_strings(fio_1[1], fio_2[1])

    if (x + y) < (x2 + y2):
        x = x2
        y = y2

    if type == 1:
        return min(x, y)
    else:
        return int((x + y) / 2)
