(function () {
    
    'use strict';

    require('angular');
    require('angular-route');
    require('angular-animate');
    require('ui-select');
    require('angular-sanitize');

    // controllers
    var mainCtrl = require('./controllers/MainCtrl');
    var favCtrl = require('./controllers/FavCtrl');
    var rateCtrl = require('./controllers/RateCtrl');
    var regLogCtrl = require('./controllers/RegLogCtrl');
    var logoutCtrl = require('./controllers/LogoutCtrl');
    var profileCtrl = require('./controllers/ProfileCtrl');

    // services
    var RegLog = require('./services/RegLog');
    var Profile = require('./services/Profile');


    angular.module('movieApp', ['ngRoute', 'ngAnimate', 'ui.select', 'ngSanitize'])
    
    .config([
        '$httpProvider',
        '$locationProvider',
        '$routeProvider',
        function($httpProvider, $locationProvider, $routeProvider) {
        // csrf
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        
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
            .when("/logout", {
                templateUrl: "./partials/logout.html",
                controller: "LogoutController"
            })
            .when("/profile", {
                templateUrl: "./partials/profile.html",
                controller: "ProfileController"
            })
            .otherwise({
                redirectTo: '/'
            });
        }
    ])


    // load controllers
    .controller('MainController', ['$scope', '$location','$rootScope', mainCtrl])
    .controller('FavController', ['$scope', '$location','$rootScope', favCtrl])
    .controller('RateController', ['$scope', '$location','$rootScope', rateCtrl])
    .controller('RegLogController', ['$scope', '$location','$rootScope', 'RegLog', regLogCtrl])
    .controller('LogoutController', ['$scope', '$location', '$rootScope', 'RegLog', logoutCtrl])
    .controller('ProfileController', ['$scope', '$location', '$rootScope', 'Profile', profileCtrl])
    // load services
    .factory('RegLog', ['$http', '$rootScope', RegLog])
    .factory('Profile', ['$http', '$rootScope', Profile])
   

    //authentication
    .run(function(RegLog){
        RegLog.isLogged().then(function(response){
            if (response.data.message === 'ok'){
                RegLog.storeCredentials(response.data.user, 'user');
            }
            else {
                RegLog.storeCredentials(null, null);
            }
        });
    });
    
    
}());
