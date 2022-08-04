import os
import pandas as pd
from tqdm import tqdm
from mongodb_database import MongoDB

path = '2020/'
file_name_list = os.listdir(path=path)
db = MongoDB(host='localhost', db='PaperBox')


for file_name in file_name_list:

    file_path = path + '/' + file_name
    print(file_path)
    journal_region = file_path.split('-')[1].split('.')[0]
    area_name = journal_region
    subject_name = ''
    sci_data_frame = pd.read_csv(file_path)
    sci_data_frame.fillna('-', inplace=True)

    for index in tqdm(range(0, sci_data_frame.shape[0])):
        sci_data_series = sci_data_frame.iloc[index]
        sci_data_dict = sci_data_series.to_dict()
        sci_data_dict['AREA'] = area_name
        # print(sci_data_dict)
        # 插入操作
        rep = db.insert_one('mdb_sfm_journal_info_2020', sci_data_dict)
