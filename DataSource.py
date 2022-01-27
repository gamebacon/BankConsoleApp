from abc import ABC, abstractmethod


class DataSource(ABC):

    def datasource_conn(self):
        pass

    def update_by_id(self):
        pass

    def find_by_id(self):
        pass

    def remove_by_id(self):
        pass

    # Saves all customer data to file.
    def save_all(self, customers):
        pass

    # Returns all customer data.
    def get_all(self):
        pass
