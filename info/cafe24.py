import requests
import io
from lxml.html import parse, submit_form
from datetime import datetime
from scrapy import Selector
from pprint import pprint


headers = {
    'origin': 'https://eclogin.cafe24.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8,ko;q=0.6',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://eclogin.cafe24.com/Shop/',
    'authority': 'eclogin.cafe24.com',
    'x-requested-with': 'XMLHttpRequest',}


def login(sess, account):
    headers = {
        'origin': 'https://eclogin.cafe24.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8,ko;q=0.6',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://eclogin.cafe24.com/Shop/',
        'authority': 'eclogin.cafe24.com',
        'x-requested-with': 'XMLHttpRequest',}
    params = (
        ('url', 'MallUseAuth'),  )
    data = [
      ('mall_id', account.userid),
      ('userid', account.userid),  ]
    sess.post('https://eclogin.cafe24.com/Shop/',
                  headers=headers, params=params, data=data)
    data = [
        ('url', 'Run'),
        ('IS_DEVSERVER', ''),
        ('login_mode', '1'),
        ('use_second_auth', 'F'),
        ('second_auth_method', ''),
        ('caller_id', ''),
        ('userid', account.userid),
        ('mall_id', account.userid),
        ('check1', 'on'),
        ('userpasswd', account.password),
        ('auth_number', ''),
        ('onnode', ''),
        ('submenu', ''),
        ('menu', ''),
        ('mode', ''),
        ('c_name', ''),
        ('loan_type', ''),
        ('addsvc_suburl', ''),
        ('is_multi', 'F'),
        ('appID', ''),
        ]
    index_resp = sess.post('https://eclogin.cafe24.com/Shop/index.php',
                  headers=headers, data=data)

    stream = io.StringIO(index_resp.text)
    form = parse(stream).getroot().xpath('//form')[0]
    check_resp = sess.post(form.action, data=dict(form.fields))

    stream = io.StringIO(index_resp.text)
    form = parse(stream).getroot().xpath('//form')[0]
    com_resp = sess.post(form.action, data=dict(form.fields))

    stream = io.StringIO(com_resp.text)
    form = parse(stream).getroot().xpath('//form')[0]
    check2_resp = sess.post(form.action, data=dict(form.fields))

    text = check2_resp.text
    text = text[text.index('>')+1:]
    text = text[text.index("'")+1:]
    url = text[:text.index("'")]
    sess.get('https://truetech02.cafe24.com/admin/php/user_id_check.php' + url)


cafe24_search_type_from_key = {
    '': None,  # default
    'ON': None,
    'GN': None,  # Not supported for cafe24
    'BN': 'o_name',
    'BI': 'member_id',
    }

# get_storefarm_status_from_stage = {
#     'neworder': 'NEW_ORDER',
#     'deliver': 'PLACE_ORDER',
#     'deliver_release': 'PLACE_ORDER_RELEASE',
# }


# SMS info part should be editied
def get_search_condition(stage, start, end, searchKey, searchKeyword):
    msk = cafe24_search_type_from_key[searchKey]
    if not msk:
        msk = 'order_id'
        searchKeyword = ''
    if stage == 'neworder':
        data = [
          ('realclick', 'T'),
          ('tabclick', 'F'),
          ('listKeyType', 'om_no'),
          ('print_select_nos', ''),
          ('listType', ''),
          ('keyType', 'om_no'),
          ('queryString', ''),
          ('isOpenMarketCancled', ''),
          ('bPrdPrepareUse', '1'),
          ('bExpressFlag', ''),
          ('excel_private_auth', 'T'),
          ('excel_public_auth', 'T'),
          ('navi_hide', ''),
          ('searchPage', 'shipped_begin_list'),
          ('menu_no', '72'),
          ('sSearchDetailView', 'F'),
          ('sSearchDetailStretch', 'F'),
          ('searched_shop_no', '1'),
          ('sIsBusanCallCenter', ''),
          ('sOrderSearchLimit', ''),
          ('MSK[]', msk),
          ('MSV[]', searchKeyword),
          ('date_type', 'pay_date'),
          ('start_date', start),
          ('btnDate', '7'),
          ('year1', start[:4]),
          ('month1', start[5:7]),
          ('day1', start[8:10]),
          ('end_date', end),
          ('year2', end[:4]),
          ('month2', end[5:7]),
          ('day2', end[8:10]),
          ('today', datetime.now().strftime("%Y-%m-%d")),
          ('product_search_type', 'product_name'),
          ('order_product_text', ''),
          ('order_product_no', ''),
          ('find_option', 'product_no'),
          ('memberType', '1'),
          ('shipment_type', 'all'),
          ('paystandard', 'choice'),
          ('product_total_price1', ''),
          ('product_total_price2', ''),
          ('item_count', 'all'),
          ('saleMarketCheck', 'on'),
          ('inflowChannelCheck', 'on'),
          ('paymethod_total_count', '21'),
          ('discountMethodCheck', 'on'),
          ('fPGMethodCheck', 'on'),
          ('search_SaleOpenMarket[]', 'cafe24'),
          ('search_SaleOpenMarket[]', 'mobile'),
          ('search_SaleOpenMarket[]', 'mobile_d'),
          ('search_SaleOpenMarket[]', 'NCHECKOUT'),
          ('search_SaleOpenMarket[]', 'INTERPARK'),
          ('search_SaleOpenMarket[]', 'auction'),
          ('search_SaleOpenMarket[]', 'sk11st'),
          ('search_SaleOpenMarket[]', 'gmarket'),
          ('search_SaleOpenMarket[]', 'coupang'),
          ('search_SaleOpenMarket[]', 'shopn'),
          ('search_SaleOpenMarket[]', 'auction_os'),
          ('search_SaleOpenMarket[]', 'INTERPARK_OS'),
          ('search_SaleOpenMarket[]', 'naver_ks'),
          ('search_SaleOpenMarket[]', 'live_link_on'),
          ('search_SaleOpenMarket[]', 'etc'),
          ('paymentMethod[]', 'cash'),
          ('paymentMethod[]', 'card'),
          ('paymentMethod[]', 'tcash'),
          ('paymentMethod[]', 'cell'),
          ('paymentMethod[]', 'icash'),
          ('paymentMethod[]', 'esc_rcash'),
          ('paymentMethod[]', 'esc_icash'),
          ('paymentMethod[]', 'esc_vcash'),
          ('paymentMethod[]', 'kpay||card'),
          ('paymentMethod[]', 'paynow||card'),
          ('paymentMethod[]', 'paynow||tcash'),
          ('paymentMethod[]', 'payco||card'),
          ('paymentMethod[]', 'payco||esc_rcash'),
          ('paymentMethod[]', 'payco||esc_icash'),
          ('paymentMethod[]', 'payco||point'),
          ('paymentMethod[]', 'kakaopay||card'),
          ('paymentMethod[]', 'mileage'),
          ('paymentMethod[]', 'deposit'),
          ('paymentMethod[]', 'npoint'),
          ('paymentMethod[]', 'ncash'),
          ('paymentMethod[]', 'cashondelv'),
          ('discountMethod[]', 'mileage'),
          ('discountMethod[]', 'deposit'),
          ('discountMethod[]', 'coupon'),
          ('discountMethod[]', 'nmileage'),
          ('discountMethod[]', 'ncash'),
          ('fPaymentMethod[]', 'paypal'),
          ('fPaymentMethod[]', 'alipay'),
          ('fPaymentMethod[]', 'axes'),
          ('fPaymentMethod[]', 'axes_over'),
          ('fPaymentMethod[]', 'eximbay'),
          ('fPaymentMethod[]', 'tenpay'),
          ('fPaymentMethod[]', 'softbank'),
          ('fPaymentMethod[]', 'ecpay'),
          ('deferPaymentMethod[]', 'npdefer'),
          ('deferPaymentMethod[]', 'gmodefer'),
          ('deferPaymentMethod[]', 'daibiki'),
          ('deferPaymentMethod[]', 'huodaofukuan'),
          ('main_search', ''),
          ('searchTimeUsed', 'F'),
          ('mkSaleTypeChg', ''),
          ('mkSaleType', 'M'),
          ('inflowPathDetail', '0000000000000000000000000000000000'),
          ('searchSorting', 'pay_date_asc'),
          ('rows', '100'),
          ('shop_no_excel', '1'),
          ('userfile', ''),
          ('bIsMultiShop', ''),
          ('radio10', 'on'),
          ('radio11', 'on'),
          ('radio12', 'on'),
          ('radio100', 'on'),
        ]
    elif stage == 'deliver':
        data = [
          ('realclick', 'T'),
          ('tabclick', 'F'),
          ('listKeyType', 'om_no'),
          ('print_select_nos', ''),
          ('listType', ''),
          ('keyType', 'om_no'),
          ('queryString', ''),
          ('isOpenMarketCancled', ''),
          ('bPrdPrepareUse', '1'),
          ('bExpressFlag', ''),
          ('excel_private_auth', 'T'),
          ('excel_public_auth', 'T'),
          ('navi_hide', ''),
          ('searchPage', 'shipped_begin_list'),
          ('menu_no', '72'),
          ('sSearchDetailView', 'F'),
          ('sSearchDetailStretch', 'F'),
          ('searched_shop_no', '1'),
          ('sIsBusanCallCenter', ''),
          ('sOrderSearchLimit', ''),
          ('MSK[]', msk),
          ('MSV[]', searchKeyword),
          ('date_type', 'pay_date'),
          ('start_date', start),
          ('btnDate', '7'),
          ('year1', start[:4]),
          ('month1', start[5:7]),
          ('day1', start[8:10]),
          ('end_date', end),
          ('year2', end[:4]),
          ('month2', end[5:7]),
          ('day2', end[8:10]),
          ('today', datetime.now().strftime("%Y-%m-%d")),
          ('product_search_type', 'product_name'),
          ('order_product_text', ''),
          ('order_product_no', ''),
          ('find_option', 'product_no'),
          ('memberType', '1'),
          ('shipment_type', 'all'),
          ('paystandard', 'choice'),
          ('product_total_price1', ''),
          ('product_total_price2', ''),
          ('item_count', 'all'),
          ('saleMarketCheck', 'on'),
          ('inflowChannelCheck', 'on'),
          ('paymethod_total_count', '21'),
          ('discountMethodCheck', 'on'),
          ('fPGMethodCheck', 'on'),
          ('search_SaleOpenMarket[]', 'cafe24'),
          ('search_SaleOpenMarket[]', 'mobile'),
          ('search_SaleOpenMarket[]', 'mobile_d'),
          ('search_SaleOpenMarket[]', 'NCHECKOUT'),
          ('search_SaleOpenMarket[]', 'INTERPARK'),
          ('search_SaleOpenMarket[]', 'auction'),
          ('search_SaleOpenMarket[]', 'sk11st'),
          ('search_SaleOpenMarket[]', 'gmarket'),
          ('search_SaleOpenMarket[]', 'coupang'),
          ('search_SaleOpenMarket[]', 'shopn'),
          ('search_SaleOpenMarket[]', 'auction_os'),
          ('search_SaleOpenMarket[]', 'INTERPARK_OS'),
          ('search_SaleOpenMarket[]', 'naver_ks'),
          ('search_SaleOpenMarket[]', 'live_link_on'),
          ('search_SaleOpenMarket[]', 'etc'),
          ('paymentMethod[]', 'cash'),
          ('paymentMethod[]', 'card'),
          ('paymentMethod[]', 'tcash'),
          ('paymentMethod[]', 'cell'),
          ('paymentMethod[]', 'icash'),
          ('paymentMethod[]', 'esc_rcash'),
          ('paymentMethod[]', 'esc_icash'),
          ('paymentMethod[]', 'esc_vcash'),
          ('paymentMethod[]', 'kpay||card'),
          ('paymentMethod[]', 'paynow||card'),
          ('paymentMethod[]', 'paynow||tcash'),
          ('paymentMethod[]', 'payco||card'),
          ('paymentMethod[]', 'payco||esc_rcash'),
          ('paymentMethod[]', 'payco||esc_icash'),
          ('paymentMethod[]', 'payco||point'),
          ('paymentMethod[]', 'kakaopay||card'),
          ('paymentMethod[]', 'mileage'),
          ('paymentMethod[]', 'deposit'),
          ('paymentMethod[]', 'npoint'),
          ('paymentMethod[]', 'ncash'),
          ('paymentMethod[]', 'cashondelv'),
          ('discountMethod[]', 'mileage'),
          ('discountMethod[]', 'deposit'),
          ('discountMethod[]', 'coupon'),
          ('discountMethod[]', 'nmileage'),
          ('discountMethod[]', 'ncash'),
          ('fPaymentMethod[]', 'paypal'),
          ('fPaymentMethod[]', 'alipay'),
          ('fPaymentMethod[]', 'axes'),
          ('fPaymentMethod[]', 'axes_over'),
          ('fPaymentMethod[]', 'eximbay'),
          ('fPaymentMethod[]', 'tenpay'),
          ('fPaymentMethod[]', 'softbank'),
          ('fPaymentMethod[]', 'ecpay'),
          ('deferPaymentMethod[]', 'npdefer'),
          ('deferPaymentMethod[]', 'gmodefer'),
          ('deferPaymentMethod[]', 'daibiki'),
          ('deferPaymentMethod[]', 'huodaofukuan'),
          ('main_search', ''),
          ('searchTimeUsed', 'F'),
          ('mkSaleTypeChg', ''),
          ('mkSaleType', 'M'),
          ('inflowPathDetail', '0000000000000000000000000000000000'),
          ('searchSorting', 'pay_date_asc'),
          ('rows', '100'),
          ('shop_no_excel', '1'),
          ('userfile', ''),
          ('bIsMultiShop', ''),
          ('radio10', 'on'),
          ('radio11', 'on'),
          ('radio12', 'on'),
          ('radio100', 'on'),
        ]
    elif stage == 'deliverstatus':
        data = [
            ('realclick', 'T'),
            ('tabclick', 'F'),
            ('keyType', 'order_id'),
            ('queryString', ''),
            ('excel_private_auth', 'T'),
            ('navi_hide', ''),
            ('searchPage', 'shipped_end_list'),
            ('menu_no', '73'),
            ('sSearchDetailView', 'F'),
            ('sSearchDetailStretch', 'F'),
            ('searched_shop_no', '1'),
            ('sIsBusanCallCenter', ''),
            ('sOrderSearchLimit', ''),
            ('MSK[]', msk),
            ('MSV[]', searchKeyword),
            ('date_type', 'shipbegin_date'),
            ('start_date', start),
            ('btnDate', '7'),
            ('year1', start[:4]),
            ('month1', start[5:7]),
            ('day1', start[8:10]),
            ('end_date', end),
            ('year2', end[:4]),
            ('month2', end[5:7]),
            ('day2', end[8:10]),
            ('today', datetime.now().strftime("%Y-%m-%d")),
            ('product_search_type', 'product_name'),
            ('order_product_text', ''),
            ('order_product_no', ''),
            ('find_option', 'product_no'),
            ('ShipCompanyId', 'all'),
            ('memberType', '1'),
            ('shipment_type', 'all'),
            ('paystandard', 'choice'),
            ('product_total_price1', ''),
            ('product_total_price2', ''),
            ('item_count', 'all'),
            ('saleMarketCheck', 'on'),
            ('inflowChannelCheck', 'on'),
            ('paymethod_total_count', '21'),
            ('discountMethodCheck', 'on'),
            ('fPGMethodCheck', 'on'),
            ('search_SaleOpenMarket[]', 'cafe24'),
            ('search_SaleOpenMarket[]', 'mobile'),
            ('search_SaleOpenMarket[]', 'mobile_d'),
            ('search_SaleOpenMarket[]', 'NCHECKOUT'),
            ('search_SaleOpenMarket[]', 'INTERPARK'),
            ('search_SaleOpenMarket[]', 'auction'),
            ('search_SaleOpenMarket[]', 'sk11st'),
            ('search_SaleOpenMarket[]', 'gmarket'),
            ('search_SaleOpenMarket[]', 'coupang'),
            ('search_SaleOpenMarket[]', 'shopn'),
            ('search_SaleOpenMarket[]', 'auction_os'),
            ('search_SaleOpenMarket[]', 'INTERPARK_OS'),
            ('search_SaleOpenMarket[]', 'naver_ks'),
            ('search_SaleOpenMarket[]', 'live_link_on'),
            ('search_SaleOpenMarket[]', 'etc'),
            ('paymentMethod[]', 'cash'),
            ('paymentMethod[]', 'card'),
            ('paymentMethod[]', 'tcash'),
            ('paymentMethod[]', 'cell'),
            ('paymentMethod[]', 'icash'),
            ('paymentMethod[]', 'esc_rcash'),
            ('paymentMethod[]', 'esc_icash'),
            ('paymentMethod[]', 'esc_vcash'),
            ('paymentMethod[]', 'kpay||card'),
            ('paymentMethod[]', 'paynow||card'),
            ('paymentMethod[]', 'paynow||tcash'),
            ('paymentMethod[]', 'payco||card'),
            ('paymentMethod[]', 'payco||esc_rcash'),
            ('paymentMethod[]', 'payco||esc_icash'),
            ('paymentMethod[]', 'payco||point'),
            ('paymentMethod[]', 'kakaopay||card'),
            ('paymentMethod[]', 'mileage'),
            ('paymentMethod[]', 'deposit'),
            ('paymentMethod[]', 'npoint'),
            ('paymentMethod[]', 'ncash'),
            ('paymentMethod[]', 'cashondelv'),
            ('discountMethod[]', 'mileage'),
            ('discountMethod[]', 'deposit'),
            ('discountMethod[]', 'coupon'),
            ('discountMethod[]', 'nmileage'),
            ('discountMethod[]', 'ncash'),
            ('fPaymentMethod[]', 'paypal'),
            ('fPaymentMethod[]', 'alipay'),
            ('fPaymentMethod[]', 'axes'),
            ('fPaymentMethod[]', 'axes_over'),
            ('fPaymentMethod[]', 'eximbay'),
            ('fPaymentMethod[]', 'tenpay'),
            ('fPaymentMethod[]', 'softbank'),
            ('fPaymentMethod[]', 'ecpay'),
            ('deferPaymentMethod[]', 'npdefer'),
            ('deferPaymentMethod[]', 'gmodefer'),
            ('deferPaymentMethod[]', 'daibiki'),
            ('deferPaymentMethod[]', 'huodaofukuan'),
            ('main_search', ''),
            ('searchTimeUsed', 'F'),
            ('mkSaleTypeChg', ''),
            ('mkSaleType', 'M'),
            ('inflowPathDetail', '0000000000000000000000000000000000'),
            ('searchSorting', 'order_desc'),
            ('rows', '20'),
            ('bIsMultiShop', ''),
            ('radio10', 'on'),
            ('radio11', 'on'),
            ('radio12', 'on'),
            ('radio100', 'on'),
        ]
    elif stage == 'cancel':
        data = [
            ('realclick', 'T'),
            ('tabclick', 'F'),
            ('queryString', ''),
            ('tabStatus', 'all'),
            ('searchPage', 'order_cancel'),
            ('menu_no', '76'),
            ('sSearchDetailView', 'F'),
            ('sSearchDetailStretch', 'F'),
            ('searched_shop_no', '1'),
            ('sIsBusanCallCenter', ''),
            ('sOrderSearchLimit', ''),
            ('MSK[]', msk),
            ('MSV[]', searchKeyword),
            ('date_type', 'order_date'),
            ('start_date', start),
            ('btnDate', '7'),
            ('year1', start[:4]),
            ('month1', start[5:7]),
            ('day1', start[8:10]),
            ('end_date', end),
            ('year2', end[:4]),
            ('month2', end[5:7]),
            ('day2', end[8:10]),
            ('today', datetime.now().strftime("%Y-%m-%d")),
            ('product_search_type', 'product_name'),
            ('order_product_text', ''),
            ('order_product_no', ''),
            ('find_option', 'product_no'),
            ('orderStatus[]', 'all'),
            ('orderStatus[]', 'CR'),
            ('orderStatus[]', 'CD'),
            ('orderStatus[]', 'CC'),
            ('memberType', '1'),
            ('shipment_type', 'all'),
            ('paystandard', 'choice'),
            ('product_total_price1', ''),
            ('product_total_price2', ''),
            ('item_count', 'all'),
            ('saleMarketCheck', 'on'),
            ('inflowChannelCheck', 'on'),
            ('paymethod_total_count', '21'),
            ('discountMethodCheck', 'on'),
            ('fPGMethodCheck', 'on'),
            ('search_SaleOpenMarket[]', 'cafe24'),
            ('search_SaleOpenMarket[]', 'mobile'),
            ('search_SaleOpenMarket[]', 'mobile_d'),
            ('search_SaleOpenMarket[]', 'NCHECKOUT'),
            ('search_SaleOpenMarket[]', 'INTERPARK'),
            ('search_SaleOpenMarket[]', 'auction'),
            ('search_SaleOpenMarket[]', 'sk11st'),
            ('search_SaleOpenMarket[]', 'gmarket'),
            ('search_SaleOpenMarket[]', 'coupang'),
            ('search_SaleOpenMarket[]', 'shopn'),
            ('search_SaleOpenMarket[]', 'auction_os'),
            ('search_SaleOpenMarket[]', 'INTERPARK_OS'),
            ('search_SaleOpenMarket[]', 'naver_ks'),
            ('search_SaleOpenMarket[]', 'live_link_on'),
            ('search_SaleOpenMarket[]', 'etc'),
            ('paymentMethod[]', 'cash'),
            ('paymentMethod[]', 'card'),
            ('paymentMethod[]', 'tcash'),
            ('paymentMethod[]', 'cell'),
            ('paymentMethod[]', 'icash'),
            ('paymentMethod[]', 'esc_rcash'),
            ('paymentMethod[]', 'esc_icash'),
            ('paymentMethod[]', 'esc_vcash'),
            ('paymentMethod[]', 'kpay||card'),
            ('paymentMethod[]', 'paynow||card'),
            ('paymentMethod[]', 'paynow||tcash'),
            ('paymentMethod[]', 'payco||card'),
            ('paymentMethod[]', 'payco||esc_rcash'),
            ('paymentMethod[]', 'payco||esc_icash'),
            ('paymentMethod[]', 'payco||point'),
            ('paymentMethod[]', 'kakaopay||card'),
            ('paymentMethod[]', 'mileage'),
            ('paymentMethod[]', 'deposit'),
            ('paymentMethod[]', 'npoint'),
            ('paymentMethod[]', 'ncash'),
            ('paymentMethod[]', 'cashondelv'),
            ('discountMethod[]', 'mileage'),
            ('discountMethod[]', 'deposit'),
            ('discountMethod[]', 'coupon'),
            ('discountMethod[]', 'nmileage'),
            ('discountMethod[]', 'ncash'),
            ('fPaymentMethod[]', 'paypal'),
            ('fPaymentMethod[]', 'alipay'),
            ('fPaymentMethod[]', 'axes'),
            ('fPaymentMethod[]', 'axes_over'),
            ('fPaymentMethod[]', 'eximbay'),
            ('fPaymentMethod[]', 'tenpay'),
            ('fPaymentMethod[]', 'softbank'),
            ('fPaymentMethod[]', 'ecpay'),
            ('deferPaymentMethod[]', 'npdefer'),
            ('deferPaymentMethod[]', 'gmodefer'),
            ('deferPaymentMethod[]', 'daibiki'),
            ('deferPaymentMethod[]', 'huodaofukuan'),
            ('main_search', ''),
            ('searchTimeUsed', 'F'),
            ('mkSaleTypeChg', ''),
            ('mkSaleType', 'M'),
            ('inflowPathDetail', '0000000000000000000000000000000000'),
            ('searchSorting', 'order_desc'),
            ('rows', '20'),
            ('bIsMultiShop', ''),
            ('radio10', 'on'),
            ('radio11', 'on'),
            ('radio12', 'on'),
            ('radio100', 'on'),
        ]
    elif stage == 'exchange':
        data = [
            ('realclick', 'T'),
            ('tabclick', 'F'),
            ('queryString', ''),
            ('tabStatus', 'all'),
            ('cs_type', 'exchange'),
            ('searchPage', 'order_change'),
            ('menu_no', '77'),
            ('sSearchDetailView', 'F'),
            ('sSearchDetailStretch', 'F'),
            ('searched_shop_no', '1'),
            ('sIsBusanCallCenter', ''),
            ('sOrderSearchLimit', ''),
            ('MSK[]', msk),
            ('MSV[]', searchKeyword),
            ('date_type', 'order_date'),
            ('start_date', start),
            ('btnDate', '7'),
            ('year1', start[:4]),
            ('month1', start[5:7]),
            ('day1', start[8:10]),
            ('end_date', end),
            ('year2', end[:4]),
            ('month2', end[5:7]),
            ('day2', end[8:10]),
            ('today', datetime.now().strftime("%Y-%m-%d")),
            ('product_search_type', 'product_name'),
            ('order_product_text', ''),
            ('order_product_no', ''),
            ('find_option', 'product_no'),
            ('orderStatus[]', 'all'),
            ('orderStatus[]', 'ER'),
            ('orderStatus[]', 'ED'),
            ('orderStatus[]', 'EC'),
            ('orderStatus[]', 'ES'),
            ('orderStatus[]', 'EW'),
            ('ShipCompanyId', 'all'),
            ('PostExpressReturn', 'all'),
            ('memberType', '1'),
            ('shipment_type', 'all'),
            ('paystandard', 'choice'),
            ('product_total_price1', ''),
            ('product_total_price2', ''),
            ('item_count', 'all'),
            ('saleMarketCheck', 'on'),
            ('inflowChannelCheck', 'on'),
            ('paymethod_total_count', '21'),
            ('discountMethodCheck', 'on'),
            ('fPGMethodCheck', 'on'),
            ('search_SaleOpenMarket[]', 'cafe24'),
            ('search_SaleOpenMarket[]', 'mobile'),
            ('search_SaleOpenMarket[]', 'mobile_d'),
            ('search_SaleOpenMarket[]', 'NCHECKOUT'),
            ('search_SaleOpenMarket[]', 'INTERPARK'),
            ('search_SaleOpenMarket[]', 'auction'),
            ('search_SaleOpenMarket[]', 'sk11st'),
            ('search_SaleOpenMarket[]', 'gmarket'),
            ('search_SaleOpenMarket[]', 'coupang'),
            ('search_SaleOpenMarket[]', 'shopn'),
            ('search_SaleOpenMarket[]', 'auction_os'),
            ('search_SaleOpenMarket[]', 'INTERPARK_OS'),
            ('search_SaleOpenMarket[]', 'naver_ks'),
            ('search_SaleOpenMarket[]', 'live_link_on'),
            ('search_SaleOpenMarket[]', 'etc'),
            ('paymentMethod[]', 'cash'),
            ('paymentMethod[]', 'card'),
            ('paymentMethod[]', 'tcash'),
            ('paymentMethod[]', 'cell'),
            ('paymentMethod[]', 'icash'),
            ('paymentMethod[]', 'esc_rcash'),
            ('paymentMethod[]', 'esc_icash'),
            ('paymentMethod[]', 'esc_vcash'),
            ('paymentMethod[]', 'kpay||card'),
            ('paymentMethod[]', 'paynow||card'),
            ('paymentMethod[]', 'paynow||tcash'),
            ('paymentMethod[]', 'payco||card'),
            ('paymentMethod[]', 'payco||esc_rcash'),
            ('paymentMethod[]', 'payco||esc_icash'),
            ('paymentMethod[]', 'payco||point'),
            ('paymentMethod[]', 'kakaopay||card'),
            ('paymentMethod[]', 'mileage'),
            ('paymentMethod[]', 'deposit'),
            ('paymentMethod[]', 'npoint'),
            ('paymentMethod[]', 'ncash'),
            ('paymentMethod[]', 'cashondelv'),
            ('discountMethod[]', 'mileage'),
            ('discountMethod[]', 'deposit'),
            ('discountMethod[]', 'coupon'),
            ('discountMethod[]', 'nmileage'),
            ('discountMethod[]', 'ncash'),
            ('fPaymentMethod[]', 'paypal'),
            ('fPaymentMethod[]', 'alipay'),
            ('fPaymentMethod[]', 'axes'),
            ('fPaymentMethod[]', 'axes_over'),
            ('fPaymentMethod[]', 'eximbay'),
            ('fPaymentMethod[]', 'tenpay'),
            ('fPaymentMethod[]', 'softbank'),
            ('fPaymentMethod[]', 'ecpay'),
            ('deferPaymentMethod[]', 'npdefer'),
            ('deferPaymentMethod[]', 'gmodefer'),
            ('deferPaymentMethod[]', 'daibiki'),
            ('deferPaymentMethod[]', 'huodaofukuan'),
            ('main_search', ''),
            ('searchTimeUsed', 'F'),
            ('mkSaleTypeChg', ''),
            ('mkSaleType', 'M'),
            ('inflowPathDetail', '0000000000000000000000000000000000'),
            ('searchSorting', 'order_desc'),
            ('rows', '20'),
            ('bIsMultiShop', ''),
            ('radio10', 'on'),
            ('radio11', 'on'),
            ('radio12', 'on'),
            ('radio100', 'on'),
        ]
    elif stage == 'refund_return':
        data = [
            ('realclick', 'T'),
            ('tabclick', 'F'),
            ('queryString', ''),
            ('tabStatus', 'all'),
            ('cs_type', 'return'),
            ('menu_no', '78'),
            ('menu_no', '78'),
            ('searchPage', 'order_returns'),
            ('sSearchDetailView', 'F'),
            ('sSearchDetailStretch', 'F'),
            ('searched_shop_no', '1'),
            ('sIsBusanCallCenter', ''),
            ('sOrderSearchLimit', ''),
            ('MSK[]', msk),
            ('MSV[]', searchKeyword),
            ('date_type', 'order_date'),
            ('start_date', start),
            ('btnDate', '7'),
            ('year1', start[:4]),
            ('month1', start[5:7]),
            ('day1', start[8:10]),
            ('end_date', end),
            ('year2', end[:4]),
            ('month2', end[5:7]),
            ('day2', end[8:10]),
            ('today', datetime.now().strftime("%Y-%m-%d")),
            ('product_search_type', 'product_name'),
            ('order_product_text', ''),
            ('order_product_no', ''),
            ('find_option', 'product_no'),
            ('orderStatus[]', 'all'),
            ('orderStatus[]', 'RR'),
            ('orderStatus[]', 'RD'),
            ('orderStatus[]', 'RB'),
            ('orderStatus[]', 'RS'),
            ('orderStatus[]', 'RC'),
            ('orderStatus[]', 'RW'),
            ('ShipCompanyId', 'all'),
            ('PostExpressReturn', 'all'),
            ('memberType', '1'),
            ('shipment_type', 'all'),
            ('paystandard', 'choice'),
            ('product_total_price1', ''),
            ('product_total_price2', ''),
            ('item_count', 'all'),
            ('saleMarketCheck', 'on'),
            ('inflowChannelCheck', 'on'),
            ('paymethod_total_count', '21'),
            ('discountMethodCheck', 'on'),
            ('fPGMethodCheck', 'on'),
            ('search_SaleOpenMarket[]', 'cafe24'),
            ('search_SaleOpenMarket[]', 'mobile'),
            ('search_SaleOpenMarket[]', 'mobile_d'),
            ('search_SaleOpenMarket[]', 'NCHECKOUT'),
            ('search_SaleOpenMarket[]', 'INTERPARK'),
            ('search_SaleOpenMarket[]', 'auction'),
            ('search_SaleOpenMarket[]', 'sk11st'),
            ('search_SaleOpenMarket[]', 'gmarket'),
            ('search_SaleOpenMarket[]', 'coupang'),
            ('search_SaleOpenMarket[]', 'shopn'),
            ('search_SaleOpenMarket[]', 'auction_os'),
            ('search_SaleOpenMarket[]', 'INTERPARK_OS'),
            ('search_SaleOpenMarket[]', 'naver_ks'),
            ('search_SaleOpenMarket[]', 'live_link_on'),
            ('search_SaleOpenMarket[]', 'etc'),
            ('paymentMethod[]', 'cash'),
            ('paymentMethod[]', 'card'),
            ('paymentMethod[]', 'tcash'),
            ('paymentMethod[]', 'cell'),
            ('paymentMethod[]', 'icash'),
            ('paymentMethod[]', 'esc_rcash'),
            ('paymentMethod[]', 'esc_icash'),
            ('paymentMethod[]', 'esc_vcash'),
            ('paymentMethod[]', 'kpay||card'),
            ('paymentMethod[]', 'paynow||card'),
            ('paymentMethod[]', 'paynow||tcash'),
            ('paymentMethod[]', 'payco||card'),
            ('paymentMethod[]', 'payco||esc_rcash'),
            ('paymentMethod[]', 'payco||esc_icash'),
            ('paymentMethod[]', 'payco||point'),
            ('paymentMethod[]', 'kakaopay||card'),
            ('paymentMethod[]', 'mileage'),
            ('paymentMethod[]', 'deposit'),
            ('paymentMethod[]', 'npoint'),
            ('paymentMethod[]', 'ncash'),
            ('paymentMethod[]', 'cashondelv'),
            ('discountMethod[]', 'mileage'),
            ('discountMethod[]', 'deposit'),
            ('discountMethod[]', 'coupon'),
            ('discountMethod[]', 'nmileage'),
            ('discountMethod[]', 'ncash'),
            ('fPaymentMethod[]', 'paypal'),
            ('fPaymentMethod[]', 'alipay'),
            ('fPaymentMethod[]', 'axes'),
            ('fPaymentMethod[]', 'axes_over'),
            ('fPaymentMethod[]', 'eximbay'),
            ('fPaymentMethod[]', 'tenpay'),
            ('fPaymentMethod[]', 'softbank'),
            ('fPaymentMethod[]', 'ecpay'),
            ('deferPaymentMethod[]', 'npdefer'),
            ('deferPaymentMethod[]', 'gmodefer'),
            ('deferPaymentMethod[]', 'daibiki'),
            ('deferPaymentMethod[]', 'huodaofukuan'),
            ('main_search', ''),
            ('searchTimeUsed', 'F'),
            ('mkSaleTypeChg', ''),
            ('mkSaleType', 'M'),
            ('inflowPathDetail', '0000000000000000000000000000000000'),
            ('searchSorting', 'order_desc'),
            ('rows', '20'),
            ('bIsMultiShop', ''),
            ('radio10', 'on'),
            ('radio11', 'on'),
            ('radio12', 'on'),
            ('radio100', 'on'),
        ]
    elif stage == 'refund_refund':
        data = [
            ('realclick', 'T'),
            ('tabclick', 'F'),
            ('queryString', ''),
            ('tabStatus', 'all'),
            ('listName', 'orderCashRefundselectedAll'),
            ('searchPage', 'order_cash_refund_f'),
            ('menu_no', '79'),
            ('sSearchDetailView', 'F'),
            ('sSearchDetailStretch', 'F'),
            ('searched_shop_no', '1'),
            ('sIsBusanCallCenter', ''),
            ('sOrderSearchLimit', ''),
            ('MSK[]', msk),
            ('MSV[]', searchKeyword),
            ('date_type', 'all_return_date'),
            ('start_date', start),
            ('btnDate', '7'),
            ('year1', start[:4]),
            ('month1', start[5:7]),
            ('day1', start[8:10]),
            ('end_date', end),
            ('year2', end[:4]),
            ('month2', end[5:7]),
            ('day2', end[8:10]),
            ('today', datetime.now().strftime("%Y-%m-%d")),
            ('orderStatus[]', 'all'),
            ('orderStatus[]', 'F'),
            ('orderStatus[]', 'T'),
            ('orderStatus[]', 'M'),
            ('RefundType', 'all'),
            ('bank_info', '0'),
            ('RefundSubType', 'all'),
            ('memberType', '1'),
            ('shipment_type', 'all'),
            ('saleMarketCheck', 'on'),
            ('inflowChannelCheck', 'on'),
            ('paymethod_total_count', '21'),
            ('discountMethodCheck', 'on'),
            ('fPGMethodCheck', 'on'),
            ('search_SaleOpenMarket[]', 'cafe24'),
            ('search_SaleOpenMarket[]', 'mobile'),
            ('search_SaleOpenMarket[]', 'mobile_d'),
            ('search_SaleOpenMarket[]', 'NCHECKOUT'),
            ('search_SaleOpenMarket[]', 'INTERPARK'),
            ('search_SaleOpenMarket[]', 'auction'),
            ('search_SaleOpenMarket[]', 'sk11st'),
            ('search_SaleOpenMarket[]', 'gmarket'),
            ('search_SaleOpenMarket[]', 'coupang'),
            ('search_SaleOpenMarket[]', 'shopn'),
            ('search_SaleOpenMarket[]', 'auction_os'),
            ('search_SaleOpenMarket[]', 'INTERPARK_OS'),
            ('search_SaleOpenMarket[]', 'naver_ks'),
            ('search_SaleOpenMarket[]', 'live_link_on'),
            ('search_SaleOpenMarket[]', 'etc'),
            ('paymentMethod[]', 'cash'),
            ('paymentMethod[]', 'card'),
            ('paymentMethod[]', 'tcash'),
            ('paymentMethod[]', 'cell'),
            ('paymentMethod[]', 'icash'),
            ('paymentMethod[]', 'esc_rcash'),
            ('paymentMethod[]', 'esc_icash'),
            ('paymentMethod[]', 'esc_vcash'),
            ('paymentMethod[]', 'kpay||card'),
            ('paymentMethod[]', 'paynow||card'),
            ('paymentMethod[]', 'paynow||tcash'),
            ('paymentMethod[]', 'payco||card'),
            ('paymentMethod[]', 'payco||esc_rcash'),
            ('paymentMethod[]', 'payco||esc_icash'),
            ('paymentMethod[]', 'payco||point'),
            ('paymentMethod[]', 'kakaopay||card'),
            ('paymentMethod[]', 'mileage'),
            ('paymentMethod[]', 'deposit'),
            ('paymentMethod[]', 'npoint'),
            ('paymentMethod[]', 'ncash'),
            ('paymentMethod[]', 'cashondelv'),
            ('discountMethod[]', 'mileage'),
            ('discountMethod[]', 'deposit'),
            ('discountMethod[]', 'coupon'),
            ('discountMethod[]', 'nmileage'),
            ('discountMethod[]', 'ncash'),
            ('fPaymentMethod[]', 'paypal'),
            ('fPaymentMethod[]', 'alipay'),
            ('fPaymentMethod[]', 'axes'),
            ('fPaymentMethod[]', 'axes_over'),
            ('fPaymentMethod[]', 'eximbay'),
            ('fPaymentMethod[]', 'tenpay'),
            ('fPaymentMethod[]', 'softbank'),
            ('fPaymentMethod[]', 'ecpay'),
            ('deferPaymentMethod[]', 'npdefer'),
            ('deferPaymentMethod[]', 'gmodefer'),
            ('deferPaymentMethod[]', 'daibiki'),
            ('deferPaymentMethod[]', 'huodaofukuan'),
            ('main_search', ''),
            ('searchTimeUsed', 'F'),
            ('mkSaleTypeChg', ''),
            ('mkSaleType', 'M'),
            ('inflowPathDetail', '0000000000000000000000000000000000'),
            ('searchSorting', 'request_date_asc'),
            ('rows', '20'),
            ('bIsMultiShop', ''),
            ('radio10', 'on'),
            ('radio11', 'on'),
            ('radio12', 'on'),
            ('radio100', 'on'),
        ]
    return data

search_urls = {
    'neworder': 'https://truetech02.cafe24.com/admin/php/shop1/s_new/product_prepare_list_ord_num.php',
    'deliver': 'https://truetech02.cafe24.com/admin/php/shop1/s_new/shipped_begin_list.php',
    'deliverstatus': 'https://truetech02.cafe24.com/admin/php/shop1/s/shipped_end_list.php',
    'cancel': 'https://truetech02.cafe24.com/admin/php/shop1/s/order_cancel.php',
    'exchange': 'https://truetech02.cafe24.com/admin/php/shop1/s/order_change.php',
    'refund_return': 'https://truetech02.cafe24.com/admin/php/shop1/s_new/order_returns.php',
    'refund_refund': 'https://truetech02.cafe24.com/admin/php/shop1/s_new/order_cash_refund_f.php',
}

def _search(account, stage, start, end,
            searchKey, searchKeyword):
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")

    with requests.Session() as sess:
        login(sess, account)
        data = get_search_condition(
            stage, start, end, searchKey, searchKeyword)
        data.append(
            ('mallId', account.userid) )
        resp = sess.post(search_urls[stage],
             headers=headers, data=data)

    return extract_entries(resp, stage)

def search(account, stage, start, end,
           searchKey='', searchKeyword=''):
   if stage == 'refund':
       return _search(account, 'refund_return',
                      start, end, searchKey, searchKeyword) +\
              _search(account, 'refund_refund',
                        start, end, searchKey, searchKeyword)
   return _search(account, stage, start, end, searchKey, searchKeyword)


def strip_selector(sel):
    ts = sel.xpath('.//text()').extract()
    ret = ''
    for t in ts:
        ret += t.strip()
        ret += " "
    return ret.strip()

def extract_entries(response, stage):
    sel = Selector(text=response.text)
    entries = []
    if stage == 'neworder':
        trs = sel.xpath("//table[@id='shipedReadyList']//tr")
        for tr in trs[1:]:
            tds = tr.xpath(".//td")
            entry = {}
            order_date = strip_selector(tds[1])
            entry['OrderDate'] = order_date[:order_date.find('(')].strip()
            entry['OrderNo'] = strip_selector(tds[2])
            entry['BuyerID'] = tds[3].xpath('span/text()')[0].extract()
            # 묶음선택 4
            # some checkbox 5
            entry['Supplier'] = strip_selector(tds[6])
            entry['Product'] = strip_selector(tds[7])[19:]
            entry['Quantity'] = strip_selector(tds[8])
            entry['Price'] = strip_selector(tds[10])
            entry['ActualPrice'] = strip_selector(tds[13])
            entry['Method'] = tds[14].xpath('.//img/@title')[0].extract()
            entries.append(entry)
    elif stage == 'deliver':
        tables = sel.xpath('//*[@id="shipedReadyList"]/table')
        # return tables, tables
        if tables[1].xpath('./tbody/@class')[0].extract() == 'empty':
            return []
        for tbl in tables[1:]:
            tds = tbl.xpath(".//tr[1]//td")
            entry = {}
            order_date = strip_selector(tds[1])
            entry['OrderDate'] = order_date[:order_date.find('(')].strip()
            entry['OrderNo'] = strip_selector(tds[2])
            entry['BuyerID'] = tds[3].xpath('span/text()')[0].extract()
            # 묶음선택 4
            # some checkbox 5
            # 운송장정보 6
            entry['DeliveryFee'] = tds[7].xpath(".//input/@value")[0].extract()  # 처음에 무조건 0으로 되어있는 듯 보임
            entry['Supplier'] = strip_selector(tds[8])
            entry['Product'] = strip_selector(tds[9])[19:]
            entry['Quantity'] = strip_selector(tds[10])
            entry['Price'] = strip_selector(tds[12])
            entry['ActualPrice'] = strip_selector(tds[15])
            entry['Method'] = tds[16].xpath('.//img/@title')[0].extract()
            entry['Addr'] = strip_selector(
                tbl.xpath(".//tr[2]//td"))
            entries.append(entry)
    elif stage == 'deliverstatus':
        trs = sel.xpath("//table[@id='searchResultList']/tbody[contains(@class,'center')]/tr")
        for tr in trs:
            tds = tr.xpath("./td")
            entry = {}
            entry['OrderDate'] = tds[1].xpath("./text()")[0].extract().strip()
            entry['OrderNo'] = tds[1].xpath("./a/text()")[0].extract()
            entry['BuyerID'] = tds[2].xpath('span/text()')[0].extract()
            inner_tds = tds[3].xpath(".//table//td")
            entry['TransDate'] = inner_tds[1].xpath('./text()')[0].extract().strip()
            entry['TransCompany'] = inner_tds[2].xpath('./text()')[0].extract().strip()
            entry['InvoiceNo'] = inner_tds[2].xpath('./text()')[1].extract().strip()
            entry['Supplier'] = strip_selector(inner_tds[3])
            entry['Product'] = strip_selector(inner_tds[4].xpath(".//a[2]"))
            entry['Quantity'] = strip_selector(inner_tds[5])
            entry['Addr'] =  inner_tds[6].xpath('.//li[3]/text()')[0].extract()
            # 전화번호 inner_tds[6].xpath('.//li[2]/text()')[0].extract()
            entries.append(entry)
    elif stage == 'cancel':
        trs = sel.xpath("//table[@id='searchResultList']/tbody[contains(@class,'center')]/tr")
        for tr in trs:
            tds = tr.xpath("./td")
            entry = {}
            entry['ClaimDate'] = strip_selector(tds[2])
            entry['OrderDate'] = entry['ClaimDate']  # 카페24 취소메뉴에선 주문일이 나오지 않기 때문에 일단 취소일로 대체
            entry['OrderNo'] = strip_selector(tds[3])
            entry['BuyerID'] = tds[4].xpath('span/text()')[0].extract()
            entry['Product'] = strip_selector(tds[5].xpath('.//a[2]'))
            entry['Quantity'] = strip_selector(tds[6])
            entry['ActualPrice'] = strip_selector(tds[7])
            entry['Method'] = tds[8].xpath('.//img/@title')[0].extract()
            entry['Status'] = tds[9].xpath('./text()')[0].extract().strip()
            entries.append(entry)
    elif stage in ('exchange', 'refund_return'):
        trs = sel.xpath("//table[@id='searchResultList']/tbody[contains(@class,'center')]/tr")
        for tr in trs:
            tds = tr.xpath("./td")
            entry = {}
            entry['ClaimDate'] = tds[2].xpath('./text()')[0].extract().strip()
            entry['OrderDate'] = entry['ClaimDate']
            entry['OrderNo'] = strip_selector(tds[3])
            entry['BuyerID'] = tds[4].xpath('span/text()')[0].extract()
            entry['Product'] = strip_selector(tds[5].xpath('.//a[2]'))
            entry['Quantity'] = strip_selector(tds[6])
            entry['Status'] = tds[8].xpath('./text()')[0].extract().strip()
            entries.append(entry)
    elif stage == 'refund_refund':
        trs = sel.xpath("//table[@id='searchResultList']/tbody[contains(@class,'center')]/tr")
        for i in range(0, len(trs), 2):
            tds1 = trs[i].xpath("./td")
            tds2 = trs[i+1].xpath("./td")
            entry = {}
            entry['OrderDate'] = strip_selector(tds1[2])
            entry['ClaimDate'] = strip_selector(tds1[3])
            entry['OrderNo'] = tds1[4].xpath('./a//text()')[0].extract()
            entry['ClaimNo'] = tds1[4].xpath('./p//text()')[0].extract()
            entry['BuyerID'] = tds1[5].xpath('span/text()')[0].extract()
            entry['Quantity'] = strip_selector(tds1[6])
            entry['ActualPrice'] = strip_selector(tds1[7])
            entry['RefundedAmount'] = strip_selector(tds1[8])
            entry['ReserveAndDepositRefundedAmount'] = strip_selector(tds1[9])
            entry['PointRefundedAmount'] = strip_selector(tds1[10])
            entry['Method'] = tds1[11].xpath('.//img/@title')[0].extract()
            entry['RefundMethod'] = tds1[12].xpath('.//img/@title')[0].extract()
            entry['Status'] = tds1[13].xpath('./text()')[0].extract().strip()
            entry['RefundBankAccount'] = tds2[0].xpath('./text()')[0].extract().strip()
            entry['Product'] = 'X'
            entries.append(entry)
    return entries


# from datetime import datetime, timedelta
# a= lambda:None
# a.userid = "truetech02"
# a.password="true3251"
# start = datetime.now() - timedelta(days=10)
# end = datetime.now()
# stage = 'refund_refund'
# tds1, tds2 = search(a, stage, start, end)
