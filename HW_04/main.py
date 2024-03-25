import os
from pathlib import Path
import requests
import time
import argparse
import threading
from multiprocessing import Process
import asyncio
import aiohttp

images = []
with open('images.txt', 'r') as f:
    for image in f.readlines():
        images.append(image.strip())

PATH = Path('images')


def download_img(url, dir_path=PATH):
    start_time = time.time()
    response = requests.get(url)
    filename = url.split('/')[-1]
    with open(os.path.join(dir_path, filename), 'wb') as f:
        for data in response.iter_content(1024):
            f.write(data)
    end_time = time.time() - start_time
    print(f'Загрузка {filename} длилась {end_time:.2f} секунд')


def parse():
    parser = argparse.ArgumentParser(description='Парсер изображений по URL-адресам')
    parser.add_argument('-u', '--urls', default=images, nargs='+', type=str, help='Список URL-адресов')
    return parser.parse_args()


async def download_img_as(url, dir_path=PATH):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            item = await response.read()
            filename = url.split('/')[-1]
            with open(os.path.join(dir_path, filename), 'wb') as f:
                f.write(item)
    end_time = time.time() - start_time
    print(f'Загрузка {filename} длилась {end_time:.2f} секунд')


def download_img_threading(urls):
    threads = []
    start_time = time.time()

    for url in urls:
        thread = threading.Thread(target=download_img, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time() - start_time
    print(f'Общее время загрузки {end_time:.2f} секунд')


def download_img_processing(urls):
    processes = []
    start_time = time.time()

    for url in urls:
        process = Process(target=download_img, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time() - start_time
    print(f'Общее время загрузки {end_time:.2f} секунд')


async def download_img_asyncio(urls):
    tasks = []
    start_time = time.time()

    for url in urls:
        task = asyncio.create_task(download_img_as(url))
        tasks.append(task)

    await asyncio.gather(*tasks)

    end_time = time.time() - start_time
    print(f'Общее время загрузки {end_time:.2f} секунд')


if __name__ == '__main__':
    urls = parse().urls

    if not os.path.exists(PATH):
        os.mkdir(PATH)

    print(f'Загрузка через многопоточный подход')
    download_img_threading(urls)

    print(f'Загрузка через многопрецессерный подход')
    download_img_processing(urls)

    print(f'Загрузка через асинхронный подход')
    asyncio.run(download_img_asyncio(urls))