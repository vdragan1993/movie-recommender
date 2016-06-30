module.exports = function ($scope, $location, $rootScope, Profile) {

    // list of all services
    $scope.services = null;
    $scope.infoMessage = null;
    $scope.actionMessage = "Register new Service:";
    $scope.buttonMessage = "Register";
    $scope.registerService = {};

    // load profile page
    Profile.display($rootScope.user.id).then(
        function (response) {
            $scope.services = response.data.services;
        }
    );
    
    // refresh function
    var refresh = function () {
        $scope.services = null;
        Profile.display($rootScope.user.id).then(
            function (response) {
                $scope.services = response.data.services;
            }
        );  
    };


     // nav
    $scope.goFavourites = function () {
        $location.path("/favourites");
    };
    
    $scope.goRated = function () {
        $location.path("/rated");
    };

    $scope.goRegLog = function () {
        $location.path("/reglog");
    };

    $scope.goProfile = function () {
        $location.path("/profile");
    };

    $scope.goLogout = function () {
        $location.path("/logout");
    };

    // actions
    // edit existing service
    $scope.edit = function (service_id) {
        for (var i = 0; i<$scope.services.length; i++)
        {
            if ($scope.services[i].id == service_id)
            {
                // set fields
                $scope.registerService.id = service_id;
                $scope.registerService.host = $scope.services[i].host;
                $scope.registerService.port = $scope.services[i].port;
                $scope.registerService.name = $scope.services[i].name;
                $scope.registerService.language = $scope.services[i].language;
                // set button and message
                $scope.actionMessage = "Edit service: ";
                $scope.buttonMessage = "Save";
                break;
            }
        }
    };

    $scope.delete = function (service_id) {
        
        Profile.delete(service_id).then(
            function (response) {
                refresh();
                $scope.infoMessage = "Service deleted successfully!";
            }
        );     
    };

    $scope.serviceAction = function () {
        
        if (!$scope.registerService.host){
            $scope.infoMessage = 'Host cannot be empty!';
        }
        else if (!$scope.registerService.port){
            $scope.infoMessage = 'Port cannot be empty!';
        }
        else if (!$scope.registerService.name){
            $scope.infoMessage = 'Name cannot be empty!';
        }
        else {
            $scope.infoMessage = null;
        }

        if ($scope.infoMessage) {
                return;
        }

        if ($scope.buttonMessage === "Register"){
            Profile.insert($scope.registerService, $rootScope.user.id).then(
                function (response) {
                    refresh();
                    $scope.infoMessage = "Service inserted successfully";
                    $scope.actionMessage = "Register new Service:";
                    $scope.buttonMessage = "Register";
                    $scope.registerService = {};
                }
            );
        }
        else
        {   
            Profile.edit($scope.registerService).then(
                function (response) {
                    refresh();
                    $scope.infoMessage = "Service updated successfully";
                    $scope.actionMessage = "Register new Service:";
                    $scope.buttonMessage = "Register";
                    $scope.registerService = {};
                }
            );
        }
    };

    $scope.cancel = function () {
        $scope.infoMessage = null;
        $scope.actionMessage = "Register new Service:";
        $scope.buttonMessage = "Register";
        $scope.registerService = {};
    };

};