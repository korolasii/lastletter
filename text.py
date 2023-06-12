import string
import asyncio

finish_spisok = {}


async def main(pleyer_sms, pleyer_name):
    await open_file_txt()
    chek_word = None
    pleyer_sms = pleyer_sms.lower().strip(string.punctuation + " " + string.digits)
    if await check_word(pleyer_sms, chek_word) and await find_word(pleyer_sms, spisok_txt):
        await dob(pleyer_sms, spisok_txt, pleyer_name)
        return True
    else:
        return False


async def open_file_txt():
    global spisok_txt
    with open('russian_nouns.txt', encoding='utf-8') as file:
        spisok_txt = file.read().split('\n')
    return spisok_txt


async def add_pleyer_in_spisok(pleyer_vubor):
    for i in range(len(pleyer_vubor)):
        finish_spisok[pleyer_vubor[i]] = []
    return finish_spisok


async def find_word(pleyer_sms, spisok_txt):
    if pleyer_sms in spisok_txt:
        return True
    else:
        return False


async def check_word(pleyer_sms, chek_word):
    if pleyer_sms[0] == chek_word or chek_word is None:
        return True
    else:
        return False


async def dob(pleyer_sms, spisok_txt, pleyer_name):
    if await find_word(pleyer_sms, spisok_txt):
        finish_spisok.get(pleyer_name).append(str(pleyer_sms))
        return finish_spisok


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pleyer_sms=None, pleyer_name=None))
