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
        'filesControllers',
        'activeProjectModule',
        'angularFileUpload',
        'ngColorPicker',
        'checklist-model',
        'ngProgress',
        'openlayers-directive',
        'settingsControllers',
        'angularSpinner',
        'flash',
        'graphsControllers',
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
            when('/:project/competitors/:competitor', {
                templateUrl: 'templates/competitor.html',
                controller: 'editCompetitorCtrl'
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
            when('/:project/coordinates', {
                templateUrl: 'templates/coordinates.html',
                controller: 'coordinatesCtrl'
            }).
            when('/:project/legends', {
                templateUrl: 'templates/legends.html',
                controller: 'legendsCtrl'
            }).
            when('/:project/workspace', {
                templateUrl: 'templates/workspace.html',
                controller: 'workspaceCtrl'
            }).
            when('/:project/calculations', {
                templateUrl: 'templates/calculations.html',
                controller: 'calculationsCtrl'
            }).
            when('/:project/favorites', {
                templateUrl: 'templates/favorites.html',
                controller: 'favoritesCtrl'
            }).
            when('/:project/performance', {
                templateUrl: 'templates/performance.html',
                controller: 'performanceCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });

    }]);

BenchApp.run(function($rootScope, $http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
});