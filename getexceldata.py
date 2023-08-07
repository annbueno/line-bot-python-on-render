from datetime import datetime
import os
import pandas as pd
import re

output_dict = {}


# 定義函式，用來將店名的最後一個字刪除
def remove_last_char(store_name):
    return '寵物公園-' + store_name[:-1]


def output_excel_data(date):
    # 設定檔案資訊
    folder_path = r'C:\Users\Ann\Downloads'
    file_prefix = 'LGC19680M_'
    if date == '':
        date_format = '%Y%m%d'
    else:
        date_format = date

    # 取得今天的日期
    today = datetime.now().strftime(date_format)
    excel_name = ''

    # 找出符合條件的檔案
    matching_files = []
    for filename in os.listdir(folder_path):
        if filename.startswith(file_prefix + today):
            excel_name = filename

    if len(excel_name) != 0:
        # 讀取訂單excel
        file_path = os.path.join(folder_path, excel_name)
        df = pd.read_excel(file_path)

        # 讀取店名excel表格
        store_name_excel_path = '寵物公園店名表.xlsx'
        df_store_name = pd.read_excel(store_name_excel_path)

        # 依照業務分組，將店名儲存在集合中
        store_sets_by_area = df_store_name.groupby('業務')['店名'].apply(lambda x: set(x.apply(remove_last_char)))

        # 將集合儲存在字典中
        store_dict_by_sales = {}
        for sales, store_set in store_sets_by_area.items():
            store_dict_by_sales[sales] = store_set

        # 建立字典
        # 格式key為店名，值為陣列，陣列中儲存字典，key1為單子總業績、key2為拜恩諾總業績、key3為路易總業績、key4為push總業績
        achievements = {}
        # 格式key為店名，值為陣列，陣列中儲存字典，key1為品名、key2為採購數量
        items = {}

        # 定義缺貨品項集合
        out_of_stock_items = {'毛管家 護駕噴噴180ml'}

        # 遍歷每一行
        for index, row in df.iterrows():
            # 取得交貨門市的名稱，並將其命名為變數"shop"
            shop = str(row['交貨門市'])
            # 如果交貨門市為"交貨門市"，則跳過此行
            if shop == '交貨門市':
                continue
            # 如果交貨門市為"毛孩Boxful"，則將其改為"毛孩Boxful倉"
            if '毛孩Boxful' in shop:
                shop = '毛孩Boxful倉'
            # 將交貨門市命名為"寵物公園-"並去除數字後綴，並將其命名為變數"shop"
            shop = '寵物公園-' + re.sub(r'\d', '', shop)
            # 取得品名，並將其命名為變數"item"
            item = str(row['品名'])
            # 取得採購金額，並將其命名為變數"amount"
            amount = row['採購金額']
            ori_amount = amount
            # 取得採購數量，並將其命名為變數"quantity"
            quantity = row['採購數量']
            # 取得單身備註
            remark = row['單身備註']
            # 取得單頭備註
            order_remark = row['單頭備註']
            # 如果該品名已經在"out_of_stock_items"中，則標註缺貨
            if item in out_of_stock_items:
                item = '(缺貨)' + item
                amount = 0
            # 如果此店家還未加入"achievement"字典中
            if shop not in achievements:
                # 將該品名添加至"items"字典中
                items[shop] = [{'品名': item, '採購數量': quantity, '備註': remark}]
                # 初始化業績的值
                if item.startswith('蝨止王') or item.startswith('毛管家'):
                    achievements[shop] = {'採購金額': ori_amount, '拜恩諾業績': amount, '貓砂業績': 0, '酵素業績': 0,
                                          'Push!業績': 0, '單頭備註': order_remark}
                elif item.startswith('路易貓砂'):
                    achievements[shop] = {'採購金額': ori_amount, '拜恩諾業績': 0, '貓砂業績': amount, '酵素業績': 0,
                                          'Push!業績': 0, '單頭備註': order_remark}
                elif item.startswith('路易MIT鳳梨酵素'):
                    achievements[shop] = {'採購金額': ori_amount, '拜恩諾業績': 0, '貓砂業績': 0, '酵素業績': amount,
                                          'Push!業績': 0, '單頭備註': order_remark}
                elif item.startswith('Push!'):
                    achievements[shop] = {'採購金額': ori_amount, '拜恩諾業績': 0, '貓砂業績': 0, '酵素業績': 0,
                                          'Push!業績': amount, '單頭備註': order_remark}
                else:
                    achievements[shop] = {'採購金額': ori_amount, '拜恩諾業績': 0, '貓砂業績': 0, '酵素業績': 0,
                                          'Push!業績': 0, '單頭備註': order_remark}
                # 如果此店家已經加入"achievement"字典中
            else:
                items[shop].append({'品名': item, '採購數量': quantity, '備註': remark})
                # 計算業績的值
                total = achievements[shop]['採購金額'] + ori_amount
                bueno_total = achievements[shop]['拜恩諾業績']
                litter_total = achievements[shop]['貓砂業績']
                enzyme_total = achievements[shop]['酵素業績']
                push_total = achievements[shop]['Push!業績']
                if item.startswith('蝨止王') or item.startswith('毛管家'):
                    bueno_total += amount
                elif item.startswith('路易貓砂'):
                    litter_total += amount
                elif item.startswith('路易MIT鳳梨酵素'):
                    enzyme_total += amount
                elif item.startswith('Push!'):
                    push_total += amount
                    achievements[shop] = {'採購金額': total, '拜恩諾業績': bueno_total, '貓砂業績': litter_total,
                                          '酵素業績': enzyme_total, 'Push!業績': push_total, '單頭備註': order_remark}

            # 輸出每個店名及其對應的品名和銷售數字
            for sales, stores in store_dict_by_sales.items():
                achievement_str = ''
                for shop, achievement in achievements.items():
                    if shop in stores:
                        items_str = ''
                        has_bueno = False
                        has_litter = False
                        has_enzyme = False
                        has_push = False
                        short_str = ''
                        for item in items[shop]:
                            name = item['品名']
                            quantity = item['採購數量']
                            remark = item['備註']
                            remark = str(remark).replace('nan', '')
                            item_str = '品名: %s 數量: %s 備註: %s\n' % (name, quantity, remark)
                            items_str += item_str
                            if name.startswith('蝨止王') or name.startswith('毛管家'):
                                has_bueno = True
                            if name.startswith('路易貓砂'):
                                has_litter = True
                            if name.startswith('路易MIT鳳梨酵素'):
                                has_enzyme = True
                            if name.startswith('Push!'):
                                has_push = True
                        amount = achievement['採購金額']

                        other_total = achievement['貓砂業績'] + achievement['酵素業績']+achievement['Push!業績']
                        # 有拜恩諾 拜恩諾金額不足三千 而且其餘加起來不足三千
                        if has_bueno and achievement['拜恩諾業績'] < 3000 and other_total < 3000:
                            short_str = '蝨止王與毛管家金額加總不足三千 路易PUSH加總不足三千'
                        # 有拜恩諾 拜恩諾金額不足三千 但其他加起來超過三千
                        elif has_bueno and achievement['拜恩諾業績'] < 3000 <= other_total:
                            short_str = '蝨止王與毛管家金額加總不足三千 只出'
                            if has_litter or has_enzyme:
                                short_str += '路易'
                            if has_push:
                                short_str += 'PUSH'
                        # 沒拜恩諾 其他加起來沒超過三千
                        elif not has_bueno and other_total < 3000:
                            short_str = '路易和Push金額加總不足三千'

                        amount_str = '採購金額：%s 拜恩諾金額：%s 路易金額：%s Push!金額：%s\n%s\n' % (
                            str(amount), str(achievement['拜恩諾業績']),
                            str(achievement['貓砂業績'] + achievement['酵素業績']),
                            str(achievement['Push!業績']), short_str)
                        remark_str = '單頭備註：' + achievement['單頭備註']
                        shop_str = '店名：%s\n%s\n%s%s\n' % (shop, remark_str, items_str, amount_str)
                        achievement_str += shop_str
                output_dict[sales] = achievement_str
    return output_dict
