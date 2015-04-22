var datasetControllers = angular.module('datasetControllers', []);

datasetControllers.controller('uploadDataSetCtrl', ['$scope', '$http', '$routeParams', '$location', 'FileUploader',
    function ($scope, $http, $routeParams, $location, FileUploader) {
        $scope.project_id = $routeParams.project;
        var uploader = $scope.uploader = new FileUploader();
        $scope.uploader.url = '/data/' + $scope.project_id + '/datasets/';
        $scope.uploader.autoUpload = true;
        $scope.uploader.onBeforeUploadItem = function(item){
            item.formData.push({dataset_name: $scope.dataset_name});
        }
        $scope.uploader.onCompleteAll = function(){
            $location.path('/' + $scope.project_id + '/datasets/')
        }
 }]);

 datasetControllers.controller('dataSetsCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $scope.project = $routeParams.project;
        activeProjectService.setProject(project_id);
        $http.get('/data/' + project_id + '/datasets').success(function(data){
            $scope.datasets = data;
        });
 }]);

 datasetControllers.controller('dataSetCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $scope.project = $routeParams.project;
        $scope.dataset_id = $routeParams.dataset_id

        activeProjectService.setProject(project_id);
        $http.get('/data/' + project_id + '/datasets/' + $scope.dataset_id).success(function(data){
            $scope.columns = data.columns;
            $scope.data = data.data;
        });
 }]);