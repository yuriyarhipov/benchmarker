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
        'uiGmapgoogle-maps',
        'filesControllers',
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
            when('/fileshub', {
                templateUrl: 'templates/fileshub.html',
                controller: 'fileshubCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });

    }]);

BenchApp.config(function(uiGmapGoogleMapApiProvider) {
    uiGmapGoogleMapApiProvider.configure({
        key: 'AIzaSyDsNl8wB__2qRld9ou_9wBv3xqA9l5t-UM',
        v: '3.17',
        libraries: 'weather,geometry,visualization'
    });
})

BenchApp.run(function($rootScope, $http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});