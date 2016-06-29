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

    // action
    $scope.ratedMovies = function () {
        console.log("get recommendations for rated movies");
        console.log($scope.movies);
    };
};