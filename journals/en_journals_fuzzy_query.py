import pymysql

# db connect
en_journal_db = pymysql.connect(host='103.215.34.6',
                                port=3306,
                                user='root',
                                password='root@zbkj_cpb_slxz~',
                                db='paperboxdb',
                                charset='utf8')

# generate cursor
en_journal_cursor = en_journal_db.cursor()

title_list = []


# 用SQL-like做模糊查询
def sql_fuzzy_fetch(user_input):
    fuzzy_sql = "SELECT TITLE FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE like '%%%%%s%%%%'" % user_input
    en_journal_cursor.execute(fuzzy_sql)
    en_journal_titles_fetch = en_journal_cursor.fetchall()
    # print(en_journal_titles_fetch)
    for title in en_journal_titles_fetch:
        title_list.append(title[0])
    return list(set(title_list))


sentence_input = input('请输入期刊名，不区分大小写：')
suggest_journal_list = sql_fuzzy_fetch(sentence_input)
# suggest_journal_list = sql_fuzzy_fetch('Issues in Teachers')


print('已检索到期刊', len(suggest_journal_list), '部')
if len(suggest_journal_list) is not 0:
    print('\n')
    print('\n')
    for journal_info in suggest_journal_list:
        print('期刊名：', journal_info)
        select_area_sql = "SELECT AREA FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_area_sql, journal_info)
        journal_info_area = en_journal_cursor.fetchone()[0]
        print('研究领域：', journal_info_area)
        select_H_sql = "SELECT H_INDEX FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_H_sql, journal_info)
        journal_info_H_index = en_journal_cursor.fetchone()[0]
        print('H指数(期刊在整个时期内至少获得H次引用的文章H篇)：', journal_info_H_index)
        select_SJR_sql = "SELECT SJR FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_SJR_sql, journal_info)
        journal_info_SJR = en_journal_cursor.fetchone()[0]
        print('近三年发表在该期刊上的文献所收到的加权引用的平均数量：', journal_info_SJR)
        select_total_sql = "SELECT TOTAL_DOCS FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_total_sql, journal_info)
        journal_info_total = en_journal_cursor.fetchone()[0]
        print('当年发表量：', journal_info_total)
        select_total3_sql = "SELECT TOTAL_DOCS_THREE FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_total3_sql, journal_info)
        journal_info_total3 = en_journal_cursor.fetchone()[0]
        print('近三年发表量：', journal_info_total3)
        select_ref_sql = "SELECT TOTAL_REFS FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_ref_sql, journal_info)
        journal_info_ref = en_journal_cursor.fetchone()[0]
        print('当年参考文献量：', journal_info_ref)
        select_cite3_sql = "SELECT TOTAL_CITES_THREE FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_cite3_sql, journal_info)
        journal_info_cite3 = en_journal_cursor.fetchone()[0]
        print('近三年发表的期刊文献当年收到的引文数：', journal_info_cite3)
        select_cite_docs3_sql = "SELECT CITABLE_DOCS_THREE FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_cite_docs3_sql, journal_info)
        journal_info_cite_doc3 = en_journal_cursor.fetchone()[0]
        print('近三年期刊的可引用文章数：', journal_info_cite_doc3)
        select_country_sql = "SELECT COUNTRY FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_country_sql, journal_info)
        journal_info_country = en_journal_cursor.fetchone()[0]
        print('国家：', journal_info_country)
        select_region_sql = "SELECT REGION FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_region_sql, journal_info)
        journal_info_region = en_journal_cursor.fetchone()[0]
        print('地区：', journal_info_region)
        select_publisher_sql = "SELECT PUBLISHER FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_publisher_sql, journal_info)
        journal_info_publisher = en_journal_cursor.fetchone()[0]
        print('发行商：', journal_info_publisher)
        select_categories_sql = "SELECT CATEGORIES FROM paperboxdb.mdb_sfm_journal_info_20 WHERE TITLE=%s"
        en_journal_cursor.execute(select_categories_sql, journal_info)
        journal_info_categories = en_journal_cursor.fetchone()[0]
        journal_info_categories_li = journal_info_categories.replace(';', '\n').replace(',', '\n')
        print('二级学科分区：\n', journal_info_categories_li)
        print('——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-')
else:
    print('没有相关期刊数据')

en_journal_cursor.close()
en_journal_db.close()
