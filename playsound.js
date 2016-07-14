function play(obj){
	var audioTag = document.getElementById('player');
	audioTag.src = parseId(obj.id);
	audioTag.play();
	audioTag.addEventListener("canplaythrough", colorBackground(obj));
	audioTag.addEventListener("canplaythrough", function(){
		audioTag.play();
	});
	audioTag.addEventListener("ended", function(){
		obj.style.backgroundColor = "transparent";
		audioTagClone = audioTag.cloneNode(true);
		audioTag.parentNode.replaceChild(audioTagClone, audioTag);
	});
	
	audioTag.addEventListener("error", function(){
		obj.style.backgroundColor = "transparent";
		audioTagClone = audioTag.cloneNode(true);
		audioTag.parentNode.replaceChild(audioTagClone, audioTag);
	});
}
function colorBackground(obj){
	obj.style.backgroundColor = "yellow";
}

function parseId(id){
	var audioFile = "./sounds/"
	audioFile += id.slice(id.indexOf("_") + 1);
	audioFile += ".mp3";
	return audioFile;
}
