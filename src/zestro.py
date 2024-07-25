from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mongodb import MongoDBHandler


# Function to scrape gaming PCs from ZestroGaming
def getGamingPcs(db_handler):
    url = 'https://zestrogaming.com/product-category/gaming-pc-price-in-pakistan/'

    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Fetch the webpage
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract product information
    products = soup.find_all(class_='jet-woo-products__item jet-woo-builder-product')
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    for product in products:
        try:
            # Extract image source, title, price, description, and link
            product_images.append(product.find(class_='jet-woo-product-thumbnail').img['src'])
            product_titles.append(product.find(class_='jet-woo-product-title').text)
            if product.find(class_='jet-woo-product-price').ins:
                product_prices.append(
                    float(product.find(class_='jet-woo-product-price').ins.bdi.text.replace('₨', '').replace(',', '')))
            else:
                product_prices.append(
                    float(product.find(class_='jet-woo-product-price').bdi.text.replace('₨', '').replace(',', '')))
            details_text = product.find(class_='jet-woo-product-excerpt').text.strip()
            details_list = [point.strip().replace('\xa0', ' ') for point in details_text.split('\n')]
            product_descriptions.append('\n'.join(details_list))
            product_links.append(product.a['href'])
        except Exception as e:
            print(f"Error processing product: {e}")

    # Save the extracted data to the database
    db_handler.saveToDB('zestrogaming', 'gaming_pc', product_images, product_titles, product_prices,
                        product_descriptions, product_links)


# Function to scrape graphic cards from ZestroGaming
def getGraphicCards(db_handler):
    url = 'https://zestrogaming.com/product-category/graphics-card-price-in-pakistan/'

    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Fetch the webpage
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract product information
    products = soup.find_all(class_='jet-woo-products__item jet-woo-builder-product')
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    for product in products:
        try:
            # Extract image source, title, price, description, and link
            product_images.append(product.find(class_='jet-woo-product-thumbnail').img['src'])
            product_titles.append(product.find(class_='jet-woo-product-title').text)
            if product.find(class_='jet-woo-product-price').ins:
                product_prices.append(
                    float(product.find(class_='jet-woo-product-price').ins.bdi.text.replace('₨', '').replace(',', '')))
            else:
                product_prices.append(
                    float(product.find(class_='jet-woo-product-price').bdi.text.replace('₨', '').replace(',', '')))
            details_text = product.find(class_='jet-woo-product-excerpt').text.strip()
            details_list = [point.strip().replace('\xa0', ' ') for point in details_text.split('\n')]
            product_descriptions.append('\n'.join(details_list))
            product_links.append(product.a['href'])
        except Exception as e:
            print(f"Error processing product: {e}")

    # Save the extracted data to the database
    db_handler.saveToDB('zestrogaming', 'graphic_card', product_images, product_titles, product_prices,
                        product_descriptions, product_links)


# Function to scrape processors from ZestroGaming
def getProcessors(db_handler):
    url = 'https://zestrogaming.com/product-category/processor-price-in-pakistan/'

    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Fetch the webpage
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract product information
    products = soup.find_all(class_='jet-woo-products__item jet-woo-builder-product')
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    for product in products:
        try:
            # Extract image source, title, price, description, and link
            product_images.append(product.find(class_='jet-woo-product-thumbnail').img['src'])
            product_titles.append(product.find(class_='jet-woo-product-title').text)
            if product.find(class_='jet-woo-product-price').ins:
                product_prices.append(
                    float(product.find(class_='jet-woo-product-price').ins.bdi.text.replace('₨', '').replace(',', '')))
            else:
                product_prices.append(
                    float(product.find(class_='jet-woo-product-price').bdi.text.replace('₨', '').replace(',', '')))
            details_text = product.find(class_='jet-woo-product-excerpt').text.strip()
            details_list = [point.strip().replace('\xa0', ' ') for point in details_text.split('\n')]
            product_descriptions.append('\n'.join(details_list))
            product_links.append(product.a['href'])
        except Exception as e:
            print(f"Error processing product: {e}")

    # Save the extracted data to the database
    db_handler.saveToDB('zestrogaming', 'processor', product_images, product_titles, product_prices,
                        product_descriptions, product_links)


# Function to run all scraping tasks
def zestroRunAll():
    db_handler = MongoDBHandler()
    try:
        # Call the scraping functions
        getGamingPcs(db_handler)
        getGraphicCards(db_handler)
        getProcessors(db_handler)
    except Exception as e:
        print(f"Error in zestroRunAll: {e}")
    finally:
        # Close the database connection
        db_handler.close_connection()
