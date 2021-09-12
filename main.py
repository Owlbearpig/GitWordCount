import requests
from bs4 import BeautifulSoup
from datetime import datetime

github_url = 'https://github.com'
git_name = '/Owlbearpig'
repository = '/Master-thesis'

commits_url = f'{github_url}{git_name}{repository}/commits/main'

page = requests.get(commits_url)
soup = BeautifulSoup(page.text, 'html.parser')

all_commits = {}
for div_class in soup.find_all('div'):
    try:
        if 'TimelineItem-body' in div_class['class']:
            datetime_object = datetime.strptime(div_class.find_all('h2')[0].text.split('Commits on ')[-1], '%b %d, %Y')

            single_day_commits = []
            for link in div_class.find_all('a'):
                href = link.get('href')
                if '/commit/' in href and href.split('/commit/')[-1] not in single_day_commits:
                    single_day_commits.append(href.split('/commit/')[-1])

            all_commits[str(datetime_object)] = single_day_commits
    except:
        continue


def commit_char_cnt(commit_id):
    tex_repository = f'{git_name}{repository}/tree/{commit_id}'

    folder_list = [tex_repository]
    tex_file_list = []
    def get_tex_files(relative_url):
        url = github_url + relative_url
        #print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            link_href = link.get('href')
            if '.tex' in link_href:
                tex_file_list.append(link_href)
            elif f'/tree/{commit_id}' in link_href and link_href not in folder_list:
                folder_list.append(link_href)
                get_tex_files(link_href)
            else:
                continue

    get_tex_files(tex_repository)

    s = 0
    for link_href in tex_file_list:
        link_href_no_blob = link_href.replace('/blob', '')
        full_raw_url = f'https://raw.githubusercontent.com{link_href_no_blob}'
        page = requests.get(full_raw_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        s +=len(soup.text)

    print(len(folder_list))
    print(len(tex_file_list))
    print(s)
    return s


with open('daily_commit_char_cnts.csv', 'w') as file:
    for day in all_commits:
        print(day)
        for commit_id in all_commits[day]:
            cnt = commit_char_cnt(commit_id)
            s = str(day) + ', ' + str(commit_id) + ', ' + str(cnt) + ', ' + '\n'
            file.write(s)
        print()
    file.close()
