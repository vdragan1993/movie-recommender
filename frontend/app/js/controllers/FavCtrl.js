module.exports = function ($scope, $location, $rootScope) {
    
    // initialization
    $scope.infoMessage = null;
  
    $scope.movie1 = {};
    $scope.movie2 = {};
    $scope.movie3 = {};
    $scope.favourites = [];

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
    $scope.favouriteMovies = function () {
        
        if ($scope.movie1.selected) {
            $scope.favourites.push($scope.movie1.selected);
        }

        if ($scope.movie2.selected) {
            $scope.favourites.push($scope.movie2.selected);
        }

        if ($scope.movie3.selected) {
            $scope.favourites.push($scope.movie3.selected);
        }

        if ($scope.favourites.length === 0){
            $scope.infoMessage = "Enter at least one favourite movie!";
            return;
        }

        console.log("Sending favourite movies...");
        console.log($scope.favourites);
        console.log(angular.toJson($scope.favourites));
        

    };


    $scope.movies = [
        {title: "Film 1", id:"id11"},
        {title: "Film 2", id:"id22"},
        {title: "Film 3", id:"id33"},
        {title: "Film 4", id:"id44"},
        {title: "Film 5", id:"id55"}
    ];


};