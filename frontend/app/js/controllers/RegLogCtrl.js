module.exports = function ($scope, $location, $rootScope, RegLog) {

    // messages
    $scope.registerMessage = null;
    $scope.loginMessage = null;

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
    // user login
    $scope.login = function () {

        if (!$scope.loginUser.username){
            $scope.loginMessage = 'Username cannot be empty!';
        }
        else if (!$scope.loginUser.password){
            $scope.loginMessage = 'Password cannot be empty!';
        }
        else {
            $scope.loginMessage = null;
        }

        if ($scope.loginMessage) {
            return;
        }
        
        RegLog.login($scope.loginUser.username, $scope.loginUser.password).then(
            function (response) {
                if (response.data.message)
                {
                    $scope.loginMessage = response.data.message;
                    return;
                }
                else
                {
                    RegLog.storeCredentials(response.data.user, 'user');
                    $location.path("/");
                }
            }
        );
    };

    // user registration
    $scope.register = function () {
        
        if (!$scope.registerUser.username){
            $scope.registerMessage = 'Username cannot be empty!';
        } 
        else if (!$scope.registerUser.email){
            $scope.registerMessage = 'Email cannot be empty!';
        }
        else if (!$scope.registerUser.password){
            $scope.registerMessage = 'Password cannot be empty!';
        }
        else {
            $scope.registerMessage = null;
        }

        if ($scope.registerMessage){
            return;
        }
        
        RegLog.register($scope.registerUser.username, $scope.registerUser.email, $scope.registerUser.password).then(
            function (response) {
                $scope.registerMessage = response.data.message;
            
                if ($scope.registerMessage.startsWith("User ")) {
                    $scope.registerUser = null;
                }
                
            }
        );

    };

};