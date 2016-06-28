(function () {
    
    'use strict';

    require('angular');
    require('angular-route');
    require('angular-animate');
    
    // controllers
    var mainCtrl = require('./controllers/MainCtrl');
    var favCtrl = require('./controllers/FavCtrl');
    var rateCtrl = require('./controllers/RateCtrl');
    var regLogCtrl = require('./controllers/RegLogCtrl');

    // services
    var RegLog = require('./services/RegLog');

    angular.module('movieApp', ['ngRoute', 'ngAnimate'])
    
    .config([
        '$httpProvider',
        '$locationProvider',
        '$routeProvider',
        function($httpProvider, $locationProvider, $routeProvider) {
        // for urls
        $locationProvider.hashPrefix('!');
        
        // cors
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
        
        
        // routes
        $routeProvider
            .when("/", {
                templateUrl: "./partials/home.html",
                controller: "MainController"
            })
            .when("/favourites", {
                templateUrl: "./partials/favourites.html",
                controller: "FavController"
            })
            .when("/rated", {
                templateUrl: "./partials/rated.html",
                controller: "RateController"
            })
            .when("/reglog", {
                templateUrl: "./partials/reglog.html",
                controller: "RegLogController"
            })
            .otherwise({
                redirectTo: '/'
            });
        }
    ])



    
    // load controllers
    .controller('MainController', ['$scope', '$location', mainCtrl])
    .controller('FavController', ['$scope', '$location', favCtrl])
    .controller('RateController', ['$scope', '$location', rateCtrl])
    .controller('RegLogController', ['$scope', '$location', 'RegLog', regLogCtrl])
    // load services
    .factory('RegLog', ['$http', RegLog]);
    
    
}());
