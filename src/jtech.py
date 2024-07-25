import requests
from bs4 import BeautifulSoup
from mongodb import MongoDBHandler


def getGraphicCards(db_handler):
    next_page_url = '/graphics-cards-gpu'
    base_url = 'https://www.junaidtech.pk'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    while True:
        try:
            url = base_url + next_page_url  # Construct the full URL for the current page
            response = requests.get(url)  # Make a GET request to the URL
            response.raise_for_status()  # Raise an error for unsuccessful status codes

            soup = BeautifulSoup(response.content, 'html.parser')  # Parse HTML content
            products = soup.find_all(class_='item col-sm-12 col-lg-12 col-md-12 col-xs-12 list-view')  # Find all product containers
            for product in products:
                try:
                    # Check if the product is out of stock
                    if product.find('div', {'name': 'list-stock'}).find(class_='product-data').text == 'Out of Stock':
                        continue  # Skip out-of-stock products

                    # Extract product image URL
                    product_images.append(product.img['src'])
                    # Extract product title
                    product_titles.append(product.h4.text)
                    # Extract product price
                    product_prices.append(float(product.find(class_='price').text.replace('Rs. ', '').replace(',', '')))

                    # Extract product description
                    if product.find(class_='description highlights text-left').find_all('li'):
                        details = product.find(class_='description highlights text-left').find_all('li')
                        description_list = [point.text for point in details]
                        product_descriptions.append('\n'.join(description_list))
                    else:
                        # Extract additional product description from <p> tags
                        description_list = [description.text for description in product.find_all('p')[1]]
                        description_list = [point.replace('• ', '') for point in description_list if point.startswith('•')]
                        product_descriptions.append('\n'.join(description_list))

                    # Extract product link
                    product_links.append(base_url + product.h4.a['href'])
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check for the next page link
            next_page_link = soup.find(class_='pagination no-margin-top').find(class_='NextPage')
            if not next_page_link or not next_page_link.has_attr('href'):
                break  # Exit loop if no more pages
            else:
                next_page_url = next_page_link['href']
        except Exception as e:
            print(f"Failed to retrieve the webpage: {e}")
            break  # Exit loop on request failure

    try:
        # Save collected data to the database
        db_handler.saveToDB('junaidtech', 'graphic_card', product_images, product_titles, product_prices,
                            product_descriptions, product_links)
    except Exception as e:
        print(f"Error saving to database: {e}")


def getProcessors(db_handler):
    next_page_url = '/processors-cpu'
    base_url = 'https://www.junaidtech.pk'
    product_images = []
    product_titles = []
    product_prices = []
    product_descriptions = []
    product_links = []

    while True:
        try:
            url = base_url + next_page_url  # Construct the full URL for the current page
            response = requests.get(url)  # Make a GET request to the URL
            response.raise_for_status()  # Raise an error for unsuccessful status codes

            soup = BeautifulSoup(response.content, 'html.parser')  # Parse HTML content
            products = soup.find_all(class_='item col-sm-12 col-lg-12 col-md-12 col-xs-12 list-view')  # Find all product containers
            for product in products:
                try:
                    # Check if the product is out of stock
                    if product.find('div', {'name': 'list-stock'}).find(class_='product-data').text == 'Out of Stock':
                        continue  # Skip out-of-stock products

                    # Extract product image URL
                    product_images.append(product.img['src'])
                    # Extract product title
                    product_titles.append(product.h4.text)
                    # Extract product price
                    product_prices.append(float(product.find(class_='price').text.replace('Rs. ', '').replace(',', '')))

                    # Extract product description
                    if product.find(class_='description highlights text-left').find_all('li'):
                        details = product.find(class_='description highlights text-left').find_all('li')
                        description_list = [point.text for point in details]
                        product_descriptions.append('\n'.join(description_list))
                    else:
                        # Extract additional product description from <p> tags
                        description_list = []
                        for p_element in product.find_all('p'):
                            points = p_element.decode_contents().split('<br>')
                            for point in points:
                                if point and point.startswith('•'):
                                    description_list.append(point.replace('• ', '').replace('<br/>', '\n'))
                                elif point:
                                    description_list.append(point.replace('<br/>', '\n'))
                        product_descriptions.append('\n'.join(description_list))

                    # Extract product link
                    product_links.append(base_url + product.h4.a['href'])
                except Exception as e:
                    print(f"Error processing product: {e}")

            # Check for the next page link
            next_page_link = soup.find(class_='pagination no-margin-top').find(class_='NextPage')
            if not next_page_link or not next_page_link.has_attr('href'):
                break  # Exit loop if no more pages
            else:
                next_page_url = next_page_link['href']
        except Exception as e:
            print(f"Failed to retrieve the webpage: {e}")
            break  # Exit loop on request failure

    try:
        # Save collected data to the database
        db_handler.saveToDB('junaidtech', 'processor', product_images, product_titles, product_prices, product_descriptions,
                            product_links)
    except Exception as e:
        print(f"Error saving to database: {e}")


def jtechRunAll():
    db_handler = MongoDBHandler()  # Create a new database handler instance
    try:
        # Run the scraping functions for different product categories
        getGraphicCards(db_handler)
        getProcessors(db_handler)
    except Exception as e:
        print(f"Error in jtechRunAll: {e}")
    finally:
        db_handler.close_connection()  # Close the database connection
