(function () {
    
    'use strict';

    require('angular');
    require('angular-route');
    require('angular-animate');
    
    // controllers
    var mainCtrl = require('./controllers/MainCtrl');

    angular.module('movieApp', ['ngRoute', 'ngAnimate'])
    
    .config([
        '$locationProvider',
        '$routeProvider',
        function($locationProvider, $routeProvider) {
        // routes
        $routeProvider
            .when("/", {
                templateUrl: "./partials/home.html",
                controller: "HomeController"
            })
            .otherwise({
                redirectTo: '/'
            });
        }
    ])

    // load controller
    .controller('HomeController', ['$scope', mainCtrl]);
    
}());
