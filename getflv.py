import json
from urllib.parse import unquote
import requests
from lxml import etree


def get_flvurl(url):
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'xgplayer_user_id=604111615373; s_v_web_id=verify_labtc4sn_vEYnrRne_Fsf0_4azn_AHiC_OqbzyIRFEBmM; passport_csrf_token=fe7840cd0bb11d3f20f82bf42b72988a; passport_csrf_token_default=fe7840cd0bb11d3f20f82bf42b72988a; ttwid=1|dJCY2tznNmltqbLrE_tAxPMU0llJP5GQfIU_Ug9gQp0|1668911423|32b2a09d8df32aab46a3ff196aeb59b5fac0ea7b94be74825aab6adfcbe45287; n_mh=_CNP3el5Re2QqlM25jKDi5dX9d9YBmc6wu3LuMNztY4; xgplayer_device_id=66498947622; LOGIN_STATUS=1; passport_assist_user=CkGJbv-GIkJ5Z9Z5bwIHI7mCOITpBW6iIRFmufHaBcUClvg5Hj7XBJllOOdXC9pFfSkn1WehhotI9Q88-LeynncF8hpICjx0T6O-NXer2h4_vAZixIwalZ3oLJf9iDz0SilSNX_dRfhYijIP8NJgxf4xfG6WZp_i-ihsAo2eVqJtMFkQ0pujDRiJr9ZUIgED7hMMGA==; session_secure=1; sso_uid_tt=d7960a702928328ca3b577b908a74caa; sso_uid_tt_ss=d7960a702928328ca3b577b908a74caa; toutiao_sso_user=9291130742ddc125d0a48a11bd26d6e3; toutiao_sso_user_ss=9291130742ddc125d0a48a11bd26d6e3; passport_auth_status=3e2a53bfc01e9ce16bcad20bd26a7bca,309cbadb331aa3e3aea40023c5079f3f; passport_auth_status_ss=3e2a53bfc01e9ce16bcad20bd26a7bca,309cbadb331aa3e3aea40023c5079f3f; odin_tt=d6cb858124604c04af7fa9f2cfeb8bbe2a02fe4815dd86400f7209a5074e11ac83b09cf17a1960e8885a04a587a80450caf16368e44ef5c9e792de10ab1ad4c5; uid_tt=2058e754da5886d27f804185b49002f0; uid_tt_ss=2058e754da5886d27f804185b49002f0; sid_tt=b541f8400cf9067003d5fe7e97b2d53c; sessionid=b541f8400cf9067003d5fe7e97b2d53c; sessionid_ss=b541f8400cf9067003d5fe7e97b2d53c; ttcid=26f872aa1ad44767b1728691116c6c2140; FOLLOW_NUMBER_YELLOW_POINT_INFO="MS4wLjABAAAAJ6uGUNjjXz4dWtIFrlmyQ94_yydynsoCV0ULdMgF2zet6Q5mmnvZL1NFScX1xmbU/1672416000000/0/1672405636491/0"; strategyABtestKey="1672488146.845"; FOLLOW_LIVE_POINT_INFO="MS4wLjABAAAAJ6uGUNjjXz4dWtIFrlmyQ94_yydynsoCV0ULdMgF2zet6Q5mmnvZL1NFScX1xmbU/1672502400000/0/1672488147024/0"; home_can_add_dy_2_desktop="1"; sid_ucp_sso_v1=1.0.0-KDNiZDYxYzE0MTc2ZmVkNWM5N2FiYmUyYTMwNWJmNmMzMmQ4NDg2MjIKHwin5-DEoPWqAxDWycCdBhjvMSAMMLiWgu0FOAZA9AcaAmxmIiA5MjkxMTMwNzQyZGRjMTI1ZDBhNDhhMTFiZDI2ZDZlMw; ssid_ucp_sso_v1=1.0.0-KDNiZDYxYzE0MTc2ZmVkNWM5N2FiYmUyYTMwNWJmNmMzMmQ4NDg2MjIKHwin5-DEoPWqAxDWycCdBhjvMSAMMLiWgu0FOAZA9AcaAmxmIiA5MjkxMTMwNzQyZGRjMTI1ZDBhNDhhMTFiZDI2ZDZlMw; sid_guard=b541f8400cf9067003d5fe7e97b2d53c|1672488151|5184000|Wed,+01-Mar-2023+12:02:31+GMT; sid_ucp_v1=1.0.0-KDljYzA5NzQyYTViNjFkMjhhMjRiNDdkZTE3MzE1NDg0YTgwMzM1MmEKGQin5-DEoPWqAxDXycCdBhjvMSAMOAZA9AcaAmhsIiBiNTQxZjg0MDBjZjkwNjcwMDNkNWZlN2U5N2IyZDUzYw; ssid_ucp_v1=1.0.0-KDljYzA5NzQyYTViNjFkMjhhMjRiNDdkZTE3MzE1NDg0YTgwMzM1MmEKGQin5-DEoPWqAxDXycCdBhjvMSAMOAZA9AcaAmhsIiBiNTQxZjg0MDBjZjkwNjcwMDNkNWZlN2U5N2IyZDUzYw; csrf_session_id=8206b2d05d284b92ec6650fae2e96e9b; passport_fe_beating_status=true; __ac_nonce=063b024e1004550c81737; __ac_signature=_02B4Z6wo00f01rbrIRgAAIDCNunbWnjMG2a2yyWAAM4XoU1oD5ctQdChUqyuF6mMIDoRT4y3j8bw0nv08F1DbtoMuCzL4ALx1GBaOlbBhWChjqXlYiGsVo0biL.ZVf5qm9dLHrLjO70LeNfDe4; msToken=yxEBjoJkjjYdYx9XdPfSa_RyiDdKXrZOlH5bjQZCom1iLsVpS-2pJP4tl-64jPEWMpiRtdItOkdsd0RKs3A93NoDUm71J9jt8uv6M6eVQ4z2eXUtNaOl_g==; msToken=SRUUK7vrt7vXE3Lp9ZcVh3Xa_RVFGuLMT3rSYiMg6EnDzjNPwZRhYe2y18kvc1UQbr0bnBAtNvs8xoDSAo3zRpK8VUxarEMvsWcvaIXe-yzwzMnlZpzScNPgKAINsko=; tt_scid=13Z2oGzXHtqxhgwmrDWSeh3voyl.dw6yJRNJ2w7OKIP65rFJwraJ1EmCUYdmbEvg7c40; live_can_add_dy_2_desktop="1"',
        'pragma': 'no-cache',
        'referer': 'https://www.douyin.com/search/%E9%82%BB%E9%87%8C%E7%9A%84%E4%BA%BA%E4%BB%AC?aid=62c7102b-53c9-4555-a45a-10dadcd2c61e&publish_time=0&sort_type=0&source=normal_search&type=video',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    html_ele = etree.HTML(response.text)
    result_list = html_ele.xpath("//script[@id='RENDER_DATA']/text()")
    if len(result_list) == 0:
        return 0,0
    # print(result_list[0])
    # print(unquote(result_list[0]))
    json_obj = json.loads(unquote(result_list[0]))
    room = json_obj['app']['initialState']['roomStore']['roomInfo']
    # with open('room_info.json', 'w') as file:
    #     json.dump(room['room'],file)
    # print(room['room'])
    try:
        if room['room']['status'] != 2:
            print(f"直播已结束,状态：{room['room']['status']}")
            return False, {
                'room_id': '',
                'state': '直播已关闭'
            }

        return True, {'room_id': room['room']['id_str'],
                      'anchor': room['anchor']['nickname'],
                      # 'flv_url': room['room']['stream_url']['flv_pull_url']['HD1'],
                      # 更低的清晰度，占用空间更小
                      'flv_url': room['room']['stream_url']['flv_pull_url']['SD1'],

                      'state': '正在直播',
                      }
    except:return False, {
            'room_id': '',
            'state': '直播已关闭'
        }

# ['FULL_HD1']
if __name__ == '__main__':
    url = 'https://live.douyin.com/814607739589'
    # get_flvurl(url)
    _,roomid = get_flvurl(url)
    print(roomid['flv_url'])
