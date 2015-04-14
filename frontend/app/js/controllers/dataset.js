var datasetControllers = angular.module('datasetControllers', []);

datasetControllers.controller('uploadDataSetCtrl', ['$scope', '$http', '$routeParams',
    function ($scope, $http, $routeParams) {
        var project_id = $routeParams.project;
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/datasets').success(function(data){
            $scope.columns = data.columns;
            $scope.data = data.data;
        });
        $scope.excel_complete = function(){
            $http.get('/data/' + project_id + '/datasets').success(function(data){
                $scope.columns = data.columns;
                $scope.data = data.data;
            });
        };
 }]);

 datasetControllers.controller('dataSetCtrl', ['$scope', '$http', '$routeParams',
    function ($scope, $http, $routeParams) {
        var project_id = $routeParams.project;
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/datasets').success(function(data){
            $scope.columns = data.columns;
            $scope.data = data.data;
        });
 }]);