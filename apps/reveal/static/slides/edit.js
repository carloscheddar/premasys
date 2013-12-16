angular.module('reveal', ['ngSanitize'])
  .controller('Ctrl', ['$scope', function Ctrl($scope) {
    $scope.slideshow = slides;
  }]);