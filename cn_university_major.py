import json
import os
from mongodb_database import MongoDB

json_dir = '/'
file_list = os.listdir(json_dir)
undergraduate = []
professional = []
both = []
others = []
db = MongoDB(host='localhost', db='test')
subjects = []
subject_dict = {}
for file_name in file_list:
    file_names = json_dir + file_name
    # print(file_name + '-------------------------------------------------------------')
    with open(file_names, 'r', encoding='UTF-8') as f:
        load_dict = json.load(f)

        # 二级学院列表只针对211院校及个别学校，其他学校暂无数据
        if load_dict['special_detail'] is not '':
            for college in load_dict['special_detail']['3']:
                # print(college)
                print(file_name + '-------------------------------------------------------------')
                rep = db.insert_one('mdb_sfm_university_211_college', college)

        # 掌上高考的前15个展示专业表
        if load_dict['special'] is not '':
            if load_dict['1'] is not '' and load_dict['2'] is '':
                for subject in load_dict['1']:
                    # print(subject)
                    rep = db.insert_one('mdb_sfm_university_first15_major', subject)
            elif load_dict['1'] is '' and load_dict['2'] is not'':
                for subject in load_dict['2']:
                    # print(subject)
                    rep = db.insert_one('mdb_sfm_university_first15_major', subject)
            elif load_dict['1'] is not '' and load_dict['2'] is not'':
                for subject in load_dict['2']:
                    # print(subject)
                    rep = db.insert_one('mdb_sfm_university_first15_major', subject)
                for subject in load_dict['1']:
                    # print(subject)
                    rep = db.insert_one('mdb_sfm_university_first15_major', subject)
            else:
                print(file_name + 'none of data')

        # 建立学科和专业的联系
        if load_dict['special'] is not '':
            for subject in load_dict['special']:
                subject_dict['name'] = subject['name']
                subject_dict['code'] = subject['code']
                subject_dict['level3_weight'] = subject['level3_weight']
                for major in subject['special']:
                    major['subject_name'] = subject_dict['name']
                    major['subject_code'] = subject_dict['code']
                    major['subject_level3_weight'] = subject_dict['level3_weight']
                    print(major['subject_name'], major['special_name'])
                    rep = db.insert_one('mdb_sfm_university_subject_major', major)
        else:
            pass

        # 查看数据分布
        if load_dict['special'] is not '':
            for key in load_dict:
                if load_dict['1'] is not '' and load_dict['2'] is '':
                    # print(1, load_dict['1'][0]['type_name'])
                    undergraduate.append(file_names)
                elif load_dict['1'] is '' and load_dict['2'] is not '':
                    # print(2, load_dict['2'][0]['type_name'])
                    professional.append(file_names)
                elif load_dict['1'] is not '' and load_dict['2'] is not '':
                    # print(3, load_dict['1'][0]['type_name'], load_dict['2'][0]['type_name'])
                    both.append(file_names)
                else:
                    others.append(file_names)
            else:
                pass
        print(file_name)

        # 处理本科专业和专科专业
        if load_dict['special'] is not '':
            if load_dict['1'] != '' or load_dict['2'] != '':
                for major in load_dict['1']:
                    # print(major)
                    # print(major['special_name'])
                    rep = db.insert_one('mdb_sfm_university_undergraduate_major', major)
                print(len(load_dict['special_detail']['1']))
                for major in load_dict['2']:
                    # print(major)
                    # print(major['special_name'])
                    rep = db.insert_one('mdb_sfm_university_professional_major', major)
                print(len(load_dict['special_detail']['2']))
            else:
                pass
        else:
            pass
        # 处理国家特色专业
        if load_dict['special'] is not '':
            if load_dict['nation_feature'] is not '':
                for major in load_dict['nation_feature']:
                    rep = db.insert_one('mdb_sfm_university_nation_major', major)
