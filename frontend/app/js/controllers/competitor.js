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
            $location.path('/' + project_id +   '/competitors/');
        }
        $http.get('/data/' + project_id + '/competitors/').success(function(data){
            $scope.data = data.data;
            $scope.columns = data.columns;

        });
 }]);

competitorControllers.controller('editCompetitorCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', '$location',
    function ($scope, $http, $routeParams, activeProjectService, $location) {
        var competitor = $routeParams.competitor;
        var project_id = $routeParams.project;
        $scope.project = project_id;
        activeProjectService.setProject(project_id);

        $http.get('/data/' + project_id + '/competitors/' + competitor).success(function(data){
            $scope.fields = data;
        });

        $scope.onSave = function(){
            var params = {};
            var i = 0;
            while ($scope.fields[i]){
                params[$scope.fields[i].label] = $scope.fields[i].value;
                i++;
            }
            $http.post('/data/' + project_id + '/competitors/' + competitor, $.param(params)).success(function(){
                $location.path('/' + project_id +   '/competitors/')
            });
        };
 }]);