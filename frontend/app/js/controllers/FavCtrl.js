module.exports = function ($scope, $location, $rootScope, Favourites) {
    
    // initialization
    $scope.infoMessage = null;
  
    $scope.movie1 = {};
    $scope.movie2 = {};
    $scope.movie3 = {};
    $scope.favourites = [];
    $scope.movies = [];
    // for user defined
    $scope.services = [];
    $scope.heuristic = {};

    // for results
    $scope.results = [];

    // load movies
    Favourites.load().then(
        function (response) {
            $scope.movies = response.data.movies;
        }
    );

    // load services for reco
    if ($rootScope.user)
    {
        Favourites.services($rootScope.user.id).then(
            function (response) {
                $scope.services = response.data.heuristics;
            }
        );
    }

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

        $scope.infoMessage = null;
        
        if ($scope.movie1.selected) {
            $scope.favourites.push($scope.movie1.selected);
        }

        if ($scope.movie2.selected) {
            $scope.favourites.push($scope.movie2.selected);
        }

        if ($scope.movie3.selected) {
            $scope.favourites.push($scope.movie3.selected);
        }

        if ($scope.favourites.length < 2){
            $scope.infoMessage = "Enter at least two favourite movies!";
            return;
        }

        Favourites.send(angular.toJson($scope.favourites), $scope.heuristic.selected).then(
            function (response) {
                
                if (response.data.message) {
                    $scope.infoMessage =  response.data.message;
                    $scope.movie1 = {};
                    $scope.movie2 = {};
                    $scope.movie3 = {};
                    $scope.favourites = [];
                }
                else {
                   $scope.results = response.data.results; 
                   $scope.favourites = [];
                   $scope.infoMessage = null;
                }
                
            }
        );
        
    };

};