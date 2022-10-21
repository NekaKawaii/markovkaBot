import json


def parse():
    """
    Парсинг выгруженных сообщений из чата телеграмма, чтобы сформировать txt файл
    корпуса текста, из которого строится цепь Маркова.
    Файл должен называться result.json и лежать в той же папке что и этот файл.
    Результирующий файл будет называться corpus.txt, и с ним уже может работать markovify
    """
    with open('result.json', 'rt') as f, open('corpus.txt', 'wt') as c:
        data = json.load(f)

        # Перебираем все сообщения в истории чата
        for msg in data['messages']:
            # Парсим сообщение
            parsed_message = parse_message(msg)
            # Если сообщени было распарсено, записываем в файл корпуса текста
            if parsed_message:
                c.write(parsed_message + "\n")


def parse_message(message):
    """
    Парсинг сообщения из чата телеграма
    """

    # Сообщение должно иметь тип message
    if message['type'] != 'message':
        return None

    # Текстовые части сообщения в виде списка, чтобы объединить их новой строкой
    texts = []

    # Перебираем все части сообщения
    for txt_part in message['text_entities']:

        # Нам нужны части с типом plain и не пустые
        if txt_part['type'] != 'plain' or txt_part['text'] == '':
            continue

        # Убираем лишние переносы строк, чтобы не было пустых строк в итоговом сообщении
        msg = "".join(l for l in txt_part['text'].splitlines() if l)

        # И добавляем часть сообщения в список частей
        texts.append(msg)

    # Объединяем части сообщений в одно сообщение через перенос строки
    return "\n".join(texts)


if __name__ == '__main__':
    """
    Запуск парсинга файла
    """
    parse()
