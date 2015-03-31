var projectControllers = angular.module('projectControllers', []);

projectControllers.controller('newProjectCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.project_data = {};
        $http.get('/data/projects/').success(function(data){
            $scope.projects = data;
        });

        $scope.processForm = function(){
            $http.post('/data/projects/', $.param($scope.project_data)).success(function(data){
                $scope.projects = data;
            });
        };
 }]);

projectControllers.controller('ProjectCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('/data/projects/').success(function(data){
            $scope.projects = data;
        });

 }]);