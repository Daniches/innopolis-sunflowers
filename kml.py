import codecs
import datetime
import json
import os
import re


def update_file(field, coorw, coorh, type, check, count, weight, name, surname, agent):
    oldfilename = "old.txt"

    if os.path.isfile('new.txt'):
        os.remove('new.txt')

    with codecs.open(oldfilename, 'r', encoding='utf-8') as f_old, open("new.txt", 'w', encoding='utf-8') as f_new:
        for line in f_old:
            f_new.write(line)
            if '<Data name="Поле"><value>' in line:
                json.dump(field, f_new, ensure_ascii=False)
            if '<Data name="Координаты"><value>' in line:
                coorh_s = coorh[:7]
                coorw_s = coorw[:7]
                json.dump(coorw_s + "," + coorh_s, f_new, ensure_ascii=False)
            if '<Data name="Вид подсолнечника"><value>' in line:
                json.dump(type, f_new, ensure_ascii=False)
            if '<Data name="Урожайность (%)"><value>' in line:
                json.dump(check, f_new, ensure_ascii=False)
            if '<Data name="Количество семян (шт)"><value>' in line:
                json.dump(count, f_new, ensure_ascii=False)
            if '<Data name="Средняя масса 1000 семян (г)"><value>' in line:
                json.dump(weight, f_new, ensure_ascii=False)
            if '<Data name="Имя"><value>' in line:
                json.dump(name, f_new, ensure_ascii=False)
            if '<Data name="Фамилия"><value>' in line:
                json.dump(surname, f_new, ensure_ascii=False)
            if '<Data name="Страховая компания"><value>' in line:
                json.dump(agent, f_new, ensure_ascii=False)
            if '<coordinates>' in line:
                coor_sum = coorw + "," + coorh
                f_new.write(coor_sum + "\n")

    now = datetime.datetime.now()
    data = now.strftime('%Y-%m-%d %H:%M:%S')
    data = re.sub(':', '-', data)

    os.rename('new.txt', str(data) + '.kml')
