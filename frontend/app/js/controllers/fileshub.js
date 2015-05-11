var filesControllers = angular.module('filesControllers', []);

filesControllers.controller('fileshubCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', 'FileUploader', '$location', 'ngProgress',
    function ($scope, $http, $routeParams, activeProjectService, FileUploader, $location, ngProgress) {
        $scope.module = {'selected': '1'};
        var project_id = $routeParams.project;
        $scope.project = project_id;
        activeProjectService.setProject(project_id);
        $scope.equipments = ['TEMS', 'NETIMIZER']
        $scope.equipment= {'selected': 'TEMS'}

        var uploader = $scope.uploader = new FileUploader();
        $scope.uploader.url = '/data/' + project_id + '/save_file/';
        $scope.uploader.queueLimit = 1;
        $scope.uploader.onCompleteAll = function(){
            console.log('onComplete');
            ngProgress.set(0);
            $location.path(project_id + '/fileshub/');
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
            console.log(progress);
            ngProgress.set(progress);
        };
        $http.get('/data/get_modules/').success(function(data){
            $scope.modules = data;
        });

        $http.get('/data/' + project_id + '/get_files/').success(function(data){
            $scope.files = data;
        });


 }]);