module.exports = function ($http, $rootScope) {
    return {
        
        // load movies for dropdowns
        load: function () {
             return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/movies/'
            });
        },

        // send recommendations
        send: function (favourites, heuristic) {
            if (!heuristic){
                heuristic = 'empty';
            }
            return $http({
                method: 'POST',
                url: 'http://localhost:8000/api/favourites/',
                data: {
                    favourites: favourites,
                    heuristic: heuristic
                }
            });
        },

        // registered services (heuristics)
        services: function (user_id) {
             return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/heuristics/' + user_id + '/'
            });
        }


    };
};