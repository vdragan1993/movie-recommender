module.exports = function ($scope, $location) {
    
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

    // action
    $scope.favouriteMovies = function () {
        console.log("get recommendations for favourite movies");
        console.log($scope.movies);
    };

};