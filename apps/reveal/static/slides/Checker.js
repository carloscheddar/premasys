var mywords = ["question", "choice", "answer", "h1", "h2", "h3", "img"]
//Parse function modified to check validity of user input
//I.E. (questions hi!) => invalid ; (question omg) => valid
var parseCheck = function(text) {
  var regExp = /\(([^)]+)\)/g;
  var werk = text
  var matches = werk.match(regExp);
  var results = [];
  for (var i = 0; i < matches.length; i++) {
    var str = matches[i];
    var parsed = str.substring(1, str.length - 1).trim();
    var index = parsed.indexOf(' ');
    results.push([parsed.substr(0, index), parsed.substr(index + 1)]);
}
//Jom addition

var question = 0;
var answer = 0; 
var correctness = 0;
  for (var i= 0 ; i < results.length; i++){
  	if(question == 0 && results[i][0] == mywords[0]){
  		question++;
  	}
	if(results[i][0] == mywords[2] && question == 0)
	{
		answer++;
	}
	if(results[i][0] == mywords[0] && answer > 0 && question == 1){
		answer = 0;
	}
	if(results[i][0] == mywords[0] && answer == 0 && question == 1){
		return "naw mane"
	}
	for(var e = 0 ; i < mywords.length; i++){
		if(mywords[e] == results[i][0]){
			correctness++;
		}
	}
}
	if(correctness != results.length){
		return "naw mane"
	}
return "iz gud mane"
};