import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

raw_git_url = 'https://raw.githubusercontent.com'
github_url = 'https://github.com'
git_name = 'Owlbearpig'
repo_name = 'Master-thesis'

repo_url = '/'.join([github_url, git_name, repo_name])


class Commit:
    def __init__(self, commit_url):
        self.commit_url = commit_url
        self.id = commit_url.split('/')[-1]

        self.commit_date = self.get_commit_date()
        self.char_cnt = self.get_char_cnt()

    def get_commit_date(self):
        page = requests.get(self.commit_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        raw_datetime = soup.find_all(name='relative-time')[-1]['datetime']

        return datetime.strptime(raw_datetime, '%Y-%m-%dT%H:%M:%SZ')

    def get_char_cnt(self):
        tex_folder_name = 'chapters'
        chapter_dir_url = self.commit_url.replace('commit', 'tree') + f'/{tex_folder_name}'

        page = requests.get(chapter_dir_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        tex_file_urls = []
        for a_class in soup.find_all(name='a', class_='js-navigation-open Link--primary'):
            if '.tex' in a_class['title']:
                file_name = a_class['title']
                raw_tex_url = '/'.join([raw_git_url, git_name, repo_name, self.id, tex_folder_name, file_name])
                tex_file_urls.append(raw_tex_url)

        char_cnt = 0
        for tex_file_url in tex_file_urls:
            page = requests.get(tex_file_url)
            soup = BeautifulSoup(page.text, 'html.parser')

            char_cnt += len(soup.text)

            time.sleep(1)

        return char_cnt


def find_page_element_url(url, name, class_=None, field='href'):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for a_class in soup.find_all(name=name, class_=class_):
        return a_class[field]


def iterate_commits(final_commit_url):
    commit_urls = [final_commit_url]

    for _ in commit_urls:
        next_commit_href = find_page_element_url(commit_urls[-1], name='a', class_='sha')
        if next_commit_href:
            next_commit_url = github_url + next_commit_href
            commit_urls.append(next_commit_url)
            print(commit_urls[-1])
        else:
            break
        time.sleep(1)

        # speedup 4 testing
        #if len(commit_urls) > 3:
        #    break

    return commit_urls


last_commit_url = github_url + find_page_element_url(repo_url, name='a', class_='Link--primary markdown-title')

all_commit_urls = iterate_commits(last_commit_url)

commits = []
for url in all_commit_urls:
    time.sleep(1)
    commits.append(Commit(url))

for commit in commits:
    print(commit.commit_date, commit.char_cnt)

with open('commit_char_cnts.csv', 'w') as file:
    for commit in commits:
        print(commit.commit_date)
        s = ', '.join([str(commit.id), str(commit.commit_date), str(commit.char_cnt), '\n'])
        file.write(s)
        print()
    file.close()
