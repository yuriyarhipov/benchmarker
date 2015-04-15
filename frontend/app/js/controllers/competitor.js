var competitorControllers = angular.module('competitorControllers', []);

competitorControllers.controller('competitorCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project;
        $scope.project = project_id;
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

        $scope.add_new = function(){

        };
 }]);

 competitorControllers.controller('editCompetiorCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', '$location',
    function ($scope, $http, $routeParams, activeProjectService, $location) {
        $scope.competitor_data = {};
        var project_id = $routeParams.project;
        $scope.project = project_id;
        var competitor_id = $routeParams.competitor;
        $http.get('/data/' + project_id + '/competitor/' + competitor_id).success(function(data){
            $scope.competitor_data.competitor_id =competitor_id;
            $scope.competitor_data.competitor =data.competitor;
            $scope.competitor_data.gsm =data.gsm;
            $scope.competitor_data.lte =data.lte;
            $scope.competitor_data.wcdma =data.wcdma;
            $scope.competitor_data.future =data.future;
            $scope.competitor_data.mcc =data.mcc;
            $scope.competitor_data.mnc =data.mnc;
            $scope.competitor_data.gsm_freq =data.gsm_freq;
            $scope.competitor_data.wcdma_carriers =data.wcdma_carriers;
            $scope.competitor_data.lte_carriers =data.lte_carriers;
            $scope.competitor_data.future_carriers =data.future_carriers;
        });

        $scope.project = project_id;
        $scope.competitor_data.competitor_id =competitor_id;

        $scope.onSave = function(){
            $http.post('/data/' + project_id +'/save_competitor/', $.param($scope.competitor_data)).success(function(){
                $location.path('/' + project_id + '/competitors');
            });
        };
 }]);