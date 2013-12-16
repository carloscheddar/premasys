var textarea = [];
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
    }
  ]);
