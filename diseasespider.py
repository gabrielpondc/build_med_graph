import requests
from lxml import html
from denycheck import deny_check

def spider_up(num):
    dict_info={}
    cookies = {
        'clientac': '1699405066692956126',
        'visit_dt': '2023-10-8',
        '_ga': 'GA1.2.1001444342.1699405067',
        '_gid': 'GA1.2.217938350.1699405067',
        '_ga_0J18S6XWJY': 'GS1.2.1699405067.1.0.1699405067.0.0.0',
        'Hm_lvt_f954228be9b5d93a74a625d18203e150': '1699404948,1699405086',
        'Hm_lpvt_f954228be9b5d93a74a625d18203e150': '1699405086',
        'bush-20480-tech-M-web-release-01': 'NDACBOAKFAAA',
        'Hm_lvt_df6ae9f94a8364bb76ee4b2d30eff681': '1699405269',
        'xywylastUrl': 'http%253A%252F%252Fjib.xywy.com%252Fil_sii%252Fgaishu%252F10122.htm',
        'xywylastRef': 'http%253A%252F%252Fjib.xywy.com%252Fil_sii_10122.htm',
        'ajsDataSession': '1699405066692330512@30@1699405370@1',
        'tj_lastUrl': 'http%3A//jib.xywy.com/il_sii/gaishu/10122.htm',
        'tj_lastUrl_time': '1699405370865',
        'ajsDataSession_js_test': '16994052693247911141@4@1699405370@1@http%253A%252F%252Fjib.xywy.com%252Fil_sii%252Fgaishu%252F10122.htm@http%253A%252F%252Fjib.xywy.com%252Fil_sii_10122.htm',
        'tj_lastUrl_js_test': 'http%3A//jib.xywy.com/il_sii/gaishu/10122.htm',
        'tj_lastUrl_js_test_time': '1699405370951',
        'Hm_lpvt_df6ae9f94a8364bb76ee4b2d30eff681': '1699405371',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ko;q=0.6,en-GB;q=0.5',
        'Cache-Control': 'max-age=0',
        # 'Cookie': 'clientac=1699405066692956126; visit_dt=2023-10-8; _ga=GA1.2.1001444342.1699405067; _gid=GA1.2.217938350.1699405067; _ga_0J18S6XWJY=GS1.2.1699405067.1.0.1699405067.0.0.0; Hm_lvt_f954228be9b5d93a74a625d18203e150=1699404948,1699405086; Hm_lpvt_f954228be9b5d93a74a625d18203e150=1699405086; bush-20480-tech-M-web-release-01=NDACBOAKFAAA; Hm_lvt_df6ae9f94a8364bb76ee4b2d30eff681=1699405269; xywylastUrl=http%253A%252F%252Fjib.xywy.com%252Fil_sii%252Fgaishu%252F10122.htm; xywylastRef=http%253A%252F%252Fjib.xywy.com%252Fil_sii_10122.htm; ajsDataSession=1699405066692330512@30@1699405370@1; tj_lastUrl=http%3A//jib.xywy.com/il_sii/gaishu/10122.htm; tj_lastUrl_time=1699405370865; ajsDataSession_js_test=16994052693247911141@4@1699405370@1@http%253A%252F%252Fjib.xywy.com%252Fil_sii%252Fgaishu%252F10122.htm@http%253A%252F%252Fjib.xywy.com%252Fil_sii_10122.htm; tj_lastUrl_js_test=http%3A//jib.xywy.com/il_sii/gaishu/10122.htm; tj_lastUrl_js_test_time=1699405370951; Hm_lpvt_df6ae9f94a8364bb76ee4b2d30eff681=1699405371',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://jib.xywy.com/il_sii_10122.htm',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }
    dict_info['_id']={"$oid": f"5bb578da831b973a137e4{num}"}
    response = requests.get(f'http://jib.xywy.com/il_sii/gaishu/{num}.htm', cookies=cookies, headers=headers, verify=False)
    etree = html.etree
    etree_html = etree.HTML(response.text)
    dict_info['name']=''.join(etree_html.xpath('/html/body/div[5]/div/text()'))
    dict_info['desc']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[1]/p/text()'))
    dict_info['cure_department']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[3]/p[1]/span[2]/text()')).split()
    common_drug=[]
    cata=[]
    for i in range(1,10):
        cata+=etree_html.xpath(f'/html/body/div[4]/a[{i}]/text()')
    dict_info['category']=cata
    for i in range(1,20):
        common_drug+=etree_html.xpath(f'/html/body/div[6]/div[1]/div[1]/div[2]/div[3]/p[5]/span[2]/a[{i}]/text()')
    dict_info['common_drug']=common_drug
    dict_info['yibao_status']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[2]/p[1]/span[2]/text()')).replace('\n','').replace(' ','')
    dict_info['get_prob']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[2]/p[2]/span[2]/text()')).replace('\n','').replace(' ','')
    dict_info['easy_get']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[2]/p[3]/span[2]/text()')).replace('\n','').replace(' ','')
    dict_info['get_way']= ''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[2]/p[4]/span[2]/text()'))
    acompany=[]
    for i in range(1,20):
        acompany+=etree_html.xpath(f'/html/body/div[6]/div[1]/div[1]/div[2]/div[2]/p[5]/span[2]/a[{i}]/text()')
    dict_info['acompany']=acompany
    dict_info['cure_way']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[3]/p[2]/span[2]/text()')).replace('\n','').split()
    dict_info['cure_lasttime']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[3]/p[3]/span[2]/text()')).replace('\n','').replace(' ','')
    dict_info['cured_prob']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[3]/p[4]/span[2]/text()')).replace('\n','').replace(' ','')
    dict_info['cost_money']=''.join(etree_html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[3]/p[6]/span[2]/text()'))
    response2 = requests.get(f'http://jib.xywy.com/il_sii/symptom/{num}.htm', cookies=cookies, headers=headers, verify=False)
    etree2 = html.etree
    etree_html2 = etree2.HTML(response2.text)
    dict_info['symptom']=deny_check(''.join(etree_html2.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p/text()')).replace('\n','').replace('\t','').replace('\r','').replace('。','').split('、')).split('、')
    response3 = requests.get(f'http://jib.xywy.com/il_sii/food/{num}.htm', cookies=cookies, headers=headers, verify=False)
    etree3 = html.etree
    etree_html3 = etree3.HTML(response3.text)
    do_eat=[]
    for i in range(1,20):
        do_eat+=etree_html3.xpath(f'/html/body/div[6]/div[1]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[{i}]/p/text()')
    dict_info['do_eat']=do_eat
    do_not_eat=[]
    for i in range(1,20):
        do_not_eat+=etree_html3.xpath(f'/html/body/div[6]/div[1]/div[1]/div[2]/div/div[2]/div[3]/div[2]/div[{i}]/p/text()')
    dict_info['not_eat']=do_not_eat
    recommand_eat=[]
    for i in range(1,20):
        recommand_eat+=etree_html3.xpath(f'/html/body/div[6]/div[1]/div[1]/div[2]/div/div[2]/div[4]/div[{i}]/div[1]/p/text()')
    dict_info['recommand_eat']=recommand_eat
    response4 = requests.get(f'http://jib.xywy.com/il_sii/prevent/{num}.htm', cookies=cookies, headers=headers, verify=False)
    etree4 = html.etree
    etree_html4 = etree4.HTML(response4.text)

    dict_info['prevent'] = ''.join(etree_html4.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p/text()')) 
    response5 = requests.get(f'http://jib.xywy.com/il_sii/drug/{num}.htm', cookies=cookies, headers=headers, verify=False)
    etree5 = html.etree
    etree_html5 = etree5.HTML(response5.text)
    drug_detail=[]
    for i in range(1,100):
        drug_detail+=etree_html5.xpath(f'/html/body/div[6]/div[1]/div/div/div/div[{i}]/div[2]/p[1]/a/text()')
    dict_info['drug_detail']= [text.replace(' ','').replace('\n','') for text in drug_detail]
    dict_info['check']=[]
    dict_info['recommand_drug']=common_drug
    response6 = requests.get(f'http://jib.xywy.com/il_sii/cause/{num}.htm', cookies=cookies, headers=headers, verify=False)
    etree6 = html.etree
    etree_html6 = etree6.HTML(response6.text)
    dict_info['cause']=''.join(etree_html6.xpath(f'/html/body/div[6]/div[1]/div[1]/div[2]/p/text()'))
    return dict_info