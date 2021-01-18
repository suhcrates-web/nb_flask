from ast import literal_eval

def make_page(d , ind, day_0):
	try:
		info = literal_eval(d[6])
		rcept_no = str(info['rcept_no'])
		bogoNm = info['bogoNm']
		url0 = info['url0']
		page = '제목: '+d[1]+'<hr>'+d[3]+'<hr>보고서 번호: '+rcept_no+'<hr>종류: '+bogoNm +' // '+ '<a target="_blank" href ='+url0+'>원문링크</a><hr>'+d[2]

	except:
		page = d[1]+'<br><br>'+d[3]+'<br><br>'+d[2]+'<br><br>여기'
	rep= ''
	re_list = d[4].split('$')
	for i in re_list:
	    rep = rep + i +'<hr>'
	page = page + rep + '<form id="sub_form"><input name="writer" id="writer" type="text" placeholder="작성자" style="width:50px" ></input><input name="repl" id="repl" type="text" value=""  style="width:300px" placeholder="입력 후 삭제·수정 불가 ㅎㅎ"></input><input id="submit_form" type="submit" value="개선사항"></input><input name="ind" id="ind" type="hidden" value="' + ind + '"></input><input name="date" id="date" type="hidden" value="' + day_0 + '"></input></input><input name="cmd" type="hidden" value="write_repl"></input></form>'

	# state ={
	# '0':'ok',
	# '1':'jja',
	# '2':'kill',
	# }
	temp = ['','','']
	if d[5] == '':
		i = 0
	else: 
		i = int(d[5])
	temp[i]= 'checked'


	
	page =  '<form id="state"> <input type="radio"  value="0" message="굳" name="state" {}>굳 </input><input type="radio" value="1" message="안 중요" name="state" {}>안 중요   </input><input type="radio" value="2" message="오류" name="state" {}>오류</input></form>'.format(temp[0], temp[1], temp[2],) + '<hr>' +page 
	return page