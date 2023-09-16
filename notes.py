"""   Задание 1. Приложение заметки (Python)
Напишите проект, содержащий функционал работы с заметками.
Программа должна уметь создавать заметку, сохранять её,
читать список заметок, редактировать заметку, удалять заметку.
"""
from datetime import datetime, timedelta
from json import dumps, dump
from io import StringIO
import csv

file_path = 'notes.csv'


def read_file(file_name):
    result = []
    with open(file_name, 'r', encoding='utf-8', newline='') as text_file:
        note_reader = csv.reader(text_file, delimiter=';')
        for note in note_reader:
            result.append(note)
    return result


def write_file(list_notes, file_name):
    with open(file_name, 'w', encoding='utf-8', newline='') as text_file:
        csv.writer(text_file, delimiter=';').writerows(list_notes)


def write_note_to_end_file(note, file_name):
    with open(file_name, 'a', encoding='utf-8', newline='') as text_file:
        csv.writer(text_file, delimiter=';').writerow(note)


def sort_key(lst):
    return int(lst[0])


def sort_by_id(list_notes):
    return sorted(list_notes, key=sort_key)


def filter_by_date(list_notes, date_filter):
    result = []
    for note in list_notes:
        if note[-1].split()[0] == date_filter:
            result.append(note)
    return result


def note_to_string(note, style='simple'):
    if style == 'simple':
        return '\n'.join(note[1:3])
    if style == 'txt':
        result = 'Идентификатор заметки = ' + note[0] + '\n'
        result += 'Заголовок заметки = ' + note[1] + '\n'
        result += 'Тело заметки = ' + note[2] + '\n'
        result += 'Дата заметки = ' + note[3]
        return result
    if style == 'json':
        columns = ['id', 'title', 'body', 'timestamp']
        return dumps(dict(zip(columns, note)), ensure_ascii=False)
    if style == 'csv':
        output = StringIO()
        csv.writer(output, delimiter=';', lineterminator='').writerow(note)
        return output.getvalue()
    return '\n'.join(note)


def print_note(note, style='simple'):
    print(note_to_string(note, style), '\n')


def print_list_notes(list_notes, style_list='simple'):
    for note in list_notes:
        print_note(note, style=style_list)


def next_id(list_notes):
    if len(list_notes) > 0:
        return int(list_notes[-1][0]) + 1
    else:
        return 1


def date_time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def show_all_notes(file_name, style_show='simple'):
    print_list_notes(read_file(file_name), style_list=style_show)


def del_last_note(file_name):
    write_file(read_file(file_name)[:-1], file_name)


def replace_last_note(note, file_name):
    list_notes = read_file(file_name)
    if len(list_notes) > 0:
        list_notes[-1] = note
        write_file(list_notes, file_name)


def edit_note(note):
    result = list()
    result.append(note[0])
    answer = input('Планируете сментить заголовок (y/n)?')
    if answer.lower() == 'y':
        result.append(input('Введите новый заголовок заметки: '))
    else:
        result.append(note[1])
    result.append(input('Введите новое тело заметки: '))
    result.append(date_time_now())
    return result


def show_notes_filter_by_date(file_name, filter_date, style_show='simple'):
    print_list_notes(filter_by_date(read_file(file_name), filter_date), style_list=style_show)


def date_now(day=0):
    return (datetime.now()-timedelta(days=day)).strftime('%Y-%m-%d')


def index_row_by_id(list_notes, note_id):
    dict_id = {note[0]: i for i, note in enumerate(list_notes)}
    return dict_id.get(note_id, -1)


def show_note_by_id(file_name, note_id, style_show):
    list_notes = read_file(file_name)
    index_row = index_row_by_id(list_notes, note_id)
    if index_row == -1:
        print('отсутствует')
    else:
        print_note(list_notes[index_row], style_show)


def del_note_by_id(file_name, note_id):
    list_notes = read_file(file_name)
    index_row = index_row_by_id(list_notes, note_id)
    if index_row == -1:
        print('отсутствует')
    else:
        new_list_notes = list_notes[:index_row] + list_notes[index_row + 1:]
        write_file(new_list_notes, file_name)
        print('удалена')


def replace_note_by_id(file_name, note_id):
    list_notes = read_file(file_name)
    index_row = index_row_by_id(list_notes, note_id)
    if index_row == -1:
        print(f'Заметка c id={note_id} отсутствует')
    else:
        list_notes[index_row] = edit_note(list_notes[index_row])
        write_file(list_notes, file_name)
        print(f'Заметка c id={note_id} отредактирована')


def input_natural_number(msg):
    num = input(msg)
    try:
        n = int(num)
        return n if n > 0 else 10
    except ValueError:
        return 10


def show_head_notes(file_name, n, style_show):
    print_list_notes(read_file(file_name)[:n], style_show)


def show_tail_notes(file_name, n, style_show):
    print_list_notes(read_file(file_name)[-n:], style_show)


def export_to_json(list_notes, file_name):
    columns = ['id', 'title', 'body', 'timestamp']
    data = list()
    for note in list_notes:
        data.append(dict(zip(columns, note)))
    with open(file_name, 'w', encoding='utf-8') as text_file:
        dump(data, text_file, ensure_ascii=False)


def export_to_csv(list_notes, file_name):
    columns = ['id', 'title', 'body', 'timestamp']
    list_notes.insert(0, columns)
    write_file(list_notes, file_name)


def main():
    choice = ''
    style_view = 'simple'
    while choice != '0':
        choice = input("""
        Выберите действие:
        1. Добавить заметку
        2. Показать все заметки
        3. Сменить стиль отображения заметок
        4. Удалить последнюю заметку 
        5. Редактировать последнюю заметку
        6. Показать заметки по дате
        7. Показать заметку по id
        8. Редактировать заметку по id
        9. Удалить заметку по id
        10. Показать n первых заметок
        11. Показать n последних заметок
        12. Экспорт заметок в json-файл
        13. Экспорт заметок в csv-файл
        ---
        0. Выход
        """)
        if choice == '1':
            new_note = list()
            new_note.append(str(next_id(read_file(file_path))))
            new_note.append(input('Введите заголовок заметки: '))
            new_note.append(input('Введите тело заметки: '))
            new_note.append(date_time_now())
            write_note_to_end_file(new_note, file_path)
            print('Заметка успешно сохранена')
        elif choice == '2':
            print('Все заметки:')
            show_all_notes(file_path, style_view)
        elif choice == '3':
            print('Текущий стиль отображения:', style_view)
            style_view = input('Введите стиль отображения simple, csv, json, txt: ')
        elif choice == '4':
            del_last_note(file_path)
            print('Последняя заметка удалена.')
        elif choice == '5':
            list_notes = read_file(file_path)
            if len(list_notes) > 0:
                old_note = list_notes[-1]
                print('Последняя заметка:')
                print_note(old_note)
                replace_last_note(edit_note(old_note), file_path)
                print('Последняя заметка отредактирована')
            else:
                print('Нет заметок для редактирования')
        elif choice == '6':
            answer = input("""
            Показать заметки:
            1. за сегодня
            2. за вчера
            3. за позавчера
            4. сам введу дату в формате ГГГГ-ММ-ДД
            """)
            user_date = ''
            if answer == '4':
                user_date = input('Введите дату (ГГГГ-ММ-ДД): ')
            elif answer == '2':
                user_date = date_now(1)
            elif answer == '3':
                user_date = date_now(2)
            else:
                user_date = date_now()
            print(f'Заметки за {user_date}:')
            show_notes_filter_by_date(file_path, user_date, style_view)
        elif choice == '7':
            user_id = input('Введите id заметки: ')
            print(f'Заметка c id={user_id}:')
            show_note_by_id(file_path, user_id, style_view)
        elif choice == '8':
            user_id = input('Введите id заметки: ')
            replace_note_by_id(file_path, user_id)
        elif choice == '9':
            user_id = input('Введите id заметки: ')
            print(f'Заметка c id={user_id}:')
            del_note_by_id(file_path, user_id)
        elif choice == '10':
            k = input_natural_number('Введите количеcтво заметок: ')
            show_head_notes(file_path, k, style_view)
        elif choice == '11':
            k = input_natural_number('Введите количеcтво заметок: ')
            show_tail_notes(file_path, k, style_view)
        elif choice == '12':
            export_to_json(read_file(file_path), 'out_notes.json')
        elif choice == '13':
            export_to_csv(read_file(file_path), 'out_notes.csv')


main()