var textarea = [];
textarea[0] = "<h1>Hello</h1>";
textarea[1] = "<h2>Welcome</h2>";

angular.module('reveal', ['ngSanitize'])
  .controller('Ctrl', ['$scope',
    function Ctrl($scope) {
      $scope.counter = 0;
      $scope.slideshow = '<section>' + textarea[$scope.counter] + '</section>';
      $scope.slide = function(count) {
        $scope.counter = count;
        $scope.slideshow = '<section>' + textarea[count] + '</section>';
      };
    }
  ]);
console.log(counter);
