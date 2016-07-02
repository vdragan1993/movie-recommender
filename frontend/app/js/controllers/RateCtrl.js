module.exports = function ($scope, $location, $rootScope, Rated) {

    // initialization
    $scope.infoMessage = null;
    $scope.number = 8;

    $scope.movies = [];
    // for user defined
    $scope.services = [];
    $scope.heuristic = {};

    // load movies
    Rated.load($scope.number).then(
        function (response) {
            $scope.movies = response.data.movies;
        }
    );

    // load services for reco
    if ($rootScope.user)
    {
        Rated.services($rootScope.user.id).then(
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

    // load more movis
    $scope.loadMore = function () {
        $scope.number = 16;
        // load movies
        Rated.load($scope.number).then(
            function (response) {
                var new_movies = response.data.movies;
                for (var i=0; i<new_movies.length; i++) {
                    $scope.movies.push(new_movies[i]);    
                }
            }
        );
    };

    // send data
    $scope.ratedMovies = function () {
        // validation
        var nonZeros = 0;

        for (var i=0; i<$scope.movies.length; i++){
            if ($scope.movies[i].rate > 10) {
                $scope.infoMessage = "Rating bust be between 0 and 10!";
                return;
            }
            else{
                if ($scope.movies[i].rate > 0) {
                    nonZeros++;
                }
            }
        }

        if (nonZeros === 0) {
            $scope.infoMessage = "Rate at least one movie!";
            return;
        }

        Rated.send(angular.toJson($scope.movies), $scope.heuristic.selected).then(
            function (response) {
                if (response.data.message) {
                    $scope.infoMessage =  response.data.message;
                }
            }
        );


    };
};