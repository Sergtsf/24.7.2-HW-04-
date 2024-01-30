from api import PetFriends
from settings import valid_email, valid_password, incorrect_email, incorrect_password
import os

pf = PetFriends()

    ### 1) Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key ###
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


    ### 2) Проверяем что запрос всех питомцев возвращает не пустой список.
    # Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    # запрашиваем список всех питомцев и проверяем что список не пустой.
    # Доступное значение параметра filter - 'my_pets' либо '' ###
def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


    ### 3) Проверяем что можно добавить питомца с корректными данными ###
def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/Dog.jpg'):

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


    ### 4) Проверяем возможность удаления питомца ###
def test_successful_delete_self_pet():

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомцаdef pure_intersection(arr1, arr2):
    assert status == 200
    assert pet_id not in my_pets.values()


    ### 5) Проверяем возможность обновления информации о питомце ###
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


    ### 6) Проверяем, что можно добавить питомца с корректными данными без фото ###
def test_create_pet_simple(name = 'Рэкс', animal_type = 'Овчарка', age = 2):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


    ### 7) Проверяем, что можно добавить фото в карточку питомца ###
def test_set_photo(pet_photo='images/PhotoCat.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

# Если список пуст, то создаем нового питомца без фото
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, 'PhotoCat', 'кот', 1)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

# Берём id первого питомца из списка и обновляяем/добавляем фото ###
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert 'photo' in result or 'pet_photo' in result


    ### 8) Проверяем, возможность добавить недопустимый формат файла ###
def test_set_incorrect_photo(pet_photo='images/GifCat.gif'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список пуст, то создаем нового питомца без фото
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, 'PhotoCat', 'кот', 1)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и обновляяем/добавляем фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 500


    ### 9) Проверяем что api ключ НЕ генерируется, при вводе невалидных данных ###
def test_get_api_key_for_incorrect_user(email=incorrect_email, password=incorrect_password):

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


    ### 10) Проверяем, возможность добавить питомца с некорректными данными (возраст) ###
def test_create_incorrect_pet_simple(name = 'Рэкс', animal_type = 'Овчарка', age = 'abc'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    #
    assert status == 200
    assert result['name'] == name


    ### 11) Проверяем возможность обновления информации о питомце некорректными данными
    ### В Имя и Порода больше 255 символов
def test_not_successful_update_self_pet_info(name='1'* 256, animal_type='$' * 256, age= 'abc'):

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


    ### 12) Возможность отчистки списка Мои питомцы ###
def test_delete_all_pets():

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем несколько и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Cat.jpeg")
        pf.add_new_pet(auth_key, "Суперкот1", "кот1", "1", "images/Cat2.jpg")
        pf.add_new_pet(auth_key, "Суперкот2", "кот2", "2", "images/Dog.jpg")
        pf.add_new_pet(auth_key, "Суперкот3", "кот3", "3", "images/PhotoCat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Перебираем всех питомцев и удаляем по очереди
    for pet in my_pets['pets']:
        pet_id = pet['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомцаdef pure_intersection(arr1, arr2):
    assert status == 200
    assert pet_id not in my_pets.values()


    ### 13) Проверяем возможность обновления на пустые значения о питомце ###
def test_empty_update_self_pet_info(name=' ', animal_type=' ', age=' '):

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пустой, добавляем нового и меняем его значения
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == ' '

    ### 14) Проверка списка Мои питомцы, значения параметра filter - 'my_pets'
def test_get_my_pets_with_valid_key(filter='my_pets'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) >= 0


    ### 15) Проверка, добавления питомца с отрицательным возрастом ###
def test_negative_age_pet(name = 'Рэкс', animal_type = 'Овчарка', age = -10):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name