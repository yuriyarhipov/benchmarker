var BenchApp = angular.module(
    'benchApp',
    [
        'ngRoute',
        'ngCookies',
        'ui.bootstrap',
        'highcharts-ng',
        'ui.select',
        'ng-context-menu',
        'projectControllers',
        'competitorControllers',
        'datasetControllers',
        'routeControllers',
        'uiGmapgoogle-maps',
        'filesControllers',
        'activeProjectModule',
        'angularFileUpload',
        'ngColorPicker',
        'checklist-model',
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
            when('/:project/competitors', {
                templateUrl: 'templates/competitors.html',
                controller: 'competitorCtrl'
            }).
            when('/:project/upload_dataset', {
                templateUrl: 'templates/upload_dataset.html',
                controller: 'uploadDataSetCtrl'
            }).
            when('/:project/datasets', {
                templateUrl: 'templates/datasets.html',
                controller: 'dataSetsCtrl'
            }).
            when('/:project/datasets/:dataset_id', {
                templateUrl: 'templates/dataset.html',
                controller: 'dataSetCtrl'
            }).
            when('/original_route', {
                templateUrl: 'templates/original_route.html',
                controller: 'originalCtrl'
            }).
            when('/:project/fileshub', {
                templateUrl: 'templates/fileshub.html',
                controller: 'fileshubCtrl'
            }).
            when('/', {
                templateUrl: 'templates/index.html',
                controller: 'appCtrl'
            }).
            when('/:project/create_standart_route', {
                templateUrl: 'templates/create_standart_route.html',
                controller: 'createStandartRouteCtrl'
            }).
            when('/:project/route/:route', {
                templateUrl: 'templates/route.html',
                controller: 'routeCtrl'
            }).
            when('/:project/routes/', {
                templateUrl: 'templates/routes.html',
                controller: 'routesCtrl'
            }).
            when('/:project/routes_merge', {
                templateUrl: 'templates/merge_routes.html',
                controller: 'merge_routesCtrl'
            }).
            when('/:project/routes_merge', {
                templateUrl: 'templates/merge_routes.html',
                controller: 'merge_routesCtrl'
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