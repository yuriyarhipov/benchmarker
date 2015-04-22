var competitorControllers = angular.module('competitorControllers', []);

competitorControllers.controller('competitorCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', 'FileUploader', '$location',
    function ($scope, $http, $routeParams, activeProjectService, FileUploader, $location) {
        var project_id = $routeParams.project;
        $scope.project = project_id;
        activeProjectService.setProject(project_id);
        var uploader = $scope.uploader = new FileUploader();
        $scope.uploader.url = '/data/' + project_id + '/competitors/';
        $scope.uploader.autoUpload = true;
        $scope.uploader.onCompleteAll = function(){
            $location.path('/' + project_id +   '/competitors/')
        }
        $http.get('/data/' + project_id + '/competitors/').success(function(data){
            $scope.data = data.data;
            $scope.columns = data.columns;

        });
 }]);
