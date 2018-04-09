import os
import requests
from pyquery import PyQuery as pq
import time




class Model():


    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):

    def __init__(self):
        self.name = ''
        self.other = ''
        self.director = ''
        self.actor = ''
        self.cover_url = ''
        self.ranking = 0


def log(*args, **kwargs):

    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)
    with open('m.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def get(url, filename):
    """
    缓存
    """
    folder = 'cache'
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 发送网络请求
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content


def movie_from_div(div):
    """
    清洗数据 使用pyquery
    从div 里面获取到一个电影各信息
    """
    e = pq(div)
    m = Movie()

    allname = e('.mov_pic a').attr.title
    namelist = allname.split('/', 1)
    m.name = namelist[0]
    m.other = namelist[1]
    m.director = e('.mov_con').find('p').eq(0).find('a').text()
    m.actor = e('.mov_con').find('p').eq(1).find('a').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.number').find('em').text()
    return m

def save_cover(movies):
    """
    保存
    """
    for m in movies:
        filename = '{}.webp'.format(m.ranking)
        get(m.cover_url, filename)

def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    lenurl = len(url.split('-'))
    if lenurl == 1:
        filename = '1.html'
    else:
        filename = '{}'.format(url.split('-', 1)[1])
    # 按filename保存到缓存
    page = get(url, filename)
    # r = requests.get(url)
    # page = r.content

    #
    e = pq(page)
    items = e('.top_list #asyncRatingRegion li')
    # 调用 movie_from_div
    movies = [movie_from_div(i) for i in items]
    save_cover(movies)
    return movies


def main():
    start = time.time()

    for i in range(1, 11, 1):
        if i == 1:
            url = 'http://www.mtime.com/top/movie/top100'
        else:
            url = 'http://www.mtime.com/top/movie/top100/index-{}.html'.format(i)
    # url = 'http://www.mtime.com/top/movie/top100'
        movies = movies_from_url(url)
        with open('m.txt', 'a', encoding='utf-8') as f:
            print(movies)


    end = time.time()
    print('duration', end-start)


if __name__ == '__main__':
    main()
