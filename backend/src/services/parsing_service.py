from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from src.models.entities import News
from src.utils.result import Result


class ParsingService:
    BASE_URL = 'https://mosday.ru/news/tags.php?metro'

    USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36'
    )

    def __init__(self):
        self.headers = {
            'User-Agent': self.USER_AGENT
        }

    def parse_latest_posts(self, last_parsed_at: datetime = datetime(1970, 1, 1, tzinfo=timezone.utc)) -> Result[list]:
        try:
            url = self.BASE_URL
            all_news = []
            parse_result: Result = self._parse_single_page(url)
            if not parse_result.is_success:
                return Result.Error(parse_result.error)

            for news_data in parse_result.value:
                publication_datetime = news_data.get('publication_date')
                if publication_datetime and publication_datetime > last_parsed_at:
                    news_result = News.create(
                        title=news_data['title'],
                        image_url=news_data['image_url'],
                        publication_datetime=publication_datetime
                    )
                    if not news_result.is_success:
                        return Result.Error(news_result.error)
                    all_news.append(news_result.value)
            return Result.Success(all_news)
        except Exception as e:
            return Result.Error(str(e))

    def _fetch_page(self, url: str) -> Result[str]:
        '''
        Page loading
        '''
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                return Result.Error(f'Page load error. Status {response.status_code}.')
            text = response.text
            return Result.Success(text)
        except Exception as e:
            return Result.Error(str(e))

    def _parse_news_block(self, page_content: str) -> Result[list]:
        ''' Parse new block '''
        try:
            soup = BeautifulSoup(page_content, 'html.parser')
            news_table = soup.find('table', {'width': '95%'})
            news_rows = news_table.find_all('tr')
            news_list = []

            for row in news_rows:
                tds = row.find_all('td', valign='top')
                if len(tds) != 2:
                    continue
                image_td, content_td = tds

                # image
                image_tag = image_td.find('img')
                if image_tag and 'src' in image_tag.attrs:
                    image_src = image_tag['src']
                    full_image_url = f'https://mosday.ru/news/{image_src}'
                else:
                    full_image_url = None

                # Datetimes
                date_font = content_td.find('font', attrs={'style': 'font-size:13px'})
                if date_font:
                    date_b_tag = date_font.find('b')
                    if date_b_tag:
                        date_str = date_b_tag.get_text(strip=True)
                        # Time after b
                        time_str = ''
                        next_sibling = date_b_tag.next_sibling
                        while next_sibling and not isinstance(next_sibling, str):
                            next_sibling = next_sibling.next_sibling
                        if next_sibling:
                            time_str = next_sibling.strip()
                        date_time_str = f'{date_str} {time_str}'
                        try:
                            publication_datetime = datetime.strptime(date_time_str, '%d.%m.%Y %H:%M')
                        except ValueError:
                            publication_datetime = None
                    else:
                        publication_datetime = None
                else:
                    publication_datetime = None

                # title
                title_font = content_td.find('font', attrs={'style': 'font-size:16px'})
                if title_font:
                    title_b_tag = title_font.find('b')
                    if title_b_tag:
                        title_text = title_b_tag.get_text(strip=True)
                    else:
                        title_text = None
                else:
                    title_text = None

                news_list.append({
                    'title': title_text,
                    'image_url': full_image_url,
                    'publication_date': publication_datetime if publication_datetime else None,
                    'parsed_at_utc': datetime.now(timezone.utc)
                })

            return Result.Success(news_list)
        except Exception as e:
            return Result.Error(str(e))

    def _parse_single_page(self, url: str) -> Result[list]:
        '''
        Get page content
        '''
        try:
            page_content_result = self._fetch_page(url)
            if not page_content_result:
                return Result.Error(page_content_result.error)

            parse_result = self._parse_news_block(page_content_result.value)
            return parse_result
        except Exception as e:
            return Result.Error(str(e))
