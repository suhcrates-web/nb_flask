from flask import Flask, render_template, url_for, request, redirect, jsonify
import csv, json
import datetime
import html, re, glob
from waitress import serve
from make_page import make_page

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bot_v3/', methods = ['GET'])
def bot_v3port():
    day_0 = datetime.datetime.today().strftime("%Y-%m-%d")
    if request.method == "POST":
        with open('file111.csv','w') as f:
            print(request.data)
        # if(request.form['day_0']):
            # day_0 = request.form['day_0']
            #이 request 건내주는게 되는지는 아직 실험 안해봄.
            #아무래도 안되는듯. 보낼때 날짜를 포함해서 보내도록 하자.
        return redirect(url_for('/bot_v3/'+day_0+'/', request = request, day_0 = day_0))
        # else:
            # return redirect(url_for('/bot_v3/'+day_0+'/', request = request, day_0 = day_0))
    else:
        return redirect('/bot_v3/'+day_0+'/')

@app.route('/bot_v3/<day_0>/', methods = ['POST','GET'])
def bot_v3(day_0):
    if request.method == "POST":
        # day_0 = datetime.datetime.today().strftime("%Y-%m-%d")
        file_0 = 'data/date/{}.csv'.format(day_0) #들어온 날짜를 그대로.
        try:
            with open(file_0, 'a+', encoding= 'utf-8') as f:
                f.seek(0)
                lines = f.readlines()
                ind = str(len(lines))
                info = json.loads(request.form['info'])

                url = info['url']

                title =  request.form['title']
                article = html.unescape(request.form['article'])
                article = article.replace('\n','')
                date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                line = [ind,'|', title,'|', article,'|', date,'|||',str(info),'\n']
                print(line)
                if ind =='0': #아무것도 없으면 헤더 만들어줌.
                    lines=['ind','|', 'title','|', 'article','|', 'date','|','repl','|','desk','|','info']
                    f.writelines(lines)
                    line[0] = '1' 

                #마지막 value 끝에 라인브레이크 없으면 다음줄 첫머리에 달아줌.
                if not bool(re.search(r'\n$',lines[-1][-1])): 
                        line = ['\n'] + line
                f.writelines(line)
            return redirect('/bot_v3/'+day_0)
        except:
            return 'issue adding data'

    else: #GET
        file_0 = 'data/date/{}.csv'.format(str(day_0))
        with open(file_0, 'a+', encoding ='utf-8') as f:
            data = csv.reader(f, delimiter = '|')
            f.seek(0) #이렇게 해야 읽힘.
            objs = []
            first_line=True
            #dict 형태로 변환.
            for row in data:
                if not first_line:
                    objs.append({
                        'ind' : row[0],
                        'title' : row[1],
                        'article' : row[2],
                        'date' : row[3],
                        'repl' : row[4],
                        'desk' : row[5]
                        # 'info' : row[6]
                    })
                else:
                    first_line = False

            #t순서 거꾸로 뒤집기.
            objs = [objs[-i] for i in range(1 , len(objs)+1)]

        #폴더에 있는 파일 모두 검색해서 본문 아래쪽에 배열하기 위함 #
        pathnames = glob.glob("./data/date/*.csv", recursive=True)
        pagenames = [re.findall(r'(?<=\\).+(?=\.)', x)[0] for x in pathnames][::-1] 
        return render_template ("bot_v3.html", day_0=day_0, objs = objs, pagenames = pagenames)

@app.route('/bot_v3/repl', methods = ['POST','GET'])
def bot_v3_repl():
    if request.method == 'POST':
        ind = request.form['ind']
        day_0 = request.form['date']
        day_0 = re.sub(r' .*', '', day_0)
        cmd = request.form['cmd']

        file_0 = 'data/date/{}.csv'.format(str(day_0))
        if cmd == "readall":
            with open(file_0, 'r', encoding= 'utf-8') as f:
                data = csv.reader(f, delimiter= '|')
                for row in data:
                    if row[0] == ind:
                        d = row
                page = make_page(d, ind, day_0)       
                return page
        elif cmd == 'read':
            with open(file_0, 'r', encoding= 'utf-8') as f:
                data = csv.reader(f, delimiter= '|')
                for row in data:
                    if row[0] == ind:
                       repl_0 = row[4]
                if repl_0 != '':
                    return repl_0
                else:
                    return "['요청사항 없음']"

        elif cmd == 'write_repl':
            repl = request.form['repl'].replace('$','').replace('|','')
            writer = request.form['writer']
            with open(file_0, 'r', encoding= 'utf-8') as f:
                data_read = csv.reader(f, delimiter = '|')
                lines = list(data_read)
                i = 0
                for row in lines:
                    try:
                        if row[0] == ind:
                            row[4] = '$'.join(row[4].split('$') +[writer + " : "+ repl])
                            d = row
                            lines[i] = row
                    except :
                        pass
                    i += 1
            with open(file_0, 'w', encoding= 'utf-8', newline='') as f:
                data_write = csv.writer(f, delimiter = '|')
                data_write.writerows(lines)
            page = make_page(d , ind, day_0)       
            return page
        elif cmd == 'state_change':
            with open('test166.csv','w') as f:
                f.writelines('here')
            desk = request.form['desk']
            with open(file_0, 'r', encoding= 'utf-8') as f:
                data_read = csv.reader(f, delimiter = '|')
                lines = list(data_read)
                i = 0
                for row in lines:
                    try:
                        if row[0] == ind:
                            row[5] = desk
                            lines[i] = row
                    except :
                        pass
                    i += 1
            with open(file_0, 'w', encoding= 'utf-8', newline='') as f:
                data_write = csv.writer(f, delimiter = '|')
                data_write.writerows(lines)

            return ''  #라디오버튼으로 페이지 안에서 직접 조종








@app.route('/bot/', methods = ['POST','GET'])
def bot():
    if request.method == "POST":
        day_0 = datetime.datetime.today().strftime("%Y-%m-%d")
        file_0 = 'data/date/{}.csv'.format(day_0)
        try:
            with open(file_0, 'a+', encoding= 'utf-8') as f:
                f.seek(0)
                lines = f.readlines()
                ind = str(len(lines))
                title =  request.form['title']
                article = html.unescape(request.form['article'])
                article = article.replace('\n','')
                date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                line = [ind,'|', title,'|', article,'|', date,'||\n']
                if ind =='0':
                    lines=['ind','|', 'title','|', 'article','|', 'date','|','repl','|','desk']
                    f.writelines(lines)
                    line[0] = '1'
                if not bool(re.search(r'\n$',lines[-1][-1])):
                        line = ['\n'] + line
                f.writelines(line)
            return redirect('/bot/')

            # with open('data/bot.csv') as csv_file:
            #     data = csv.reader(csv_file, delimiter = '|')
            #     ind_ = 0
            #     for i in data:
            #         ind_ = ind_+1
                
            # with open('data/bot.csv', 'a', newline= '') as csv_file:
            #     spanwriter = csv.writer(csv_file, delimiter = '|')
            #     title =  request.form['title']
            #     article = html.unescape(request.form['article'])
            #     article = article.replace('\n','')
            #    # article = re.sub('\"','\\\"', article)  #이건 필요없음
            #     ind = ind_
            #     date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            #     spanwriter.writerow([ind, title, article, date])
            # return redirect('/bot/')
        except:
            return 'issue adding data'

    else:
        day_0 = datetime.datetime.today().strftime("%Y-%m-%d")
        file_0 = 'data/date/{}.csv'.format(day_0)
        with open(file_0, 'a+', encoding ='utf-8') as f:
            data = csv.reader(f, delimiter = '|')
            f.seek(0)
            # if f.readlines() ==[]:
            #     f.writelines("ind|title|article|date")
            objs = []
            first_line=True
            for row in data:
                if not first_line:
                    objs.append({
                        'ind' : row[0],
                        'title' : row[1],
                        'article' : row[2],
                        'date' : row[3],
                        'repl' : row[4],
                        'desk' : row[5]
                    })
                else:
                    first_line = False

            objs = [objs[-i] for i in range(1 , len(objs)+1)]


        pathnames = glob.glob("./data/date/*.csv", recursive=True)
        pagenames = [re.findall(r'(?<=\\).+(?=\.)', x)[0] for x in pathnames] 

        return render_template ("bot.html", objs = objs, pagenames = pagenames)

@app.route('/bot/<day_0>/') #int가 아닌데 <int:day_0>라고 써서 안됐음
def page(day_0):
    
    file_0 = 'data/date/{}.csv'.format(str(day_0))
    try:
        with open(file_0, 'r', encoding ='utf-8') as f:
            data = csv.reader(f, delimiter = '|')
            # f.seek(0)
            # if f.readlines() ==[]:
            #     f.writelines("ind|title|article|date")
            objs = []
            first_line=True
            for row in data:
                if not first_line:
                    objs.append({
                        'ind' : row[0],
                        'title' : row[1],
                        'article' : row[2],
                        'date' : row[3],
                        'repl' : row[4],
                        'desk' : row[5]
                    })
                else:
                    first_line = False

            objs = [objs[-i] for i in range(1 , len(objs)+1)]


        pathnames = glob.glob("./data/date/*.csv", recursive=True)
        pagenames = [re.findall(r'(?<=\\).+(?=\.)', x)[0] for x in pathnames] 

        return render_template ("bot.html", objs = objs, pagenames = pagenames)
    except:
        
        pathnames = glob.glob("./data/date/*.csv", recursive=True)
        pagenames = [re.findall(r'(?<=\\).+(?=\.)', x)[0] for x in pathnames] 
        return render_template ("warning.html", alarm="해당 날짜 데이터 없음")

@app.route('/bot/repl', methods = ['POST','GET'])
def repl():
    if request.method == "POST":
        try: 
            date = request.form['date']
            date = re.sub(r' .*','',date)
            ind = request.form['ind']
            repl = request.form['repl']
            
            v = request.form['v']

            file_0 = 'data/date/{}.csv'.format(date)
            data_read = []
            with open(file_0, 'r', encoding= 'utf-8') as inf:
                data_read = csv.reader(inf, delimiter = '|')
                data_read= list(data_read)
            with open('data/test123.csv', 'a+') as f:
                f.writelines(data_read)
            
            with open(file_0, 'w', encoding= 'utf-8', newline='') as outf:
                data_write = csv.writer(outf, delimiter = '|')
                for row in data_read:
                    if row[0] == ind:
                        row[4] = row[4] + '<hr>'+repl
                    data_write.writerow(row)
            
            #다시 페이지 띄울 준비.
            objs = []
            first_line=True
            for row in data_read:
                if not first_line:
                    objs.append({
                        'ind' : row[0],
                        'title' : row[1],
                        'article' : row[2],
                        'date' : row[3],
                        'repl' : row[4],
                        'desk' : row[5]
                    })
                else:
                    first_line = False
            
            

            objs = [objs[-i] for i in range(1 , len(objs)+1)]

            #하단 페이지네임.
            pathnames = glob.glob("./data/date/*.csv", recursive=True)
            pagenames = [re.findall(r'(?<=\\).+(?=\.)', x)[0] for x in pathnames] 
            if v=='bot2':
                return redirect('/bot2/', current_ind = ind, objs=objs, pagenames=pagenames)
            else:
                return redirect('/bot/')
        except :
            return "issue in repl"
    else:
        return "get"


##다시만들기
@app.route('/bot2/', methods = ['POST','GET'])
def bot2():
    if request.method == "POST":
        day_0 = datetime.datetime.today().strftime("%Y-%m-%d")
        file_0 = 'data/date/{}.csv'.format(day_0)
        try:
            with open(file_0, 'a+', encoding= 'utf-8') as f:
                f.seek(0)
                lines = f.readlines()
                ind = str(len(lines))
                title =  request.form['title']
                article = html.unescape(request.form['article'])
                article = article.replace('\n','')
                date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                line = [ind,'|', title,'|', article,'|', date,'||\n']
                if ind =='0':
                    lines=['ind','|', 'title','|', 'article','|', 'date','|','repl','|','desk']
                    f.writelines(lines)
                    line[0] = '1'
                if not bool(re.search(r'\n$',lines[-1][-1])):
                        line = ['\n'] + line
                f.writelines(line)
            return redirect('/bot2/')

            # with open('data/bot.csv') as csv_file:
            #     data = csv.reader(csv_file, delimiter = '|')
            #     ind_ = 0
            #     for i in data:
            #         ind_ = ind_+1
                
            # with open('data/bot.csv', 'a', newline= '') as csv_file:
            #     spanwriter = csv.writer(csv_file, delimiter = '|')
            #     title =  request.form['title']
            #     article = html.unescape(request.form['article'])
            #     article = article.replace('\n','')
            #    # article = re.sub('\"','\\\"', article)  #이건 필요없음
            #     ind = ind_
            #     date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            #     spanwriter.writerow([ind, title, article, date])
            # return redirect('/bot/')
        except:
            return 'issue adding data'

    else:
        day_0 = datetime.datetime.today().strftime("%Y-%m-%d")
        file_0 = 'data/date/{}.csv'.format(day_0)
        with open(file_0, 'a+', encoding ='utf-8') as f:
            data = csv.reader(f, delimiter = '|')
            f.seek(0)
            # if f.readlines() ==[]:
            #     f.writelines("ind|title|article|date")
            objs = []
            first_line=True
            for row in data:
                if not first_line:
                    objs.append({
                        'ind' : row[0],
                        'title' : row[1],
                        'article' : row[2],
                        'date' : row[3],
                        'repl' : row[4],
                        'desk' : row[5]
                    })
                else:
                    first_line = False

            objs = [objs[-i] for i in range(1 , len(objs)+1)]

        #하단 페이지네임.
        pathnames = glob.glob("./data/date/*.csv", recursive=True)
        pagenames = [re.findall(r'(?<=\\).+(?=\.)', x)[0] for x in pathnames] 

        return render_template ("bot2.html", objs = objs, pagenames = pagenames)

@app.route('/bot2/<day_0>/') #int가 아닌데 <int:day_0>라고 써서 안됐음
def page2(day_0):
    
    file_0 = 'data/date/{}.csv'.format(str(day_0))
    try:
        with open(file_0, 'r', encoding ='utf-8') as f:
            data = csv.reader(f, delimiter = '|')
            # f.seek(0)
            # if f.readlines() ==[]:
            #     f.writelines("ind|title|article|date")
            objs = []
            first_line=True
            for row in data:
                if not first_line:
                    objs.append({
                        'ind' : row[0],
                        'title' : row[1],
                        'article' : row[2],
                        'date' : row[3]
                    })
                else:
                    first_line = False

            objs = [objs[-i] for i in range(1 , len(objs)+1)]


        pathnames = glob.glob("./data/date/*.csv", recursive=True)
        pagenames = [re.findall(r'(?<=\\).+(?=\.)', x)[0] for x in pathnames] 

        return render_template ("bot2.html", objs = objs, pagenames = pagenames)
    except:
        
        pathnames = glob.glob("./data/date/*.csv", recursive=True)
        pagenames = [re.findall(r'(?<=\\).+(?=\.)', x)[0] for x in pathnames] 
        return render_template ("warning.html", alarm="해당 날짜 데이터 없음")






@app.route('/bot/<int:ind_>/')
def show_article(ind_):
    with open('data/bot.csv') as csv_file:
            data = csv.reader(csv_file, delimiter = '|')
            first_line = True
            objs = []
            for row in data:
                if not first_line:
                    objs.append({
                        'ind' : row[0],
                        'title' : row[1],
                        'article' : row[2],
                        'date' : row[3],
                        'repl' : row[4],
                        'desk' : row[5]
                    })
                else:
                    first_line = False

            l = []
            i=0
            for obj in objs:
                if obj['ind'] == str(ind_):
                    l.append(i)
                i = i+1
            obj = objs[l[0]]
            
    
    return render_template ("article.html", obj = obj) # objs 아님

@app.route('/bot_v3/update/')
def update():
    return render_template("update.html")

@app.route('/corona/')
def corona_page():
    return render_template()

@app.route('/data/', methods = ['POST','GET'])
def data():
    if request.method == "POST":
        try:
            with open('data/test.csv', 'a+', newline= '') as csv_file:
                spanwriter = csv.writer(csv_file, delimiter = ',')
                in_con = request.form['content']
                in_con = str.split(in_con, ',')
                spanwriter.writerow(in_con)
            return redirect('/data/')
        except:
            return 'issue adding data'


    else:
        with open('data/test.csv') as csv_file:
            data = csv.reader(csv_file, delimiter = ',')
            first_line = True
            objs = []
            for row in data:
                if not first_line:
                    objs.append({
                        "ind": row[0],
                        "a": row[1],
                        "b": row[2],
                        "c": row[3]
                    })
                else:
                    first_line = False
        return render_template ("data.html", objs = objs)

if __name__ == "__main__":
    # serve(app, host = '0.0.0.0', port = '3389', threads=1)
    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')#노트북 5232, 데스크탑 5231
        port = port[0]
    print(port)

    app.run(host = '0.0.0.0', port = port, debug=True)


