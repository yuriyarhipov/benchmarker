var datasetControllers = angular.module('datasetControllers', []);

datasetControllers.controller('dataSetCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('/data/datasets').success(function(data){
            $scope.columns = data.measurement_devices;
        });
        $scope.excel_complete = function(){
            console.log()
        };
 }]);