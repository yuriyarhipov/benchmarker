var competitorControllers = angular.module('competitorControllers', []);

competitorControllers.controller('competitorCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project;
        activeProjectService.setProject(project_id);
        $scope.project_id = project_id;
        $http.get('/data/' + project_id + '/competitors/').success(function(data){
            $scope.competitors = data;
        });

        $scope.excel_complete = function(){
            $http.get('/data/' + project_id + '/competitors/').success(function(data){
                $scope.competitors = data;
            });
        };
 }]);