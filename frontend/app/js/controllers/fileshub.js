var filesControllers = angular.module('filesControllers', []);

filesControllers.controller('fileshubCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', 'FileUploader', '$location', 'ngProgress',
    function ($scope, $http, $routeParams, activeProjectService, FileUploader, $location, ngProgress) {
        $scope.module = {'selected': '1'};
        var project_id = $routeParams.project;
        $scope.project = project_id;
        activeProjectService.setProject(project_id);
        $scope.equipments = ['TEMS', 'NETIMIZER', 'Mark-Azq']
        $scope.equipment= {'selected': 'TEMS'}

        var uploader = $scope.uploader = new FileUploader();
        $scope.uploader.url = '/data/' + project_id + '/save_file/';
        $scope.uploader.queueLimit = 1;

        $scope.uploader.onCompleteAll = function(data){
            ngProgress.set(0);
            console.log('oe');
            $location.path(project_id + '/dashboard/');

        };

        $scope.uploader.onBeforeUploadItem = function(item){
            item.formData.push({
                'equipment': $scope.equipment.selected,
                'module': $scope.module.selected
                });
        };

        $scope.onUpload = function(){
            $scope.uploader.uploadAll();
        };

        $scope.uploader.onProgressItem = function(item, progress){
            ngProgress.set(progress);
        };
        $http.get('/data/get_modules/').success(function(data){
            $scope.modules = data;
        });

        $http.get('/data/' + project_id + '/get_files/').success(function(data){
            $scope.files = data;
        });
 }]);

filesControllers.controller('dashboardCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', '$location', '$timeout',
    function ($scope, $http, $routeParams, activeProjectService, $location, $timeout) {
        function get_tasks(){
            $http.get('/data/' + project_id + '/tasks/').success(function(data){
                $scope.tasks = data;
                $timeout(get_tasks, 1000);
            });
        };
        var project_id = $routeParams.project;
        $scope.project = project_id;
        activeProjectService.setProject(project_id);
        get_tasks();

        $scope.onDeleteTask = function(task_id){
            $http.post('/data/' + project_id + '/tasks/', $.param({'id': task_id})).success(function(data){
                $scope.tasks = data;
                $timeout(get_tasks, 1000);
            });
        };
 }]);