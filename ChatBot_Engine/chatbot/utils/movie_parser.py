import httplib, urllib, bs4, re
from copy import deepcopy
from bs4 import BeautifulSoup

'''
MovieShowtimes class
This class is used for getting response from www.google.com/movies

movies = MovieShowtimes('Boston','','')
movies = movies.parse()
'''
class MovieShowtimes:
    '''
    Constructor for MovieShowtimes class.
    Parameters:
        near (optional)     - (string) valid name of the location (city)
        mid (optional)      - (string) valid movie ID. Can be taken from
                              www.google.com/movies
        tid (optional)      -   (string) valid theater ID. Can be taken from
                              www.google.com/movies
    '''
    def __init__(self, near, mid, tid):
        self.params = {'near': near, 'mid': mid, 'tid': tid}

        params = deepcopy(self.params)
        for key, val in params.iteritems():
            if val == '':
                self.params.pop(key)
        params = urllib.urlencode(self.params)

        conn = httplib.HTTPConnection('www.google.com')
        conn.request("GET", "/movies?" + params, "")

        response = conn.getresponse()
        self.response_code = response.status
        self.response = response.getheaders
        self.response_body = response.read()

        if (self.response_code == 200):
            self.html = BeautifulSoup(self.response_body, "lxml")

    '''
    Function for parsing the response and getting all the important data
    as a huge dictionary object.
    No parameters are required.
    '''
    def parse(self):
        if 'mid' in self.params:
            resp = {'movie': []}
            movies = self.html.findAll('div', attrs={'class': 'movie'})
            for div in movies:
                resp['movie'].append({})

                index = resp['movie'].index({})

                movie = []

                name = div.div.h2
                movie.append(('name', div.div.h2.contents[0]))

                movie.append(('info', div.div.find('div', attrs={'class':  'info'})))
                movie.append(('info_links', div.div.find('div', attrs={'class':  'links'})))
                movie.append(('theater', []))

                resp['movie'][index] = dict(movie)

                theaters = div.findAll('div', {'class': 'theater'})
                for div_theater in theaters:
                    resp['movie'][index]['theater'].append({})

                    index_th = resp['movie'][index]['theater'].index({})

                    theater = []

                    name = div_theater.div.find(attrs={'class': 'name'}).a.contents[0]
                    theater.append(('name', name))

                    theater.append(('address', div_theater.div.find(attrs={'class': 'address'}).contents[0]))
                    theater.append(('times', []))

                    resp['movie'][index]['theater'][index_th] = dict(theater)

                    times = div_theater.find('div', {'class': 'times'})
                    times = times.findAll('span')
                    for div_time in times:
                        time = []

                        if len(div_time.contents) == 3:
                            time_val = div_time.contents[2]
                            time_val = re.search('(.*)&#', time_val)
                            resp['movie'][index]['theater'][index_th]['times'].append(time_val.group(1))

            return resp

        resp = {'theater': []}
        theaters = self.html.findAll('div', attrs={'class': 'theater'})
        for div in theaters:
            resp['theater'].append({})

            index = resp['theater'].index({})

            theater = []
            theater.append(('name', div.div.h2.a.contents[0]))
            theater.append(('info', div.div.div.contents[0]))
            theater.append(('movies', []))

            resp['theater'][index] = dict(theater)

            movies = div.findAll('div', {'class': 'movie'})
            for div_movie in movies:
                resp['theater'][index]['movies'].append({})

                index_m = resp['theater'][index]['movies'].index({})

                movie = []
                movie.append(('name', div_movie.div.a.contents[0]))
                movie.append(('info', div_movie.span.contents[0]))
                movie.append(('times', []))

                resp['theater'][index]['movies'][index_m] = dict(movie)

                times = div_movie.find('div', {'class': 'times'})
                times = times.findAll('span')
                for div_time in times:
                    if len(div_time.contents) == 3:
                        time_val = div_time.contents[2]
                        try:
                            time_val = re.search('^((([1-9])|(1[0-2])):([0-5])(0|5)((a|p)m)*)?$', time_val)
                            resp['theater'][index]['movies'][index_m]['times'].append(time_val.group(1))
                        except (TypeError, AttributeError) as e:
                            resp['theater'][index]['movies'][index_m]['times'].append("")
        return resp
