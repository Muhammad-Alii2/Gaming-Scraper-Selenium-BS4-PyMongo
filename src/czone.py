import requests
from bs4 import BeautifulSoup
from mongodb import MongoDBHandler


def getGraphicCards(db_handler):
    next_page_url = '/graphic-cards-pakistan-ppt.154.aspx'
    base_url = 'https://www.czone.com.pk'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    while True:
        url = base_url + next_page_url
        try:
            response = requests.get(url)  # Make a GET request to the URL
            response.raise_for_status()  # Raise an error for HTTP requests that return an unsuccessful status code
            soup = BeautifulSoup(response.content, 'html.parser')  # Parse HTML content
            products = soup.find_all(class_='col-lg-12 col-md-12 col-sm-12 col-xs-12')  # Find all product containers

            for product in products:
                try:
                    stock_status = product.find(class_='product-stock').find(class_='product-data').text
                    if stock_status == 'Out of Stock':
                        continue  # Skip products that are out of stock
                    # Extract product image URL
                    image_src = base_url + product.find(class_='image').img['src']
                    # Extract product title
                    title = product.h4.text
                    # Extract product price
                    price = float(product.find(class_='price').span.text.replace('Rs.', '').replace(',', ''))
                    # Extract product description
                    description_list = [desc.text for desc in product.find('ul').find_all('li')]
                    # Extract product link
                    link = base_url + product.h4.a['href']

                    # Append extracted data to respective lists
                    product_images.append(image_src)
                    product_titles.append(title)
                    product_prices.append(price)
                    product_descriptions.append('\n'.join(description_list))
                    product_links.append(link)
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check for the next page link
            next_page_link = soup.find(class_='pagination no-margin-top').find(class_='NextPage')
            if not next_page_link or not next_page_link.has_attr('href'):
                break  # Exit loop if no more pages
            else:
                next_page_url = next_page_link['href']
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve the webpage: {e}")
            break  # Exit loop on request failure

    try:
        # Save collected data to the database
        db_handler.saveToDB('czone', 'graphic_card', product_images, product_titles, product_prices,
                            product_descriptions, product_links)
    except Exception as e:
        print(f"Error saving to database: {e}")


def getProcessors(db_handler):
    next_page_url = '/processors-pakistan-ppt.85.aspx'
    base_url = 'https://www.czone.com.pk'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    while True:
        url = base_url + next_page_url
        try:
            response = requests.get(url)  # Make a GET request to the URL
            response.raise_for_status()  # Raise an error for HTTP requests that return an unsuccessful status code
            soup = BeautifulSoup(response.content, 'html.parser')  # Parse HTML content
            products = soup.find_all(class_='col-lg-12 col-md-12 col-sm-12 col-xs-12')  # Find all product containers

            for product in products:
                try:
                    stock_status = product.find(class_='product-stock').find(class_='product-data').text
                    if stock_status == 'Out of Stock':
                        continue  # Skip products that are out of stock
                    # Extract product image URL
                    image_src = base_url + product.find(class_='image').img['src']
                    # Extract product title
                    title = product.h4.text
                    # Extract product price
                    price = float(product.find(class_='price').span.text.replace('Rs.', '').replace(',', ''))
                    # Extract product description
                    description_list = [desc.text for desc in product.find('ul').find_all('li')]
                    # Extract product link
                    link = base_url + product.h4.a['href']

                    # Append extracted data to respective lists
                    product_images.append(image_src)
                    product_titles.append(title)
                    product_prices.append(price)
                    product_descriptions.append('\n'.join(description_list))
                    product_links.append(link)
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check for the next page link
            next_page_link = soup.find(class_='pagination no-margin-top').find(class_='NextPage')
            if not next_page_link or not next_page_link.has_attr('href'):
                break  # Exit loop if no more pages
            else:
                next_page_url = next_page_link['href']
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve the webpage: {e}")
            break  # Exit loop on request failure

    try:
        # Save collected data to the database
        db_handler.saveToDB('czone', 'processor', product_images, product_titles, product_prices, product_descriptions,
                            product_links)
    except Exception as e:
        print(f"Error saving to database: {e}")


def czoneRunAll():
    db_handler = MongoDBHandler()  # Create a new database handler instance
    try:
        # Run the scraping functions for different product categories
        getGraphicCards(db_handler)
        getProcessors(db_handler)
    except Exception as e:
        print(f"Error in czoneRunAll: {e}")
    finally:
        db_handler.close_connection()  # Close the database connection
