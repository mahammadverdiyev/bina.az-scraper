import scraper

url = 'https://bina.az/baki/alqi-satqi/menziller'

if __name__ == '__main__':
    try:
        room_count = int(input("Enter room count: "))
    except ValueError:
        room_count = None

    if room_count:
        url += f"/{room_count}-otaqli"

    try:
        price_from = int(input("Minimum price: "))
    except ValueError:
        price_from = None

    try:
        price_to = int(input("Maximum price: "))
    except ValueError:
        price_to = None

    if price_from:
        url += f"?price_from={price_from}"

    if price_to:
        url += f"?price_to={price_to}" if price_from is None else f"&price_to={price_to}"

    file_name = input("Enter file name: ")

    try:
        row_limit = int(input("Enter row limit: "))
    except ValueError:
        row_limit = None

    scraper.start_scraping(url, file_name, row_limit)
