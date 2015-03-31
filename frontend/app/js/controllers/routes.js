var routeControllers = angular.module('routeControllers', []);

routeControllers.controller('originalCtrl', ['$scope', '$http',
    function ($scope, $http) {
        console.log('OK');
        $scope.map = { center: { latitude: 45, longitude: -73 }, zoom: 8 };
        console.log('OK1');
}]);