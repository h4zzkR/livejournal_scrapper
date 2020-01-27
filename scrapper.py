#!/usr/bin/env python
import sys
import os
import json
import pandas

sys.path.append('..')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
blog2csv = os.path.join(BASE_DIR, 'livejournal_blog2csv/blog2csv.py')
# from blog2csv_scrap.blog2csv import main as blog2csv


def create_parser():
    from optparse import OptionParser
    p = OptionParser(
        "usage: %prog http://yourusername.livejournal.com/most-recent-entry.html")  # noqa
    p.add_option(
        "-b",
        "--blogs",
        dest="blogs",
        type="string",
        default='blogs.json',
        help="Set blogs.json path")
    p.add_option(
        '--min_len',
        dest='min_len',
        type='int',
        default=10,
        help='Default len of blog text'
    )
    return p

class ProcessBlogs(object):
    def __init__(self, blogs, save_dir='blogs'):
        self.blogs_path = os.path.join(BASE_DIR, blogs)
        self.blogs_list = self.read_json(self.blogs_path)
        self.save_dir = os.path.join(BASE_DIR, save_dir)

    def read_json(self, json_path):
        f = open(json_path, 'r')
        data = json.load(f)
        f.close()
        return data

    def get_csv(self, start_blog_url, max_posts):
        command = f"python {blog2csv} {start_blog_url} --destination {self.save_dir}" + \
            f" --max_posts {max_posts}"
        os.system(command)

    def csv_name(self, url, full=True):
        s = url[url.find('//') + 2:url.find('.live')]
        fname = f'{s}_lj_blog.csv'
        if full is True:
            fname = os.path.join(self.save_dir, fname)
        return fname
        
    def get_from_list(self):
        csv_pathes = []
        length = len(self.blogs_list)
        for (i,blog) in enumerate(self.blogs_list):
            print('________________________________________________')
            print(f'Blog {i+1}/{length}')
            print('________________________________________________')

            try:
                max_posts = blog['max_posts']
            except KeyError:
                max_posts = 100000

            csv_name = self.csv_name(blog['url'], full=False)
            csv_path = self.csv_name(blog['url'])
            if csv_name not in os.listdir(self.save_dir):
                self.get_csv(blog['url'], max_posts)
            csv_pathes.append(csv_path)



def main():
    p = create_parser()
    if not os.path.exists('blogs'):
        os.makedirs('blogs')
    args = p.parse_args()

    blogs = ProcessBlogs(args[0].blogs)

    blogs.get_from_list()

if __name__ == "__main__":
    main()
