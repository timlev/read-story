function play(obj){
	var audioTag = document.getElementById('player');
	audioTag.src = parseId(obj.id);
	obj.style.backgroundColor = "yellow";
	audioTag.addEventListener("canplaythrough", function(){
		audioTag.play();
	});
	audioTag.addEventListener("ended", function(){
		obj.style.backgroundColor = "transparent";;
	});
}

function parseId(id){
	var audioFile = "./sounds/"
	audioFile += id.slice(id.indexOf("_") + 1);
	audioFile += ".mp3";
	return audioFile;
}
