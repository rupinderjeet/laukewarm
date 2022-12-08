import yaml


class Config:

    def __init__(self):
        with open('config/.config.yaml', "r") as file:
            self._config = yaml.safe_load(file)
        return

    def __api(self):
        return self._config['API']

    def api_base_url(self):
        return self.__api()['BASE']

    def api_books_list_endpoint(self):
        return self.__api()['ENDPOINT_BOOK_LIST']

    def __params(self):
        return self._config['PARAMS']

    def param_books_folder_path(self):
        return self.__params()['BOOKS_FOLDER']

    def param_books_per_page(self):
        return self.__params()['BOOKS_PER_PAGE']

    def param_output_directory_path(self):
        return self.__params()['OUTPUT_DIR']

    def param_temp_folder_path(self):
        return self.__params()['TEMP_FOLDER']


configuration = Config()
