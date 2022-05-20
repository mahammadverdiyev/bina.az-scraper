from csv import writer


class Apartment(object):
    def __init__(self, price, currency, location, room, area, floor):
        self.price = price
        self.currency = currency
        self.location = location
        self.room = room
        self.area = area
        self.floor = floor

    def get_all_in_list(self):
        return [self.price, self.currency, self.location, self.room, self.area, self.floor]


class CsvWriter(object):
    def __init__(self, file_name, rows, iterable_data):
        self.iterable_data = iterable_data
        self.file_name = file_name
        self.rows = rows

    def write(self):
        pass


class ApartmentsDataWriter(CsvWriter):
    def __init__(self, file_name, rows, all_apartment_data):
        super().__init__(file_name, rows, all_apartment_data)

    def write(self):
        with open(f"{self.file_name}.csv", "w", encoding="utf-8", newline='') as file_csv:
            data_writer = writer(file_csv)
            data_writer.writerow(self.rows)
            for each_data in self.iterable_data:
                try:
                    data_writer.writerow(each_data.get_all_in_list())
                except:
                    print("Unknown error occurred")
                    return
