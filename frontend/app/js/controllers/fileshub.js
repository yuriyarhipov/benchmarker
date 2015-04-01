var filesControllers = angular.module('filesControllers', []);

filesControllers.controller('fileshubCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('/data/get_modules/').success(function(data){
            $scope.modules = data;
        });
        $http.get('/data/get_files/').success(function(data){
            $scope.files = data;
        });
 }]);