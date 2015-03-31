var BenchApp = angular.module(
    'benchApp',
    [
        'ngRoute',
        'ngCookies',
        'ui.bootstrap',
        'highcharts-ng',
        'ngUpload',
        'ui.select',
        'ng-context-menu',
        'projectControllers',
        'competitorControllers',
        'datasetControllers',
        'routeControllers',
    ]);

BenchApp.config(['$routeProvider',
    function($routeProvider){
        $routeProvider.
            when('/projects',{
                templateUrl: 'templates/projects.html',
                controller: 'ProjectCtrl',
            }).
            when('/new_project',{
                templateUrl: 'templates/new_project.html',
                controller: 'newProjectCtrl'
            }).
            when('/competitors', {
                templateUrl: 'templates/competitors.html',
                controller: 'competitorCtrl'
            }).
            when('/upload_data_set', {
                templateUrl: 'templates/upload_data_set.html',
                controller: 'dataSetCtrl'
            }).
            when('/original_route', {
                templateUrl: 'templates/original_route.html',
                controller: 'originalCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });

    }]);

BenchApp.run(function($rootScope, $http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});