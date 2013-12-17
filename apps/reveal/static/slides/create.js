var textarea = [];
var html = [];
var template = '<section>\n' + "<h1>Write</h1>\n<h2>Here!</h2>\n" + '</section>';

angular.module('reveal', ['ngSanitize'])
  .controller('Ctrl', ['$scope',
    function Ctrl($scope) {
      $scope.counter = 0;
      $scope.slideshow = template;
      $scope.slide = function(count) {
        $scope.counter = count;
        if (textarea[count]) {
          $scope.slideshow = textarea[count];
        } else{
          $scope.slideshow = template;
        }
        console.log(textarea);
      };
      $scope.update = function() {
        textarea[$scope.counter] = $scope.slideshow;
        Reveal.toggleOverview();
        Reveal.toggleOverview();
        console.log(js2html(parse($scope.slideshow)));
      };
      $scope.save = function() {
        var json = JSON.stringify(textarea);
        $.ajax({
            type: "POST",
            url: '/reveal/save',
            data: json,
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
        console.log("Saved");
      };
      $scope.parse = function(text) {
        var regExp = /\(([^)]+)\)/g;
        var matches = text.match(regExp);
        var results =[];
        for (var i = 0; i < matches.length; i++) {
            var str = matches[i];
            var parsed = str.substring(1, str.length - 1).trim();
            var index = parsed.indexOf(' ');
            results.push([parsed.substr(0, index), parsed.substr(index+1)]);
        }
        return results;
      };
      $scope.js2html = function(results) {
        var string='';
        for (var i = 0; i < results.length; i++) {
          type = results[i][0];
          content = results[i][1];
          string += "<" + type + ">" + content + "</" + type + ">";
        }
        return string;
      };
    }
  ]);
