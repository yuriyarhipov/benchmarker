var competitorControllers = angular.module('competitorControllers', []);

competitorControllers.controller('competitorCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('/data/competitors/').success(function(data){
            $scope.competitors = data
        });
 }]);