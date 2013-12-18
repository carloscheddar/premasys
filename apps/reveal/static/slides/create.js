var textarea = [];
var html = [];
var template = "(h1 Hello) (h2 World)";

String.prototype.contains = function(it) { return this.indexOf(it) != -1; };

angular.module('reveal', ['ngSanitize'])
  .controller('Ctrl', ['$scope',
    function Ctrl($scope) {
      $scope.counter = 0;
      $scope.slideshow = template;
      $scope.value= js2html(parse(template));

      // Function that moves the lesson forwards or backwards
      // Ex. slide(3) gives you the third slide
      $scope.slide = function(count) {
        if (count >= 0 && count <= textarea.length) {
          $scope.counter = count;
          if (textarea[count]) {
            $scope.slideshow = textarea[count];
          } else {
            $scope.slideshow = template;
          }
          $scope.value= js2html(parse($scope.slideshow));
          console.log(textarea);
        }
      };

      // This function is called on keyup() so that the lesson
      // updates its values
      $scope.update = function() {
        textarea[$scope.counter] = $scope.slideshow;
        console.log($scope.slideshow);
        $scope.value= js2html(parse($scope.slideshow));
        console.log($scope.value);
      };

      // This function converts the lesson and sends it to
      // the django view to be stored
      $scope.save = function() {
        var json = JSON.stringify(les2json(textarea));
        // console.log("Array2Plis",array2Plist(textarea));
        console.log("json", json);
        $.ajax({
          type: "POST",
          url: '/reveal/save',
          data: json,
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          }
        });
        console.log("Saved");
      };
    }
  ]);


// Function that finds blocks of parenthesis and outputs arrays
// Ex: (h1 Hello) (h2 World) --> [[h1, 'Hello'], [h2, 'World']]
var parse = function(text) {
  var regExp = /\(([^)]+)\)/g;
  var matches = text.match(regExp);
  var results = [];
  for (var i = 0; i < matches.length; i++) {
    var str = matches[i];
    var parsed = str.substring(1, str.length - 1).trim();
    var index = parsed.indexOf(' ');
    results.push([parsed.substr(0, index), parsed.substr(index + 1)]);
  }
  return results;
};

// Function that receives an array and converts it to html
// Ex. [[h1, 'Hello'], [h2, 'World']] --> <h1>Hello</h1><h2>World</h2>
// Function that receives an array and converts it to html
// Ex. [[h1, 'Hello'], [h2, 'World']] --> <h1>Hello</h1><h2>World</h2>
var js2html = function(results) {
  var string = '';
  for (var i = 0; i < results.length; i++) {
    type = results[i][0];
    content = results[i][1];
    if (type == "question") {
      type = "h3";
    }
    else if (type == "choice") {
      type = "li";
    }
    else if (type == "answer") {
      type = "li";
      string += "<" + type + " id='answer'>" + content + "</" + type + ">";
      continue;
    }
    else if (type == "img") {
      type = "h3"
      content = "Image goes here"
    }
    else if (type == "video") {
      type = 'h3'
      content = "Video goes here"
    }
    string += "<" + type + ">" + content + "</" + type + ">";
  }
  return string;
};

//Lesson to json
var les2json = function(argument) {
  var json = [];
  for (var i = 0; i < argument.length; i++) {
    if(argument[i].contains("(question")){
      json.push({
        "type": "question",
        "text": argument[i]
      });
    }
    else{
      json.push({
        "type": "text",
        "text": argument[i]
      });
    }
  }
  return json;
};

// --------- PLIST FUNCTIONS ----------

// Receive a slide as a json object and return
// as PList
function jsonToPList(slide){
  if (slide["type"] == "question")
  {
    var question = slide["question"];
    var pList = [getQuestionText(question),
                 getQuestionChoices(question),
                 getQuestionAnswers(question)];
  }

  else if (slide["type"] == "text"){
    var text = slide["text"];
    var pList = [text];
  }
  console.log(pList);
  return pList.join("");
}

// Get the body of the question is PList format
function getQuestionText(question){
  var text = question["body"];
  return makeEntry("question",text)
}

// Get a string that contains all choices as PLists
function getQuestionChoices(question){
  // Get the list of choices that aren't answers
  var choices = question["choices"];
  var answers = question["answers"];
  choices = $(choices).not(answers).get();
  choices = choices.map(
    function(x) { return makeEntry("choice",x); }
  );
  return choices.join("");
}

// Get a string that contains all the correct answers
// as PLists
function getQuestionAnswers(question){
  answers = question["answers"];
  answers = answers.map(
    function(x) { return makeEntry("answer",x); }
  );
  return answers.join("");
}

// Receive a keyword and content, format to PList entry
function makeEntry(keyword, content){
  return "(" + keyword + " " + content + ")";
}

function array2Plist(array){
  var val = []
  for (var i = 0; i < array.length; i++) {
    val.push(jsonToPList(array[i]));
  };
  return val;
}
