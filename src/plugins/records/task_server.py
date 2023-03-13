from flask import Flask, request
import json
import jieba
import requests
import os
import random
app = Flask(__name__)


url = 'http://localhost:8089/api/tr-run/'
invertedIndex = {}
with open('src/plugins/records/inverted_index.json', 'r') as fr:
    invertedIndex = json.load(fr)


@app.route('/offer', methods=['POST'])
def offer_task():
    try:
        group_id = request.form['group_id']
        img_file = request.form['img_file']
        content = request.form['content'] #base64

        # 分词
        res = requests.post(url=url, data={'img': content})

        raw_data = res.json()['data']['raw_out']

        content = ''

        for raw in raw_data:
            content += raw[1]

        cut_words = jieba.lcut_for_search(content)

        cut_words = list(set(cut_words))

        # 更新查询表
        # print(cut_words)

        # 群号是否在表中
        if group_id not in invertedIndex:
            invertedIndex[group_id] = {}
        
        # 分词是否在群的hashmap里
        for word in cut_words:
            if word not in invertedIndex[group_id]:
                invertedIndex[group_id][word] = [img_file]
            else:
                invertedIndex[group_id][word].append(img_file)
        
        with open('src/plugins/records/inverted_index.json', 'w',encoding='utf-8') as f:
            json.dump(invertedIndex, f,indent=2,separators=(',', ': '),ensure_ascii=False)

        return json.dumps({'status': 'success', 'cut': cut_words},ensure_ascii=False)

    except Exception as e:
        return json.dumps({'status': 'error', 'msg': str(e)})


@app.route('/query', methods=['GET'])
def query():
    try:
        sentence = request.args.get('sentence')
        group_id = request.args.get('group_id')

        cut_words = jieba.lcut_for_search(sentence)

        cut_words = list(set(cut_words))

        # 查询
        if group_id not in invertedIndex:
            return json.dumps({'status': -1})
        hash_map = invertedIndex[group_id]

        count_map = {}

        result_pool = []
        for word in cut_words:
            if word not in hash_map:
                return json.dumps({'status': 2})
            for img in hash_map[word]:
                if img not in count_map:
                    count_map[img] = 1
                else:
                    count_map[img] += 1
                if count_map[img] == len(cut_words):
                    result_pool.append(img)
        
        if len(result_pool) == 0:
            return json.dumps({'status': 2})
        idx = random.randint(0, len(result_pool)-1)
        return json.dumps({'status': 1, 'msg': result_pool[idx]})
    except Exception as e:
        return json.dumps({'status': 0, 'msg': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)