module.exports = function ($scope, $location, $rootScope) {

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

};