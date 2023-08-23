import requests
import concurrent.futures
import json
import random
import datetime
import progress_bar

with open('config.json', encoding='utf-8') as f:
    config = json.load(f)

cookies = config['cookies']

def check_page(page):
    url = f"{config['base_url']}/{page}"
    response = requests.get(url, cookies=cookies).status_code
    if response != 404:
        if 3 > config['log_level'] > 0:
            print(f"Found: {page}")
        with open('found_pages.txt', 'a', encoding='utf-8') as f:
            f.write(f"{page}\n")
    
    if config['log_level'] == 3:
        progress_bar.update()
            
    return {'page': page, 'status': response}




with open("first_names.txt", "r", encoding='utf-8') as f:
    first_names = []
    for name in f.readlines():
        first_names.append(name.replace('\n', '').replace(' ',''))

with open("last_names.txt", "r", encoding='utf-8') as f:
    last_names = []
    for name in f.readlines():
        last_names.append(name.replace('\n', '').replace(' ',''))

def generate_name():
    first = random.choice(first_names)
    last = random.choice(last_names)

    page = first.lower()

    if random.random() < 0.5:
        if random.random() < 0.5:
            page = page + last.lower()
        else:
            page = page + "-" + last.lower()

    if random.random() < 0.5:
        if "-" in page:
            if random.random() < 0.5:
                page = page + "s-portfolio"
            else:
                page = page + "-portfolio"
        else:
            if random.random() < 0.5:
                page = page + "sportfolio"
            else:
                page = page + "portfolio"

    return page

def get_pages_to_try(num):
    tried = set(open('tried_pages.txt', encoding='utf-8').read().split())    
    pages = []
    if config['log_level'] == 3:
        progress_bar.init('Generating possible pages', 'pages', num)
    
    num_of_pages = 0
    n=1
    for i in range(500*num):
        n+=1
        page = generate_name()
        if page not in tried:
            num_of_pages +=1
            pages.append(page)
            tried.add(page)
            if config['log_level'] == 3:
                progress_bar.update()
        if num_of_pages >= num:
            break
    if n >=500*num:
        exit('\nExiting. Cannot find find any new pages to try')
            
    with open('tried_pages.txt', 'a',  encoding='utf-8') as f:
        f.writelines([f"{p}\n" for p in tried - set(open('tried_pages.txt',  encoding='utf-8').read().split())])
        
    return pages
        
def scan_pages(num_pages, threads):
    pages = get_pages_to_try(num_pages)
    if config['log_level'] == 3:
            progress_bar.init('Scanning throgh pages', 'pages', len(pages))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_page, page) for page in pages]
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result["status"] == 200:
                results.append(result)

        if config['log_level'] == 3:
            print(f'')
            for result in results:
                print(f'Found: {result["page"]}')
        
            

def lines_in_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        line_count = len(lines)

    return line_count



if __name__ == '__main__':

    try:
        f = open('tried_pages.txt', 'r')
        f.close()
    except:
        with open('tried_pages.txt', 'w') as f:
            f.write('')


    print('------------------------------------------------------------------------------------------------------------------------------------------------------')
    print(f'Scanning for pages on {config["base_url"]}\nbatch_size={config["batch_size"]}, threads={config["threads"]}')
    print('------------------------------------------------------------------------------------------------------------------------------------------------------')

    while True:
        start_time = datetime.datetime.now()

        

        scan_pages(config['batch_size'], config['threads'])        

        if config['log_level'] >1:
            delta = (datetime.datetime.now() - start_time).total_seconds()
            tried_pages=lines_in_file("tried_pages.txt")
            found_pages=lines_in_file("found_pages.txt")
            speed=config["batch_size"]/delta

            print(f'\nTime Delta: {delta}s.    Scanned Pages:{config["batch_size"]} pages.    Avg. Pace: {round(speed,2)} pages/s.    Scanned: {tried_pages} pages.    Found: {found_pages} pages.    Success: {round(found_pages/tried_pages, 10)} p/f')
            print('------------------------------------------------------------------------------------------------------------------------------------------------------')


