

$(document).ready(function(){
	
	$(document).on('click', 'tr', function(event){
		var clicked = this.id
		if(clicked != 'avoid'){
		$(this).siblings('tr').removeClass('onclick')
		$(this).addClass('onclick')
		$.ajax({
			data:{
				ind : clicked,
				date: $('#day_here').text(),
				cmd : "readall",
			},
			type : 'POST',
			url : '/bot_v3/repl'
		})
		.done(function(data){
			$('#content').html(data)
		})
		//아직 on click
		// event.preventDefault();

		;	
		}
		
	});
});

$(document).ready(function(){
	//fly에 있는 버튼 누를땐 아래처럼 지정해줘야함.
	$(document).on('submit', '#sub_form', function(event){
		if ($('#writer').val() ==''){
			event.preventDefault();
			return alert('작성자를 입력해주세요')
		}
		$.ajax({
			data:{
				writer : $('#writer').val(),
				repl : $('#repl').val(),
				ind : $('#ind').val(),
				date : $('#date').val(),
				cmd : "write_repl"
			},
			type : 'POST',
			url : '/bot_v3/repl'
		})
		.done(function(data){
			$('#content').html(data)
		})		
		event.preventDefault();
	})
	//상태버튼
	$(document).on('change', '#state', function(event){
		var ind = $('#ind').val();
		var desk = $(":checked").val(); 
		var desk_class = {
			color:{
			'0':'ok',
			'1':'jja',
			'2':'kill'	
			},
			word:{
			'0':'굳',
			'1':'안 중요',
			'2':'오류'		
			}

			
		}
		$.ajax({
			data:{
				desk :desk,
				ind : ind,
				date : $('#date').val(),
				cmd : "state_change"
			},
			type : 'POST',
			url : '/bot_v3/repl'
		})
		.done(function(data){
			$('#'+ind+'td').removeClass().addClass(desk_class.color[desk])
			$('#'+ind+'td').html('<h6>'+desk_class.word[desk]+'<h6>')
		})		
		event.preventDefault();
		// if ($('#writer').val() ==''){
		// 	event.preventDefault();
		// 	return alert('작성자를 입력해주세요')
		// }
		// $.ajax({
		// 	data:{
		// 		writer : $('#writer').val(),
		// 		repl : $('#repl').val(),
		// 		ind : $('#ind').val(),
		// 		date : $('#date').val(),
		// 		cmd : "write_repl"
		// 	},
		// 	type : 'POST',
		// 	url : '/bot_v3/repl'
		// })
		// .done(function(data){
		// 	console.log(data)
		// 	$('#content').html(data)
		// })		
		
	})
});

// $(document).ready(function(){
// 	$('form').on('submit', function(event){
// 		console.log('here')

// 	})

// })


