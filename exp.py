@app.route('/bot_v3/repl', methods = ['POST','GET'])
def bot_v3_repl():
    if request.method == 'POST':
        with open('test124.csv','w') as f:
            f.writelines(request.values)
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
        elif cmd == 'sate_change':
            