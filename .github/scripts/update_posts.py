"""블로그 RSS 에서 최근 글 5편을 읽어 README 의 posts 마커 사이를 바꾼다."""
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://yesj1234.github.io/rss.xml"
COUNT = 5
README = Path(__file__).resolve().parents[2] / "README.md"
# RSS 는 KST 자정을 UTC 로 적어 하루 앞 날짜가 된다. 블로그에 보이는 날짜와 맞추려고 KST 로 되돌린다
KST = timezone(timedelta(hours=9))

with urllib.request.urlopen(FEED, timeout=30) as response:
    root = ET.fromstring(response.read())

items = []
for item in root.iter("item"):
    published = parsedate_to_datetime(item.findtext("pubDate")).astimezone(KST)
    items.append((published, item.findtext("title"), item.findtext("link")))
# 같은 날 올린 글이 많아 날짜만으로는 순서가 흔들린다. 제목으로 한 번 더 정렬해 매번 같은 결과를 낸다
items.sort(key=lambda entry: (entry[0], entry[1]), reverse=True)

lines = [f"- [{title}]({link}) — {published:%Y-%m-%d}" for published, title, link in items[:COUNT]]
block = "<!-- posts:start -->\n" + "\n".join(lines) + "\n<!-- posts:end -->"

text = README.read_text(encoding="utf-8")
updated = re.sub(r"<!-- posts:start -->.*?<!-- posts:end -->", block, text, flags=re.S)
README.write_text(updated, encoding="utf-8")
