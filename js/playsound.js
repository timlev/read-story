clickedWords = [];
originalTitle = "";
function play(obj){
	word = obj.id;
	word = word.slice(word.indexOf("_") + 1);
	if (clickedWords.indexOf(word) == -1){
		clickedWords.push(word);
		console.log(clickedWords);
		console.log(clickedWords.length);
		if (document.title.indexOf("---") == -1){
			originalTitle = document.title;
		}
		
		document.title = clickedWords.length.toString() + "---" + originalTitle;
	}
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

function increaseFont(){
  var fs = document.body.style.fontSize;
  console.log(fs);
  if (fs == ""){
	  document.body.style.fontSize = "1em";
  }
  else {
	  fs = fs.replace("em","");
	  fs = Number(fs);
	  fs += .2;
	  document.body.style.fontSize = fs.toString() + "em";
	  console.log(fs);
  }
}

function decreaseFont(){
  var fs = document.body.style.fontSize;
  console.log(fs);
  if (fs == ""){
	  document.body.style.fontSize = "1em";
  }
  else {
	  fs = fs.replace("em","");
	  fs = Number(fs);
	  fs -= .2;
	  document.body.style.fontSize = fs.toString() + "em";
	  console.log(fs);
  }
}
