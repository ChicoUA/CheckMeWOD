import json
import os, os.path
import pandas as pd


class json_reader:
    def __init__(self, folder):
        self.output_folder = folder
        self.number_of_files = 0

    def get_number_of_files(self):
        path, dirs, files = next(os.walk(self.output_folder))
        self.number_of_files = len(files)

    def get_values(self, iteration, points):
        if iteration <= self.number_of_files:
            filename = self.output_folder + "frame_number_" + str(iteration) + ".json"
            trust = True
            values = 0
            with open(filename) as json_file:
                try:
                    data = json.load(json_file)
                    data = data[iteration]
                    data = data['body keypoint']
                    data = data[0]
                    data = data[points[0]]
                    if data[2] == 0:
                        trust = False
                    values = data
                except Exception:
                    trust = False


            json_file.close()
            return values, trust

        else:
            return 0, False


def main():
    reader = json_reader("output_json/")
    reader.get_number_of_files()
    lista = []
    for i in range(0, 126):
        values, trust = reader.get_values(i, (10,))
        if values == 0 or trust == False:
            continue
        lista.append(values[1])

    print(lista)
    df = pd.DataFrame()
    df['Values'] = lista
    df.to_excel('result.xlsx', index=False)


if __name__ == "__main__":
    main()
