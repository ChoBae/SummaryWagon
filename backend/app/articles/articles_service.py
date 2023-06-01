from . import articles_repository
from ..users import users_repository

from .articles_schema import addArticleDto, getKeywordDto
from ..models import ResponseModel

from ..utils.bs4.preprocess import title_image_parsing, text_parsing
from ..utils.bs4.keyword import keyword_finder
from ..utils.chat_gpt.summary import summarize
from ..utils.thumbnail.image_resizing import upload_to_s3

from time import time, process_time
from datetime import datetime
from decouple import config

IMAGE_URL = config('IMAGE_URL')
DEFAULT_IMAGE_URL = config('DEFAULT_IMAGE_URL')


async def read_all_articles(email: str):
    user = await users_repository.find_user_by_email(email)
    article_ids = user["article_ids"]

    return await articles_repository.find_all_articles(article_ids)


async def read_hot_articles():
    return await articles_repository.find_hot_articles()


async def read_article(article_id: str):
    return await articles_repository.find_article(article_id)


async def add_article(addArticleDto: addArticleDto):
    # start_time = process_time()
    start_time = time()

    email = addArticleDto.email
    link = addArticleDto.link

    # 기사가 이미 존재하는지 확인
    isExist = await articles_repository.find_article_by_link(link)

    if isExist:
        await articles_repository.update_article_cnt(isExist)

        isSameUser = await users_repository.find_user_by_article_id(email, isExist)

        if isSameUser is None:
            await users_repository.update_user(email, isExist)

        return ResponseModel(isExist, "Article already exists in DB.")
    
    # text 및 title, image 파싱
    text_all = text_parsing(link)
    title, image, image_content_type = title_image_parsing(link)
    
    # text 요약
    summary = summarize(text_all)

    article = {
        "link": link,
        "datetime": datetime.now(),
        "title": title,
        "image": image,
        "cnt": 1,
        "summary": summary,
        "description": summary[0], # og_description으로 수정
        "categories": [keyword]
    }

    article_id = await articles_repository.add_article(article)

    # file extension setting 
    idx_start = image_content_type.find('/')
    extension = image_content_type[(idx_start+1):]

    # image_resizing 
    upload_to_s3(article_id['id'], image, extension)
    image_url = IMAGE_URL + 'resized-' + article_id["id"] + "." + extension
    
    await articles_repository.update_article(article_id, image_url)
    print("Resized image updated to DB successfully")
    
    # 유저 히스토리에 추가
    await users_repository.update_user(email, article_id)

    # end_time = process_time()
    end_time = time()
    print("time: ", end_time - start_time)

    return ResponseModel(article_id, "Article added successfully.")


async def get_keyword(getKeywordDto: getKeywordDto):
    link = getKeywordDto.link
    text_all = text_parsing(link)
    keyword = keyword_finder(text_all)
    
    return keyword
    
    