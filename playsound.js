function play(obj){
	var audioTagId = parseId(obj.id);
	var audioTag = document.getElementById(audioTagId);
	colorBackground(obj, "yellow");
	audioTag.play();


	audioTag.addEventListener("ended", function(){
		obj.style.backgroundColor = "transparent";
	});
	
}

function colorBackground(obj, color){
	obj.style.backgroundColor = color;
}

function parseId(id){
	var audioTagId = id.slice(id.indexOf("_") + 1);
	audioTagId += "_audio";
	return audioTagId;
}
