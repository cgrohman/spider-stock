import os
import argparse
import subprocess

DOMAIN_DICT = {
      'cnn':
        {
        'start_url':['http://money.cnn.com/'],
        'article_xpath_sel':'//*[@id="storytext"]/*[self::h2 or self::p]',
        'article_css_sel':'',
        'author_css_sel':['.byline a::text','.byline::text'],
        'author_xpath_sel':'',
        'date_xpath_sel':'',
        'date_css_sel':'.cnnDateStamp::text',
        'allow':[r'money.cnn.com'],
        'deny':[r'/quote.*',r'/video.*',r'/services/privacy/',r'/services/terms.html'],
        'title_css':'.article-title::text',
        },
      'nbc':
        {
        'start_url':['http://www.nbcnews.com/'],
        'article_xpath_sel':'',
        'article_css_sel':'.article-body p::text',
        'author_css_sel':['.byline_author::text'],
        'author_xpath_sel':'',
        'date_xpath_sel':'',
        'date_css_sel':'.timestamp_article::text',
        'allow':[r'nbcnews.com'],
        'deny':[],
        'title_css':'h1::text',
        },
      }

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-name')
  parser.add_argument('-find')
  args = parser.parse_args()

  with open('env_config.py','w') as f:
    f.write("DOMAIN_NAME='{}'\nREG_FIND='{}'\nDOMAIN_DICT={}".format(args.name, args.find, DOMAIN_DICT))

# subprocess.run(["scrapy", "runspider", "newsSpider.py",'-o','output.json'], stdout=subprocess.PIPE)


if __name__=='__main__':main()