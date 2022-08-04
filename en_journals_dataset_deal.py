import os
from tqdm import tqdm

or_path = '2020'
file_name_list = os.listdir(or_path)


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(or_path + '_new/')
for file_name in file_name_list:
    # print(file_name)
    dataset_path = or_path + '/' + file_name
    dataset_deal = or_path + '_new/' + file_name
    if not os.path.exists(dataset_deal):
        f = open(dataset_deal, 'w')
        f.close()

    with open(dataset_path, 'r', encoding='utf-8') as fp1:
        for line in tqdm(fp1):
            new_line = line.replace(',', '.')
            new_line = new_line.replace(';', ',')
            # print(new_line)
            fp2 = open(dataset_deal, 'a', encoding='utf=8')
            fp2.writelines(new_line)

    fp1.close()
    fp2.close()
