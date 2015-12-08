var routeControllers = angular.module('routeControllers', []);

routeControllers.controller('originalCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.routeMarkers = [];
        $http.get('/data/get_points/').success(function(data){
            $scope.routeMarkers = data
            latitude = parseFloat($scope.routeMarkers[0].latitude);
            longitude = parseFloat($scope.routeMarkers[0].longitude);

            $scope.map = { center: { latitude: latitude, longitude: longitude }, zoom: 3 };
        });
}]);

routeControllers.controller('createStandartRouteCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', '$location', 'ngProgress', 'usSpinnerService', 'Flash',
    function ($scope, $http, $routeParams, activeProjectService, $location, ngProgress, usSpinnerService, Flash) {
        var project_id = $routeParams.project

        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $scope.selected_files = [];
        $scope.distance = 1;
        $scope.show_form = true;

        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });

        $http.get('/data/' + project_id + '/modules/').success(function(data){
            $scope.modules = data;
        });

        $scope.onModule = function(module_id){
            $http.get('/data/' + project_id + '/module_files/' + module_id).success(function(data){
                $scope.files = data;
            });
        }

        $scope.onSelectAllClick = function(){
            $scope.selected_files = $scope.files.map(function(item) { return item.filename; });
        };

        $scope.saveRoute = function(){
            ngProgress.start();
            usSpinnerService.spin('spinner-1');
            $scope.show_form = false;
            $http.post('/data/' + project_id + '/routes/',$.param(
                    {
                        'route_name':$scope.route_name,
                        'distance': $scope.distance,
                        'color': $scope.color,
                        'files': $scope.selected_files.toString()})).success(function(){
                ngProgress.stop();
                ngProgress.set(0);
                usSpinnerService.stop('spinner-1');
                message = 'Route "' + $scope.route_name + '" is ready'
                Flash.create('success', message, 'custom-class');
                $location.path('/' + project_id +   '/dashboard/');
            })
        };
}]);

routeControllers.controller('routeCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', 'leafletData',
    function ($scope, $http, $routeParams, activeProjectService, leafletData) {
        var project_id = $routeParams.project
        var route_id = $routeParams.route;
        activeProjectService.setProject(project_id);
        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });
        $http.get('/data/' + project_id + '/routes/' + route_id).success(function(data){
            var latitude = parseFloat(data.route[0].lat);
            var longitude = parseFloat(data.route[0].lon);
            var route_name = data.name;
            $scope.center = {
                    lat: latitude,
                    lon: longitude,
                    zoom: $scope.zoom,
            };
            leafletData.getMap().then(function(map) {
                map.setView([latitude, longitude], 15);
                map_bounds = map.getBounds();
                var params = {
                    'bounds': map_bounds.toBBoxString(),
                };
                map._routes = {};
                map._routes[route_name] =  L.layerGroup();
                map._layers_control = L.control.layers({},{},{collapsed:false}).addTo(map);
                map._layers_control.addOverlay(map._routes[route_name], route_name);

                $http.post('/data/' + project_id + '/routes/' + route_id + '/frame/', $.param(params)).success(function(route_data){
                    for (id in route_data){
                        var circle = L.circle([route_data[id].lat, route_data[id].lon], 2, {
                            color: route_data[id].color,
                            fillColor: route_data[id].color,
                            fillOpacity: 1,
                            opacity:1,
                        });
                        map._routes[route_name].addLayer(circle);
                    }
                });
                map._routes[route_name].addTo(map);

                map.on('moveend', function(e){
                    filter_markers(map);
                });

            });

        });

        var filter_markers = function(map){
            map_bounds = map.getBounds();
            var params = {
                    'bounds': map_bounds.toBBoxString(),
            };
            for (route_name in map._routes){
                map._routes[route_name].clearLayers();
                $http.post('/data/' + project_id + '/routes/' + route_id + '/frame/', $.param(params)).success(function(route_data){
                    for (id in route_data){
                        var circle = L.circle([route_data[id].lat, route_data[id].lon], 2, {
                            color: route_data[id].color,
                            fillColor: route_data[id].color,
                            fillOpacity: 1,
                            opacity:1,
                        });
                        map._routes[route_name].addLayer(circle);
                    }
                });
            }
        }


        $scope.onAddRoute =function(route){
            $http.get('/data/' + project_id + '/routes/' + route.id).success(function(data){
                var route_name = data.name;
                leafletData.getMap().then(function(map) {
                    map._routes[route_name] = {route: [], route_layer: L.layerGroup()};
                    map._layers_control.addOverlay(map._routes[route_name].route_layer, route_name);
                    map_bounds = map.getBounds();

                    for (id in data.route){
                        var circle = L.circle([data.route[id].lat, data.route[id].lon], 2, {
                            color: data.route[id].color,
                            fillColor: data.route[id].color,
                            fillOpacity: 1,
                            opacity:1,
                        });
                        map._routes[route_name].route.push(circle);
                        if (map_bounds.contains([data.route[id].lat, data.route[id].lon])){
                            map._routes[route_name].route_layer.addLayer(circle);
                        }
                    }
                    map._routes[route_name].route_layer.addTo(map);
                });
            });
        };

}]);

routeControllers.controller('routesCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });

        $scope.onDelete = function(route_id){
            $http.delete('/data/' + project_id + '/routes/' + route_id).success(function(data){
                $scope.routes = data;
            });
        };

}]);

routeControllers.controller('merge_routesCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        $scope.colors = [
            '#468966',
            '#FFF0A5',
            '#FFB03B',
            '#B64926',
            '#8E2800',
            '#e1e1e1'
        ];
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.routes = {};
        $scope.routeMarkers = [];
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes.entities = data;
        });

        $scope.onMerge = function(){
            for (i=0;i<$scope.routes.entities.length; i++){
                if ($scope.routes.entities[i].isChecked){
                    $http.get('/data/' + project_id + '/routes/' + $scope.routes.entities[i].id).success(function(data){
                        $scope.routeMarkers = data.route;
                        $scope.distance = data.distance;
                        latitude = parseFloat($scope.routeMarkers[0].latitude);
                        longitude = parseFloat($scope.routeMarkers[0].longitude);
                        $scope.map = { center: { latitude: latitude, longitude: longitude }, zoom: 10 };
                    });
                }
            }
        };

}]);


routeControllers.controller('mapCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', 'olData',
    function ($scope, $http, $routeParams, activeProjectService, olData) {
        var project_id = $routeParams.project
        var map_id = $routeParams.map_id;
        var custom_point = new ol.style.Circle({
            radius: 5,
            fill: new ol.style.Fill({
                color: '#ff9900',
                opacity: 0.6
            }),
            stroke: new ol.style.Stroke({
                color: '#ffcc00',
                opacity: 0.4
            })
        });
        var custom_style = {
                image: custom_point,
            };

        var colored_points = {
            '#000000':{
                image: new ol.style.Circle({
                radius: 5,
                fill: new ol.style.Fill({
                    color: '#000000',
                    opacity: 0.6
                }),
                stroke: new ol.style.Stroke({
                    color: '#000000',
                    opacity: 0.4
                })
            }),
            },
        }
        activeProjectService.setProject(project_id);
        $http.get('/data/' + project_id + '/graphs/map/' + map_id).success(function(data){
            $scope.markers = data;
            $scope.distance = data.distance;
            latitude = parseFloat($scope.markers[0].lat);
            longitude = parseFloat($scope.markers[0].lon);
            $scope.zoom = 15;
            $scope.center = {
                    lat: latitude,
                    lon: longitude,
                    zoom: $scope.zoom,
                };

            $scope.point_style = function(point_color){
                if (!(point_color  in colored_points)){
                    colored_points[point_color] = {
                        image: new ol.style.Circle({
                            radius: 5,
                            fill: new ol.style.Fill({
                                color: point_color,
                                opacity: 0.6
                            }),
                            stroke: new ol.style.Stroke({
                                color: point_color,
                                opacity: 0.4
                            })
                            }),
                    };

                }
                return colored_points[point_color];
            };
        });

}]);