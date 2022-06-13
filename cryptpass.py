print('Программа для шифрования/дешифрования текста')
choose = input('Выберите нужный вариант ("Шифрование" или "Дешифрование"): ')
if choose.lower() == 'шифрование':
    print('---Шифрование---')
    message = input('Введите сообщение для зашифровки: ')
    key = int(input('Введите ключ: '))
    message_arr = list()
    for x in message:
        message_arr.append((ord(x)))
    encrypt_arr = list()
    for i in range(len(message_arr)):
        encrypt_arr.append(message_arr[i] ^ key)
    encrypt_message = ''
    for char in encrypt_arr:
        encrypt_message += chr(int(char))
    print(f'Зашифрованное сообщение: {encrypt_message}')

elif choose.lower() == 'дешифрование':
    print('---Дешифрование---')
    encrypt_message = input('Введите сообщение для дешифровки: ')
    key = int(input('Введите ключ: '))
    encrypt_arr = list()
    for x in encrypt_message:
        encrypt_arr.append((ord(x)))
    decrypt_arr = list()
    for i in range(len(encrypt_arr)):
        decrypt_arr.append(int(encrypt_arr[i]) ^ key)
    decrypt_message = ''
    for char in decrypt_arr:
        decrypt_message += chr(int(char))
    print(f'Дешифрованное сообщение: {decrypt_message}')
else:
    print('Некорректный ввод')

