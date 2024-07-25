from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError


class MongoDBHandler:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='product_database', collection_name='product_data'):
        try:
            # Establish a connection to the MongoDB server
            self.client = MongoClient(uri)
            self.db = self.client[db_name]  # Access the specified database
            self.collection = self.db[collection_name]  # Access the specified collection
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def saveToDB(self, name, category, images, titles, prices, details, links):
        try:
            bulk_operations = []  # List to store bulk write operations
            data_length = len(titles)  # Get the number of products
            current_entries = set()  # Set to keep track of current entries

            for i in range(data_length):
                # Prepare product data
                product_data = {
                    'website': name,
                    'category': category,
                    'image': images[i],
                    'title': titles[i],
                    'price': prices[i],
                    'description': details[i],
                    'link': links[i]
                }

                # Query to check for existing product
                filter_query = {'website': name, 'category': category, 'title': titles[i]}
                existing_product = self.collection.find_one(filter_query)  # Find existing product

                # Add current entry to the set
                current_entries.add((name, category, titles[i]))

                if existing_product:
                    # If the product exists, check for changes
                    changes_detected = False
                    for key, value in product_data.items():
                        if existing_product.get(key) != value:
                            changes_detected = True
                            break

                    if changes_detected:
                        # If changes are detected, prepare an update operation
                        update_query = {'$set': product_data}
                        bulk_operations.append(UpdateOne(filter_query, update_query))
                else:
                    # If the product does not exist, prepare an upsert operation
                    bulk_operations.append(UpdateOne(filter_query, {'$set': product_data}, upsert=True))

            try:
                # Perform bulk write operations
                if bulk_operations:
                    result = self.collection.bulk_write(bulk_operations)
                    print(
                        f'For {name} {category} Matched {result.matched_count}, Updated {result.modified_count}, Upserted {result.upserted_count}')
            except BulkWriteError as bwe:
                print(bwe.details)  # Print details of bulk write errors

            # Remove entries from the database that are no longer present
            all_db_entries = self.collection.find({'website': name, 'category': category})
            entries_to_delete = []
            for entry in all_db_entries:
                if (entry['website'], entry['category'], entry['title']) not in current_entries:
                    entries_to_delete.append(entry['_id'])

            if entries_to_delete:
                self.collection.delete_many({'_id': {'$in': entries_to_delete}})
                print(f'Deleted {len(entries_to_delete)} entries not present in the current scrape.')

        except Exception as e:
            print(f"Error in saveToDB: {e}")

    def close_connection(self):
        try:
            # Close the MongoDB client connection
            self.client.close()
        except Exception as e:
            print(f"Error closing MongoDB connection: {e}")
