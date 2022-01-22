import requests
import json
from django.views import generic

from .forms import SearchForm



# リクエスト先を動的に指定 apiをjson形式で取得(クラス内部で呼び出す)
def get_api_data(name, keyword):

    with open('search/json/info.json', 'r') as f:
        info = json.load(f)

        # Qiitaが選択されたとき
        if name == 'Qiita':
            url = info[name]['url']
            params = {
                'per_page': 100,
                'query': keyword
            }

            result = json.loads(requests.get(url, params).text)

        # GitHubが選択されとき
        elif name == 'GitHub':
            url = info[name]['url']
            params = {
                'per_page': 100,
                'q': keyword
            }

            result = json.loads(requests.get(url, params).text)['items']

        else:
            '''error handling'''
            pass

    return result


class SearchView(generic.ListView):
    context_object_name = 'data'

    def get_queryset(self):
        keyword = self.request.GET.get('q', default=None)
        name = self.request.GET.get('name')

        if keyword:
            queryset = get_api_data(name, keyword)
            return queryset

    # 検索フォームをレンダリング フォーム入力値をページ更新後も保持
    def get_context_data(self, **kwargs):
        if self.request.GET:
            form = SearchForm(initial={
                'q': self.request.GET.get('q'),
                'name': self.request.GET.get('name')
            })
        else:
            form = SearchForm
        keyword = self.request.GET.get('q', default=None)

        context = super().get_context_data(**kwargs)
        context['form'], context['keyword'] = (form, keyword)
        return context

    # nameの値によってtemplate_nameを動的に指定
    def get_template_names(self):
        name = self.request.GET.get('name', default=None)
        if name:
            template_name = f'main/sch{name}.html'
        else:
            template_name = 'main/search.html'
        return [template_name]

    '''NEXT --> pagenation機能実装 後々できたらでもいっか。'''