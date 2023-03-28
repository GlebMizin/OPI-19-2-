#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path
import click


def add_bank_acc(account, s_b_a, b_a, t_a):
    """
    Request for bank account details with verification
    """
    account.append(
        {
            "s_b_a": s_b_a,
            "b_a": b_a,
            "t_a": t_a
        }
    )
    return account


def display_accs(accounts):
    """
    Отобразить список аккаунтов.
    """

    if accounts:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 2,
            '-' * 25,
            '-' * 25,
            '-' * 10
        )
        print(line)
        print(
            '| {:^2} | {:^25} | {:^25} | {:^10} |'.format(
                "№",
                "Sender bank account",
                "beneficiary account",
                "Amount",
            )
        )
        print(line)
        # Вывести данные о всех сотрудниках.
        for ind, requisite in enumerate(accounts, 1):
            print(
                '| {:^2} | {:^25} | {:^25} | {:^10} |'.format(
                    ind,
                    requisite.get('s_b_a'),
                    requisite.get('b_a'),
                    requisite.get('t_a'),
                )
            )
            print(line)
    else:
        print("Нет введенных банковских счетов.")


def sum_check(requisites, account):
    """"
    Amount of all money withdrawn
    """
    full_summa = 0
    for sender_req in requisites:

        if int(sender_req.get("s_b_a")) == int(account):
            full_summa += float(sender_req.get("t_a"))

    if full_summa == 0:
        print("Данного аккаунта нет в выбранном файле!")
    else:
        return print(f"Сумма трансфера введенного аккаунта: {full_summa}")


def save_workers(file_name, accounts):
    """
    Сохранить все данные в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(accounts, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить все данные из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


@click.command()
@click.argument('command')
@click.argument('filename')
@click.option('--s_b_a', help='The person`s name')
@click.option('--b_a', help='The zodiac_sign')
@click.option('--t_a', help='The birth')
def main(command, filename, s_b_a, b_a, t_a):
    is_dirty = False
    if os.path.exists(filename):
        requisites = load_workers(filename)
    else:
        requisites = []

    if command == "add":
        s_b_a = click.prompt("Введите счёт отправителя: ")
        b_a = click.prompt("Введите счёт отправителя: ")
        t_a = click.prompt("Введите сумму трансфера: ")
        requisites = add_bank_acc(
            requisites,
            s_b_a,
            b_a,
            t_a
        )
        is_dirty = True

    elif command == "display":
        display_accs(requisites)

    elif command == "select":
        sum_check(requisites, t_a)

    if is_dirty:
        save_workers(filename, requisites)


if __name__ == "__main__":
    main()