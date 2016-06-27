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
    $scope.ratedMovies = function () {
        console.log("get recommendations for rated movies");
        console.log($scope.movies);
    };
};