
$(document).ready(
	function(){
			var lt = ['#feature1','#feature2','#feature3','#feature4'];
			var t = $(lt[0]);
			var maxheight = 0;
			for (var j = 0; j < lt.length; j++){
				t=$(lt[j]);
				maxheight=Math.max(maxheight,parseFloat(t.css('height')));
			}
			for (j = 0; j < lt.length; j++){
				t=$(lt[j]);
				t.css({'height':maxheight});
			}
	}
);

$(window).resize(
	function(){
		var lt = ['#feature1','#feature2','#feature3','#feature4'];
		var t = $(lt[0]);
		for (var j = 0; j < lt.length; j++){
			t=$(lt[j]);
			t.css({'height':'auto','min-height':'1px'});
		}
		var maxheight = 0;
		for (j = 0; j < lt.length; j++){
			t=$(lt[j]);
			maxheight=Math.max(maxheight,parseFloat(t.css('height')));
		}
		for (j = 0; j < lt.length; j++){
			t=$(lt[j]);
			t.css({'height':maxheight});
		}
	}
);



$(document).ready(
	function(){
			var lt = ['#us1','#us2','#us3','#us4'];
			var t = $(lt[0]);
			var maxheight = 0;
			for (var j = 0; j < lt.length; j++){
				t=$(lt[j]);
				maxheight=Math.max(maxheight,parseFloat(t.css('height')));
			}
			for (j = 0; j < lt.length; j++){
				t=$(lt[j]);
				t.css({'height':maxheight});
			}
	}
);

$(window).resize(
	function(){
		var lt = ['#us1','#us2','#us3','#us4'];
		var t = $(lt[0]);
		for (var j = 0; j < lt.length; j++){
			t=$(lt[j]);
			t.css({'height':'auto','min-height':'1px'});
		}
		var maxheight = 0;
		for (j = 0; j < lt.length; j++){
			t=$(lt[j]);
			maxheight=Math.max(maxheight,parseFloat(t.css('height')));
		}
		for (j = 0; j < lt.length; j++){
			t=$(lt[j]);
			t.css({'height':maxheight});
		}
	}
);



$(window).scroll(
	function(){
		if(!document.getElementById('landing-slide')){
			return;
		}
		var rect = document.getElementById('landing-slide').getBoundingClientRect();
		
		pos= (960-rect.bottom+rect.top)/window.innerHeight*($(window).scrollTop()+window.innerHeight-rect.bottom)
		pos= -180/(window.innerWidth-240)*window.innerWidth+window.innerHeight/(window.innerHeight+rect.bottom-rect.top)/4*($(window).scrollTop()+window.innerHeight-rect.top)
		//pos= -960+window.innerHeight/(window.innerHeight+rect.bottom-rect.top)/1.3*($(window).scrollTop()+window.innerHeight-rect.top)
//		$('#landing-slide').css({'background-position-x': "54%"})
//		$('#landing-slide').css({'background-position-y': pos})
		
	}
);





