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
        'competitorControllers'
    ]);

BenchApp.config(['$routeProvider',
    function($routeProvider){
        $routeProvider.
            when('/projects',{
                templateUrl: 'templates/projects.html',
            }).
            when('/new_project',{
                templateUrl: 'templates/new_project.html',
                controller: 'newProjectCtrl'
            }).
            when('/competitors', {
                templateUrl: 'templates/competitors.html',
                controller: 'competitorCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });

    }]);

BenchApp.run(function($rootScope, $http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});