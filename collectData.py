import json
from datetime import datetime

import requests
from fake_useragent import UserAgent


def collect_data(request_time):
    required_time = 0
    user_agent_random = UserAgent().random
    page_number = 1
    page_increment = 1
    result = []

    if request_time == "today":
        required_time = str((datetime.now().timestamp() - 86400) * 1000)

    if request_time == "month":
        required_time = str((datetime.now().timestamp() - 2629743) * 1000)

    if request_time == "year":
        required_time = str((datetime.now().timestamp() - 31556926) * 1000)

    while True:

        runout_flag = False

        for article in range(page_number, 300, page_increment):

            url = f'https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query?type=1&pageNo={page_number}&pageSize=10&catalogId=161'
            response = requests.get(
                url=url,
                headers={'user-agent': f'{user_agent_random}'}
            )

            page_number += page_increment

            data = response.json()

            if not data["data"]["catalogs"] or runout_flag:
                with open('result.json', 'w') as file:
                    json.dump(result, file, indent=4, ensure_ascii=False)
                return

            articles = data["data"]["catalogs"][0]["articles"]

            for i in articles:
                if 'Binance Will Delist' in i.get('title') and 'Options' not in i.get('title') and 'Margin' not in i.get('title'):
                    if str(i.get('releaseDate')) > required_time:
                        print(i.get('title'))
                        article_full_title = i.get('title')
                        article_timestamp = i.get('releaseDate')
                        article_code = i.get('code')
                        article_link = f'https://www.binance.com/en/support/announcement/{article_code}'
                        article_date = datetime.utcfromtimestamp(int(article_timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S')

                        result.append(
                            {
                                'full_title': article_full_title,
                                'link': article_link,
                                'date': article_date,
                                'timestamp': article_timestamp
                            }
                        )
                    else:
                        runout_flag = True


if __name__ == '__main__':
    collect_data(request_time="year")
